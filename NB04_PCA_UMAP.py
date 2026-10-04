# ============================================================
# NB04 - PCA + UMAP + MULTIVARIATE ANALYSIS
# ============================================================
#
# Judul:
# "Sepuh dan Sejahtera: Mengurai Pola Multivariat
#  Penuaan Penduduk di Jawa dan Sumatera"
#
# Tujuan:
# 1. Merangkum indikator ageing dan kesejahteraan menggunakan PCA
# 2. Mengidentifikasi kontribusi setiap indikator terhadap PC
# 3. Memetakan kemiripan kab/kota menggunakan UMAP
# 4. Mengevaluasi korelasi antarvariabel
# 5. Melakukan diagnostik multikolinearitas sebagai pemeriksaan tambahan
# 6. Menghasilkan dataset multivariat untuk web story
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
print("NB04 - PCA + UMAP + MULTIVARIATE ANALYSIS")
print("=" * 70)


# ============================================================
# 2. LOAD DATA
# ============================================================

PANEL_FILE = OUTPUT_DIR / "panel_clean.csv"

TYPOLOGY_FILE = (
    OUTPUT_DIR / "panel_nb03_1_typology_validation.csv"
)


if not PANEL_FILE.exists():
    raise FileNotFoundError(
        f"""
File tidak ditemukan:
{PANEL_FILE}

Pastikan NB01_Preprocessing.py sudah dijalankan.
"""
    )


if not TYPOLOGY_FILE.exists():
    raise FileNotFoundError(
        f"""
File tidak ditemukan:
{TYPOLOGY_FILE}

Pastikan NB03_1_VALIDASI_TIPOLOGI.py sudah dijalankan.
"""
    )


df_panel = pd.read_csv(PANEL_FILE)

df_typology = pd.read_csv(TYPOLOGY_FILE)


print("\n[1] DATA")
print("-" * 70)

print(f"Panel utama : {PANEL_FILE}")
print(f"Shape       : {df_panel.shape}")

print(f"\nData tipologi : {TYPOLOGY_FILE}")
print(f"Shape         : {df_typology.shape}")


# ============================================================
# 3. GABUNGKAN DATA TIPOLOGI
# ============================================================

typology_cols = [
    "Kab_kota",
    "Tahun",
    "Tipologi_Lansia_Tahunan",
    "Tipologi_Pooled"
]


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


df = df_panel.merge(
    df_typology_small,
    on=["Kab_kota", "Tahun"],
    how="left",
    validate="one_to_one"
)


print("\nData setelah merge:")
print(f"Shape     : {df.shape}")
print(f"Tahun     : {sorted(df['Tahun'].unique())}")
print(f"Kab/kota  : {df['Kab_kota'].nunique()}")


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
# 4. VALIDASI PANEL
# ============================================================

print("\n[2] VALIDASI PANEL")
print("-" * 70)


duplicate_panel = df.duplicated(
    subset=["Kab_kota", "Tahun"]
).sum()


print(
    f"Duplikasi Kab/kota-Tahun : {duplicate_panel}"
)

print(
    f"Jumlah kab/kota          : "
    f"{df['Kab_kota'].nunique()}"
)


if duplicate_panel > 0:
    raise ValueError(
        "Terdapat duplikasi Kab/kota-Tahun."
    )


# ============================================================
# 5. TAHUN ANALISIS DAN BASELINE
# ============================================================

YEAR_ANALYSIS = 2024
YEAR_BASELINE = 2020


df_2024 = df[
    df["Tahun"] == YEAR_ANALYSIS
].copy()


df_2020 = df[
    df["Tahun"] == YEAR_BASELINE
].copy()


print("\n[3] DATA ANALISIS")
print("-" * 70)

print(f"Tahun analisis : {YEAR_ANALYSIS}")
print(f"Tahun baseline : {YEAR_BASELINE}")

print(
    f"Jumlah baris 2024 : "
    f"{len(df_2024)}"
)

print(
    f"Jumlah baris 2020 : "
    f"{len(df_2020)}"
)

print(
    f"Jumlah kab/kota   : "
    f"{df_2024['Kab_kota'].nunique()}"
)


duplicate_2024 = df_2024.duplicated(
    subset=["Kab_kota"]
).sum()


duplicate_2020 = df_2020.duplicated(
    subset=["Kab_kota"]
).sum()


print(
    f"\nDuplikasi kab/kota 2024 : "
    f"{duplicate_2024}"
)

print(
    f"Duplikasi kab/kota 2020 : "
    f"{duplicate_2020}"
)


if duplicate_2024 > 0:
    raise ValueError(
        "Terdapat duplikasi kab/kota pada tahun 2024."
    )


if duplicate_2020 > 0:
    raise ValueError(
        "Terdapat duplikasi kab/kota pada tahun 2020."
    )


# ============================================================
# 6. FEATURE ENGINEERING
# ============================================================

print("\n[4] FEATURE ENGINEERING")
print("-" * 70)


# ------------------------------------------------------------
# 6.1 Pastikan variabel baseline tersedia
# ------------------------------------------------------------

baseline_vars = [
    "Kab_kota",
    "pct_lansia",
    "p0_miskin"
]


missing_baseline_vars = [
    col
    for col in baseline_vars
    if col not in df_2020.columns
]


if missing_baseline_vars:
    raise ValueError(
        "Variabel baseline tidak ditemukan: "
        f"{missing_baseline_vars}"
    )


# ------------------------------------------------------------
# 6.2 Ambil perubahan 2020 -> 2024
# ------------------------------------------------------------

df_change = df_2020[
    [
        "Kab_kota",
        "pct_lansia",
        "p0_miskin"
    ]
].copy()


df_change = df_change.rename(
    columns={
        "pct_lansia": "pct_lansia_2020",
        "p0_miskin": "p0_miskin_2020"
    }
)


# ------------------------------------------------------------
# 6.3 Merge dengan data 2024
# ------------------------------------------------------------

df_2024 = df_2024.merge(
    df_change,
    on="Kab_kota",
    how="left",
    validate="one_to_one"
)


# ------------------------------------------------------------
# 6.4 Hitung perubahan
# ------------------------------------------------------------

df_2024["delta_pct_lansia"] = (
    df_2024["pct_lansia"]
    - df_2024["pct_lansia_2020"]
)


df_2024["delta_p0_miskin"] = (
    df_2024["p0_miskin"]
    - df_2024["p0_miskin_2020"]
)


# ------------------------------------------------------------
# 6.5 Gender life expectancy gap
# ------------------------------------------------------------

if (
    "ahh_laki" in df_2024.columns
    and
    "ahh_perempuan" in df_2024.columns
):

    df_2024["gap_ahh_gender"] = (
        df_2024["ahh_perempuan"]
        - df_2024["ahh_laki"]
    )

else:

    print(
        "PERINGATAN: ahh_laki / ahh_perempuan "
        "tidak tersedia."
    )


print("Variabel hasil feature engineering:")

print("- delta_pct_lansia")
print("- delta_p0_miskin")
print("- gap_ahh_gender")


# ============================================================
# 7. AUDIT VARIABEL KANDIDAT
# ============================================================

print("\n[5] AUDIT VARIABEL NUMERIK")
print("-" * 70)


CANDIDATE_VARS = [
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


candidate_audit = []


for var in CANDIDATE_VARS:

    if var in df_2024.columns:

        candidate_audit.append(
            {
                "Variabel": var,
                "Missing_2024": df_2024[var].isna().sum(),
                "Unique_2024": df_2024[var].nunique()
            }
        )


candidate_audit = pd.DataFrame(
    candidate_audit
)


print(
    candidate_audit.to_string(
        index=False
    )
)


candidate_audit.to_csv(
    TABEL_DIR /
    "nb04_audit_variabel_kandidat.csv",
    index=False
)


# ============================================================
# 8. VARIABEL FINAL PCA
# ============================================================

print("\n[6] VARIABEL FINAL PCA")
print("-" * 70)


# ------------------------------------------------------------
# FINAL MODEL A
# ------------------------------------------------------------
#
# 8 variabel:
#
# 1. jumlah_penduduk
# 2. jumlah_lansia
# 3. pct_lansia
# 4. pct_anak
# 5. rls
# 6. pengeluaran
# 7. ahh_rata2
# 8. delta_pct_lansia
#
# Kombinasi ini dipilih untuk merepresentasikan:
# - skala demografi
# - jumlah lansia
# - intensitas ageing
# - struktur umur
# - pendidikan
# - standar hidup
# - kesehatan
# - dinamika ageing 2020-2024
#
# ------------------------------------------------------------


PCA_VARS = [
    "jumlah_penduduk",
    "jumlah_lansia",
    "pct_lansia",
    "pct_anak",
    "rls",
    "pengeluaran",
    "ahh_rata2",
    "delta_pct_lansia"
]


print(
    f"Jumlah variabel PCA : "
    f"{len(PCA_VARS)}"
)


for i, var in enumerate(
    PCA_VARS,
    start=1
):

    print(
        f"{i:02d}. {var}"
    )


# ------------------------------------------------------------
# Validasi variabel
# ------------------------------------------------------------

missing_vars = [
    var
    for var in PCA_VARS
    if var not in df_2024.columns
]


if missing_vars:

    raise ValueError(
        f"Variabel PCA tidak ditemukan: "
        f"{missing_vars}"
    )


# ============================================================
# 9. CEK MISSING VALUE
# ============================================================

print("\n[7] MISSING VALUE")
print("-" * 70)


missing = df_2024[
    PCA_VARS
].isna().sum()


print(missing)


if missing.sum() > 0:

    raise ValueError(
        """
Terdapat missing value pada variabel PCA.

Data sebelumnya tidak memiliki missing value.
Periksa kembali proses preprocessing.
Tidak dilakukan imputasi pada NB04.
"""
    )


# ============================================================
# 10. DATA MATRIX
# ============================================================

X = df_2024[
    PCA_VARS
].copy()


# ============================================================
# 11. KORELASI VARIABEL FINAL
# ============================================================

print("\n[8] KORELASI VARIABEL FINAL")
print("-" * 70)


corr = X.corr()


print(
    corr.round(3).to_string()
)


corr.to_csv(
    TABEL_DIR /
    "nb04_korelasi_variabel_final.csv"
)


# ------------------------------------------------------------
# Heatmap korelasi
# ------------------------------------------------------------

plt.figure(
    figsize=(11, 9)
)


sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    square=True
)


plt.title(
    "Korelasi 8 Variabel Final PCA"
)


plt.tight_layout()


plt.savefig(
    GRAFIK_DIR /
    "nb04_korelasi_variabel_final.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ============================================================
# 12. DIAGNOSTIK MULTIKOLINEARITAS - VIF
# ============================================================

print("\n[9] DIAGNOSTIK MULTIKOLINEARITAS")
print("-" * 70)


def calculate_vif(dataframe):

    """
    Menghitung VIF menggunakan regresi linear
    antarvariabel.

    Catatan:
    VIF digunakan sebagai diagnostik tambahan.
    PCA sendiri tidak mensyaratkan VIF rendah.
    """

    data = dataframe.values.astype(float)

    vif_values = []

    for i in range(data.shape[1]):

        y = data[:, i]

        X_other = np.delete(
            data,
            i,
            axis=1
        )

        X_design = np.column_stack(
            [
                np.ones(
                    X_other.shape[0]
                ),
                X_other
            ]
        )

        coefficients = np.linalg.lstsq(
            X_design,
            y,
            rcond=None
        )[0]

        y_pred = X_design @ coefficients

        ss_res = np.sum(
            (y - y_pred) ** 2
        )

        ss_tot = np.sum(
            (y - y.mean()) ** 2
        )

        if ss_tot == 0:

            r_squared = 1.0

        else:

            r_squared = (
                1
                -
                ss_res / ss_tot
            )

        # Hindari error numerik
        r_squared = min(
            max(r_squared, 0),
            0.999999
        )

        vif = 1 / (
            1 - r_squared
        )

        vif_values.append(vif)

    return pd.DataFrame(
        {
            "Variabel": dataframe.columns,
            "VIF": vif_values
        }
    )


vif_result = calculate_vif(X)


vif_result["Keterangan"] = pd.cut(
    vif_result["VIF"],
    bins=[
        -np.inf,
        5,
        10,
        np.inf
    ],
    labels=[
        "Rendah",
        "Perlu perhatian",
        "Tinggi"
    ]
)


print(
    vif_result.round(3).to_string(
        index=False
    )
)


vif_result.to_csv(
    TABEL_DIR /
    "nb04_vif.csv",
    index=False
)


# ============================================================
# 13. STANDARDISASI
# ============================================================

print("\n[10] STANDARDISASI")
print("-" * 70)


print(
    "Standardisasi dilakukan dengan "
    "StandardScaler (mean = 0, standar deviasi = 1)."
)


scaler = StandardScaler()


X_scaled = scaler.fit_transform(
    X
)


# ============================================================
# 14. PCA
# ============================================================

print("\n[11] PCA")
print("-" * 70)


pca = PCA()


X_pca = pca.fit_transform(
    X_scaled
)


explained_variance = (
    pca.explained_variance_ratio_
)


cumulative_variance = np.cumsum(
    explained_variance
)


pca_summary = pd.DataFrame(
    {
        "Komponen": [
            f"PC{i+1}"
            for i in range(
                len(PCA_VARS)
            )
        ],

        "Eigenvalue":
            pca.explained_variance_,

        "Explained_Variance":
            explained_variance * 100,

        "Cumulative_Variance":
            cumulative_variance * 100
    }
)


print(
    pca_summary.round(6).to_string(
        index=False
    )
)


pca_summary.to_csv(
    TABEL_DIR /
    "nb04_pca_explained_variance.csv",
    index=False
)


# ============================================================
# 15. RINGKASAN VARIANCE UTAMA
# ============================================================

pc1_pc2 = (
    cumulative_variance[1] * 100
)


pc1_pc3 = (
    cumulative_variance[2] * 100
)


pc1_pc4 = (
    cumulative_variance[3] * 100
)


print("\nRingkasan explained variance:")
print(
    f"PC1              : "
    f"{explained_variance[0] * 100:.2f}%"
)

print(
    f"PC1 + PC2        : "
    f"{pc1_pc2:.2f}%"
)

print(
    f"PC1 + PC2 + PC3  : "
    f"{pc1_pc3:.2f}%"
)

print(
    f"PC1 - PC4        : "
    f"{pc1_pc4:.2f}%"
)


# ============================================================
# 16. PCA LOADINGS
# ============================================================

print("\n[12] PCA LOADINGS")
print("-" * 70)


loadings = pd.DataFrame(
    pca.components_.T,
    index=PCA_VARS,
    columns=[
        f"PC{i+1}"
        for i in range(
            len(PCA_VARS)
        )
    ]
)


print(
    loadings.round(4).to_string()
)


loadings.to_csv(
    TABEL_DIR /
    "nb04_pca_loadings.csv"
)


# ------------------------------------------------------------
# Absolute loadings
# ------------------------------------------------------------

absolute_loadings = (
    loadings.abs()
)


absolute_loadings.to_csv(
    TABEL_DIR /
    "nb04_pca_absolute_loadings.csv"
)


# ============================================================
# 17. PCA SCORE DATASET
# ============================================================

pca_scores = pd.DataFrame(
    X_pca,
    columns=[
        f"PC{i+1}"
        for i in range(
            len(PCA_VARS)
        )
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


# ------------------------------------------------------------
# Tipologi
# ------------------------------------------------------------

if (
    "Tipologi_Lansia_Tahunan"
    in df_2024.columns
):

    pca_scores[
        "Tipologi_Lansia"
    ] = (
        df_2024[
            "Tipologi_Lansia_Tahunan"
        ].values
    )


elif (
    "Tipologi_Pooled"
    in df_2024.columns
):

    pca_scores[
        "Tipologi_Lansia"
    ] = (
        df_2024[
            "Tipologi_Pooled"
        ].values
    )


# ------------------------------------------------------------
# Tambahkan variabel PCA
# ------------------------------------------------------------

for var in PCA_VARS:

    pca_scores[var] = (
        df_2024[var].values
    )


pca_scores.to_csv(
    OUTPUT_DIR /
    "nb04_pca_scores_2024.csv",
    index=False
)


# ============================================================
# 18. PCA BIPLOT PC1-PC2
# ============================================================

print("\n[13] MEMBUAT PCA BIPLOT")
print("-" * 70)


plt.figure(
    figsize=(13, 10)
)


# ------------------------------------------------------------
# Scatter kab/kota
# ------------------------------------------------------------

if "Tipologi_Lansia" in pca_scores.columns:

    sns.scatterplot(
        data=pca_scores,
        x="PC1",
        y="PC2",
        hue="Tipologi_Lansia",
        alpha=0.75,
        s=65
    )

    plt.legend(
        title="Tipologi Lansia",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

else:

    plt.scatter(
        pca_scores["PC1"],
        pca_scores["PC2"],
        alpha=0.70,
        s=55
    )


# ------------------------------------------------------------
# Garis nol
# ------------------------------------------------------------

plt.axhline(
    0,
    linewidth=0.8
)


plt.axvline(
    0,
    linewidth=0.8
)


# ------------------------------------------------------------
# Loading vectors
# ------------------------------------------------------------

arrow_scale = 3.0


for var in PCA_VARS:

    x = loadings.loc[
        var,
        "PC1"
    ]

    y = loadings.loc[
        var,
        "PC2"
    ]


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
        x * arrow_scale * 1.10,
        y * arrow_scale * 1.10,
        var,
        fontsize=9
    )


plt.xlabel(
    f"PC1 "
    f"({explained_variance[0] * 100:.2f}% varians)"
)


plt.ylabel(
    f"PC2 "
    f"({explained_variance[1] * 100:.2f}% varians)"
)


plt.title(
    "PCA Indikator Ageing dan Kesejahteraan\n"
    "Kabupaten/Kota Jawa dan Sumatera, 2024"
)


plt.tight_layout()


plt.savefig(
    GRAFIK_DIR /
    "nb04_pca_biplot_2024.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ============================================================
# 19. PCA 3D PC1-PC2-PC3
# ============================================================

print("\n[14] MEMBUAT PCA 3D")
print("-" * 70)


from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure(
    figsize=(12, 9)
)


ax = fig.add_subplot(
    111,
    projection="3d"
)


if "Tipologi_Lansia" in pca_scores.columns:

    categories = (
        pca_scores[
            "Tipologi_Lansia"
        ].astype(str)
    )

    unique_categories = (
        categories.unique()
    )

    for category in unique_categories:

        mask = (
            categories == category
        )

        ax.scatter(
            pca_scores.loc[
                mask, "PC1"
            ],
            pca_scores.loc[
                mask, "PC2"
            ],
            pca_scores.loc[
                mask, "PC3"
            ],
            label=category,
            alpha=0.75,
            s=45
        )

    ax.legend(
        title="Tipologi",
        bbox_to_anchor=(1.15, 1)
    )

else:

    ax.scatter(
        pca_scores["PC1"],
        pca_scores["PC2"],
        pca_scores["PC3"],
        alpha=0.70,
        s=45
    )


ax.set_xlabel(
    f"PC1 ({explained_variance[0] * 100:.2f}%)"
)


ax.set_ylabel(
    f"PC2 ({explained_variance[1] * 100:.2f}%)"
)


ax.set_zlabel(
    f"PC3 ({explained_variance[2] * 100:.2f}%)"
)


ax.set_title(
    "PCA 3D Kabupaten/Kota\n"
    f"PC1-PC3 = {pc1_pc3:.2f}% Varians"
)


plt.tight_layout()


plt.savefig(
    GRAFIK_DIR /
    "nb04_pca_3d_2024.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ============================================================
# 20. SCREE PLOT
# ============================================================

print("\n[15] MEMBUAT SCREE PLOT")
print("-" * 70)


plt.figure(
    figsize=(11, 6)
)


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
    [
        f"PC{i}"
        for i in components
    ]
)


# ------------------------------------------------------------
# Garis cumulative 80%
# ------------------------------------------------------------

plt.axhline(
    80,
    linestyle="--",
    linewidth=1
)


plt.text(
    3.15,
    81,
    "80%",
    fontsize=10
)


plt.xlabel(
    "Komponen Utama"
)


plt.ylabel(
    "Explained Variance (%)"
)


plt.title(
    "Scree Plot PCA\n"
    f"PC1-PC3 = {pc1_pc3:.2f}% Varians"
)


plt.grid(
    alpha=0.3
)


plt.tight_layout()


plt.savefig(
    GRAFIK_DIR /
    "nb04_pca_scree_plot.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ============================================================
# 21. HEATMAP PCA LOADINGS
# ============================================================

print("\n[16] MEMBUAT HEATMAP PCA LOADINGS")
print("-" * 70)


plt.figure(
    figsize=(11, 7)
)


sns.heatmap(
    loadings.iloc[:, :4],
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)


plt.title(
    "Loading PCA Variabel Final\n"
    "PC1-PC4"
)


plt.xlabel(
    "Komponen Utama"
)


plt.ylabel(
    "Variabel"
)


plt.tight_layout()


plt.savefig(
    GRAFIK_DIR /
    "nb04_pca_loading_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ============================================================
# 22. UMAP
# ============================================================

print("\n[17] UMAP")
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


umap_result = pd.DataFrame(
    {
        "Kab_kota":
            df_2024["Kab_kota"].values,

        "Provinsi":
            df_2024["Provinsi"].values,

        "Tahun":
            YEAR_ANALYSIS,

        "UMAP1":
            X_umap[:, 0],

        "UMAP2":
            X_umap[:, 1]
    }
)


# ------------------------------------------------------------
# Tipologi
# ------------------------------------------------------------

if (
    "Tipologi_Lansia_Tahunan"
    in df_2024.columns
):

    umap_result[
        "Tipologi_Lansia"
    ] = (
        df_2024[
            "Tipologi_Lansia_Tahunan"
        ].values
    )


elif (
    "Tipologi_Pooled"
    in df_2024.columns
):

    umap_result[
        "Tipologi_Lansia"
    ] = (
        df_2024[
            "Tipologi_Pooled"
        ].values
    )


# ------------------------------------------------------------
# PCA scores
# ------------------------------------------------------------

umap_result["PC1"] = (
    pca_scores["PC1"].values
)

umap_result["PC2"] = (
    pca_scores["PC2"].values
)

umap_result["PC3"] = (
    pca_scores["PC3"].values
)


# ------------------------------------------------------------
# Variabel PCA
# ------------------------------------------------------------

for var in PCA_VARS:

    umap_result[var] = (
        df_2024[var].values
    )


umap_result.to_csv(
    OUTPUT_DIR /
    "nb04_umap_2024.csv",
    index=False
)


# ============================================================
# 23. VISUALISASI UMAP
# ============================================================

print("\n[18] MEMBUAT VISUALISASI UMAP")
print("-" * 70)


plt.figure(
    figsize=(12, 9)
)


if "Tipologi_Lansia" in umap_result.columns:

    sns.scatterplot(
        data=umap_result,
        x="UMAP1",
        y="UMAP2",
        hue="Tipologi_Lansia",
        alpha=0.75,
        s=65
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
        alpha=0.70,
        s=60
    )


plt.xlabel(
    "UMAP 1"
)


plt.ylabel(
    "UMAP 2"
)


plt.title(
    "UMAP Kabupaten/Kota Berdasarkan\n"
    "Indikator Ageing dan Kesejahteraan, 2024"
)


plt.tight_layout()


plt.savefig(
    GRAFIK_DIR /
    "nb04_umap_2024.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ============================================================
# 24. PARALLEL COORDINATES
# ============================================================

print("\n[19] MEMBUAT PARALLEL COORDINATES")
print("-" * 70)


# ------------------------------------------------------------
# Standardized dataframe
# ------------------------------------------------------------

parallel_df = pd.DataFrame(
    X_scaled,
    columns=PCA_VARS
)


parallel_df[
    "Tipologi_Lansia"
] = (
    df_2024[
        "Tipologi_Lansia_Tahunan"
    ].values
    if
    "Tipologi_Lansia_Tahunan"
    in df_2024.columns
    else "Tidak tersedia"
)


# ------------------------------------------------------------
# Batasi jumlah garis untuk visualisasi
# ------------------------------------------------------------

# Semua 273 observasi tetap tersedia dalam CSV.
# Untuk grafik, gunakan seluruh observasi
# dengan transparansi rendah.

plt.figure(
    figsize=(15, 8)
)


for _, row in parallel_df.iterrows():

    plt.plot(
        range(len(PCA_VARS)),
        row[PCA_VARS].values,
        alpha=0.08,
        linewidth=0.8
    )


plt.xticks(
    range(len(PCA_VARS)),
    PCA_VARS,
    rotation=35,
    ha="right"
)


plt.axhline(
    0,
    linestyle="--",
    linewidth=1
)


plt.xlabel(
    "Variabel"
)


plt.ylabel(
    "Nilai terstandarisasi"
)


plt.title(
    "Parallel Coordinates\n"
    "Profil Multivariat Kabupaten/Kota, 2024"
)


plt.tight_layout()


plt.savefig(
    GRAFIK_DIR /
    "nb04_parallel_coordinates_2024.png",
    dpi=300,
    bbox_inches="tight"
)


plt.close()


# ============================================================
# 25. DATASET MULTIVARIAT GABUNGAN
# ============================================================

print("\n[20] MEMBUAT DATASET MULTIVARIAT")
print("-" * 70)


umap_merge = umap_result[
    [
        "Kab_kota",
        "UMAP1",
        "UMAP2"
    ]
]


multivariate = pca_scores.merge(
    umap_merge,
    on="Kab_kota",
    how="left",
    validate="one_to_one"
)


multivariate.to_csv(
    OUTPUT_DIR /
    "nb04_multivariate_2024.csv",
    index=False
)


# ============================================================
# 26. FEATURE ENGINEERING DOCUMENTATION
# ============================================================

feature_documentation = pd.DataFrame(
    {
        "Variabel": [
            "delta_pct_lansia"
        ],

        "Formula": [
            "pct_lansia_2024 - pct_lansia_2020"
        ],

        "Makna": [
            "Perubahan proporsi lansia "
            "selama periode 2020-2024"
        ],

        "Tahun": [
            "2020-2024"
        ]
    }
)


feature_documentation.to_csv(
    TABEL_DIR /
    "nb04_feature_engineering.csv",
    index=False
)


# ============================================================
# 27. RINGKASAN HASIL
# ============================================================

print("\n[21] RINGKASAN HASIL")
print("-" * 70)


summary = pd.DataFrame(
    {
        "Indikator": [
            "Jumlah kab/kota",
            "Jumlah variabel PCA",
            "Jumlah observasi per variabel",
            "PC1 explained variance (%)",
            "PC2 explained variance (%)",
            "PC3 explained variance (%)",
            "PC1+PC2 explained variance (%)",
            "PC1+PC2+PC3 explained variance (%)",
            "PC1+PC2+PC3+PC4 explained variance (%)"
        ],

        "Nilai": [
            len(df_2024),
            len(PCA_VARS),
            len(df_2024),

            explained_variance[0] * 100,
            explained_variance[1] * 100,
            explained_variance[2] * 100,

            pc1_pc2,
            pc1_pc3,
            pc1_pc4
        ]
    }
)


print(
    summary.round(4).to_string(
        index=False
    )
)


summary.to_csv(
    TABEL_DIR /
    "nb04_ringkasan.csv",
    index=False
)


# ============================================================
# 28. VALIDASI HASIL UTAMA
# ============================================================

print("\n[22] VALIDASI HASIL UTAMA")
print("-" * 70)


print(
    f"Jumlah variabel : {len(PCA_VARS)}"
)


print(
    f"Jumlah observasi: {len(df_2024)}"
)


print(
    f"Missing value   : {missing.sum()}"
)


print(
    f"PC1-PC3         : {pc1_pc3:.2f}%"
)


if len(PCA_VARS) >= 8:

    print(
        "STATUS variabel: MEMENUHI "
        "minimum 8 variabel."
    )

else:

    print(
        "STATUS variabel: BELUM memenuhi "
        "minimum 8 variabel."
    )


if len(df_2024) >= 34:

    print(
        "STATUS observasi: MEMENUHI "
        "minimum 34 observasi."
    )

else:

    print(
        "STATUS observasi: BELUM memenuhi "
        "minimum 34 observasi."
    )


if pc1_pc3 >= 80:

    print(
        "STATUS PCA: PC1-PC3 menjelaskan "
        ">= 80% variasi."
    )

else:

    print(
        "STATUS PCA: PC1-PC3 belum mencapai "
        "80% variasi."
    )


# ============================================================
# 29. OUTPUT
# ============================================================

print("\n[23] OUTPUT DATA FINAL")
print("-" * 70)


output_files = [

    OUTPUT_DIR /
    "nb04_pca_scores_2024.csv",

    OUTPUT_DIR /
    "nb04_umap_2024.csv",

    OUTPUT_DIR /
    "nb04_multivariate_2024.csv",

    TABEL_DIR /
    "nb04_pca_explained_variance.csv",

    TABEL_DIR /
    "nb04_pca_loadings.csv",

    TABEL_DIR /
    "nb04_pca_absolute_loadings.csv",

    TABEL_DIR /
    "nb04_korelasi_variabel_final.csv",

    TABEL_DIR /
    "nb04_vif.csv",

    TABEL_DIR /
    "nb04_feature_engineering.csv",

    TABEL_DIR /
    "nb04_ringkasan.csv",

    GRAFIK_DIR /
    "nb04_pca_biplot_2024.png",

    GRAFIK_DIR /
    "nb04_pca_3d_2024.png",

    GRAFIK_DIR /
    "nb04_pca_scree_plot.png",

    GRAFIK_DIR /
    "nb04_pca_loading_heatmap.png",

    GRAFIK_DIR /
    "nb04_umap_2024.png",

    GRAFIK_DIR /
    "nb04_parallel_coordinates_2024.png",

    GRAFIK_DIR /
    "nb04_korelasi_variabel_final.png"
]


for i, file in enumerate(
    output_files,
    start=1
):

    print(
        f"{i:02d}. {file}"
    )


# ============================================================
# 30. SELESAI
# ============================================================

print("\n" + "=" * 70)
print("NB04 SELESAI")
print("=" * 70)

print(
    "\nPCA menggunakan "
    f"{len(PCA_VARS)} variabel dan "
    f"{len(df_2024)} kab/kota."
)

print(
    f"PC1-PC3 menjelaskan "
    f"{pc1_pc3:.2f}% variasi."
)

print(
    "\nSemua proses NB04 berhasil."
)