# 🚲  Analisis dan Dasbor Capital Bikeshare

## 📝  Analisis dengan Jupyter Notebook

Lihat detail analisis dan visualisasi pada [notebook](https://colab.research.google.com/drive/1XfNXg2WmAXtFVu6Y_0b7vLM_Uiloy0On?usp=sharing) 

### Pertanyaan
1. Apa korelasi antara suhu dan jumlah total sepeda yang disewa?
2. Berapa peresentasi penyewaan sepeda berbeda antara hari kerja dan hari libur?

### Jawaban
1.Terdapat hubungan positif antara suhu dan jumlah total sepeda, informasi ini bisa berguna untuk pengelola sistem penyewaan sepeda. Mereka dapat mengoptimalkan strategi pemasaran atau menyesuaikan inventaris sepeda berdasarkan perubahan musim.

2. Terdapat perbedaan yang signifikan dalam pola penyewaan sepeda antara hari kerja dan hari libur. Mayoritas penyewaan terjadi pada hari kerja, sedangkan penyewaan pada hari libur merupakan sebagian kecil dari total penyewaan sepeda. Ini mungkin disebabkan oleh aktivitas bersepeda yang lebih tinggi di hari kerja, saat orang-orang mungkin menggunakan sepeda untuk transportasi sehari-hari.

## 📊 Dasbor dengan Streamlit
### Streamlit Cloud

Lihat dasbor secara langsung di streamlit cloud melalui tautan ini: https://dashboarda.streamlit.app/

### Menjalankan Streamlit Secara Lokal

#### Install Dependensi

Untuk menginstal semua perpustakaan yang diperlukan, buka terminal/prompt perintah/conda prompt, navigasi ke folder proyek ini, dan jalankan perintah berikut:

```bash
pip install -r requirements.txt
```
### run app
```bash
streamlit run app.py
```
