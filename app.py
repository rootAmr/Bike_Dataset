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
# 🔧 Fitur Interaktif
# ======================

# Filter musim
season_options = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}
selected_season = st.selectbox("🗓️ Pilih Musim", options=list(season_options.keys()), format_func=lambda x: season_options[x])

# Konversi kolom 'tanggal' menjadi datetime
data_day['tanggal'] = pd.to_datetime(data_day['tanggal'])

# Sidebar: Pilih rentang tanggal
st.sidebar.header("🗓️ Filter Berdasarkan Tanggal")
min_tanggal = data_day['tanggal'].min()
max_tanggal = data_day['tanggal'].max()

start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal:",
    value=[min_tanggal, max_tanggal],
    min_value=min_tanggal,
    max_value=max_tanggal
)

# Filter data berdasarkan tanggal yang dipilih
filtered_data = data_day[
    (data_day['tanggal'] >= pd.to_datetime(start_date)) &
    (data_day['tanggal'] <= pd.to_datetime(end_date))
]

# ======================
# 🔎 Analisis & Visualisasi
# ======================

st.title('📊 Analisis Penyewaan Sepeda Harian (Dengan Filter Interaktif)')

with st.expander("🔍 Lihat Data Terfilter"):
    st.dataframe(filtered_data)

# Hitung jumlah & persentase penyewaan per jenis hari
jumlah_penyewaan = filtered_data.groupby('jenis_hari')['total_count'].sum().reset_index()
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
st.header('🌡️ Korelasi antara Suhu dan Jumlah Penyewaan Sepeda (Terfilter)')

korelasi = filtered_data['temp'].corr(filtered_data['total_count'])
interpretasi_korelasi = (
    "Terdapat korelasi positif antara suhu dan jumlah total penyewaan sepeda." if korelasi > 0 else
    "Terdapat korelasi negatif antara suhu dan jumlah total penyewaan sepeda." if korelasi < 0 else
    "Tidak ada hubungan linear yang signifikan antara suhu dan jumlah total penyewaan sepeda."
)

scatter_chart = alt.Chart(filtered_data).mark_circle(color='orange').encode(
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
- 📅 Data dianalisis pada musim **{season_options[selected_season]}** antara tanggal **{start_date}** hingga **{end_date}**.
- 📈 **Suhu** tetap menunjukkan hubungan {'positif' if korelasi > 0 else 'negatif' if korelasi < 0 else 'tidak signifikan'} dengan penyewaan.
- 🔍 Interaktif ini memungkinkan eksplorasi data yang lebih fleksibel oleh pengguna.
""")
