import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit import cache_data

# Настраиваем режим отображения и заголовок страницы
st.set_page_config(page_title = "Airbnb NYC Dashboard", layout = "wide")
st.title("Airbnb NYC Analytics Dashboard")
st.markdown("Интерактивная панель для анализа предложений Airbnb в Нью-Йорке. Используйте фильтры в боковой панели для настройки данных.")

@cache_data
def load_data():
    # Используем встроенный датасет из Plotly
    try:
        # Пробуем загрузить датасет Airbnb из Plotly
        df = px.data.airbnb()
        if df is not None and not df.empty:
            return df
    except:
        pass
    
    # Если не получилось, создаем демо-датасет
    st.warning("Используется демонстрационный набор данных")
    import numpy as np
    np.random.seed(42)
    
    data = {
        'neighbourhood_group': np.random.choice(['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island'], 1000),
        'room_type': np.random.choice(['Entire home/apt', 'Private room', 'Shared room'], 1000),
        'price': np.random.randint(50, 500, 1000),
        'number_of_reviews': np.random.randint(0, 200, 1000),
        'minimum_nights': np.random.randint(1, 30, 1000),
        'availability_365': np.random.randint(0, 365, 1000)
    }
    return pd.DataFrame(data)

df = load_data()

st.sidebar.header("Фильтры")

# Фильтр 1: Слайдер для выбора диапазона цен
price_range = st.sidebar.slider(
    "Выберите диапазон цены:",
    min_value = int(df['price'].min()),
    max_value = int(df['price'].max()),
    value = (50, 300)
)

# Фильтр 2: Мультиселект для выбора районов
neighbourhood_groups = st.sidebar.multiselect(
    "Выберите район:",
    options = df['neighbourhood_group'].unique(),
    default = df['neighbourhood_group'].unique()
)

# Фильтр 3: Селектбокс для выбора типа комнаты
room_type = st.sidebar.selectbox(
    "Выберите тип комнаты:",
    options = df['room_type'].unique()
)

# Применяем фильтры к данным
filtered_data = df[
    (df['price'].between(price_range[0], price_range[1])) &
    (df['neighbourhood_group'].isin(neighbourhood_groups)) &
    (df['room_type'] == room_type)
]

# Показываем отфильтрованные данные в интерактивной таблице
st.subheader("Отфильтрованные данные")
st.dataframe(filtered_data)

col1, col2 = st.columns(2)

# График 1: гистограмма
with col1:
    fig_price = px.histogram(filtered_data, x = 'price', title = 'Распределение цен', nbins = 50)
    fig_price.update_layout(bargap = 0.1)
    st.plotly_chart(fig_price, use_container_width = True)

# График 2: Scatter plot
with col2:
    fig_scatter = px.scatter(
        filtered_data,
        x = 'price',
        y = 'number_of_reviews',
        color = 'neighbourhood_group',
        title = 'Цена vs. Количество отзывов',
        labels = {'price': 'Цена ($)', 'number_of_reviews': 'Кол-во отзывов'}
    )
    st.plotly_chart(fig_scatter, use_container_width = True)
    
# График 3: bar chart
st.subheader("Количество предложений по районам")
fig_bar = px.bar(
    filtered_data['neighbourhood_group'].value_counts().reset_index(),
    x = 'neighbourhood_group',
    y = 'count',
    title = 'Предложения по районам',
    labels = {'neighbourhood_group': 'Район', 'count': 'Количество'}
)
st.plotly_chart(fig_bar, use_container_width = True)
