# AI_Presentation_Generator

AI_Presentation_Generator — это инструмент для автоматической генерации презентаций с использованием модели Kandinsky 3 и gigachat 20B для создания изображений. Программа принимает текстовое описание (промпт) и генерирует изображения, которые могут быть использованы в презентациях. Поддерживается работа на GPU для ускорения процесса генерации.

## Запуск:

```bash
python main.py -d "Сгенерируй презентацию про планеты солнечной системы" -l 'ru'  # 'ru' для русского языка, 'en' для английского
```

## Требуется скачать:

1. Модель Kandinsky 3:
   - Скачайте репозиторий по ссылке: [Kandinsky-3](https://github.com/ai-forever/Kandinsky-3/tree/25d55515b177fab34af190abee822a3411b2f24d).
   - Распакуйте содержимое в папку `slides_generator-main`.

Примерно такой путь у вас будет:  
`"C:\Users\User\Desktop\slides_generator-main\Kandinsky-3"`

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

Этот запрос создаст презентацию, связанную с планетами солнечной системы, на русском языке.

## Логи и настройки:

- В папке `logs` находится пример генерации, где можно отслеживать процесс создания презентации.
- Вы можете изменить файл `slides_generator-main\src\gigachat.py` для использования другой модели. В текущей версии используется модель GigaChat 20B, запущенная на LM Studio.

## Настройка модели:

Если вы хотите использовать другую модель для генерации текста или изображений, откройте файл `slides_generator-main\src\gigachat.py` и измените настройки. В текущей версии используется модель GigaChat 20B(Q8 от ai-sage), интегрированная через LM Studio.


```
ДЛЯ РАБОТЫ С МОДЕЛЬЮ GIGACHAT В LM Studio:

Нужно настраивать секцию с Prompt Template (https://lmstudio.ai/docs/configuration/prompt-template)

Template Settings
- Type: Manual
- Mode: Custom

Template Fields
Before System: <s>
After System: <|message_sep|>
Before User: user<|role_sep|>
After User: <|message_sep|>
Before Assistant: available functions<|role_sep|>[]<|message_sep|>assistant<|role_sep|>
After Assistant: <|message_sep|>

Additional Settings
Additional Stop Strings: [Empty/Not Set]```
