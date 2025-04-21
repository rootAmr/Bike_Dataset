import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
data_url = "https://raw.githubusercontent.com/rootAmr/Bike_Dataset/refs/heads/main/data_day_CLEAND.csv"
data_day = pd.read_csv(data_url)

# Konversi kolom 'tanggal' ke datetime
data_day['tanggal'] = pd.to_datetime(data_day['tanggal'])

# Konversi kolom kategorikal sesuai isi sebenarnya
data_day['workingday'] = data_day['workingday'].map({'Ya': 1, 'Tidak': 0})
data_day['holiday'] = data_day['holiday'].map({'Ya': 1, 'Tidak': 0})
data_day['day_type'] = data_day['day_type'].map({1: 'Hari Libur', 0: 'Hari Kerja'})  # sesuai datamu

# Pastikan kolom kategorikal
kategori_kolom = ['musim', 'bulan', 'holiday', 'weekday', 'cuaca', 'day_type']
for col in kategori_kolom:
    data_day[col] = data_day[col].astype('category')

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
# Persentase Penyewaan Hari Kerja vs Hari Libur
# ========================

st.subheader('🚲 Persentase Penyewaan: Hari Kerja vs Hari Libur')

# Hitung jumlah penyewaan per jenis hari
day_type_rentals = data_day.groupby('day_type')['total_count'].sum().reindex(['Hari Kerja', 'Hari Libur'], fill_value=0)
day_type_percent = (day_type_rentals / day_type_rentals.sum()) * 100

# Visualisasi bar chart
fig, ax = plt.subplots()
bars = ax.bar(day_type_percent.index, day_type_percent, color=['skyblue', 'salmon'])

# Label persen
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', ha='center', fontweight='bold')

# Tambahan pengaturan visual
ax.set_ylim(0, 100)
ax.set_ylabel('Persentase (%)')
ax.set_title('Persentase Penyewaan Sepeda: Hari Kerja vs Hari Libur', fontsize=14, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Tampilkan chart
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
