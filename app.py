import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns

# Load data
data_url = "https://raw.githubusercontent.com/rootAmr/Bike_Dataset/refs/heads/main/data_day_clean.csv"
data_day = pd.read_csv(data_url)

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

data_day['day_type'] = data_day['workingday'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Hari Libur')

# Hitung jumlah dan persentase penyewaan per jenis hari
jumlah_penyewaan = (
    data_day.groupby('day_type')['total_count']
    .sum()
    .reset_index()
    .rename(columns={'total_count': 'jumlah_penyewaan'})
)
jumlah_penyewaan['persentase'] = (
    jumlah_penyewaan['jumlah_penyewaan'] / jumlah_penyewaan['jumlah_penyewaan'].sum()
) * 100

# Subheader
st.subheader('🚲 Persentase Penyewaan Sepeda: Hari Kerja vs Hari Libur (Berdasarkan workingday)')

# Membuat bar plot menggunakan Seaborn
plt.figure(figsize=(8, 6))
sns.barplot(x='day_type', y='jumlah_penyewaan', data=jumlah_penyewaan, palette=['skyblue', 'salmon'])

# Menambahkan label persentase di atas batang
for index, row in jumlah_penyewaan.iterrows():
    plt.text(index, row['jumlah_penyewaan'] + 10, f'{row["persentase"]:.1f}%', 
             ha='center', va='bottom', fontweight='bold')

# Memberikan judul dan label sumbu
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Jenis Hari', fontsize=16)
plt.xlabel('Jenis Hari', fontsize=12)
plt.ylabel('Jumlah Penyewaan', fontsize=12)

# Menampilkan chart di Streamlit
st.pyplot(plt)

# Menampilkan data dalam format teks
for _, row in jumlah_penyewaan.iterrows():
    st.write(f"- **{row['day_type']}**: {row['jumlah_penyewaan']} penyewaan ({row['persentase']:.1f}%)")

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
