import streamlit as st
import pandas as pd
import sidetable as stb 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title("Análisis :blue[vehicular] : Estados Unidos")
st.write("Exploración y visualización de datos de vehículos en EE.UU.")

# Cargar el archivo CSV
file_path = 'datasets/vehicles_us.csv'
raw_data = pd.read_csv(file_path)

# Convertir date_posted a tipo datetime
raw_data['date_posted'] = pd.to_datetime(raw_data['date_posted'])

st.header('Tipos de datos de las columnas:')
st.dataframe(raw_data.dtypes.rename('datatype'))

st.header('Primeras y últimas filas del dataset:')
st.dataframe(raw_data.head())
st.dataframe(raw_data.tail())

st.header('Valores ausentes:')
st.dataframe(raw_data.stb.missing(style=True))

st.header('Revisar filas duplicadas:')
st.write(f'El número de filas duplicadas es: {raw_data.duplicated().sum()}')

st.header('Limpieza y curación de los datos')
clean_data = raw_data.copy()

# Llenar valores nulos
clean_data['model_year'].fillna(clean_data['model_year'].median(), inplace=True)
clean_data['cylinders'].fillna(clean_data['cylinders'].median(), inplace=True)
clean_data['odometer'].fillna(clean_data['odometer'].median(), inplace=True)
clean_data['paint_color'].fillna('unknown', inplace=True)
clean_data['is_4wd'].fillna(0, inplace=True)

# Convertir is_4wd en booleano
clean_data['is_4wd'] = clean_data['is_4wd'].astype(bool)

# Eliminar columna 'color' (parece ser 'paint_color')
clean_data.drop(columns=['paint_color'], inplace=True)

# Resetear el índice
clean_data.reset_index(drop=True, inplace=True)

st.dataframe(clean_data.head())

st.subheader('Total de filas en el dataframe después de limpieza')
st.write(len(clean_data))

st.header('Valores ausentes después de limpieza')
st.dataframe(clean_data.stb.missing(style=True))

st.header('Estadísticas descriptivas de los datos numéricos')
st.write(clean_data.describe())

st.header('Distribución de Precios')
fig, ax = plt.subplots()
sns.histplot(clean_data['price'], bins=50, kde=True, ax=ax)
st.pyplot(fig)

st.header('Distribución de Modelos por Año')
st.line_chart(clean_data, x='model_year', y='price')

st.header('Gráfico de Barras: Model vs. Type')
st.write("Seleccione el tipo de vehículo para filtrar los modelos correspondientes.")
selected_type = st.selectbox("Seleccione un tipo de vehículo:", clean_data['type'].unique())
filtered_data = clean_data[clean_data['type'] == selected_type]
fig_bar = px.bar(filtered_data, x='model', title=f'Modelos de vehículos - {selected_type}')
st.plotly_chart(fig_bar)

st.header('Histograma: Condition vs. Model Year')
fig_hist = px.histogram(clean_data, x='model_year', color='condition', barmode='group', title='Condición de los vehículos por año modelo')
st.plotly_chart(fig_hist)

st.header('Comparador de Precios entre Modelos')
st.write("Seleccione dos modelos para comparar precios.")
model_options = clean_data['model'].unique()
model_1 = st.selectbox("Seleccione el primer modelo:", model_options)
model_2 = st.selectbox("Seleccione el segundo modelo:", model_options)

filtered_data_comp = clean_data[(clean_data['model'] == model_1) | (clean_data['model'] == model_2)]
fig_comp = px.histogram(filtered_data_comp, x='model', y='price', color='model', barmode='group', title=f'Comparación de precios entre {model_1} y {model_2}')
st.plotly_chart(fig_comp)

