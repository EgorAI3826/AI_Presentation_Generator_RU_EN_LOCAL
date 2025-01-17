from typing import List, Callable
from googletrans import Translator
import random
import asyncio  # Добавлен импорт asyncio для работы с асинхронными функциями

from src.prompt_configs import PromptConfig, prefix

translator = Translator()

# Асинхронная функция для перевода текста
async def get_translation(text: str, dest: str = 'en') -> str:
    translated = await translator.translate(text, dest=dest)  # Используем await
    return translated.text

def llm_generate_titles(
    llm_generate: Callable[[str], str], 
    description: str, 
    prompt_config: PromptConfig,
) -> List[str]:
    """
    Generate presentation slide titles using a language model.

    Args:
        llm_generate (Callable[[str], str]): Function to generate text using a language model.
        description (str): Description of the presentation.
        prompt_config (PromptConfig): Configuration for prompts.

    Returns:
        List[str]: List of generated slide titles.
    """
    prompt = prompt_config.title_prompt.format(
        description=description
    )
    titles_str = llm_generate(prompt)
    titles = []
    for title in titles_str.split("\n"):
        # Проверяем, содержит ли строка подстроку ". "
        if ". " in title:
            sep_index = title.index('. ') + 1
            title = title.strip()[sep_index:]
        else:
            # Если подстрока ". " отсутствует, просто убираем лишние пробелы
            title = title.strip()
        
        # Убираем лишние символы
        title = title.replace('.', '')
        title = title.replace('\n', '')
        
        # Убираем префикс, если он есть
        if prefix in title.lower():
            title = title[
                title.lower().index(prefix)+len(prefix):
            ]
        
        # Добавляем заголовок в список, если он не пустой
        if title:
            titles.append(title)
    return titles

def llm_generate_text(
    llm_generate: Callable[[str], str], 
    description: str, 
    titles: List[str], 
    prompt_config: PromptConfig
) -> List[str]:
    """
    Generate text for each slide title using a language model.

    Args:
        llm_generate (Callable[[str], str]): Function to generate text using a language model.
        description (str): Description of the presentation.
        titles (List[str]): List of slide titles.
        prompt_config (PromptConfig): Configuration for prompts.

    Returns:
        List[str]: List of generated texts for each slide.
    """
    texts = []
    for title in titles:
        query = prompt_config.text_prompt.format(description=description, title=title)
        text = llm_generate(query)
        if prefix in text.lower():
            text = text[text.lower().index(prefix)+len(prefix):]
            text = text.replace('\n', '') 
        texts.append(text)
    return texts

# Асинхронная функция для генерации промпта изображения
async def llm_generate_image_prompt(
    llm_generate: Callable[[str], str], 
    description: str, 
    title: str, 
    prompt_config: PromptConfig
) -> str:
    """
    Generate an image prompt for a slide using a language model and translate it.

    Args:
        llm_generate (Callable[[str], str]): Function to generate text using a language model.
        description (str): Description of the presentation.
        title (str): Slide title.
        prompt_config (PromptConfig): Configuration for prompts.

    Returns:
        str: Translated image prompt.
    """
    query = prompt_config.image_prompt.format(description=description, title=title)
    prompt = llm_generate(query)
    if prefix in prompt: 
        prompt = prompt[prompt.lower().index(prefix)+len(prefix):]
        prompt = prompt.replace('\n', '')
    return await get_translation(prompt)  # Используем await

# Асинхронная функция для генерации промпта фона
async def llm_generate_background_prompt(
    llm_generate: Callable[[str], str], 
    description: str, 
    title: str, 
    prompt_config: PromptConfig, 
    background_style: str = ''
) -> str:
    """
    Generate a background prompt for a slide using a language model and translate it.

    Args:
        llm_generate (Callable[[str], str]): Function to generate text using a language model.
        description (str): Description of the presentation.
        title (str): Slide title.
        prompt_config (PromptConfig): Configuration for prompts.

    Returns:
        str: Translated background prompt.
    """
    query = prompt_config.background_prompt.format(description=description, title=title)
    
    keywords = llm_generate(query)
    background_prompt = f'{keywords}, {background_style}'
        
    return await get_translation(background_prompt)  # Используем await