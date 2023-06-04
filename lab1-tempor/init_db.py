import sqlite3
import pandas as pd
import numpy as np

# Создаем соединение с базой данных (или создаем новую базу данных, если она не существует)
conn = sqlite3.connect('temporal_data.db')

# Создаем курсор для выполнения SQL-запросов
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('''
    CREATE TABLE temporal_data (
        event TEXT,
        start_time TEXT,
        end_time TEXT
    )
''')

# Генерируем случайные временные промежутки
np.random.seed(0)
df_simulation = pd.DataFrame({
    'event': ['event' + str(i) for i in range(5)],
    'start_time': pd.to_datetime(
        np.random.choice(pd.date_range('2023-06-01 10:00:00', '2023-06-01 11:30:00', freq='1min'), 5)),
    'end_time': pd.to_datetime(
        np.random.choice(pd.date_range('2023-06-01 10:15:00', '2023-06-01 11:45:00', freq='1min'), 5))
})

# Для каждой записи в DataFrame
for record in df_simulation.to_dict('records'):
    # Преобразуем объекты Timestamp в строки
    record['start_time'] = record['start_time'].isoformat()
    record['end_time'] = record['end_time'].isoformat()

    # Вставляем запись в таблицу
    cursor.execute('''
        INSERT INTO temporal_data (event, start_time, end_time)
        VALUES (:event, :start_time, :end_time)
    ''', record)

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
