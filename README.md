# SmolVLM2 - Preview App

## Описание
2 use cases:
- Visual Question Answering<br>
    В интерфейсе можно добавить картинку и вопрос. На выходе получается ответ нейросети в текстовом поле.
- Optical Character Recognition<br>
    В интерфейсе можно приложить картику или pdf. На выходе можно скачать результат в виде файла txt.

## Запуск проекта
Технические требования: CUDA>=12.1

1. **Склонировать репозиторий**
```bash
git clone https://github.com/ka-lina/smolvlm2-app.git
cd smolvlm2-app
```
2. **Build Docker Container**
```bash
docker build -t smolvlm2-app .
```
3. **Run Docker Container**<br>
Возможные параметры при запуске:
- DEVICE: cuda/cpu, default: cuda
- MODEL_PATH - Путь к директории с параметрами модели, если они сохранены с помощью save_pretrained() (default: None)
- MODEL_SIZE - Размер модели: 256M, 500M, 2.2B (default: 256M)
- SAVE_MODEL - Сохранять или нет веса модели с помощью save_pretrained() (default: False)
- SAVE_PARAMS_PATH - Путь к директории для сохранения параметров модели (default: model_params)

3.1. Как добавить существующие веса SmolVLM2:<br>
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
Добавляем путь к директории с параметрами модели в volume и параметр MODEL_PATH=model_params:
    ```bash
    docker run -v $(pwd)/examples:/app/examples \
        -v path/to/model_params:/app/model_params \
        -v $(pwd)/results:/app/results \
        -e MODEL_PATH=model_params \
        -p 7860:7860 \
        -it --gpus all --name smolvlm2-app smolvlm2-app
    ```

3.2. Смена device GPU/CPU<br>
1. С использованием GPU: добавляем параметр --gpus all <br>
    ```bash
    docker run -v $(pwd)/examples:/app/examples \
        -v $(pwd)/model_params:/app/model_params \
        -v $(pwd)/results:/app/results \
        -v path/to/hf_cache:/root/.cache/huggingface \
        -e MODEL_SIZE=256M \
        -p 7860:7860 \
        -it --gpus all --name smolvlm2-app smolvlm2-app
    ```
2. CPU-only: добавляем параметр -e DEVICE=cpu<br>
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

3.3. Смена размера модели<br>
Задаем параметр MODEL_SIZE: 256M, 500M, 2.2B (по умолчанию 256M).
```bash
docker run -v $(pwd)/examples:/app/examples \
    -v $(pwd)/model_params:/app/model_params \
    -v $(pwd)/results:/app/results \
    -v path/to/hf_cache:/root/.cache/huggingface \
    -e MODEL_SIZE=500M \
    -p 7860:7860 \
    -it --gpus all --name smolvlm2-app smolvlm2-app
```

3.4. Смена порта<br>
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

4. Перейти на http://127.0.0.1:7860/ (либо выбранный порт)<br>
Нужно время, чтобы приложение запустилось - секунд 15-20.
