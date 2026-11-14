# Proyek Analisis Data: E-Commerce Public Dataset

Analisis data E-Commerce (periode Januari 2017 - Agustus 2018) beserta dashboard interaktif menggunakan Streamlit.

## Pertanyaan Bisnis
1. Kategori produk apa yang menghasilkan total revenue tertinggi dan terendah selama Januari-Agustus 2018, dan kategori mana yang perlu diprioritaskan promosinya?
2. Bagaimana tren jumlah order dan total revenue bulanan dari Januari 2017 sampai Agustus 2018, dan bulan mana yang perlu diperkuat kampanyenya?

Analisis lanjutan: RFM Analysis dengan binning kuartil dan manual grouping.

## Struktur Direktori
```
submission
├───dashboard
│   ├───main_data.csv
│   ├───rfm_data.csv
│   └───dashboard.py
├───data
│   └───(dataset E-Commerce asli, 9 berkas .csv)
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Setup Environment

### Menggunakan Anaconda
```
conda create --name main-ds python=3.12
conda activate main-ds
pip install -r requirements.txt
```

### Menggunakan Shell/Terminal
```
cd submission
python -m venv venv
# Windows: venv\Scripts\activate    |    Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

## Menjalankan Dashboard
Dari folder `submission`:
```
streamlit run dashboard/dashboard.py
```
Dashboard akan terbuka di `http://localhost:8501`.

## Menjalankan Notebook
Buka `notebook.ipynb` dengan Jupyter/Colab dari folder `submission` (agar path `data/` terbaca), lalu pilih Run All.
Bagian akhir notebook menghasilkan `dashboard/main_data.csv` dan `dashboard/rfm_data.csv` yang dipakai dashboard.

## Dashboard Online
Dashboard sudah di-deploy dan dapat diakses di:
https://dashboard-ecommerce-rifqi.streamlit.app/ 


