#!/bin/bash

#IMAGE_URL="https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"
#IMAG_URLE="https://huggingface.co/spaces/merve/chameleon-7b/resolve/main/bee.jpg"
IMAGE_URL="https://shop.manner.com/media/catalog/product/1/7/1700_neapolitaner_grosspkg_18er.jpg"


# Via URL
curl -X POST "http://127.0.0.1:8000/caption" \
    -H "Content-Type: application/json" \
    -d "{
    \"prompt\": \"Describe the image\",
    \"image_url\": \"$IMAGE_URL\"
}"


# Via Base64 Data
IMAGE_DATA=$(curl -s "$IMAGE_URL" | base64)
JSON_FILE="/tmp/payload.json"
echo "{
    \"prompt\": \"Describe the image\",
    \"image_data\": \"$IMAGE_DATA\"
}" > $JSON_FILE

curl -X POST "http://127.0.0.1:8000/caption" \
    -H "Content-Type: application/json" \
    -d @$JSON_FILE