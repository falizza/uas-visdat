# ============================================================
# NB02 - EXPLORATORY DATA ANALYSIS (EDA)
# Proyek UAS Visualisasi Data dan Informasi
# "Sepuh dan Sejahtera: Mengurai Pola Spasial
#  Penuaan Penduduk di Jawa dan Sumatera"
#
# Input:
#   output/panel_clean.csv
#   data/peta_kabkota_jawa_sumatera.geojson
#
# Output:
#   output/eda/
#       tabel/
#       grafik/
#       peta/
# ============================================================


# ============================================================
# 1. IMPORT LIBRARY
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import geopandas as gpd

from scipy.stats import pearsonr, spearmanr


# ============================================================
# 2. KONFIGURASI FOLDER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
EDA_DIR = OUTPUT_DIR / "eda"

TABLE_DIR = EDA_DIR / "tabel"
FIG_DIR = EDA_DIR / "grafik"
MAP_DIR = EDA_DIR / "peta"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)
MAP_DIR.mkdir(parents=True, exist_ok=True)

PANEL_PATH = OUTPUT_DIR / "panel_clean.csv"

GEOJSON_PATH = (
    BASE_DIR
    / "data"
    / "peta_kabkota_jawa_sumatera.geojson"
)


# ============================================================
# 3. LOAD DATA
# ============================================================

print("=" * 70)
print("LOAD DATA")
print("=" * 70)

panel = pd.read_csv(PANEL_PATH)

print(f"Data berhasil dibaca: {PANEL_PATH}")
print(f"Ukuran data: {panel.shape}")

print("\n5 baris pertama:")
print(panel.head())


# ============================================================
# 4. VALIDASI DATA
# ============================================================

print("\n" + "=" * 70)
print("VALIDASI DATA")
print("=" * 70)

print("\nDimensi:")
print(panel.shape)

print("\nTahun:")
print(sorted(panel["Tahun"].unique()))

print("\nJumlah kab/kota:")
print(panel["Kab_kota"].nunique())

print("\nJumlah provinsi:")
print(panel["Provinsi"].nunique())

print("\nPulau:")
print(panel["Pulau"].value_counts())

print("\nMissing value:")
print(panel.isna().sum())

print("\nDuplikasi Kab_kota-Tahun:")
dup = panel.duplicated(subset=["Kab_kota", "Tahun"]).sum()
print(dup)

if dup == 0:
    print("✓ Tidak ada duplikasi Kab_kota-Tahun")
else:
    print("⚠ Terdapat duplikasi!")


# ============================================================
# 5. DEFINISI VARIABEL ANALISIS
# ============================================================

numeric_vars = [
    "jumlah_penduduk",
    "jumlah_lansia",
    "pct_lansia",
    "pct_anak",
    "rasio_lansia",
    "p0_miskin",
    "rls",
    "pengeluaran",
    "ahh_laki",
    "ahh_perempuan",
    "ahh_rata2",
    "tpt_total"
]

ageing_var = "pct_lansia"

welfare_vars = [
    "p0_miskin",
    "rls",
    "pengeluaran",
    "ahh_rata2",
    "tpt_total"
]


# ============================================================
# 6. STATISTIK DESKRIPTIF KESELURUHAN
# ============================================================

print("\n" + "=" * 70)
print("STATISTIK DESKRIPTIF KESELURUHAN")
print("=" * 70)

desc = panel[numeric_vars].describe().T

desc["median"] = panel[numeric_vars].median()

desc = desc[
    [
        "count",
        "mean",
        "std",
        "min",
        "25%",
        "median",
        "50%",
        "75%",
        "max"
    ]
]

print(desc.round(3))

desc.to_csv(
    TABLE_DIR / "01_statistik_deskriptif.csv"
)


# ============================================================
# 7. STATISTIK PER TAHUN
# ============================================================

print("\n" + "=" * 70)
print("PERKEMBANGAN PER TAHUN")
print("=" * 70)

year_summary = (
    panel
    .groupby("Tahun")
    .agg(
        jumlah_kab_kota=("Kab_kota", "nunique"),
        jumlah_lansia_total=("jumlah_lansia", "sum"),
        rata_pct_lansia=("pct_lansia", "mean"),
        median_pct_lansia=("pct_lansia", "median"),
        rata_p0_miskin=("p0_miskin", "mean"),
        rata_rls=("rls", "mean"),
        rata_pengeluaran=("pengeluaran", "mean"),
        rata_ahh=("ahh_rata2", "mean"),
        rata_tpt=("tpt_total", "mean")
    )
    .reset_index()
)

print(year_summary.round(3))

year_summary.to_csv(
    TABLE_DIR / "02_ringkasan_per_tahun.csv",
    index=False
)


# ============================================================
# 8. PERBANDINGAN JAWA VS SUMATERA
# ============================================================

print("\n" + "=" * 70)
print("PERBANDINGAN JAWA VS SUMATERA")
print("=" * 70)

island_summary = (
    panel
    .groupby("Pulau")
    .agg(
        jumlah_kab_kota=("Kab_kota", "nunique"),
        rata_pct_lansia=("pct_lansia", "mean"),
        median_pct_lansia=("pct_lansia", "median"),
        min_pct_lansia=("pct_lansia", "min"),
        max_pct_lansia=("pct_lansia", "max"),
        rata_p0_miskin=("p0_miskin", "mean"),
        rata_rls=("rls", "mean"),
        rata_pengeluaran=("pengeluaran", "mean"),
        rata_ahh=("ahh_rata2", "mean"),
        rata_tpt=("tpt_total", "mean")
    )
    .reset_index()
)

print(island_summary.round(3))

island_summary.to_csv(
    TABLE_DIR / "03_ringkasan_jawa_sumatera.csv",
    index=False
)


# ============================================================
# 9. PERBANDINGAN PULAU PER TAHUN
# ============================================================

island_year = (
    panel
    .groupby(["Tahun", "Pulau"])
    .agg(
        rata_pct_lansia=("pct_lansia", "mean"),
        median_pct_lansia=("pct_lansia", "median"),
        rata_p0_miskin=("p0_miskin", "mean"),
        rata_rls=("rls", "mean"),
        rata_pengeluaran=("pengeluaran", "mean"),
        rata_ahh=("ahh_rata2", "mean"),
        rata_tpt=("tpt_total", "mean")
    )
    .reset_index()
)

print("\nRingkasan pulau per tahun:")
print(island_year.round(3))

island_year.to_csv(
    TABLE_DIR / "04_pulau_per_tahun.csv",
    index=False
)


# ============================================================
# 10. RINGKASAN PER PROVINSI
# ============================================================

print("\n" + "=" * 70)
print("RINGKASAN PER PROVINSI")
print("=" * 70)

province_summary = (
    panel
    .groupby(["Pulau", "Provinsi"])
    .agg(
        jumlah_kab_kota=("Kab_kota", "nunique"),
        rata_pct_lansia=("pct_lansia", "mean"),
        median_pct_lansia=("pct_lansia", "median"),
        min_pct_lansia=("pct_lansia", "min"),
        max_pct_lansia=("pct_lansia", "max"),
        rata_p0_miskin=("p0_miskin", "mean"),
        rata_rls=("rls", "mean"),
        rata_pengeluaran=("pengeluaran", "mean"),
        rata_ahh=("ahh_rata2", "mean"),
        rata_tpt=("tpt_total", "mean")
    )
    .reset_index()
)

province_summary = province_summary.sort_values(
    "rata_pct_lansia",
    ascending=False
)

print(province_summary.round(3))

province_summary.to_csv(
    TABLE_DIR / "05_ringkasan_provinsi.csv",
    index=False
)


# ============================================================
# 11. TOP 10 KAB/KOTA DENGAN PCT LANSIA TERTINGGI
#    PER TAHUN
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 PCT LANSIA TERTINGGI PER TAHUN")
print("=" * 70)

top10 = (
    panel.groupby("Tahun", group_keys=False)
    .apply(
        lambda x: x.nlargest(10, "pct_lansia"),
        include_groups=True
    )
    .reset_index(drop=True)
)

print(
    top10[
        [
            "Tahun",
            "Kab_kota",
            "Provinsi",
            "Pulau",
            "pct_lansia",
            "p0_miskin",
            "rls",
            "pengeluaran",
            "ahh_rata2"
        ]
    ].to_string(index=False)
)

# ============================================================
# 12. BOTTOM 10 KAB/KOTA
# ============================================================
print("\n" + "=" * 70)
print("BOTTOM 10 PCT LANSIA TERENDAH PER TAHUN")
print("=" * 70)

bottom10 = (
    panel.groupby("Tahun", group_keys=False)
    .apply(
        lambda x: x.nsmallest(10, "pct_lansia"),
        include_groups=True
    )
    .reset_index(drop=True)
)

print(
    bottom10[
        [
            "Tahun",
            "Kab_kota",
            "Provinsi",
            "Pulau",
            "pct_lansia",
            "p0_miskin",
            "rls",
            "pengeluaran",
            "ahh_rata2"
        ]
    ].to_string(index=False)
)

# ============================================================
# 13. PERUBAHAN PCT LANSIA 2020 → 2024
# ============================================================

print("\n" + "=" * 70)
print("PERUBAHAN PCT LANSIA 2020-2024")
print("=" * 70)

pivot_age = (
    panel
    .pivot(
        index=["Pulau", "Provinsi", "Kab_kota"],
        columns="Tahun",
        values="pct_lansia"
    )
    .reset_index()
)

pivot_age.columns.name = None

pivot_age["delta_pct_lansia"] = (
    pivot_age[2024] - pivot_age[2020]
)

pivot_age["persen_perubahan_pct_lansia"] = (
    pivot_age["delta_pct_lansia"]
    / pivot_age[2020]
    * 100
)

# Ganti nama kolom tahun agar aman untuk GeoJSON
pivot_age = pivot_age.rename(
    columns={
        2020: "pct_lansia_2020",
        2024: "pct_lansia_2024"
    }
)

change_summary = pivot_age.sort_values(
    "delta_pct_lansia",
    ascending=False
)

print("\n10 kenaikan terbesar:")
print(change_summary.head(10).round(3))

print("\n10 kenaikan terkecil / penurunan terbesar:")
print(change_summary.tail(10).round(3))

change_summary.to_csv(
    TABLE_DIR / "08_perubahan_pct_lansia_2020_2024.csv",
    index=False
)


# ============================================================
# 14. PERUBAHAN JUMLAH LANSIA
# ============================================================

pivot_lansia = (
    panel
    .pivot(
        index=["Pulau", "Provinsi", "Kab_kota"],
        columns="Tahun",
        values="jumlah_lansia"
    )
    .reset_index()
)

pivot_lansia["delta_jumlah_lansia"] = (
    pivot_lansia[2024] - pivot_lansia[2020]
)

pivot_lansia["pertumbuhan_jumlah_lansia"] = (
    (pivot_lansia[2024] - pivot_lansia[2020])
    / pivot_lansia[2020]
    * 100
)

pivot_lansia.to_csv(
    TABLE_DIR / "09_perubahan_jumlah_lansia_2020_2024.csv",
    index=False
)


# ============================================================
# 15. DISTRIBUSI PCT LANSIA
# ============================================================

print("\n" + "=" * 70)
print("MEMBUAT GRAFIK DISTRIBUSI")
print("=" * 70)

plt.figure(figsize=(10, 6))

sns.histplot(
    data=panel,
    x="pct_lansia",
    bins=30,
    kde=True
)

plt.axvline(
    panel["pct_lansia"].mean(),
    linestyle="--",
    label=f"Mean = {panel['pct_lansia'].mean():.2f}%"
)

plt.axvline(
    panel["pct_lansia"].median(),
    linestyle=":",
    label=f"Median = {panel['pct_lansia'].median():.2f}%"
)

plt.xlabel("Persentase Penduduk Lansia (%)")
plt.ylabel("Frekuensi")
plt.title("Distribusi Persentase Penduduk Lansia\n2020–2024")
plt.legend()

plt.tight_layout()

plt.savefig(
    FIG_DIR / "01_distribusi_pct_lansia.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 16. BOXPLOT JAWA VS SUMATERA
# ============================================================

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=panel,
    x="Pulau",
    y="pct_lansia"
)

sns.stripplot(
    data=panel,
    x="Pulau",
    y="pct_lansia",
    alpha=0.25,
    size=3
)

plt.xlabel("Pulau")
plt.ylabel("Persentase Penduduk Lansia (%)")
plt.title("Distribusi Persentase Penduduk Lansia\nJawa dan Sumatera, 2020–2024")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "02_boxplot_jawa_sumatera.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 17. TREN PCT LANSIA 2020–2024
# ============================================================

plt.figure(figsize=(10, 6))

trend = (
    panel
    .groupby("Tahun")["pct_lansia"]
    .mean()
    .reset_index()
)

sns.lineplot(
    data=trend,
    x="Tahun",
    y="pct_lansia",
    marker="o",
    linewidth=2.5
)

plt.xticks(sorted(panel["Tahun"].unique()))
plt.xlabel("Tahun")
plt.ylabel("Rata-rata Persentase Lansia (%)")
plt.title("Perkembangan Rata-rata Persentase Penduduk Lansia\n2020–2024")

plt.grid(alpha=0.2)

plt.tight_layout()

plt.savefig(
    FIG_DIR / "03_tren_pct_lansia_nasional.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 18. TREN JAWA VS SUMATERA
# ============================================================

plt.figure(figsize=(10, 6))

sns.lineplot(
    data=island_year,
    x="Tahun",
    y="rata_pct_lansia",
    hue="Pulau",
    marker="o",
    linewidth=2.5
)

plt.xticks(sorted(panel["Tahun"].unique()))
plt.xlabel("Tahun")
plt.ylabel("Rata-rata Persentase Lansia (%)")
plt.title("Perkembangan Persentase Lansia\nJawa vs Sumatera, 2020–2024")

plt.grid(alpha=0.2)

plt.tight_layout()

plt.savefig(
    FIG_DIR / "04_tren_jawa_vs_sumatera.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 19. TREN PER PROVINSI
# ============================================================

province_year = (
    panel
    .groupby(["Tahun", "Provinsi"])["pct_lansia"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(14, 8))

sns.lineplot(
    data=province_year,
    x="Tahun",
    y="pct_lansia",
    hue="Provinsi",
    marker="o"
)

plt.xticks(sorted(panel["Tahun"].unique()))
plt.xlabel("Tahun")
plt.ylabel("Rata-rata Persentase Lansia (%)")
plt.title("Perkembangan Persentase Lansia per Provinsi\n2020–2024")

plt.legend(
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    fontsize=8
)

plt.grid(alpha=0.2)

plt.tight_layout()

plt.savefig(
    FIG_DIR / "05_tren_per_provinsi.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 20. BAR CHART PROVINSI
# ============================================================

province_2024 = (
    panel[panel["Tahun"] == 2024]
    .groupby(["Pulau", "Provinsi"])["pct_lansia"]
    .mean()
    .reset_index()
    .sort_values("pct_lansia", ascending=True)
)

plt.figure(figsize=(10, 8))

sns.barplot(
    data=province_2024,
    y="Provinsi",
    x="pct_lansia",
    hue="Pulau",
    dodge=False
)

plt.xlabel("Persentase Lansia (%)")
plt.ylabel("Provinsi")
plt.title("Persentase Lansia per Provinsi, 2024")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "06_provinsi_pct_lansia_2024.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 21. KORELASI AGEING DENGAN INDIKATOR SOSIAL EKONOMI
# ============================================================

print("\n" + "=" * 70)
print("KORELASI PCT LANSIA DENGAN INDIKATOR SOSIAL EKONOMI")
print("=" * 70)

correlation_results = []

for var in welfare_vars:

    temp = panel[[ageing_var, var]].dropna()

    pearson_r, pearson_p = pearsonr(
        temp[ageing_var],
        temp[var]
    )

    spearman_r, spearman_p = spearmanr(
        temp[ageing_var],
        temp[var]
    )

    correlation_results.append({
        "variabel": var,
        "pearson_r": pearson_r,
        "pearson_p": pearson_p,
        "spearman_rho": spearman_r,
        "spearman_p": spearman_p
    })

correlation_results = pd.DataFrame(
    correlation_results
)

print(
    correlation_results.round(4)
)

correlation_results.to_csv(
    TABLE_DIR / "10_korelasi_pct_lansia_sosial_ekonomi.csv",
    index=False
)


# ============================================================
# 22. SCATTERPLOT AGEING VS KEMISKINAN
# ============================================================

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=panel,
    x="pct_lansia",
    y="p0_miskin",
    hue="Pulau",
    alpha=0.55
)

sns.regplot(
    data=panel,
    x="pct_lansia",
    y="p0_miskin",
    scatter=False,
    color="black",
    line_kws={"linestyle": "--"}
)

plt.xlabel("Persentase Lansia (%)")
plt.ylabel("Persentase Penduduk Miskin (%)")
plt.title("Hubungan Persentase Lansia dan Kemiskinan\n2020–2024")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "07_scatter_lansia_vs_kemiskinan.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 23. SCATTERPLOT AGEING VS RLS
# ============================================================

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=panel,
    x="pct_lansia",
    y="rls",
    hue="Pulau",
    alpha=0.55
)

sns.regplot(
    data=panel,
    x="pct_lansia",
    y="rls",
    scatter=False,
    color="black",
    line_kws={"linestyle": "--"}
)

plt.xlabel("Persentase Lansia (%)")
plt.ylabel("Rata-rata Lama Sekolah (tahun)")
plt.title("Hubungan Persentase Lansia dan Rata-rata Lama Sekolah\n2020–2024")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "08_scatter_lansia_vs_rls.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 24. SCATTERPLOT AGEING VS PENGELUARAN
# ============================================================

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=panel,
    x="pct_lansia",
    y="pengeluaran",
    hue="Pulau",
    alpha=0.55
)

sns.regplot(
    data=panel,
    x="pct_lansia",
    y="pengeluaran",
    scatter=False,
    color="black",
    line_kws={"linestyle": "--"}
)

plt.xlabel("Persentase Lansia (%)")
plt.ylabel("Pengeluaran per Kapita")
plt.title("Hubungan Persentase Lansia dan Pengeluaran\n2020–2024")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "09_scatter_lansia_vs_pengeluaran.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 25. SCATTERPLOT AGEING VS AHH
# ============================================================

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=panel,
    x="pct_lansia",
    y="ahh_rata2",
    hue="Pulau",
    alpha=0.55
)

sns.regplot(
    data=panel,
    x="pct_lansia",
    y="ahh_rata2",
    scatter=False,
    color="black",
    line_kws={"linestyle": "--"}
)

plt.xlabel("Persentase Lansia (%)")
plt.ylabel("Angka Harapan Hidup")
plt.title("Hubungan Persentase Lansia dan Angka Harapan Hidup\n2020–2024")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "10_scatter_lansia_vs_ahh.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 26. SCATTERPLOT AGEING VS TPT
# ============================================================

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=panel,
    x="pct_lansia",
    y="tpt_total",
    hue="Pulau",
    alpha=0.55
)

sns.regplot(
    data=panel,
    x="pct_lansia",
    y="tpt_total",
    scatter=False,
    color="black",
    line_kws={"linestyle": "--"}
)

plt.xlabel("Persentase Lansia (%)")
plt.ylabel("Tingkat Pengangguran Terbuka (%)")
plt.title("Hubungan Persentase Lansia dan TPT\n2020–2024")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "11_scatter_lansia_vs_tpt.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 27. KORELASI SEMUA VARIABEL NUMERIK
# ============================================================

corr_matrix = panel[numeric_vars].corr(
    method="spearman"
)

corr_matrix.to_csv(
    TABLE_DIR / "11_korelasi_spearman_semua_variabel.csv"
)

plt.figure(figsize=(12, 10))

sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    square=True
)

plt.title("Matriks Korelasi Spearman\nVariabel Numerik")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "12_heatmap_korelasi_spearman.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 28. LOAD GEOJSON
# ============================================================

print("\n" + "=" * 70)
print("LOAD GEOJSON")
print("=" * 70)

gdf = gpd.read_file(GEOJSON_PATH)

print("Shape GeoJSON:", gdf.shape)
print("CRS:", gdf.crs)

print("\nGeometry:")
print(gdf.geometry.geom_type.value_counts())


# ============================================================
# 29. VALIDASI NAMA KAB/KOTA
# ============================================================

excel_names = set(panel["Kab_kota"].unique())
geo_names = set(gdf["Kab_kota"].unique())

print("\nExcel tetapi tidak ada di GeoJSON:")
print(sorted(excel_names - geo_names))

print("\nGeoJSON tetapi tidak ada di Excel:")
print(sorted(geo_names - excel_names))


# ============================================================
# 30. SIAPKAN GEOMETRY SAJA
# ============================================================
# GeoJSON dapat memiliki atribut statistik lama seperti
# pct_lansia, p0_miskin, rls, dll.
#
# Untuk menghindari konflik nama kolom, kita hanya mengambil
# geometry dan identitas wilayah dari GeoJSON.

geo_cols = [
    "Kab_kota",
    "geometry"
]

gdf_geometry = gdf[geo_cols].copy()


# ============================================================
# 31. JOIN DATA 2024 KE GEOMETRY
# ============================================================

data_2024 = panel[
    panel["Tahun"] == 2024
].copy()

map_2024 = gdf_geometry.merge(
    data_2024,
    on="Kab_kota",
    how="left",
    validate="one_to_one"
)

print("\nMap 2024:")
print("Shape:", map_2024.shape)

print(
    "Missing pct_lansia setelah join:",
    map_2024["pct_lansia"].isna().sum()
)

print(
    "Missing jumlah_lansia setelah join:",
    map_2024["jumlah_lansia"].isna().sum()
)


# ============================================================
# 32. PETA PCT LANSIA 2024
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 10)
)

map_2024.plot(
    column="pct_lansia",
    cmap="YlOrRd",
    linewidth=0.2,
    edgecolor="black",
    legend=True,
    ax=ax,
    missing_kwds={
        "color": "lightgrey",
        "label": "Tidak tersedia"
    }
)

ax.set_title(
    "Persentase Penduduk Lansia Menurut Kabupaten/Kota\n"
    "Jawa dan Sumatera, 2024",
    fontsize=14
)

ax.axis("off")

plt.tight_layout()

plt.savefig(
    MAP_DIR / "01_peta_pct_lansia_2024.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ============================================================
# 33. JOIN PERUBAHAN 2020–2024 KE GEOJSON
# ============================================================

map_change = gdf_geometry.merge(
    change_summary[
        [
            "Kab_kota",
            "Pulau",
            "Provinsi",
            "pct_lansia_2020",
            "pct_lansia_2024",
            "delta_pct_lansia",
            "persen_perubahan_pct_lansia"
        ]
    ],
    on="Kab_kota",
    how="left",
    validate="one_to_one"
)

print("\nMap perubahan 2020–2024:")
print("Shape:", map_change.shape)

print(
    "Missing delta_pct_lansia:",
    map_change["delta_pct_lansia"].isna().sum()
)

map_change.columns = [
    str(col)
    for col in map_change.columns
]

print("\nKolom map_change:")
print(map_change.columns.tolist())

print("\nTipe data kolom:")
print(map_change.dtypes)


# ============================================================
# 34. PETA PERUBAHAN PCT LANSIA
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 10)
)

map_change.plot(
    column="delta_pct_lansia",
    cmap="RdBu_r",
    linewidth=0.2,
    edgecolor="black",
    legend=True,
    ax=ax,
    vmin=map_change["delta_pct_lansia"].min(),
    vmax=map_change["delta_pct_lansia"].max(),
    missing_kwds={
        "color": "lightgrey",
        "label": "Tidak tersedia"
    }
)

ax.set_title(
    "Perubahan Persentase Penduduk Lansia\n"
    "2020–2024",
    fontsize=14
)

ax.axis("off")

plt.tight_layout()

plt.savefig(
    MAP_DIR / "02_peta_perubahan_pct_lansia_2020_2024.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 35. SIMPAN DATA PETA UNTUK WEB
# ============================================================

# GeoJSON 2024
map_2024.columns = [
    str(col)
    for col in map_2024.columns
]

map_2024.to_file(
    MAP_DIR / "map_2024_master.geojson",
    driver="GeoJSON"
)

# GeoJSON perubahan 2020–2024
map_change.to_file(
    MAP_DIR / "map_change_2020_2024.geojson",
    driver="GeoJSON"
)

print("\n✓ GeoJSON 2024 berhasil disimpan")
print("✓ GeoJSON perubahan 2020–2024 berhasil disimpan")


# ============================================================
# 36. SELESAI
# ============================================================

print("\n" + "=" * 70)
print("NB02 SELESAI")
print("=" * 70)

print(f"Output tabel : {TABLE_DIR}")
print(f"Output grafik: {FIG_DIR}")
print(f"Output peta  : {MAP_DIR}")