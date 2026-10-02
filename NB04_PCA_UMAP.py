# ============================================================
# NB04 - PCA + UMAP
# ============================================================
# Judul:
# "Sepuh dan Sejahtera: Mengurai Pola Multivariat
#  Penuaan Penduduk di Jawa dan Sumatera"
#
# Tujuan:
# 1. Merangkum indikator ageing dan kesejahteraan menggunakan PCA
# 2. Mengidentifikasi kontribusi setiap indikator terhadap PC
# 3. Memetakan kemiripan kab/kota menggunakan UMAP
# 4. Menghasilkan dataset multivariat untuk web story
#
# Unit analisis:
# Kabupaten/kota tahun 2024
#
# ============================================================


from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


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
print("NB04 - PCA + UMAP")
print("=" * 70)

# ============================================================
# 2. LOAD DATA
# ============================================================

# Data utama berisi seluruh indikator yang dibutuhkan PCA
PANEL_FILE = OUTPUT_DIR / "panel_clean.csv"

# Data hasil validasi tipologi dari NB03_1
TYPOLOGY_FILE = OUTPUT_DIR / "panel_nb03_1_typology_validation.csv"


if not PANEL_FILE.exists():
    raise FileNotFoundError(
        f"File tidak ditemukan:\n{PANEL_FILE}\n\n"
        "Pastikan NB01_Preprocessing.py sudah dijalankan."
    )


if not TYPOLOGY_FILE.exists():
    raise FileNotFoundError(
        f"File tidak ditemukan:\n{TYPOLOGY_FILE}\n\n"
        "Pastikan NB03_1_VALIDASI_TIPOLOGI.py sudah dijalankan."
    )


# ------------------------------------------------------------
# Data utama
# ------------------------------------------------------------

df_panel = pd.read_csv(PANEL_FILE)


# ------------------------------------------------------------
# Data tipologi
# ------------------------------------------------------------

df_typology = pd.read_csv(TYPOLOGY_FILE)


print("\n[1] DATA")
print("-" * 70)

print(f"Panel utama : {PANEL_FILE}")
print(f"Shape       : {df_panel.shape}")

print(f"\nData tipologi : {TYPOLOGY_FILE}")
print(f"Shape         : {df_typology.shape}")


# ============================================================
# 3. GABUNGKAN DATA
# ============================================================

# Ambil informasi tipologi saja dari hasil NB03_1
typology_cols = [
    "Kab_kota",
    "Tahun",
    "Tipologi_Lansia_Tahunan",
    "Tipologi_Pooled"
]

# Pastikan kolom tersedia
missing_typology = [
    col
    for col in typology_cols
    if col not in df_typology.columns
]

if missing_typology:
    raise ValueError(
        f"Kolom tipologi tidak ditemukan: {missing_typology}"
    )


df_typology_small = df_typology[
    typology_cols
].copy()


# Merge berdasarkan Kab_kota dan Tahun
df = df_panel.merge(
    df_typology_small,
    on=["Kab_kota", "Tahun"],
    how="left",
    validate="one_to_one"
)


print("\nData setelah merge:")
print(f"Shape       : {df.shape}")
print(f"Tahun       : {sorted(df['Tahun'].unique())}")
print(f"Kab/kota    : {df['Kab_kota'].nunique()}")


# Cek apakah tipologi berhasil masuk
print("\nMissing tipologi setelah merge:")
print(
    df[
        [
            "Tipologi_Lansia_Tahunan",
            "Tipologi_Pooled"
        ]
    ].isna().sum()
)

# ============================================================
# 3. PILIH TAHUN ANALISIS
# ============================================================

YEAR_ANALYSIS = 2024

df_2024 = df[
    df["Tahun"] == YEAR_ANALYSIS
].copy()

print("\n[2] DATA ANALISIS")
print("-" * 70)
print(f"Tahun analisis : {YEAR_ANALYSIS}")
print(f"Jumlah baris   : {len(df_2024)}")
print(f"Jumlah kab/kota: {df_2024['Kab_kota'].nunique()}")


# ============================================================
# 4. VALIDASI SATU BARIS PER KAB/KOTA
# ============================================================

duplicate = df_2024.duplicated(
    subset=["Kab_kota"]
).sum()

print(f"Duplikasi kab/kota: {duplicate}")

if duplicate > 0:
    raise ValueError(
        "Terdapat duplikasi kab/kota pada tahun 2024."
    )


# ============================================================
# 5. VARIABEL PCA
# ============================================================

PCA_VARS = [
    "pct_lansia",
    "p0_miskin",
    "rls",
    "pengeluaran",
    "ahh_rata2",
    "tpt_total"
]


print("\n[3] VARIABEL PCA")
print("-" * 70)

for var in PCA_VARS:
    print(f"- {var}")


# Validasi kolom
missing_vars = [
    var for var in PCA_VARS
    if var not in df_2024.columns
]

if missing_vars:
    raise ValueError(
        f"Variabel PCA tidak ditemukan: {missing_vars}"
    )


# ============================================================
# 6. CEK MISSING VALUE
# ============================================================

missing = df_2024[PCA_VARS].isna().sum()

print("\n[4] MISSING VALUE")
print("-" * 70)
print(missing)

if missing.sum() > 0:
    raise ValueError(
        "Terdapat missing value pada variabel PCA."
    )


# ============================================================
# 7. DATA MATRIX
# ============================================================

X = df_2024[PCA_VARS].copy()


# ============================================================
# 8. STANDARDISASI
# ============================================================

print("\n[5] STANDARDISASI")
print("-" * 70)
print(
    "Standardisasi dilakukan dengan StandardScaler "
    "(mean = 0, standar deviasi = 1)."
)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ============================================================
# 9. PCA
# ============================================================

print("\n[6] PCA")
print("-" * 70)

pca = PCA()

X_pca = pca.fit_transform(X_scaled)


# Explained variance
explained_variance = pca.explained_variance_ratio_

cumulative_variance = np.cumsum(
    explained_variance
)


pca_summary = pd.DataFrame({
    "Komponen": [
        f"PC{i+1}"
        for i in range(len(PCA_VARS))
    ],
    "Eigenvalue": pca.explained_variance_,
    "Explained_Variance": explained_variance * 100,
    "Cumulative_Variance": cumulative_variance * 100
})


print(pca_summary.to_string(index=False))


pca_summary.to_csv(
    TABEL_DIR / "nb04_pca_explained_variance.csv",
    index=False
)


# ============================================================
# 10. LOADINGS PCA
# ============================================================

loadings = pd.DataFrame(
    pca.components_.T,
    index=PCA_VARS,
    columns=[
        f"PC{i+1}"
        for i in range(len(PCA_VARS))
    ]
)


print("\n[7] PCA LOADINGS")
print("-" * 70)
print(loadings.round(4).to_string())


loadings.to_csv(
    TABEL_DIR / "nb04_pca_loadings.csv"
)


# ============================================================
# 11. DATASET SKOR PCA
# ============================================================

pca_scores = pd.DataFrame(
    X_pca,
    columns=[
        f"PC{i+1}"
        for i in range(len(PCA_VARS))
    ]
)

pca_scores.insert(
    0,
    "Kab_kota",
    df_2024["Kab_kota"].values
)

pca_scores.insert(
    1,
    "Provinsi",
    df_2024["Provinsi"].values
)

pca_scores.insert(
    2,
    "Tahun",
    YEAR_ANALYSIS
)


# Tambahkan tipologi
if "Tipologi_Lansia_Tahunan" in df_2024.columns:

    pca_scores["Tipologi_Lansia"] = (
        df_2024["Tipologi_Lansia_Tahunan"].values
    )

elif "Tipologi_Pooled" in df_2024.columns:

    pca_scores["Tipologi_Lansia"] = (
        df_2024["Tipologi_Pooled"].values
    )


# Tambahkan indikator asli
for var in PCA_VARS:
    pca_scores[var] = df_2024[var].values


pca_scores.to_csv(
    OUTPUT_DIR / "nb04_pca_scores_2024.csv",
    index=False
)


# ============================================================
# 12. PCA BIPLOT
# ============================================================

print("\n[8] MEMBUAT PCA BIPLOT")
print("-" * 70)

plt.figure(figsize=(12, 9))


# Plot kab/kota
plt.scatter(
    pca_scores["PC1"],
    pca_scores["PC2"],
    alpha=0.65
)


# Tambahkan garis nol
plt.axhline(
    0,
    linewidth=0.8
)

plt.axvline(
    0,
    linewidth=0.8
)


# Panah loading
arrow_scale = 3

for var in PCA_VARS:

    x = loadings.loc[var, "PC1"]
    y = loadings.loc[var, "PC2"]

    plt.arrow(
        0,
        0,
        x * arrow_scale,
        y * arrow_scale,
        head_width=0.08,
        head_length=0.08,
        length_includes_head=True
    )

    plt.text(
        x * arrow_scale * 1.1,
        y * arrow_scale * 1.1,
        var,
        fontsize=10
    )


pc1_var = explained_variance[0] * 100
pc2_var = explained_variance[1] * 100


plt.xlabel(
    f"PC1 ({pc1_var:.2f}% varians)"
)

plt.ylabel(
    f"PC2 ({pc2_var:.2f}% varians)"
)

plt.title(
    "PCA Indikator Ageing dan Kesejahteraan Kabupaten/Kota, 2024"
)

plt.tight_layout()


plt.savefig(
    GRAFIK_DIR / "nb04_pca_biplot_2024.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 13. SCREE PLOT
# ============================================================

print("\n[9] MEMBUAT SCREE PLOT")
print("-" * 70)

plt.figure(figsize=(10, 6))

components = range(
    1,
    len(explained_variance) + 1
)

plt.plot(
    components,
    explained_variance * 100,
    marker="o"
)

plt.xticks(
    components,
    [f"PC{i}" for i in components]
)

plt.xlabel("Komponen Utama")
plt.ylabel("Explained Variance (%)")

plt.title(
    "Explained Variance PCA"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    GRAFIK_DIR / "nb04_pca_scree_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 14. UMAP
# ============================================================

print("\n[10] UMAP")
print("-" * 70)

try:

    import umap

except ImportError:

    raise ImportError(
        """
Library umap-learn belum terinstall.

Install dengan:

pip install umap-learn

Setelah itu jalankan kembali:

python -u NB04_PCA_UMAP.py
"""
    )


# ------------------------------------------------------------
# UMAP menggunakan data yang sudah distandardisasi
# ------------------------------------------------------------

reducer = umap.UMAP(
    n_neighbors=15,
    min_dist=0.1,
    n_components=2,
    metric="euclidean",
    random_state=2024
)


X_umap = reducer.fit_transform(
    X_scaled
)


umap_result = pd.DataFrame({
    "Kab_kota": df_2024["Kab_kota"].values,
    "Provinsi": df_2024["Provinsi"].values,
    "Tahun": YEAR_ANALYSIS,
    "UMAP1": X_umap[:, 0],
    "UMAP2": X_umap[:, 1]
})


# Tambahkan tipologi
if "Tipologi_Lansia_Tahunan" in df_2024.columns:

    umap_result["Tipologi_Lansia"] = (
        df_2024["Tipologi_Lansia_Tahunan"].values
    )

elif "Tipologi_Pooled" in df_2024.columns:

    umap_result["Tipologi_Lansia"] = (
        df_2024["Tipologi_Pooled"].values
    )


# Tambahkan PCA
umap_result["PC1"] = pca_scores["PC1"].values
umap_result["PC2"] = pca_scores["PC2"].values


# Tambahkan indikator
for var in PCA_VARS:
    umap_result[var] = df_2024[var].values


umap_result.to_csv(
    OUTPUT_DIR / "nb04_umap_2024.csv",
    index=False
)


# ============================================================
# 15. VISUALISASI UMAP
# ============================================================

print("\n[11] MEMBUAT VISUALISASI UMAP")
print("-" * 70)

plt.figure(figsize=(12, 9))


# Jika tipologi tersedia, gunakan sebagai warna
if "Tipologi_Lansia" in umap_result.columns:

    sns.scatterplot(
        data=umap_result,
        x="UMAP1",
        y="UMAP2",
        hue="Tipologi_Lansia",
        alpha=0.75,
        s=60
    )

    plt.legend(
        title="Tipologi",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

else:

    plt.scatter(
        umap_result["UMAP1"],
        umap_result["UMAP2"],
        alpha=0.7
    )


plt.xlabel("UMAP 1")
plt.ylabel("UMAP 2")

plt.title(
    "UMAP Kabupaten/Kota Berdasarkan Indikator "
    "Ageing dan Kesejahteraan, 2024"
)

plt.tight_layout()


plt.savefig(
    GRAFIK_DIR / "nb04_umap_2024.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 16. PCA + UMAP GABUNGAN
# ============================================================

multivariate = pca_scores.merge(
    umap_result[
        [
            "Kab_kota",
            "UMAP1",
            "UMAP2"
        ]
    ],
    on="Kab_kota",
    how="left",
    validate="one_to_one"
)


multivariate.to_csv(
    OUTPUT_DIR / "nb04_multivariate_2024.csv",
    index=False
)


# ============================================================
# 17. RINGKASAN HASIL
# ============================================================

summary = pd.DataFrame({
    "Indikator": [
        "Jumlah kab/kota",
        "Jumlah variabel PCA",
        "PC1 explained variance (%)",
        "PC2 explained variance (%)",
        "PC1+PC2 explained variance (%)"
    ],
    "Nilai": [
        len(df_2024),
        len(PCA_VARS),
        explained_variance[0] * 100,
        explained_variance[1] * 100,
        (explained_variance[0] + explained_variance[1]) * 100
    ]
})


summary.to_csv(
    TABEL_DIR / "nb04_ringkasan.csv",
    index=False
)


# ============================================================
# 18. SELESAI
# ============================================================

print("\n" + "=" * 70)
print("NB04 SELESAI")
print("=" * 70)

print("\nOutput utama:")

print(
    f"1. {OUTPUT_DIR / 'nb04_pca_scores_2024.csv'}"
)

print(
    f"2. {OUTPUT_DIR / 'nb04_umap_2024.csv'}"
)

print(
    f"3. {OUTPUT_DIR / 'nb04_multivariate_2024.csv'}"
)

print(
    f"4. {TABEL_DIR / 'nb04_pca_explained_variance.csv'}"
)

print(
    f"5. {TABEL_DIR / 'nb04_pca_loadings.csv'}"
)

print(
    f"6. {GRAFIK_DIR / 'nb04_pca_biplot_2024.png'}"
)

print(
    f"7. {GRAFIK_DIR / 'nb04_pca_scree_plot.png'}"
)

print(
    f"8. {GRAFIK_DIR / 'nb04_umap_2024.png'}"
)

print("\nSemua proses NB04 berhasil.")