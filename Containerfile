#FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04
FROM nvidia/cuda:12.2.2-devel-ubuntu22.04 AS env

RUN apt-get update && apt-get install -y python3-pip git nvidia-cuda-toolkit

RUN mkdir -p /opt/server
ADD requirements.txt /opt/server
WORKDIR /opt/server

RUN pip3 install -r requirements.txt
RUN pip3 install flash-attn --no-build-isolation
#RUN pip3 install packaging

FROM env
WORKDIR /opt/server
ADD main.py /opt/server

EXPOSE 8000/tcp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
