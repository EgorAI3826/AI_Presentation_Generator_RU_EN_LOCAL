import time
import argparse
import asyncio
import logging
from src.constructor import generate_presentation 
from src.prompt_configs import en_gigachat_config, ru_gigachat_config
from src.gigachat import giga_generate
from src.kandinsky import api_k31_generate
from src.font import Font

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    """
    Основная асинхронная функция для генерации презентации.
    """
    parser = argparse.ArgumentParser(
        description='Generate a presentation.'
    )
    parser.add_argument(
        '-d', '--description', 
        type=str, 
        required=True, 
        help='Description of the presentation'
    )
    parser.add_argument(
        '-l', '--language', 
        type=str, 
        choices=['en', 'ru'], 
        default='en', 
        help='Language for the presentation. Choices are: English, Russian. Default is English.'
    )
    args = parser.parse_args()

    # Выбор конфигурации промптов в зависимости от языка
    if args.language == 'en':
        prompt_config = en_gigachat_config
    elif args.language == 'ru':
        prompt_config = ru_gigachat_config
    else: 
        logger.warning("Only 'en' and 'ru' configs are available. Setting default to 'en'.")
        prompt_config = en_gigachat_config

    fonts_dir = "./fonts"
    logs_dir = "./logs"
    
    # Инициализация шрифта
    font = Font(fonts_dir)
    font.set_random_font() 
    
    # Создание директории для выходных данных
    output_dir = f'{logs_dir}/{int(time.time())}'
    logger.info(f"Output directory: {output_dir}")
    
    try:
        # Генерация презентации
        await generate_presentation(
            llm_generate=giga_generate, 
            generate_image=api_k31_generate,
            prompt_config=prompt_config,    
            description=args.description,
            font=font,
            output_dir=output_dir,
        )
        logger.info("Presentation generated successfully!")
    except Exception as e:
        logger.error(f"An error occurred while generating the presentation: {e}")
        raise  # Повторно выбрасываем исключение для завершения программы

if __name__ == "__main__": 
    # Запуск асинхронной функции main
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error: {e}")