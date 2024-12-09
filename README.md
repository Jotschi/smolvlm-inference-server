# SmolVLM Inference Server

A simple FastAPI inference server for the [SmolVLM-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-Instruct) MultiModal LLM.


## Env

* **MODEL_ID**: HuggingFaceTB/SmolVLM-Instruct
* **DEFAULT_PROMPT**: "Describe the image"

## Container


```
podman run \
    --device nvidia.com/gpu=all \
    --shm-size 1g \
    --name smolvlm-server \
    -p 8000:8000 \
    --rm \
    -v /opt/cache/huggingface:/root/.cache/huggingface \
    metaloom/smolvlm-server:latest
```

## Spec

```json
{
  "prompt": "Describe the image",
  "image_url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/SmolVLM.png"
}
```


## Build

```bash
./build.sh
```

## Test

```bash
./test.sh
```

## Development

```bash
pip3 install -r requirements.txt
pip3 install flash-attn --no-build-isolation

uvicorn main:app --reload
```