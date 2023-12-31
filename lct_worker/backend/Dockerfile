FROM nvidia/cuda:12.0.0-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        git \
        python3.10 \
        python3.10-distutils \
        libglib2.0-0 \
        ffmpeg \
        libsm6 \
        libxext6 \
        curl

# Upgrade pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.10 get-pip.py && \
    rm get-pip.py
# RUN python3.10 -m venv venv
# RUN . venv/bin/activate
RUN pip install --upgrade pip

# # Install PyTorch, torchvision and adapter-transformers
# RUN pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu111/torch_stable.html

WORKDIR /backend

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir logs/

ENV PYTHONPATH="."

# Run your app
COPY . .
CMD [ "python3.10", "-m", "app" ]
