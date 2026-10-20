import os
import re
import csv


def clean_text(text):
    """Очищает текст от лишних пробелов, спецсимволов и приводит к единому регистру."""
    if not text:
        return ""
    # Удаляем HTML-теги, если они случайно попали из интернета
    text = re.sub(r'<[^>]+>', '', text)
    # Заменяем несколько пробелов или переносов строк на один
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def process_exam_data(input_csv_path, output_csv_path):
    """
    Читает сырые вопросы к экзаменам, очищает их
    и сохраняет в структурированном виде для ИИ-помощника.
    """
    if not os.path.exists(input_csv_path):
        print(f"Ошибка: Исходный файл {input_csv_path} не найден!")
        return

    processed_data = []

    print("Начало обработки данных для ИИ-помощника...")

    with open(input_csv_path, mode='r', encoding='utf-8') as file:
        # Предполагаем, что в сыром файле есть колонки: Тема, Вопрос, Сырой_Ответ
        reader = csv.DictReader(file)

        for row in reader:
            topic = clean_text(row.get('Тема', 'Общая тема'))
            question = clean_text(row.get('Вопрос', ''))
            raw_answer = clean_text(row.get('Сырой_Ответ', ''))

            # Пропускаем строки без вопросов
            if not question:
                continue

            # ИИ-помощнику нужен четкий формат. Формируем структуру.
            processed_data.append({
                'subject_topic': topic,
                'ai_prompt_question': f"Объясни простую суть вопроса: {question}",
                'reference_answer': raw_answer,
                'status': 'ready_for_fine_tuning'
            })

    # Сохраняем очищенные данные в новый файл, который пойдет на вход нейросети
    fieldnames = ['subject_topic', 'ai_prompt_question', 'reference_answer', 'status']
    with open(output_csv_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_data)

    print(f"Успешно обработано и сохранено в: {output_csv_path}")


if __name__ == "__main__":
    # Этот код сам определит, где находится папка проекта, откуда бы вы его ни запускали
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    INPUT_DATA = os.path.join(BASE_DIR, "practical-works", "practical-work-04", "assets", "data.csv")
    OUTPUT_DATA = os.path.join(BASE_DIR, "practical-works", "practical-work-04", "assets", "cleaned_exam_data.csv")

    # Запуск обработки
    process_exam_data(INPUT_DATA, OUTPUT_DATA)