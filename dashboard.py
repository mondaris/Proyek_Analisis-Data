import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("all_data.csv")

season_labels = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}
df['Season Name'] = df['season_x'].map(season_labels)

seasonal_rentals = df.groupby('season_x')['cnt_x'].mean().reset_index()
seasonal_rentals.columns = ['Season', 'Average Rentals']

hourly_rentals = df.groupby(['hr', 'weekday_y'])['cnt_y'].mean().reset_index()
hourly_rentals.columns = ['Hour', 'Weekday', 'Average Rentals']

st.title("Dashboard Penyewaan Sepeda")

tab1, tab2 = st.tabs(["Tren Musiman", "Penyewaan Berdasarkan Jam"])

with tab1:
    st.header("Tren Penyewaan Sepeda Berdasarkan Musim")

    st.write("Tabel: Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    st.dataframe(seasonal_rentals)

    st.write("Visualisasi: Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x='Season',
        y='Average Rentals',
        data=seasonal_rentals,
        palette='coolwarm',
        ax=ax
    )
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim", fontsize=14)
    ax.set_xlabel("Musim", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    st.pyplot(fig)

with tab2:
    st.header("Penyewaan Sepeda Berdasarkan Jam dalam Seminggu")

    st.write("Pilih Hari untuk Melihat Rata-rata Penyewaan Berdasarkan Jam")
    weekdays_map = {
        0: "Senin",
        1: "Selasa",
        2: "Rabu",
        3: "Kamis",
        4: "Jumat",
        5: "Sabtu",
        6: "Minggu"
    }
    df['Weekday Name'] = df['weekday_y'].map(weekdays_map)
    selected_day = st.selectbox("Pilih Hari:", list(weekdays_map.values()))

    filtered_data = hourly_rentals[hourly_rentals['Weekday'] == list(weekdays_map.keys())[list(weekdays_map.values()).index(selected_day)]]

    st.write(f"Tabel: Rata-rata Penyewaan Berdasarkan Jam pada {selected_day}")
    st.dataframe(filtered_data)

    st.write(f"Visualisasi: Rata-rata Penyewaan Berdasarkan Jam pada {selected_day}")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        x='Hour',
        y='Average Rentals',
        data=filtered_data,
        marker='o',
        color='blue',
        ax=ax
    )
    ax.set_title(f"Rata-rata Penyewaan Sepeda pada {selected_day}", fontsize=14)
    ax.set_xlabel("Jam (0-23)", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.grid(True)
    st.pyplot(fig)

    # Menghitung rata-rata penyewaan berdasarkan jam
    hourly_rentals = df.groupby('hr')['cnt_y'].mean().reset_index()
    hourly_rentals.columns = ['Hour', 'Average Rentals']

    # Menentukan jam dengan rata-rata tertinggi
    max_rentals = hourly_rentals['Average Rentals'].max()
    max_hour = hourly_rentals[hourly_rentals['Average Rentals'] == max_rentals]['Hour'].values[0]

    # Streamlit Layout
    st.title("Penyewaan Sepeda Berdasarkan Jam dengan Sorotan Rata-rata Tertinggi")

    # Tabel Data
    st.write("Tabel: Rata-rata Penyewaan Sepeda Berdasarkan Jam")
    st.dataframe(hourly_rentals)

    # Visualisasi: Diagram Batang dengan Sorotan
    st.write("Visualisasi: Penyewaan Sepeda Berdasarkan Jam dengan Sorotan pada Rata-rata Tertinggi")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Menentukan warna berdasarkan rata-rata tertinggi
    colors = ['red' if hour == max_hour else 'blue' for hour in hourly_rentals['Hour']]

    # Membuat bar plot
    sns.barplot(
        x='Hour', 
        y='Average Rentals', 
        data=hourly_rentals, 
        palette=colors, 
        ax=ax
    )

    # Menambahkan detail pada plot
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam (0-23)", fontsize=14)
    ax.set_xlabel("Jam (0-23)", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)

    # Menampilkan jam dengan rata-rata tertinggi
    st.write(f"Jam dengan rata-rata penyewaan tertinggi adalah pukul **{max_hour}:00**, dengan rata-rata penyewaan sebesar **{max_rentals:.2f}** sepeda.")
    st.pyplot(fig)