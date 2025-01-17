from pptx import Presentation
from pptx.util import Inches
from pptx.oxml.xmlchemy import OxmlElement
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE

from typing import List, Callable, Optional
from PIL import Image
import random
import tqdm
import os


from .image_slide import generate_image_slide
from .plain_text_slide import generate_plain_text_slide
from .title_slide import generate_title_slide

from src.font import Font

def generate_slide(
    presentation: Presentation,
    title: str,
    text: Optional[str] = None,
    background_path: Optional[str] = None,
    picture_path: Optional[str] = None,
    font: Font = None, 
    text_font_coeff:float=0.6,
) -> None:
    """
    Generate a slide in the presentation based on the provided content.

    Args:
        presentation (Presentation): The presentation object.
        title (str): The title of the slide.
        text (Optional[str]): The text content for the slide (default is None).
        picture_path (Optional[str]): The path to the picture for the slide (default is None).
        background_path (Optional[str]): The path to the background image for the slide (default is None).
        font (Font): Font object to manage font styles and paths.
        text_font_coeff (float): Coefficient to adjust the font size 
            of the text relative to the title (default is 0.6).
    """
    
    if title and text is None and picture_path is None and background_path:
        generate_title_slide(
            presentation=presentation,
            title=title,
            font=font,
            background_path=background_path,
        )
    elif title and text and background_path and picture_path is None:
        generate_plain_text_slide(
            presentation=presentation,
            title=title,
            text=text,
            background_path=background_path,
            font=font,
            text_font_coeff=text_font_coeff,
        )
    elif title and text and picture_path and background_path is None:
        generate_image_slide(
            presentation=presentation,
            title=title,
            text=text,
            picture_path=picture_path,
            font=font,
            text_font_coeff=text_font_coeff,
        )