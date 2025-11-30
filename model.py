import re
import os

import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
import pdf2image


MODEL_SIZES = {
    '256M': 'HuggingFaceTB/SmolVLM2-256M-Video-Instruct',
    '500M': 'HuggingFaceTB/SmolVLM2-500M-Video-Instruct',
    '2.2B': 'HuggingFaceTB/SmolVLM2-2.2B-Instruct'
}


def is_folder_empty(folder_path):
    if not os.path.exists(folder_path):
        return True
    return len(os.listdir(folder_path)) == 0


class SmolVLM2:
    def __init__(self, device=None, parameters_path=None, model_size='256M',
                 save_model=False, save_params_path='model_params'):
        self.device = device if device is not None else "cuda" if torch.cuda.is_available() else "cpu"
        print(self.device)
        if parameters_path is None or parameters_path == 'None':
            self.model_name = MODEL_SIZES.get(model_size)
            if self.model_name is None:
                raise Exception(
                    f'Invalid model_size: {model_size}. '
                    f'model_size should be one of {list(MODEL_SIZES.keys())}')
        else:
            self.model_name = parameters_path

        self.processor = AutoProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForImageTextToText.from_pretrained(
            self.model_name,
            dtype=torch.bfloat16,
        ).to(self.device)
        if save_model and is_folder_empty(save_params_path):
            self.model.save_pretrained(save_params_path)
            self.processor.save_pretrained(save_params_path)
        elif save_model and is_folder_empty(save_params_path) == False:
            print(
                f"Directory {save_params_path} is not empty. "
                "Cannot save model to this directory."
            )

    def get_messages(self, image_number, prompt):
        return [
            {
                "role": "user",
                "content":
                    [{"type": "image"} for i in range(image_number)] +
                    [{"type": "text", "text": prompt}]
            },
        ]

    def visual_qa(self, images, question):
        prompt = self.processor.apply_chat_template(
            self.get_messages(1, question),
            add_generation_prompt=True)
        inputs = self.processor(text=prompt, images=images,
                                return_tensors="pt")
        inputs = inputs.to(self.device)
        outputs = self.model.generate(**inputs)
        response = self.processor.decode(outputs[0], skip_special_tokens=True)
        match = re.search('Assistant: ', response)
        return response[match.end():]

    def perform_ocr(self, images):
        all_text = []
        for img in images:
            question = ('Perform OCR (optical character recognition. '
                        'Extract text from this image')
            prompt = self.processor.apply_chat_template(
                self.get_messages(1, question),
                add_generation_prompt=True)
            inputs = self.processor(text=prompt, images=[img],
                                    return_tensors="pt")
            inputs = inputs.to(self.device)
            outputs = self.model.generate(**inputs, max_new_tokens=500)
            extracted_text = self.processor.decode(outputs[0],
                                                   skip_special_tokens=True)
            match = re.search('Assistant: ', extracted_text)
            all_text.append(extracted_text[match.end():])
        return "\n".join(all_text)


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
