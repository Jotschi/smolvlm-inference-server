from io import BytesIO
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
from transformers.image_utils import load_image
from fastapi.responses import JSONResponse
import logging
import torch
import base64

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
app = FastAPI()
modelid = os.getenv("MODEL_ID", "HuggingFaceTB/SmolVLM-Instruct")
default_prompt = os.getenv("DEFAULT_PROMPT", "Describe the image")

# Initialize processor and model
processor = AutoProcessor.from_pretrained(modelid)
model = AutoModelForVision2Seq.from_pretrained(
    modelid,
    torch_dtype=torch.bfloat16,
    _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager",
).to(DEVICE)

class Request(BaseModel):
    prompt: str | None = None
    image_url: str | None = None
    image_data: str | None = None


@app.post("/caption")
async def caption(item: Request):

    if item.image_data and item.image_url:
        raise HTTPException(status_code=400, detail="image_url and image_data specified. Only provide one.")

    if item.image_data is None and item.image_url is None:
        raise HTTPException(status_code=400, detail="image_url or image_data must be specified.")


    prompt = None
    if item.prompt:
        prompt = item.prompt
    else:
        prompt = default_prompt
    logger.info(f"Using prompt: {prompt}")

    # Setup the chat msg
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt}
            ]
        },
    ]


    image = None
    if item.image_data:
        # Load image via Base64 data
        logger.info("Loading image from base64 data")
        image_data = base64.b64decode(item.image_data)
        image = Image.open(BytesIO(image_data))
    elif item.image_url:
        # Load the image via URL
        image = load_image(item.image_url)


    # Prepare inputs
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt")
    inputs = inputs.to(DEVICE)

    # Generate outputs
    generated_ids = model.generate(**inputs, max_new_tokens=500)
    generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)

    clean_output = extract_assistant_text(generated_texts[0])
    logger.info(f"Caption: {clean_output}")
    msg = {"caption": clean_output}

    return JSONResponse(content=msg, status_code=200)

def extract_assistant_text(log):
    return "\n".join(line[11:] for line in log.splitlines() if line.startswith("Assistant:"))



