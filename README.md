```
# AI_Presentation_Generator

AI_Presentation_Generator — это инструмент для автоматической генерации презентаций с использованием модели Kandinsky 3 для создания изображений. Программа принимает текстовое описание (промпт) и генерирует изображения, которые могут быть использованы в презентациях. Поддерживается работа на GPU для ускорения процесса генерации.

## Запуск:

```bash
python main.py -d "Сгенерируй презентацию про планеты солнечной системы" -l 'ru'  # 'ru' для русского языка, 'en' для английского
```

## Требуется скачать:

1. Модель Kandinsky 3:
   - Скачайте репозиторий по ссылке: [Kandinsky-3](https://github.com/ai-forever/Kandinsky-3/tree/25d55515b177fab34af190abee822a3411b2f24d).
   - Распакуйте содержимое в папку `slides_generator-main`.

2. Установите необходимые зависимости:
   - Убедитесь, что у вас установлены Python 3.8 или выше, а также библиотеки `torch`, `PIL` и другие зависимости, указанные в репозитории Kandinsky 3.

## Как использовать:

1. Убедитесь, что у вас есть доступ к GPU для ускорения генерации изображений.
2. Запустите скрипт `main.py` с указанием текстового описания и языка.
3. Программа сгенерирует изображения и сохранит их в указанной папке для дальнейшего использования в презентации.

## Пример:

```bash
python main.py -d "Сгенерируй презентацию про планеты солнечной системы" -l 'ru'
```

Этот запрос создаст изображения, связанные с планетами солнечной системы, на русском языке.
```
