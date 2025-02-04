import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import ImageTk, Image
from pathlib import Path
import torch
from torch.backends import cudnn
from diffusers import StableDiffusionPipeline
from transformers import MarianMTModel, MarianTokenizer
import os

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

def setup_cuda_optimization():
    cudnn.benchmark = True

def translate_to_english(text: str) -> str:
        src_lang = "vi"
        tgt_lang = "en"
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text

def load_pipeline(model_name: str = "Ojimi/anime-kawai-diffusion", device: str = DEVICE):
        pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16).to(device)
        return pipe

def generate_image(pipe, prompt: str, output_path: Path):
        image = pipe(prompt, guidance_scale=8, num_inference_steps=50).images[0]
        image.save(output_path)
        return image

def get_unique_filename(base_path: Path, base_name: str, extension: str) -> Path:
    counter = 0
    new_path = base_path / f"{base_name}{extension}"
    while new_path.exists():
        counter += 1
        new_path = base_path / f"{base_name}_{counter}{extension}"
    return new_path

def create_gui():
    app = ctk.CTk()
    app.geometry("800x800")
    app.title("TẠO NY CHO BẠN")
    ctk.set_appearance_mode("light")

    PRIMARY_COLOR = "#FF66B2"
    SECONDARY_COLOR = "#FF99CC"
    FONT_STYLE = ("Arial", 16)

    prompt_label = ctk.CTkLabel(app, text="Mô tả hình mẫu ny của bạn:", font=("Arial", 18), text_color=PRIMARY_COLOR)
    prompt_label.pack(pady=20)

    prompt_entry = ctk.CTkEntry(app, width=700, height=40, font=("Arial", 20),
                                placeholder_text="Nhập mô tả về ny mà bạn muốn", placeholder_text_color=SECONDARY_COLOR)
    prompt_entry.pack(pady=10)

    generate_button = ctk.CTkButton(
        app,
        text="Tạo ny",
        font=("Arial", 20),
        fg_color=PRIMARY_COLOR,
        hover_color=SECONDARY_COLOR,
        command=lambda: on_generate_image(prompt_entry.get())
    )
    generate_button.pack(pady=20)

    image_label = ctk.CTkLabel(app, width=700, height=512, text="Đang tạo ny cho bạn đâyyy", font=("Arial", 16), text_color=PRIMARY_COLOR)
    image_label.pack(pady=20)

    def on_generate_image(vietnamese_prompt):
        translated_prompt = translate_to_english(vietnamese_prompt)
        print(f"Prompt dịch sang tiếng Anh: {translated_prompt}")

        base_name = "ny_cua_ban"
        output_file = get_unique_filename(OUTPUT_DIR, base_name, ".png")
        image = generate_image(pipe, translated_prompt, output_file)

        img = Image.open(output_file)
        img_ctk = ctk.CTkImage(light_image=img, dark_image=img, size=(512, 512))
        image_label.configure(image=img_ctk, text="")
        image_label.image = img_ctk

    global pipe
    pipe = load_pipeline()
    app.mainloop()

if __name__ == "__main__":
    setup_cuda_optimization()
    create_gui()