FROM python:3.10-slim

ARG CUDA_AVAILABLE=true
ENV PORT 7860
ENV DEVICE cuda
ENV MODEL_PATH None
ENV MODEL_SIZE 256M
ENV SAVE_MODEL False
ENV SAVE_PARAMS_PATH model_params

WORKDIR /app

RUN if [ "$CUDA_AVAILABLE" = "true" ]; then \
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121; \
    else \
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu; \
    fi


COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

EXPOSE ${PORT}

# CMD ["/bin/bash"]
CMD python app.py --device=${DEVICE} --model_path=${MODEL_PATH} \
    --model_size=${MODEL_SIZE} --port=${PORT} --save_model=${SAVE_MODEL} \
    --save_params_path=${SAVE_PARAMS_PATH}