#!/bin/bash

podman run \
    --device nvidia.com/gpu=all \
    --shm-size 1g \
    --name smolvlm-server \
    -p 8000:8000 \
    --rm \
    -v /opt/cache/huggingface:/root/.cache/huggingface \
    localhost/metaloom/smolvlm-server:latest