import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Dashboard E-Commerce", page_icon="🛒", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COLOR_MAIN = "#1f77b4"
COLOR_LOW = "#d62728"
COLOR_ACCENT = "#2ca02c"


@st.cache_data
def load_data():
    main_df = pd.read_csv(
        os.path.join(BASE_DIR, "main_data.csv"),
        parse_dates=["order_purchase_timestamp"],
    )
    rfm_df = pd.read_csv(os.path.join(BASE_DIR, "rfm_data.csv"))
    return main_df, rfm_df


def fmt_thousand(x, _):
    return f"{x / 1000:,.0f}K"


main_df, rfm_df = load_data()

# ---------------- Sidebar ----------------
st.sidebar.header("Filter Data")
min_date = main_df["order_purchase_timestamp"].min().date()
max_date = main_df["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Rentang tanggal order",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

all_categories = sorted(main_df["product_category"].unique())
selected_categories = st.sidebar.multiselect(
    "Kategori produk (kosongkan untuk semua)", all_categories
)
top_n = st.sidebar.slider("Jumlah kategori ditampilkan", 5, 15, 10)

filtered_df = main_df[
    (main_df["order_purchase_timestamp"].dt.date >= start_date)
    & (main_df["order_purchase_timestamp"].dt.date <= end_date)
]
if selected_categories:
    filtered_df = filtered_df[filtered_df["product_category"].isin(selected_categories)]

# ---------------- Header ----------------
st.title("Dashboard Analisis E-Commerce")
st.caption(
    "Data: E-Commerce Public Dataset, order berstatus delivered, "
    "Januari 2017 - Agustus 2018. Nilai dalam Real Brasil (R$)."
)

if filtered_df.empty:
    st.warning("Tidak ada data untuk filter yang dipilih. Ubah rentang tanggal atau kategori.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"R$ {filtered_df['price'].sum():,.0f}")
col2.metric("Jumlah Order", f"{filtered_df['order_id'].nunique():,}")
col3.metric("Jumlah Pelanggan Unik", f"{filtered_df['customer_unique_id'].nunique():,}")

# ---------------- Pertanyaan 1 ----------------
st.header("Kategori Produk dengan Revenue Tertinggi dan Terendah")
category_revenue = (
    filtered_df.groupby("product_category")["price"].sum().sort_values(ascending=False)
)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
top = category_revenue.head(top_n).sort_values()
bottom = category_revenue.tail(top_n).sort_values(ascending=False)

axes[0].barh(top.index, top.values, color=COLOR_MAIN)
axes[0].set_title(f"{len(top)} Kategori Revenue Tertinggi", fontsize=13, fontweight="bold")
axes[0].xaxis.set_major_formatter(mtick.FuncFormatter(fmt_thousand))

axes[1].barh(bottom.index, bottom.values, color=COLOR_LOW)
axes[1].set_title(f"{len(bottom)} Kategori Revenue Terendah", fontsize=13, fontweight="bold")

for ax in axes:
    ax.set_xlabel("Revenue (R$)")
    ax.set_ylabel("")
    ax.set_xlim(left=0)
plt.tight_layout()
st.pyplot(fig)

# ---------------- Pertanyaan 2 ----------------
st.header("Tren Order dan Revenue Bulanan")
monthly_df = (
    filtered_df.groupby("order_month")
    .agg(order_count=("order_id", "nunique"), revenue=("price", "sum"))
    .reset_index()
)

fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
axes[0].plot(monthly_df["order_month"], monthly_df["order_count"], marker="o", color=COLOR_MAIN, linewidth=2)
axes[0].set_title("Jumlah Order per Bulan", fontsize=13, fontweight="bold")
axes[0].set_ylabel("Jumlah order")
axes[0].set_ylim(0, monthly_df["order_count"].max() * 1.15)

axes[1].plot(monthly_df["order_month"], monthly_df["revenue"], marker="o", color=COLOR_ACCENT, linewidth=2)
axes[1].set_title("Total Revenue per Bulan", fontsize=13, fontweight="bold")
axes[1].set_ylabel("Revenue (R$)")
axes[1].yaxis.set_major_formatter(mtick.FuncFormatter(fmt_thousand))
axes[1].set_ylim(0, monthly_df["revenue"].max() * 1.15)

plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# ---------------- Analisis lanjutan: RFM ----------------
st.header("Segmentasi Pelanggan (RFM)")
st.caption(
    "Segmentasi dihitung dari seluruh periode data dan tidak terpengaruh filter di sidebar. "
    "Hanya sekitar 3% pelanggan yang pernah membeli lebih dari satu kali."
)

segment_summary = (
    rfm_df.groupby("segment")
    .agg(
        customers=("customer_unique_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
    )
    .sort_values("customers")
)

col_a, col_b, col_c = st.columns(3)
col_a.metric("Rata-rata Recency", f"{rfm_df['recency'].mean():,.0f} hari")
col_b.metric("Rata-rata Frequency", f"{rfm_df['frequency'].mean():.2f} order")
col_c.metric("Rata-rata Monetary", f"R$ {rfm_df['monetary'].mean():,.0f}")

fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].barh(segment_summary.index, segment_summary["customers"], color=COLOR_MAIN)
axes[0].set_title("Jumlah Pelanggan per Segmen", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Jumlah pelanggan")

axes[1].barh(segment_summary.index, segment_summary["avg_monetary"], color="#ff7f0e")
axes[1].set_title("Rata-rata Monetary per Segmen", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Rata-rata nilai belanja (R$)")
axes[1].set_yticklabels([])
for ax in axes:
    ax.set_xlim(left=0)
plt.tight_layout()
st.pyplot(fig)

with st.expander("Lihat tabel ringkasan segmen"):
    st.dataframe(segment_summary.sort_values("customers", ascending=False).round(1))

st.caption("Proyek Analisis Data - E-Commerce Public Dataset")
