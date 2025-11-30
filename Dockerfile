FROM python:3.10-slim

ARG CUDA_AVAILABLE=true
ENV PORT 7860
ENV DEVICE cuda
ENV MODEL_PATH None
ENV MODEL_SIZE 256M
ENV SAVE_MODEL False
ENV SAVE_PARAMS_PATH model_params

WORKDIR /app

RUN  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN apt-get update && apt-get install -y poppler-utils

COPY . /app/

EXPOSE ${PORT}

CMD python app.py --device=${DEVICE} --model_path=${MODEL_PATH} \
    --model_size=${MODEL_SIZE} --port=${PORT} --save_model=${SAVE_MODEL} \
    --save_params_path=${SAVE_PARAMS_PATH}