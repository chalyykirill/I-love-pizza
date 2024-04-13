from transformers import pipeline


def analyze_comments(comments):
    # Загрузка предобученной модели и токенизатора
    classifier = pipeline("sentiment-analysis", model="seara/rubert-base-cased-russian-sentiment")

    # Предсказание тональности для списка комментариев
    results = classifier(comments)

    # Возвращаем результаты в виде списка словарей
    return results


# Пример использования функции
comments = [
    "Это было просто потрясающе!",
    "Ужасный сервис, никогда больше не вернусь сюда.",
    "Довольно неплохо, но могло бы быть и лучше."
]

predictions = analyze_comments(comments)
for comment, prediction in zip(comments, predictions):
    print(f"Комментарий: {comment} \nТональность: {prediction['label']} \nВероятность: {prediction['score']:.2f}\n")

# Пример вывода:
# Комментарий: Это было просто потрясающе!
# Тональность: positive
# Вероятность: 0.99

# Комментарий: Ужасный сервис, никогда больше не вернусь сюда.
# Тональность: negative
# Вероятность: 0.95

# Комментарий: Довольно неплохо, но могло бы быть и лучше.
# Тональность: positive
# Вероятность: 0.79