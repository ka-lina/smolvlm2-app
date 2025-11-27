# SmolVLM2 - Preview App

## Описание

## Запуск проекта
Технические требования: Ubuntu22.04, CUDA>=12.1

1. **Склонировать репозиторий**
```bash
git clone 
cd 
```
2. **Build Docker Container**
```bash
docker build -t smolvlm2-app .
```

Если на устройстве нет GPU или поддержки CUDA (от этого зависит установка pytorch - для cuda/cpu)
```bash
docker buildx build --build-arg CUDA_AVAILABLE=false -t smolvlm2-app .
```
3. **Run Docker Container**<br>
3.1. Как добавить существующие веса SmolVLM2:
    1. Если это huggingface cache.
    Добавляем путь к директории с huggingface кэшем как volume и указываем размер модели: '256M', '500M', '2.2B' (по умолчанию 256M).
    ```bash
    docker run -v $(pwd)/examples:/app/examples \
        -v $(pwd)/model_params:/app/model_params \
        -v $(pwd)/results:/app/results \
        -v path/to/hf_cache:/root/.cache/huggingface \
        -e MODEL_SIZE=256M \
        -p 7860:7860 \
        -it --name smolvlm2-app smolvlm2-app
    ```
    2. Если это веса модели, сохраненные с помощью save_pretrained
    Добавляем путь к директории с параметрами модели в:
    ```bash
    docker run -v $(pwd)/examples:/app/examples \
        -v path/to/model_params:/app/model_params \
        -v $(pwd)/results:/app/results \
        -e MODEL_PATH=model_params
        -p 7860:7860 \
        -it --name smolvlm2-app smolvlm2-app
    ```

3.2. Смена device GPU/CPU
    1. С использованием GPU:
    ```bash
    docker run -v $(pwd)/examples:/app/examples \ 
        -v $(pwd)/model_params:/app/model_params \
        -v $(pwd)/results:/app/results \
        -v path/to/hf_cache:/root/.cache/huggingface \
        -e MODEL_SIZE=256M \
        -p 7860:7860 \
        -it --gpus all --name smolvlm2-app smolvlm2-app
    ```
    2. CPU-only:
    ```bash
    docker run -v $(pwd)/examples:/app/examples \
        -v $(pwd)/model_params:/app/model_params \
        -v $(pwd)/results:/app/results \
        -v path/to/hf_cache:/root/.cache/huggingface \
        -e MODEL_SIZE=256M \
        -e DEVICE=cpu \
        -p 7860:7860 \
        -it --name smolvlm2-app smolvlm2-app
    ```

3.3. Смена размера модели - параметр MODEL_SIZE: '256M', '500M', '2.2B' (по умолчанию 256M).
```bash
docker run -v $(pwd)/examples:/app/examples \
    -v $(pwd)/model_params:/app/model_params \
    -v $(pwd)/results:/app/results \
    -v path/to/hf_cache:/root/.cache/huggingface \
    -e MODEL_SIZE=500M \
    -p 7860:7860 \
    -it --name smolvlm2-app smolvlm2-app
```

3.4. Смена порта
Меняем порт, публикуемый при запуске контейнера:
```bash
docker run -v $(pwd)/examples:/app/examples \ 
    -v $(pwd)/model_params:/app/model_params \
    -v $(pwd)/results:/app/results \
    -v path/to/hf_cache:/root/.cache/huggingface \
    -e MODEL_SIZE=256M \
    -p 8080:7860 \
    -it --gpus all --name smolvlm2-app smolvlm2-app
```

4. Перейти на http://127.0.0.1:7860/ (либо выбранный порт)
Нужно время, чтобы приложение запустилось - секунд 15-20
