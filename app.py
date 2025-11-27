import random
import string
import argparse
import os

import torch
import gradio as gr
from PIL import Image
import pdf2image

from model import SmolVLM2

parser = argparse.ArgumentParser(description='Запуск модели с параметрами')

parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                    help='Устройство для запуска модели: cuda/cpu (default: cuda если доступно, иначе cpu)')
parser.add_argument('--model_path', type=str, default=None,
                    help='Путь к директории с параметрами модели (default: None)')
parser.add_argument('--model_size', type=str, default='256M',
                    choices=['256M', '500M', '2.2B'],
                    help='Размер модели: 256M, 500M, 2.2B (default: 256M)')
parser.add_argument('--port', type=int, default=7860,
                    help='Порт для работы программы (default: 7860)')
parser.add_argument('--save_model', type=str, default='False',
                    help='Сохранять или нет веса модели (default: False)')
parser.add_argument('--save_params_path', type=str, default='model_params',
                    help='Путь к директории для сохранения параметров модели (default: model_params)')

args = parser.parse_args()

print(f"Device: {args.device}")
if args.model_path and not args.model_path == 'None':
    print(f"Model path: {args.model_path}")
print(f"Model size: {args.model_size}")
# print(f"Port: {args.port}")
if args.save_model == 'True':
    save_model = True
elif args.save_model == 'False':
    save_model = False
else:
    save_model = args.save_model
print(f"Save model params: {save_model}")
if save_model:
    print(f"Save model params to: {args.save_params_path}")


model = SmolVLM2(model_size=args.model_size, device=args.device,
                 parameters_path=args.model_path,
                 save_model=save_model,
                 save_params_path=args.save_params_path)


def handle_image(input_file):
    if hasattr(input_file, 'name'):
        return Image.open(input_file)
    else:
        return input_file


def handle_input(input_file):
    if isinstance(input_file, str) and input_file.lower().endswith('.pdf'):
        return pdf2image.convert_from_path(input_file)
    elif isinstance(input_file, list):
        return [handle_image(file) for file in input_file]
    else:
        return [handle_image(input_file),]


def perform_ocr(input_file):
    input_file = handle_input(input_file)
    output_text = model.perform_ocr(input_file)
    random_file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    with open('results/my_file.txt', 'w', encoding='utf-8') as file:
        file.write(output_text)
    return output_text, 'results/my_file.txt'


image_description = gr.Interface(
    fn=model.visual_qa,
    inputs=[gr.Image(type="pil"),
            gr.Textbox(label="Question",
                       placeholder="Describe this image",
                       value="describe this image",
                       lines=2)],
    outputs=gr.Textbox(lines=20, label="Result"),
    title="Visual Question Answering",
    description="Upload an image and ask a question about it.",
    examples=[
        ["examples/Dog_Breeds.jpg"],
    ]
)

ocr = gr.Interface(
    fn=perform_ocr,
    inputs=gr.File(label="Upload Image or PDF",
                   file_types=[".png", ".jpg", ".jpeg", ".pdf"],
                   height=150),
    outputs=[gr.Textbox(lines=10, label="Result"),
             gr.File(label="Download Result", height=50)],
    title="Optical Character Recognition",
    description="Upload an image for the model to read the text from it.",
    examples=[
        ["examples/OCR_test.jpg"], ["examples/OCR_test_pdf.pdf"]
    ]
)

# Create the tabbed interface
demo = gr.TabbedInterface(
    [image_description, ocr],
    ["Visual Question Answering", "Optical Character Recognition"]
)

print("Launching app")
demo.launch(share=False, server_name="0.0.0.0", server_port=args.port, quiet=True) #server_name="0.0.0.0",
