import streamlit as st
import pandas as pd
import numpy as np
from streamlit import cache_data

# Настраиваем широкий режим отображения и заголовок страницы
st.set_page_config(page_title="Airbnb Analytics Dashboard", layout="wide")
st.title("🎯 Airbnb Analytics Dashboard")
st.markdown("Интерактивная панель для анализа данных аренды. Используйте фильтры в боковой панели для настройки данных.")

# Загружаем данные с кэшированием - создаем демо-датасет
@cache_data
def load_data():
    # Создаем демонстрационный набор данных
    np.random.seed(42)
    
    data = {
        'neighbourhood_group': np.random.choice(['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island'], 1000),
        'room_type': np.random.choice(['Entire home/apt', 'Private room', 'Shared room'], 1000),
        'price': np.random.randint(50, 500, 1000),
        'number_of_reviews': np.random.randint(0, 200, 1000),
        'minimum_nights': np.random.randint(1, 30, 1000),
        'availability_365': np.random.randint(0, 365, 1000),
        'latitude': np.random.uniform(40.50, 40.90, 1000),
        'longitude': np.random.uniform(-74.25, -73.70, 1000)
    }
    return pd.DataFrame(data)

df = load_data()

# Создаем сайдбар для фильтров
st.sidebar.header("Фильтры")

# Фильтр 1: Слайдер для выбора диапазона цен
price_range = st.sidebar.slider(
    "Выберите диапазон цены:",
    min_value=int(df['price'].min()),
    max_value=int(df['price'].max()),
    value=(50, 300)
)

# Фильтр 2: Мультиселект для выбора районов
available_neighbourhoods = df['neighbourhood_group'].unique()
neighbourhood_groups = st.sidebar.multiselect(
    "Выберите район:",
    options=available_neighbourhoods,
    default=available_neighbourhoods
)

# Фильтр 3: Селектбокс для выбора типа комнаты
room_type = st.sidebar.selectbox(
    "Выберите тип комнаты:",
    options=df['room_type'].unique()
)

# Применяем фильтры к данным
filtered_data = df[
    (df['price'].between(price_range[0], price_range[1])) &
    (df['neighbourhood_group'].isin(neighbourhood_groups)) &
    (df['room_type'] == room_type)
]

# Показываем основную информацию
st.subheader("📊 Общая статистика")
col1, col2, col3 = st.columns(3)
col1.metric("Всего объявлений", len(filtered_data))
col2.metric("Средняя цена", f"${filtered_data['price'].mean():.2f}")
col3.metric("Медианная цена", f"${filtered_data['price'].median():.2f}")

# Показываем отфильтрованные данные
st.subheader("📋 Отфильтрованные данные (первые 20 записей)")
st.dataframe(filtered_data.head(20))

# Создаем два столбца для графиков
st.subheader("📈 Визуализация данных")

# График 1: Распределение цен (гистограмма)
st.write("#### Распределение цен")
hist_values = np.histogram(filtered_data['price'], bins=30, range=(0, 500))[0]
st.bar_chart(hist_values)

# График 2: Количество объявлений по районам
st.write("#### Количество объявлений по районам")
neighbourhood_counts = filtered_data['neighbourhood_group'].value_counts()
st.bar_chart(neighbourhood_counts)

# График 3: Scatter plot (Цена vs. Количество отзывов)
st.write("#### Соотношение цены и количества отзывов")
scatter_data = filtered_data[['price', 'number_of_reviews']].copy()
scatter_data = scatter_data[scatter_data['number_of_reviews'] < 200]  # Фильтруем выбросы
st.scatter_chart(scatter_data, x='price', y='number_of_reviews')

# Карта расположения объявлений
st.write("#### Карта расположения объявлений")
map_data = filtered_data[['latitude', 'longitude', 'price', 'neighbourhood_group']].copy()
map_data = map_data.dropna()
st.map(map_data, zoom=10)

# Таблица с сводной статистикой
st.write("#### Сводная статистика по районам")
pivot_table = filtered_data.groupby('neighbourhood_group').agg({
    'price': ['mean', 'median', 'count'],
    'number_of_reviews': 'mean'
}).round(2)
st.dataframe(pivot_table)

# Добавляем информацию о данных
st.sidebar.markdown("---")
st.sidebar.info("""
**О данных:**
- Демонстрационный набор данных
- 1000 записей о вариантах аренды
- Включает информацию о цене, районе и типе жилья
""")

# Информация о развертывании
st.markdown("---")
st.success("🚀 Это приложение развернуто на Streamlit Community Cloud!")
