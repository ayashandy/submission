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
    return pd.read_csv('../data/day.csv')

day_df = load_data()

# Menampilkan dataset
st.write('Data Penyewaan Sepeda (5 contoh teratas):')
st.write(day_df.head())

# Rata-rata Penyewaan Sepeda Berdasarkan Musim
st.header("Pengaruh Musim Terhadap Penyewaan Sepeda (Season)")
avg_season = day_df.groupby('season')['cnt'].mean()

# Tampilkan data rata-rata dalam tabel
st.write("Rata-rata Penyewaan Sepeda per Musim:", avg_season, "1 : Winter, 2 : Spring, 3 : Summer, 4 : Fall")

# Membuat visualisasi rata-rata penyewaan sepeda berdasarkan musim
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=day_df['season'], y=day_df['cnt'], ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda per Musim (Season)')
ax.set_xlabel('Musim (Season)')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_xticklabels(['Winter', 'Spring', 'Summer', 'Fall'])

# Menampilkan visualisasi pada Streamlit
st.pyplot(fig)

# Menambahkan slider untuk memilih rentang bulan
st.sidebar.header("Filter Data")
selected_months = st.sidebar.slider('Pilih Rentang Bulan', 1, 12, (1, 12))

# Memfilter data berdasarkan bulan yang dipilih
filtered_data = day_df[(day_df['mnth'] >= selected_months[0]) & (day_df['mnth'] <= selected_months[1])]

# Rata-rata Penyewaan Sepeda Berdasarkan Musim (Filter Bulan)
st.header(f"Pengaruh Musim Terhadap Penyewaan Sepeda per Bulan (Bulan {selected_months[0]} - {selected_months[1]})")
avg_season_filtered = filtered_data.groupby('season')['cnt'].mean().reset_index()
st.write("Rata-rata Penyewaan Sepeda per Musim (Bulan):", avg_season_filtered, "1 : Winter, 2 : Spring, 3 : Summer, 4 : Fall")

# Visualisasi setelah filter
fig_filtered, ax_filtered = plt.subplots(figsize=(10, 6))
sns.barplot(x=filtered_data['season'], y=filtered_data['cnt'], ax=ax_filtered)
ax_filtered.set_title(f'Rata-rata Penyewaan Sepeda per Musim (Bulan)')
ax_filtered.set_xlabel('Musim (Season)')
ax_filtered.set_ylabel('Jumlah Penyewaan Sepeda')
ax_filtered.set_xticklabels(['Winter', 'Spring', 'Summer', 'Fall'])

# Menampilkan visualisasi filtered
st.pyplot(fig_filtered)

# Visualisasi Penyewaan Sepeda Berdasarkan Cuaca (Weathersit)
st.header("Pengaruh Cuaca Terhadap Penyewaan Sepeda (Weather)")
avg_weather = day_df.groupby('weathersit')['cnt'].mean().reset_index()

# Menampilkan data rata-rata per cuaca
st.write("Rata-rata Penyewaan Sepeda per Cuaca:", avg_weather, "1: Clear or partly cloudy, 2: Cloudy, 3: Light rain + Light snow")

# Membuat visualisasi penyewaan sepeda berdasarkan cuaca
fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
sns.barplot(x=day_df['weathersit'], y=day_df['cnt'], ax=ax_weather)
ax_weather.set_title('Rata-rata Penyewaan Sepeda per Cuaca (Weathersit)')
ax_weather.set_xlabel('Cuaca (Weathersit)')
ax_weather.set_ylabel('Jumlah Penyewaan Sepeda')
ax_weather.set_xticklabels(['Clear or partly cloudy', 'Cloudy', 'Light rain + Light snow'])

# Menampilkan visualisasi cuaca pada Streamlit
st.pyplot(fig_weather)

# Sidebar untuk memilih kondisi cuaca
st.sidebar.header("Filter Berdasarkan Cuaca")
selected_weathers = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca", 
    options=[1, 2, 3], 
    format_func=lambda x: {1: 'Clear or partly cloudy', 2: 'Cloudy', 3: 'Light rain + Light snow'}.get(x)
)

# Visualisasi dinamis untuk penyewaan sepeda berdasarkan cuaca yang dipilih
st.header("Visualisasi Penyewaan Sepeda Berdasarkan Kondisi Cuaca yang Dipilih")

if selected_weathers:
    # Memfilter dan mengurutkan data berdasarkan cuaca yang dipilih
    filtered_weather_data = day_df[day_df['weathersit'].isin(selected_weathers)]
    
    # Mengurutkan data berdasarkan urutan cuaca yang dipilih
    filtered_weather_data['weathersit'] = pd.Categorical(
        filtered_weather_data['weathersit'], 
        categories=selected_weathers, 
        ordered=True
    )
    filtered_weather_data = filtered_weather_data.sort_values('weathersit')
    
    # Rata-rata penyewaan per kondisi cuaca yang dipilih
    avg_filtered_weather = filtered_weather_data.groupby('weathersit')['cnt'].mean().reset_index()
    
    # Membuat visualisasi penyewaan sepeda per cuaca yang dipilih
    fig_filtered_weather, ax_filtered_weather = plt.subplots(figsize=(10, 6))
    sns.barplot(x=filtered_weather_data['weathersit'], y=filtered_weather_data['cnt'], ax=ax_filtered_weather)
    ax_filtered_weather.set_title('Rata-rata Penyewaan Sepeda per Cuaca (Filtered)')
    ax_filtered_weather.set_xlabel('Cuaca (Weathersit)')
    ax_filtered_weather.set_ylabel('Jumlah Penyewaan Sepeda')
    ax_filtered_weather.set_xticklabels([ 
        {1: 'Clear or partly cloudy', 2: 'Cloudy', 3: 'Light rain + Light snow'}.get(x) for x in selected_weathers
    ])
    
    # Menampilkan visualisasi bar chart
    st.pyplot(fig_filtered_weather)
    
else:
    st.write("Pilih kondisi cuaca dari sidebar untuk melihat visualisasi.")
