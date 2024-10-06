import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur tampilan halaman
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# Judul untuk dashboard
st.title('Dashboard Penyewaan Sepeda Berdasarkan Musim dan Cuaca')

# Memuat dataset
@st.cache_data
def load_data():
    return pd.read_csv('./data/day.csv')

day_df = load_data()

st.write('Data Penyewaan Sepeda (5 contoh teratas):')
st.write(day_df.head())

# Sidebar untuk memilih Case (Musim atau Cuaca)
st.sidebar.header("Pilih Pertanyaan/Question:")
case_option = st.sidebar.selectbox(
    "Pilih hasil analisis berdasarkan:", 
    options=["Question 1", "Question 2"]
)

if case_option == "Question 1":
    st.header("Bagaimana pengaruh musim terhadap jumlah penyewaan sepeda?")

    avg_season = day_df.groupby('season')['cnt'].mean().reset_index()
    avg_season.columns = ['Musim', 'Rata-rata Penyewaan Sepeda']
    
    season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    avg_season['Musim'] = avg_season['Musim'].map(season_mapping)
    
    st.write(avg_season.to_html(index=False), unsafe_allow_html=True)
    
    # Membuat visualisasi bar chart
    fig_season, ax_season = plt.subplots(figsize=(10, 6))
    sns.barplot(x=avg_season['Musim'], y=avg_season['Rata-rata Penyewaan Sepeda'], ax=ax_season)
    ax_season.set_title('Rata-rata Penyewaan Sepeda per Musim')
    ax_season.set_xlabel('Musim (Season)')
    ax_season.set_ylabel('Jumlah Penyewaan Sepeda')

    # Menampilkan visualisasi pada Streamlit
    st.pyplot(fig_season)

elif case_option == "Question 2":
    st.header("Bagaimana pengaruh cuaca terhadap jumlah penyewaan sepeda?")
    
    avg_weather = day_df.groupby('weathersit')['cnt'].mean().reset_index()
    avg_weather.columns = ['Cuaca', 'Rata-rata Penyewaan Sepeda']

    weather_mapping = {1: 'Clear or partly cloudy', 2: 'Cloudy', 3: 'Light rain + Light snow'}
    avg_weather['Cuaca'] = avg_weather['Cuaca'].map(weather_mapping)

    st.write(avg_weather.to_html(index=False), unsafe_allow_html=True)
    
    # Membuat visualisasi bar chart
    fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
    sns.barplot(x=avg_weather['Cuaca'], y=avg_weather['Rata-rata Penyewaan Sepeda'], ax=ax_weather)
    ax_weather.set_title('Rata-rata Penyewaan Sepeda per Cuaca')
    ax_weather.set_xlabel('Cuaca (Weathersit)')
    ax_weather.set_ylabel('Jumlah Penyewaan Sepeda')

    # Menampilkan visualisasi pada Streamlit
    st.pyplot(fig_weather)
