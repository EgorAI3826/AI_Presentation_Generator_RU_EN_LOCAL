
# README

## Overview

This project generates a PowerPoint presentation based on user-provided descriptions. It leverages language models to generate text content and an image generation API to create images for the slides. The architecture is modular, allowing for easy extension and customization of the text and image generation components.

## How to Use

### Prerequisites

- Python 3.10 or higher
- Required Python packages (listed in `requirements.txt`)

### Setup

1. **Clone the repository**:

   ```bash
   git clone --recurse-submodules https://github.com/ai-forever/slides_generator.git
   cd slides_generator
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a .env file** in the root directory with GigaChat credentials:

Here is the [documentation](https://developers.sber.ru/portal/products/gigachat-api) on how to get access token.

   ```plaintext
   AUTH_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   COOKIE=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```


4. **Run the FastAPI server** for the image generation API:

   ```bash
   python src/kandinsky.py
   ```

### Running the Script

To generate a presentation, use the following command:

```bash
python main.py -d "Description of the presentation"  -l 'en'
```

This will generate a presentation based on the provided description and save it in the `logs` directory with a timestamp.

## Examples

```bash
python main.py -d "Сгенерируй презентацию про планеты солнечной системы" -l 'ru'
```

```bash
python main.py -d "Generate presentation about planets of Solar system" -l 'en'
```

This command will create a presentation on the topic "Planets of the Solar System" using the configured text and image generation functions.

## Architecture

### Main Components

1. **main.py**: The entry point of the application. It parses command-line arguments, initializes required components, and orchestrates the presentation generation process.

2. **Font Class (src/font.py)**: Manages fonts used in the presentation. It can select a random font with basic and bold styles and provide paths to various font styles (basic, bold, italic, and italic bold).

3. **Presentation Generation Functions (src/constructor.py)**: Functions that generate different types of slides in the presentation. They handle the layout, font settings, and placement of text and images.

4. **Text Generation (src/gigachat.py)**: Contains the `giga_generate` function, which generates text based on a given prompt.

5. **Image Generation (src/kandinsky.py)**: Includes the `api_k31_generate` function, which generates images based on a prompt using an external API. Additionally, it provides a FastAPI server for the image generation API.

6. **Prompt Configuration (src/prompt_configs.py)**: Defines the structure of prompts used for generating titles, text, images, and backgrounds for slides.

### How It Works

1. **Initialization**:
    - `main.py` parses command-line arguments to get the presentation description.
    - It initializes the `Font` class with the directory containing font files and sets a random font.

2. **Prompt Configuration**:
    - The `ru_gigachat_config` defines the structure and content of prompts used for generating slide components (titles, text, images, backgrounds).

3. **Text and Image Generation**:
    - The `giga_generate` function generates text based on the provided description.
    - The `api_k31_generate` function generates images based on prompts using the FastAPI server.

4. **Slide Generation**:
    - The `generate_presentation` function orchestrates the creation of slides by calling appropriate functions to generate text and images, and then formats them into slides.

## Extending the Project

### Adding New Font Styles

To add new font styles, place the font files in the `fonts` directory and update the `Font` class if necessary to recognize the new styles.

### Changing Text Generation

To use a different text generation function, replace the `giga_generate` function from `src/gigachat.py` or add a new function and update the call in `main.py`.

### Changing Image Generation

To use a different image generation API, modify the `api_k31_generate` function in `src/kandinsky.py` or add a new function and update the call in `main.py`.

## Acknowledgements

This project leverages the `python-pptx` library for PowerPoint generation, PIL for image processing, and other Python libraries for various functionalities. The text and image generation models are based on external APIs and language models.

---

Feel free to reach out with any questions or suggestions!

## Authors

+ Said Azizov: [Github](https://github.com/stazizov), [Blog](https://t.me/said_azizau)

## Citation

```
@misc{arkhipkin2023kandinsky,
      title={Kandinsky 3.0 Technical Report}, 
      author={Vladimir Arkhipkin and Andrei Filatov and Viacheslav Vasilev and Anastasia Maltseva and Said Azizov and Igor Pavlov and Julia Agafonova and Andrey Kuznetsov and Denis Dimitrov},
      year={2023},
      eprint={2312.03511},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```
