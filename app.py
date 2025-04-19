import streamlit as st
import pandas as pd
import altair as alt

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

with st.expander("🔍 Lihat Data"):
    st.dataframe(data_day)

# Hitung jumlah & persentase penyewaan per jenis hari
jumlah_penyewaan = data_day.groupby('jenis_hari')['total_count'].sum().reset_index()
jumlah_penyewaan.columns = ['jenis_hari', 'total_count']
jumlah_penyewaan['persentase'] = (jumlah_penyewaan['total_count'] / jumlah_penyewaan['total_count'].sum()) * 100

st.subheader('🚲 Persentase Penyewaan Sepeda: Hari Kerja vs Hari Libur')

bar_chart = alt.Chart(jumlah_penyewaan).mark_bar(color='skyblue').encode(
    x=alt.X('jenis_hari', title='Jenis Hari'),
    y=alt.Y('total_count', title='Jumlah Penyewaan'),
    tooltip=['jenis_hari', 'total_count', alt.Tooltip('persentase', format='.1f')]
).properties(
    width=600,
    height=400
)

text = alt.Chart(jumlah_penyewaan).mark_text(
    align='center',
    baseline='bottom',
    dy=-5,
    fontWeight='bold'
).encode(
    x='jenis_hari',
    y='total_count',
    text=alt.Text('persentase', format='.1f')
)

st.altair_chart(bar_chart + text, use_container_width=True)

for _, row in jumlah_penyewaan.iterrows():
    st.write(f"- **{row['jenis_hari']}**: {row['total_count']} penyewaan ({row['persentase']:.1f}%)")

# Korelasi suhu dan penyewaan
st.header('🌡️ Korelasi antara Suhu dan Jumlah Penyewaan Sepeda')

korelasi = data_day['temp'].corr(data_day['total_count'])
interpretasi_korelasi = (
    "Terdapat korelasi positif antara suhu dan jumlah total penyewaan sepeda." if korelasi > 0 else
    "Terdapat korelasi negatif antara suhu dan jumlah total penyewaan sepeda." if korelasi < 0 else
    "Tidak ada hubungan linear yang signifikan antara suhu dan jumlah total penyewaan sepeda."
)

scatter_chart = alt.Chart(data_day).mark_circle(color='orange').encode(
    x=alt.X('temp', title='Suhu (°C)'),
    y=alt.Y('total_count', title='Jumlah Penyewaan'),
    tooltip=['temp', 'total_count']
).properties(
    title=f'Korelasi: {korelasi:.2f}',
    width=600,
    height=400
)

st.altair_chart(scatter_chart, use_container_width=True)
st.success(interpretasi_korelasi)

st.header('📝 Kesimpulan')
st.markdown(f"""
- 📅 Analisis dilakukan pada seluruh rentang data yang tersedia.
- 📈 **Suhu** menunjukkan hubungan {'positif' if korelasi > 0 else 'negatif' if korelasi < 0 else 'tidak signifikan'} dengan jumlah penyewaan sepeda.
- 🔍 Analisis ini memberikan gambaran umum pola penyewaan sepeda berdasarkan hari dan suhu.
""")
