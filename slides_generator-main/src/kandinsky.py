import sys
sys.path.append('Kandinsky-3')

import torch
from kandinsky3 import get_T2I_Flash_pipeline
from PIL import Image
import asyncio

# Проверка доступности CUDA
if not torch.cuda.is_available():
    raise RuntimeError("CUDA is not available. Please check your GPU and PyTorch installation.")

# Инициализация пайплайна для генерации изображений
device_map = torch.device('cuda:0')  # Используем GPU
dtype_map = {
    'unet': torch.float32,
    'text_encoder': torch.float16,  # Используем половинную точность для экономии памяти
    'movq': torch.float32,
}

# Инициализация пайплайна
try:
    t2i_pipe = get_T2I_Flash_pipeline(
        device_map, dtype_map
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize pipeline: {e}")

# Асинхронная функция для генерации изображения
async def api_k31_generate(prompt, width=512, height=512, steps=30):  # Уменьшено разрешение и количество шагов
    """
    Генерация изображения с использованием локального пайплайна Kandinsky-3.

    Args:
        prompt (str): Промпт для генерации изображения.
        width (int): Ширина изображения.
        height (int): Высота изображения.
        steps (int): Количество шагов генерации.

    Returns:
        Image.Image: Сгенерированное изображение.
    """
    try:
        # Генерация изображения
        with torch.no_grad():  # Отключаем вычисление градиентов для экономии памяти
            pil_image = t2i_pipe(prompt, width=width, height=height, steps=steps)[0]
            torch.cuda.empty_cache()  # Очищаем кэш GPU после генерации
        return pil_image
    except Exception as e:
        print(f"Error generating image: {e}")
        torch.cuda.empty_cache()  # Очищаем кэш GPU в случае ошибки
        return None