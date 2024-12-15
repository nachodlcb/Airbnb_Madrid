# IMPORTAMOS LIBRERIAS
import streamlit as st
import pandas as pd
import numpy as np 
import seaborn as sns
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import geopandas as gpd
from branca.colormap import LinearColormap
from streamlit_folium import st_folium
import plotly.express as px
# CONFIGURACION DE LA PAGINA
st.set_page_config(page_title='Análisis de alojamientos de Airbnb en Madrid, España',
                   page_icon=':smiley:', 
                   layout='centered', 
                   initial_sidebar_state='expanded'
)

# FUNCION PARA CARGAR EL DATASET
@st.cache_data
def cargar_datos():
    return pd.read_csv(r'C:\Users\Usuario\Desktop\botcamp\libreria\mi_entorno\modulo2\proyecto2\datos_limpios_listings.csv')

df = cargar_datos()

# TITULO DE LA APLICACION
st.title('Análisis de alojamientos de Airbnb en Madrid, España')

# SUBCATEGORÍAS INTERACTIVAS
subcategoria = st.selectbox('Seleccione una subcategoría', ['Introducción', 'Anuncios', 'Mapas geográficos', 'Análisis de las leyes', 'Power BI'])

# SIDEBAR
st.sidebar.image('pngegg.png', width=200)
st.sidebar.title('Airbnb Madrid')

# FILTROS EN EL SIDEBAR
tipo_alojamiento = st.sidebar.multiselect('Tipo de Alojamiento', df['room_type'].unique())
barrio = st.sidebar.multiselect('Barrio', df['neighbourhood_group_cleansed'].unique())
capacidad = st.sidebar.slider('Capacidad de Alojamiento', min_value=int(df['accommodates'].min()), max_value=int(df['accommodates'].max()), value=(int(df['accommodates'].min()), int(df['accommodates'].max())))
rango_precio = st.sidebar.slider('Rango de Precios', min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(int(df['price'].min()), int(df['price'].max())))

# APLICAR FILTROS
df_filtrado = df.copy()

if tipo_alojamiento:
    df_filtrado = df_filtrado[df_filtrado['room_type'].isin(tipo_alojamiento)]

if barrio:
    df_filtrado = df_filtrado[df_filtrado['neighbourhood_group_cleansed'].isin(barrio)]

df_filtrado = df_filtrado[(df_filtrado['accommodates'] >= capacidad[0]) & (df_filtrado['accommodates'] <= capacidad[1])]
df_filtrado = df_filtrado[(df_filtrado['price'] >= rango_precio[0]) & (df_filtrado['price'] <= rango_precio[1])]

# MOSTRAR DATOS FILTRADOS
st.write(f"Total de alojamientos encontrados: {df_filtrado.shape[0]}")
st.dataframe(df_filtrado)

# MOSTRAR GRÁFICOS SEGÚN LA SUBCATEGORÍA SELECCIONADA
if subcategoria == 'Introducción':
    col1, col2, col3 = st.columns(3)
    st.markdown("""
        - **Introducción:** En esta sección se mostrará una introducción al análisis de los alojamientos de Airbnb en Madrid, España.
        Es la capital de España y conocida habitualmente como Villa y Corte, Madrid es la mayor ciudad del país y la segunda de la Unión Europea, con una población de más de 3 millones de habitantes (más de 6 en el área metropolitana).
        """)
    
    with col1:
        st.markdown("""
        Entire home/apt    6210
        Private room       4564
        Shared room          84
        Hotel room           62    
        """)
    
    with col2:
        st.markdown("""
        Barrios más caros: Centro, Salamanca, Chamartín y Chamberí
        Barrios más baratos: Vicálvaro, Usera, Puente de Vallecas y Villa de Vallecas
        """)

    with col3:("""            
        Destacar que el centro de Madrid concentra la mayor cantidad de alojamientos de Airbnb.
        """)

elif subcategoria == 'Anuncios':
    st.subheader('Cantidad de Anuncios a lo Largo del Tiempo')
    
    # Suponiendo que hay un dataframe 'calendar' con las columnas 'date' y 'available'
    calendar = pd.read_csv(r'C:\Users\Usuario\Desktop\botcamp\libreria\mi_entorno\modulo2\proyecto2\datos_limpios_calendar.csv')
    anuncios_por_fecha = calendar.groupby('date')['available'].sum().reset_index(name='count')
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=anuncios_por_fecha, x='date', y='count', marker='o', color='skyblue')
    plt.title('Número de Anuncios Disponibles a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Anuncios Disponibles')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
    st.subheader('Tiempo de Respuesta por cada Anuncio')

    # Contar la cantidad de anuncios por tiempo de respuesta
    anuncios_por_tiempo = df['host_response_time'].value_counts().reset_index()
    anuncios_por_tiempo.columns = ['host_response_time', 'count']

    # Crear un gráfico de línea para mostrar la cantidad de anuncios por tiempo de respuesta
    fig = px.line(anuncios_por_tiempo, x='host_response_time', y='count', 
                title='Tiempo de Respuesta por cada Anuncio', markers=True)

    # Mostrar el gráfico interactivo en Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif subcategoria == 'Mapas geográficos':
    st.subheader('Precios distribuidos por Barrios')
    
    # Gráfico de dispersión
    fig, ax = plt.subplots(figsize=(10, 8))
    df.plot(kind='scatter', x='longitude', y='latitude', alpha=0.4, c='price', cmap='viridis', colorbar=True, ax=ax)
    st.pyplot(fig)
    
    # Mapa interactivo con Folium
    st.subheader('Mapa Interactivo de Precios')
    map1 = folium.Map(location=[40.4165, -3.70256], zoom_start=12)
    
    # Creamos un solo grupo de marcadores
    marker_cluster = MarkerCluster()
    
    # Iteramos sobre el DataFrame directamente usando itertuples (más eficiente que zip)
    for row in df.itertuples():
        folium.Marker(
            location=[row.latitude, row.longitude],
            popup=f'Price: {row.price}'
        ).add_to(marker_cluster)
    
    # Añadimos el cluster al mapa
    marker_cluster.add_to(map1)
    
    # Mostramos el mapa en Streamlit
    st_folium(map1, width=700, height=500)

elif subcategoria == 'Power BI':
    # Mostrar el informe de Power BI
    st.subheader('Informe de Power BI')
    powerbi_url = f"https://app.powerbi.com/view?r=eyJrIjoiZDA1NmFiODMtYzNhZi00ZjQ0LTllZDgtM2RiNzFmOTVkNjBlIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9"
    # Mostrar el informe en un iframe
    st.markdown(
    f"""
    <iframe width="100%" height="600"
            src="{powerbi_url}"
            frameborder="0" allowFullScreen="true"></iframe>
    """,
    unsafe_allow_html=True
    )

elif subcategoria == 'Análisis de las leyes':
    # Mostrar el texto sobre la nueva normativa
    st.subheader('Nueva Normativa de Apartamentos Turísticos de Madrid')
    st.markdown("""
    - La nueva normativa de apartamentos turísticos de Madrid fue aprobada el pasado año 2020 para frenar la transformación de pisos en alojamientos turísticos, especialmente en el centro de la urbe.

    En la capital existían casi 17.000 viviendas de uso turístico (VUT) en agosto de dicho año, por lo que esta regularización afectó a un enorme porcentaje de las mismas. Pero.. ¿cuáles son los principales cambios de este texto?

    **3 puntos importantes de la nueva normativa de apartamentos turísticos de Madrid**
    Hay tres aspectos fundamentales en el Plan Especial de Hospedaje (oficialmente Plan Especial de regulación del uso de servicios terciarios en la clase de hospedaje y extraoficialmente ley ‘anti Airbnb’) de Madrid:

    1. **Acceso y ascensor independientes**
    Los pisos turísticos tendrán que contar con acceso y ascensor independientes, si fuera necesario, del resto de vecinos del edificio.

    2. **Recepción**
    Si los alojamientos turísticos están en los anillos 1 y 2, deben tener una recepción entre el exterior del edificio y el interior de la propiedad.

    3. **Aprobación municipal**
    Se necesita aprobación municipal para destinar un edificio entero al alquiler turístico.

    **IMPORTANTE:** esta legislación limita a 90 días la posibilidad de alquilar una vivienda con fines turísticos sin permiso, por lo que a partir de ese plazo es obligatorio disponer de una licencia de uso terciario de hospedaje.
    """)

    # Mostrar el número de viviendas con maximum_nights superior a 90 días
    st.subheader('Viviendas con Maximum Nights Superior a 90 Días')
    viviendas_90_dias = df[df['maximum_nights'] > 90]
    st.write(f"Número de viviendas con maximum nights superior a 90 días: {viviendas_90_dias.shape[0]}")

    # Gráfico circular para mostrar la distribución de esas casas según el tipo de habitación
    st.subheader('Distribución de Viviendas con Maximum Nights Superior a 90 Días por Tipo de Habitación')
    fig, ax = plt.subplots()
    viviendas_90_dias['room_type'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)