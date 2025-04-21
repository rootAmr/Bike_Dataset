import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
data_url = "https://raw.githubusercontent.com/rootAmr/Bike_Dataset/refs/heads/main/data_day_clean.csv"
data_day = pd.read_csv(data_url)

# Sidebar untuk filter
st.sidebar.header('Filter Data')
selected_year = st.sidebar.multiselect('Pilih Tahun', sorted(data_day['tahun'].unique()), default=data_day['tahun'].unique())
selected_season = st.sidebar.multiselect('Pilih Musim', sorted(data_day['musim'].unique()), default=data_day['musim'].unique())

# Filter berdasarkan input
filtered_data = data_day[(data_day['tahun'].isin(selected_year)) & (data_day['musim'].isin(selected_season))]

# Konversi kolom 'tanggal' ke datetime
data_day['tanggal'] = pd.to_datetime(data_day['tanggal'])

# Kategorisasi hari
def kategorikan_hari(hari):
    return 'Akhir Pekan/Libur' if hari in ['Sabtu', 'Minggu'] else 'Hari Kerja'

data_day['jenis_hari'] = data_day['weekday'].apply(kategorikan_hari)

# ======================
# 🔎 Analisis & Visualisasi
# ======================

st.title('📊 Analisis Penyewaan Sepeda Harian (Tanpa Filter)')

# Menampilkan data dalam bentuk tabel
with st.expander("🔍 Lihat Data"):
    st.dataframe(data_day)

# Korelasi suhu dan penyewaan
st.header('🌡️ Korelasi antara Suhu dan Jumlah Penyewaan Sepeda')

# Menghitung korelasi antara suhu dan jumlah penyewaan
korelasi = data_day['temp'].corr(data_day['total_count'])

# Interpretasi korelasi
interpretasi_korelasi = (
    "Terdapat korelasi positif antara suhu dan jumlah total penyewaan sepeda." if korelasi > 0 else
    "Terdapat korelasi negatif antara suhu dan jumlah total penyewaan sepeda." if korelasi < 0 else
    "Tidak ada hubungan linear yang signifikan antara suhu dan jumlah total penyewaan sepeda."
)

# Membuat scatter chart untuk korelasi
scatter_chart = alt.Chart(data_day).mark_circle(color='orange').encode(
    x=alt.X('temp', title='Suhu (°C)'),
    y=alt.Y('total_count', title='Jumlah Penyewaan'),
    tooltip=['temp', 'total_count']
).properties(
    title=f'Korelasi: {korelasi:.2f}',
    width=600,
    height=400
)

# Menampilkan chart
st.altair_chart(scatter_chart, use_container_width=True)

# Menampilkan interpretasi korelasi
st.success(interpretasi_korelasi)

# ========================
# Persentase Penyewaan
# ========================

# Section 2: Persentase Penyewaan Hari Kerja vs Libur (sudah kamu buat)
filtered_data['day_type'] = filtered_data['workingday'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Hari Libur')
day_type_rentals = filtered_data.groupby('day_type')['total_count'].sum().reindex(['Hari Kerja', 'Hari Libur'], fill_value=0)
day_type_percent = (day_type_rentals / day_type_rentals.sum()) * 100

st.subheader('🚲 Persentase Penyewaan: Hari Kerja vs Hari Libur')
fig, ax = plt.subplots()
bars = ax.bar(day_type_percent.index, day_type_percent, color=['skyblue', 'salmon'])
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', ha='center', fontweight='bold')
ax.set_ylim(0, 100)
ax.set_ylabel('Persentase (%)')
st.pyplot(fig)

# Menambahkan elemen visual
ax.set_title('Presentase Penyewaan Sepeda: Hari Kerja vs Hari Libur', fontsize=14, fontweight='bold')
ax.set_ylabel('Persentase (%)')
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Menampilkan chart di Streamlit
st.pyplot(fig)

# Menampilkan data dalam format teks
for day_type, percentage in day_type_percent.items():
    st.write(f"- **{day_type}**: {percentage:.1f}%")

# ========================
# Kesimpulan
# ========================

st.header('📝 Kesimpulan')

# Menyusun kesimpulan analisis
st.markdown(f"""
- 📅 Analisis dilakukan pada seluruh rentang data yang tersedia.
- 📈 **Suhu** menunjukkan hubungan {'positif' if korelasi > 0 else 'negatif' if korelasi < 0 else 'tidak signifikan'} dengan jumlah penyewaan sepeda.
- 🔍 Analisis ini memberikan gambaran umum pola penyewaan sepeda berdasarkan hari dan suhu.
""")
