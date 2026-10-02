# ============================================================
# NB03_1 - VALIDASI TIPOLOGI AGEING × KESEJAHTERAAN
# ============================================================
# Tujuan:
# 1. Menghitung threshold median pct_lansia dan p0_miskin per tahun
# 2. Membentuk tipologi tahunan berdasarkan median tahun tersebut
# 3. Membandingkan tipologi pooled (NB03) dengan tipologi tahunan
# 4. Menganalisis perubahan tipologi 2020 -> 2024
# 5. Menghasilkan tabel yang dapat digunakan untuk web story
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. SETUP DIREKTORI
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

EDA_DIR = OUTPUT_DIR / "eda"
TABEL_DIR = EDA_DIR / "tabel"
GRAFIK_DIR = EDA_DIR / "grafik"

TABEL_DIR.mkdir(parents=True, exist_ok=True)
GRAFIK_DIR.mkdir(parents=True, exist_ok=True)


print("=" * 70)
print("NB03_1 - VALIDASI TIPOLOGI AGEING × KESEJAHTERAAN")
print("=" * 70)


# ============================================================
# 2. LOAD DATA HASIL NB03
# ============================================================

INPUT_FILE = OUTPUT_DIR / "panel_nb03_typology.csv"

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"File tidak ditemukan:\n{INPUT_FILE}\n\n"
        "Pastikan NB03_EDA_AGEING_WELFARE.py sudah dijalankan."
    )

df = pd.read_csv(INPUT_FILE)

print("\n[1] DATA")
print("-" * 70)
print(f"File       : {INPUT_FILE}")
print(f"Shape      : {df.shape}")
print(f"Tahun      : {sorted(df['Tahun'].unique())}")
print(f"Kab/kota   : {df['Kab_kota'].nunique()}")


# ============================================================
# 3. VALIDASI STRUKTUR DATA
# ============================================================

required_cols = [
    "Kab_kota",
    "Provinsi",
    "Tahun",
    "pct_lansia",
    "p0_miskin"
]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    raise ValueError(
        f"Kolom berikut tidak ditemukan: {missing_cols}"
    )

duplicate = df.duplicated(
    subset=["Kab_kota", "Tahun"]
).sum()

print("\n[2] VALIDASI")
print("-" * 70)
print(f"Duplikasi Kab_kota-Tahun : {duplicate}")
print(f"Missing pct_lansia       : {df['pct_lansia'].isna().sum()}")
print(f"Missing p0_miskin        : {df['p0_miskin'].isna().sum()}")


if duplicate > 0:
    raise ValueError(
        "Terdapat duplikasi Kab_kota-Tahun. "
        "Periksa panel_clean.csv sebelum melanjutkan."
    )


# ============================================================
# 4. MEDIAN POOLED
#    Menggunakan threshold yang sama untuk seluruh periode
#    Ini adalah pendekatan yang digunakan NB03.
# ============================================================

median_lansia_pooled = df["pct_lansia"].median()
median_miskin_pooled = df["p0_miskin"].median()

print("\n[3] MEDIAN POOLED 2020-2024")
print("-" * 70)
print(f"Median pct_lansia : {median_lansia_pooled:.3f}")
print(f"Median p0_miskin  : {median_miskin_pooled:.3f}")


# ============================================================
# 5. MEDIAN PER TAHUN
# ============================================================

median_tahunan = (
    df.groupby("Tahun")
      .agg(
          median_pct_lansia=("pct_lansia", "median"),
          median_p0_miskin=("p0_miskin", "median")
      )
      .reset_index()
)

print("\n[4] MEDIAN PER TAHUN")
print("-" * 70)
print(median_tahunan.to_string(index=False))


median_tahunan.to_csv(
    TABEL_DIR / "nb03_1_median_per_tahun.csv",
    index=False
)


# ============================================================
# 6. BENTUK TIPOLOGI TAHUNAN
# ============================================================

# Tambahkan threshold median ke setiap baris
df = df.merge(
    median_tahunan,
    on="Tahun",
    how="left",
    validate="many_to_one"
)


# ------------------------------------------------------------
# Status lansia
# ------------------------------------------------------------

df["status_lansia_tahunan"] = np.where(
    df["pct_lansia"] >= df["median_pct_lansia"],
    "Lansia tinggi",
    "Lansia rendah"
)


# ------------------------------------------------------------
# Status kemiskinan
# ------------------------------------------------------------

df["status_miskin_tahunan"] = np.where(
    df["p0_miskin"] >= df["median_p0_miskin"],
    "Kemiskinan tinggi",
    "Kemiskinan rendah"
)


# ------------------------------------------------------------
# Tipologi gabungan
# ------------------------------------------------------------

df["Tipologi_Lansia_Tahunan"] = (
    df["status_lansia_tahunan"]
    + " - "
    + df["status_miskin_tahunan"]
)


# ============================================================
# 7. TABEL DISTRIBUSI TIPOLOGI PER TAHUN
# ============================================================

tipologi_order = [
    "Lansia rendah - Kemiskinan rendah",
    "Lansia rendah - Kemiskinan tinggi",
    "Lansia tinggi - Kemiskinan rendah",
    "Lansia tinggi - Kemiskinan tinggi"
]

tipologi_tahunan = (
    df.groupby(
        ["Tahun", "Tipologi_Lansia_Tahunan"]
    )
    .size()
    .reset_index(name="Jumlah")
)

tipologi_tahunan["Persentase"] = (
    tipologi_tahunan.groupby("Tahun")["Jumlah"]
    .transform(lambda x: x / x.sum() * 100)
)

tipologi_tahunan = (
    tipologi_tahunan
    .sort_values(["Tahun", "Tipologi_Lansia_Tahunan"])
)

print("\n[5] DISTRIBUSI TIPOLOGI TAHUNAN")
print("-" * 70)
print(tipologi_tahunan.to_string(index=False))


tipologi_tahunan.to_csv(
    TABEL_DIR / "nb03_1_tipologi_per_tahun.csv",
    index=False
)


# ============================================================
# 8. BANDINGKAN TIPOLOGI POOLED vs TAHUNAN
# ============================================================

# Tipologi pooled dari NB03
df["Tipologi_Pooled"] = np.where(
    df["pct_lansia"] >= median_lansia_pooled,
    np.where(
        df["p0_miskin"] >= median_miskin_pooled,
        "Lansia tinggi - Kemiskinan tinggi",
        "Lansia tinggi - Kemiskinan rendah"
    ),
    np.where(
        df["p0_miskin"] >= median_miskin_pooled,
        "Lansia rendah - Kemiskinan tinggi",
        "Lansia rendah - Kemiskinan rendah"
    )
)


# Apakah hasilnya berbeda?
df["Tipologi_Berbeda"] = (
    df["Tipologi_Pooled"]
    != df["Tipologi_Lansia_Tahunan"]
)


jumlah_berbeda = df["Tipologi_Berbeda"].sum()
jumlah_sama = (~df["Tipologi_Berbeda"]).sum()

persen_berbeda = jumlah_berbeda / len(df) * 100
persen_sama = jumlah_sama / len(df) * 100


print("\n[6] PERBANDINGAN POOLED vs TAHUNAN")
print("-" * 70)
print(f"Jumlah observasi        : {len(df)}")
print(f"Tipologi sama           : {jumlah_sama}")
print(f"Tipologi berbeda        : {jumlah_berbeda}")
print(f"Persentase sama         : {persen_sama:.2f}%")
print(f"Persentase berbeda      : {persen_berbeda:.2f}%")


perbandingan = (
    df.groupby(
        ["Tipologi_Pooled", "Tipologi_Lansia_Tahunan"]
    )
    .size()
    .reset_index(name="Jumlah")
)

perbandingan.to_csv(
    TABEL_DIR / "nb03_1_perbandingan_tipologi_pooled_vs_tahunan.csv",
    index=False
)


# ============================================================
# 9. DATASET HASIL VALIDASI
# ============================================================

validation_cols = [
    "Kab_kota",
    "Provinsi",
    "Tahun",
    "pct_lansia",
    "p0_miskin",
    "median_pct_lansia",
    "median_p0_miskin",
    "status_lansia_tahunan",
    "status_miskin_tahunan",
    "Tipologi_Lansia_Tahunan",
    "Tipologi_Pooled",
    "Tipologi_Berbeda"
]

df_validation = df[validation_cols].copy()

df_validation.to_csv(
    OUTPUT_DIR / "panel_nb03_1_typology_validation.csv",
    index=False
)


# ============================================================
# 10. TRANSISI TIPOLOGI 2020 -> 2024
# ============================================================

print("\n[7] TRANSISI TIPOLOGI 2020 -> 2024")
print("-" * 70)

df_2020 = df[
    df["Tahun"] == 2020
][
    [
        "Kab_kota",
        "Provinsi",
        "Tipologi_Lansia_Tahunan"
    ]
].copy()

df_2024 = df[
    df["Tahun"] == 2024
][
    [
        "Kab_kota",
        "Tipologi_Lansia_Tahunan"
    ]
].copy()

df_2020 = df_2020.rename(
    columns={
        "Tipologi_Lansia_Tahunan": "Tipologi_2020"
    }
)

df_2024 = df_2024.rename(
    columns={
        "Tipologi_Lansia_Tahunan": "Tipologi_2024"
    }
)


transisi = df_2020.merge(
    df_2024,
    on="Kab_kota",
    how="inner",
    validate="one_to_one"
)


transisi["Berubah"] = (
    transisi["Tipologi_2020"]
    != transisi["Tipologi_2024"]
)


jumlah_kabkota = len(transisi)
jumlah_berubah = transisi["Berubah"].sum()
jumlah_tetap = (~transisi["Berubah"]).sum()

persen_berubah = jumlah_berubah / jumlah_kabkota * 100
persen_tetap = jumlah_tetap / jumlah_kabkota * 100


print(f"Jumlah kab/kota      : {jumlah_kabkota}")
print(f"Berubah              : {jumlah_berubah}")
print(f"Tetap                : {jumlah_tetap}")
print(f"Persentase berubah   : {persen_berubah:.2f}%")
print(f"Persentase tetap     : {persen_tetap:.2f}%")


transisi.to_csv(
    TABEL_DIR / "nb03_1_transisi_tipologi_2020_2024.csv",
    index=False
)


# ============================================================
# 11. MATRIKS TRANSISI
# ============================================================

matriks_transisi = pd.crosstab(
    transisi["Tipologi_2020"],
    transisi["Tipologi_2024"]
)


# Urutkan baris dan kolom
matriks_transisi = matriks_transisi.reindex(
    index=tipologi_order,
    columns=tipologi_order,
    fill_value=0
)


print("\n[8] MATRIKS TRANSISI 2020 -> 2024")
print("-" * 70)
print(matriks_transisi)


matriks_transisi.to_csv(
    TABEL_DIR / "nb03_1_matriks_transisi_2020_2024.csv"
)


# ============================================================
# 12. IDENTIFIKASI KAB/KOTA YANG BERUBAH
# ============================================================

kabkota_berubah = transisi[
    transisi["Berubah"]
].copy()

kabkota_berubah.to_csv(
    TABEL_DIR / "nb03_1_kabkota_berubah_2020_2024.csv",
    index=False
)


print("\n[9] KAB/KOTA YANG BERUBAH")
print("-" * 70)

print(
    kabkota_berubah[
        [
            "Kab_kota",
            "Provinsi",
            "Tipologi_2020",
            "Tipologi_2024"
        ]
    ].to_string(index=False)
)


# ============================================================
# 13. VISUALISASI DISTRIBUSI TIPOLOGI TAHUNAN
# ============================================================

plt.figure(figsize=(12, 7))

plot_data = (
    tipologi_tahunan
    .pivot(
        index="Tahun",
        columns="Tipologi_Lansia_Tahunan",
        values="Jumlah"
    )
    .fillna(0)
)

plot_data = plot_data.reindex(
    columns=tipologi_order,
    fill_value=0
)

plot_data.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 7)
)

plt.title(
    "Distribusi Tipologi Lansia × Kemiskinan per Tahun"
)

plt.xlabel("Tahun")
plt.ylabel("Jumlah Kabupaten/Kota")
plt.xticks(rotation=0)
plt.legend(
    title="Tipologi",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()

plt.savefig(
    GRAFIK_DIR / "nb03_1_distribusi_tipologi_tahunan.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 14. HEATMAP MATRIKS TRANSISI
# ============================================================

plt.figure(figsize=(10, 8))

sns.heatmap(
    matriks_transisi,
    annot=True,
    fmt="d",
    cmap="Blues",
    cbar=False
)

plt.title(
    "Matriks Transisi Tipologi 2020 → 2024"
)

plt.xlabel("Tipologi 2024")
plt.ylabel("Tipologi 2020")

plt.xticks(rotation=30, ha="right")
plt.yticks(rotation=0)

plt.tight_layout()

plt.savefig(
    GRAFIK_DIR / "nb03_1_heatmap_transisi_2020_2024.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 15. RINGKASAN VALIDASI
# ============================================================

ringkasan = pd.DataFrame({
    "Indikator": [
        "Median pct_lansia pooled",
        "Median p0_miskin pooled",
        "Jumlah observasi",
        "Jumlah kab/kota",
        "Tipologi sama pooled vs tahunan",
        "Tipologi berbeda pooled vs tahunan",
        "Persentase sama pooled vs tahunan",
        "Persentase berbeda pooled vs tahunan",
        "Kab/kota berubah 2020-2024",
        "Kab/kota tetap 2020-2024",
        "Persentase berubah 2020-2024",
        "Persentase tetap 2020-2024"
    ],
    "Nilai": [
        median_lansia_pooled,
        median_miskin_pooled,
        len(df),
        df["Kab_kota"].nunique(),
        jumlah_sama,
        jumlah_berbeda,
        persen_sama,
        persen_berbeda,
        jumlah_berubah,
        jumlah_tetap,
        persen_berubah,
        persen_tetap
    ]
})

ringkasan.to_csv(
    TABEL_DIR / "nb03_1_ringkasan_validasi.csv",
    index=False
)


# ============================================================
# 16. SELESAI
# ============================================================

print("\n" + "=" * 70)
print("NB03_1 SELESAI")
print("=" * 70)

print("\nOutput utama:")
print(f"1. {OUTPUT_DIR / 'panel_nb03_1_typology_validation.csv'}")
print(f"2. {TABEL_DIR / 'nb03_1_median_per_tahun.csv'}")
print(f"3. {TABEL_DIR / 'nb03_1_tipologi_per_tahun.csv'}")
print(f"4. {TABEL_DIR / 'nb03_1_perbandingan_tipologi_pooled_vs_tahunan.csv'}")
print(f"5. {TABEL_DIR / 'nb03_1_transisi_tipologi_2020_2024.csv'}")
print(f"6. {TABEL_DIR / 'nb03_1_matriks_transisi_2020_2024.csv'}")
print(f"7. {TABEL_DIR / 'nb03_1_kabkota_berubah_2020_2024.csv'}")
print(f"8. {GRAFIK_DIR / 'nb03_1_distribusi_tipologi_tahunan.png'}")
print(f"9. {GRAFIK_DIR / 'nb03_1_heatmap_transisi_2020_2024.png'}")

print("\nSemua proses berhasil.")