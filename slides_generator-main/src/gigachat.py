import requests
import json
import uuid
import time
from typing import Dict, Optional, Any
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_response(
    prompt: str,
    model: str = "ai-sage/gigachat-20b-a3b-instruct",
    timeout: int = 300,  # Увеличенный таймаут
    n: int = 1,
    fuse_key_word: Optional[str] = None,
    use_giga_censor: bool = False,
    max_tokens: int = 512,
) -> Optional[requests.Response]:
    """
    Send a text generation request to the local LM Studio API.

    Args:
        prompt (str): The input prompt.
        model (str): The model to be used for generation.
        timeout (int): Timeout duration in seconds.
        n (int): Number of responses.
        fuse_key_word (Optional[str]): Additional keyword to include in the prompt.
        use_giga_censor (bool): Whether to use profanity filtering.
        max_tokens (int): Maximum number of tokens in the response.

    Returns:
        Optional[requests.Response]: API response or None if an error occurs.
    """
    url = "http://localhost:1234/v1/chat/completions"
    
    messages = [
        {
            "role": "user",
            "content": ' '.join([fuse_key_word, prompt]) if fuse_key_word else prompt
        }
    ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.87,
        "top_p": 0.47,
        "n": n,
        "stream": False,
        "max_tokens": max_tokens,
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def giga_generate(
    prompt: str, 
    model_version: str = "ai-sage/gigachat-20b-a3b-instruct", 
    max_tokens: int = 2048
) -> str:
    """
    Generate text using the local GigaChat model.

    Args:
        prompt (str): The input prompt.
        model_version (str): The version of the model to use.
        max_tokens (int): Maximum number of tokens in the response.

    Returns:
        str: Generated text or an error message.
    """
    response = get_response(
        prompt,
        model_version,
        use_giga_censor=False,
        max_tokens=max_tokens,
    )

    if response is None:
        return "Error: Failed to get response from the server."

    try:
        response_dict = response.json()
        response_str = response_dict['choices'][0]['message']['content']
        return response_str
    except (KeyError, IndexError) as e:
        print(f'Error processing response: {e}')
        return 'Error: Failed to generate response'
    except Exception as e:
        print(f'Unexpected error: {e}')
        return 'Error: Unexpected error occurred'