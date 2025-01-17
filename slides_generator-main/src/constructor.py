from pptx import Presentation
from pptx.util import Inches
from pptx.oxml.xmlchemy import OxmlElement
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE

import random
import os
from PIL import Image
from typing import List, Callable
import asyncio  # Добавлен импорт asyncio для работы с асинхронными функциями

from .llm_utils import llm_generate_titles, llm_generate_text, llm_generate_image_prompt, llm_generate_background_prompt
from .prompt_configs import PromptConfig
from .slides import generate_slide
from .font import Font

import tqdm


async def generate_presentation(
    llm_generate: Callable[[str], str],
    generate_image: Callable[[str, int, int], Image.Image],
    prompt_config: PromptConfig,
    description: str,
    font: Font, 
    output_dir: str,
) -> Presentation:
    """
    Generate a PowerPoint presentation based on a description using language and image models.

    Args:
        llm_generate (Callable[[str], str]): Function to generate text using a language model.
        generate_image (Callable[[str, int, int], Image.Image]): Function to generate images.
        prompt_config (PromptConfig): Configuration for prompts.
        description (str): Description of the presentation.
        output_dir (str): Directory to save generated images and presentation.
        font (Font): Font object to manage font styles and paths.
    Returns:
        Presentation: The generated PowerPoint presentation.
    """
    os.makedirs(os.path.join(output_dir, 'backgrounds'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'pictures'), exist_ok=True)
    presentation = Presentation()
    presentation.slide_height = Inches(9)
    presentation.slide_width = Inches(16)

    pbar = tqdm.tqdm(total=4, desc="Presentation goes brrr...")
    
    pbar.set_description("Generating titles for presentation")
    titles = llm_generate_titles(llm_generate, description, prompt_config)
    pbar.update(1)
    
    pbar.set_description("Generating text for slides")
    texts = [None] + llm_generate_text(
        llm_generate, 
        description, 
        titles[1:], 
        prompt_config
    )
    pbar.update(1)

    # postfix added to keywords describing presentation
    background_style = random.choice(prompt_config.background_styles)
    
    picture_paths = []
    background_paths = []
    pbar.set_description("Generating images for slides")
    for t_index, (title, text) in enumerate(zip(titles, texts)):
        # Decide randomly presence of image on current slide
        if random.choices(
            [True, False], 
            # side-image/plain-text with background image
            weights=[4, 1], 
        k=1)[0] and text:
            image_width, image_height = random.choice(
                [(768, 1344), (1024, 1024)]
            )
            caption_prompt = await llm_generate_image_prompt(
                llm_generate, 
                description, 
                title, 
                prompt_config
            )
            picture = await generate_image(
                prompt=caption_prompt, 
                width=image_width, 
                height=image_height
            )
            picture_path = os.path.join(
                output_dir, 
                'pictures', 
                f'{t_index:06}.png'
            )
            picture.save(picture_path)
        else:
            picture_path = None
        picture_paths.append(picture_path)

        if picture_path is None:
            background_width, background_height = 1344, 768
            background_prompt = await llm_generate_background_prompt(
                llm_generate, 
                description, 
                title, 
                prompt_config,
                background_style
            )
            background = await generate_image(
                prompt=background_prompt, 
                width=background_width, 
                height=background_height
            )
            background_path = os.path.join(
                output_dir, 
                'backgrounds', 
                f'{t_index:06}.png'
            )
            background.save(background_path)
        else:
            background_path = None
        background_paths.append(background_path)
    pbar.update(1)
    
    pbar.set_description("Packing presentation")
    
    for index in range(len(titles)):
        title = titles[index]
        text = texts[index]
        picture_path = picture_paths[index]
        background_path = background_paths[index]

        generate_slide(
            presentation=presentation,
            title=title,
            text=text,
            picture_path=picture_path,
            background_path=background_path,
            font=font,
        )
    pbar.update(1)
    
    pbar.set_description("Done")
    output_path = os.path.join(output_dir, 'presentation.pptx')
    presentation.save(output_path)
    return presentation