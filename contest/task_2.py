import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

# Загрузка данных
train = pd.read_csv('train_runes.csv')
test = pd.read_csv('test_runes.csv')


# Функция создания признаков (та же, что использовалась для дерева)
def create_all_features(df):
    features = []
    for rune in df['rune']:
        # Базовые частоты
        f = rune.count('F')
        w = rune.count('W')
        e = rune.count('E')

        # Позиционные признаки (индексы первого вхождения каждого символа)
        pos_features = []
        for c in 'FWE':
            try:
                pos_features.append(rune.index(c))
            except ValueError:
                pos_features.append(-1)

        # Попарные сравнения (одинаковы ли символы на позициях i и j)
        comparisons = []
        for i in range(5):
            for j in range(i + 1, 5):
                comparisons.append(1 if rune[i] == rune[j] else 0)

        # N-граммы (2 и 3 символа)
        ngrams_2 = [rune[i:i + 2] for i in range(4)]
        ngrams_3 = [rune[i:i + 3] for i in range(3)]

        # Кодируем n-граммы в числа (используем ord для стабильности)
        ngram_features = []
        for ng in ngrams_2 + ngrams_3:
            # Преобразуем строку в число
            val = sum(ord(c) * (i + 1) for i, c in enumerate(ng))
            ngram_features.append(val % 100)  # берем по модулю 100 для стабильности

        features.append([f, w, e] + pos_features + comparisons + ngram_features)

    return np.array(features)


# Создаем признаки
X_train = create_all_features(train)
y_train = train['spell']
X_test = create_all_features(test)

# Кросс-валидация для проверки стабильности
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(DecisionTreeClassifier(max_depth=9, random_state=42),
                         X_train, y_train, cv=cv, scoring='accuracy')
print(f"Cross-validation scores: {scores}")
print(f"Mean CV accuracy: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

# Обучаем финальную модель
final_model = DecisionTreeClassifier(max_depth=9, random_state=42)
final_model.fit(X_train, y_train)

# Проверяем точность на тренировочных данных
train_pred = final_model.predict(X_train)
train_accuracy = (train_pred == y_train).mean()
print(f"\nTraining accuracy: {train_accuracy:.4f}")

# Предсказываем для тестовых данных
test_predictions = final_model.predict(X_test)

# Создаем файл ответов
submission = pd.DataFrame({
    'rune': test['rune'],
    'spell': test_predictions
})

# Проверяем, что формат соответствует example.csv
print(f"\nSubmission shape: {submission.shape}")
print(f"Predictions distribution:\n{submission['spell'].value_counts()}")

# Сохраняем
submission.to_csv('answers.csv', index=False)
print("\n✅ Файл answers.csv успешно создан!")

# Дополнительно: проверим несколько примеров из test_runes.csv
print("\nПримеры предсказаний для первых 10 тестовых рун:")
for i in range(min(10, len(test))):
    print(f"{test['rune'].iloc[i]} -> {test_predictions[i]}")