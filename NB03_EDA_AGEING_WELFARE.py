# ============================================================
# NB03 - ANALISIS AGEING × KESEJAHTERAAN
# Sepuh dan Sejahtera:
# Mengurai Pola Spasial Penuaan Penduduk di Jawa dan Sumatera
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from scipy.stats import pearsonr, spearmanr


# ============================================================
# 1. SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
EDA_DIR = OUTPUT_DIR / "eda"
TABEL_DIR = EDA_DIR / "tabel"
GRAFIK_DIR = EDA_DIR / "grafik"
PETA_DIR = EDA_DIR / "peta"

TABEL_DIR.mkdir(parents=True, exist_ok=True)
GRAFIK_DIR.mkdir(parents=True, exist_ok=True)
PETA_DIR.mkdir(parents=True, exist_ok=True)


print("=" * 70)
print("NB03 - ANALISIS AGEING × KESEJAHTERAAN")
print("=" * 70)


# ============================================================
# 2. LOAD DATA
# ============================================================

panel_path = OUTPUT_DIR / "panel_clean.csv"

panel = pd.read_csv(panel_path)

print("\nData berhasil dibaca:")
print(panel_path)

print("Ukuran data:", panel.shape)


# ============================================================
# 3. VALIDASI
# ============================================================

print("\n" + "=" * 70)
print("VALIDASI DATA")
print("=" * 70)

print("\nTahun:")
print(sorted(panel["Tahun"].unique()))

print("\nJumlah kab/kota:")
print(panel["Kab_kota"].nunique())

print("\nMissing value:")
print(
    panel[
        [
            "pct_lansia",
            "p0_miskin",
            "rls",
            "pengeluaran",
            "ahh_rata2",
            "tpt_total"
        ]
    ].isna().sum()
)

print("\nDuplikasi Kab_kota-Tahun:")
print(
    panel.duplicated(
        subset=["Kab_kota", "Tahun"]
    ).sum()
)


# ============================================================
# 4. INDIKATOR AGEING × KESEJAHTERAAN
# ============================================================

print("\n" + "=" * 70)
print("RINGKASAN AGEING × KESEJAHTERAAN")
print("=" * 70)

indikator = [
    "pct_lansia",
    "p0_miskin",
    "rls",
    "pengeluaran",
    "ahh_rata2",
    "tpt_total"
]

summary_indicator = (
    panel[indikator]
    .describe()
    .T
    .round(3)
)

print(summary_indicator)

summary_indicator.to_csv(
    TABEL_DIR / "ringkasan_indikator_nb03.csv"
)


# ============================================================
# 5. PERKEMBANGAN AGEING DAN KEMISKINAN PER TAHUN
# ============================================================

print("\n" + "=" * 70)
print("PERKEMBANGAN AGEING DAN KEMISKINAN")
print("=" * 70)

annual_summary = (
    panel
    .groupby("Tahun")
    .agg(
        rata_pct_lansia=("pct_lansia", "mean"),
        median_pct_lansia=("pct_lansia", "median"),
        rata_p0_miskin=("p0_miskin", "mean"),
        median_p0_miskin=("p0_miskin", "median"),
        rata_ahh=("ahh_rata2", "mean"),
        rata_rls=("rls", "mean"),
        rata_pengeluaran=("pengeluaran", "mean")
    )
    .reset_index()
)

print(
    annual_summary.round(3).to_string(index=False)
)

annual_summary.to_csv(
    TABEL_DIR / "perkembangan_ageing_kesejahteraan.csv",
    index=False
)


# ============================================================
# 6. KORELASI AGEING × KEMISKINAN PER TAHUN
# ============================================================

print("\n" + "=" * 70)
print("KORELASI AGEING × KEMISKINAN PER TAHUN")
print("=" * 70)

corr_yearly = []

for tahun, df_year in panel.groupby("Tahun"):

    x = df_year["pct_lansia"]
    y = df_year["p0_miskin"]

    pearson_r, pearson_p = pearsonr(x, y)
    spearman_rho, spearman_p = spearmanr(x, y)

    corr_yearly.append({
        "Tahun": tahun,
        "pearson_r": pearson_r,
        "pearson_p": pearson_p,
        "spearman_rho": spearman_rho,
        "spearman_p": spearman_p
    })

corr_yearly = pd.DataFrame(corr_yearly)

print(
    corr_yearly.round(4).to_string(index=False)
)

corr_yearly.to_csv(
    TABEL_DIR / "korelasi_ageing_kemiskinan_per_tahun.csv",
    index=False
)


# ============================================================
# 7. KORELASI PER PULAU
# ============================================================

print("\n" + "=" * 70)
print("KORELASI AGEING × KEMISKINAN PER PULAU")
print("=" * 70)

corr_island = []

for pulau, df_island in panel.groupby("Pulau"):

    pearson_r, pearson_p = pearsonr(
        df_island["pct_lansia"],
        df_island["p0_miskin"]
    )

    spearman_rho, spearman_p = spearmanr(
        df_island["pct_lansia"],
        df_island["p0_miskin"]
    )

    corr_island.append({
        "Pulau": pulau,
        "pearson_r": pearson_r,
        "pearson_p": pearson_p,
        "spearman_rho": spearman_rho,
        "spearman_p": spearman_p
    })

corr_island = pd.DataFrame(corr_island)

print(
    corr_island.round(4).to_string(index=False)
)

corr_island.to_csv(
    TABEL_DIR / "korelasi_ageing_kemiskinan_per_pulau.csv",
    index=False
)


# ============================================================
# 8. SCATTERPLOT AGEING × KEMISKINAN
# ============================================================

print("\n" + "=" * 70)
print("MEMBUAT SCATTERPLOT AGEING × KEMISKINAN")
print("=" * 70)


# ------------------------------------------------------------
# Scatterplot pooled 2020-2024
# ------------------------------------------------------------

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=panel,
    x="pct_lansia",
    y="p0_miskin",
    hue="Pulau",
    alpha=0.55,
    s=45
)

sns.regplot(
    data=panel,
    x="pct_lansia",
    y="p0_miskin",
    scatter=False,
    color="black",
    line_kws={"linewidth": 2}
)

plt.title(
    "Proporsi Lansia dan Tingkat Kemiskinan\n"
    "Kabupaten/Kota di Jawa dan Sumatera, 2020–2024"
)

plt.xlabel("Proporsi Lansia (%)")
plt.ylabel("Persentase Penduduk Miskin (%)")

plt.tight_layout()

plt.savefig(
    GRAFIK_DIR / "scatter_ageing_kemiskinan_pooled.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 9. SCATTERPLOT PER TAHUN
# ============================================================

for tahun in sorted(panel["Tahun"].unique()):

    df_year = panel[
        panel["Tahun"] == tahun
    ]

    plt.figure(figsize=(9, 6))

    sns.scatterplot(
        data=df_year,
        x="pct_lansia",
        y="p0_miskin",
        hue="Pulau",
        alpha=0.65,
        s=50
    )

    sns.regplot(
        data=df_year,
        x="pct_lansia",
        y="p0_miskin",
        scatter=False,
        color="black",
        line_kws={"linewidth": 2}
    )

    plt.title(
        f"Proporsi Lansia dan Tingkat Kemiskinan\n"
        f"Kabupaten/Kota, {tahun}"
    )

    plt.xlabel("Proporsi Lansia (%)")
    plt.ylabel("Persentase Penduduk Miskin (%)")

    plt.tight_layout()

    plt.savefig(
        GRAFIK_DIR / f"scatter_ageing_kemiskinan_{tahun}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# 10. MENENTUKAN BATAS TIPOLOGI
# ============================================================

print("\n" + "=" * 70)
print("BATAS TIPOLOGI")
print("=" * 70)

median_pct_lansia = panel["pct_lansia"].median()
median_p0_miskin = panel["p0_miskin"].median()

print(
    f"Median pct_lansia 2020–2024 : "
    f"{median_pct_lansia:.3f}%"
)

print(
    f"Median p0_miskin 2020–2024  : "
    f"{median_p0_miskin:.3f}%"
)


# ============================================================
# 11. MEMBENTUK TIPOLOGI
# ============================================================

panel_typology = panel.copy()

panel_typology["kategori_lansia"] = np.where(
    panel_typology["pct_lansia"] >= median_pct_lansia,
    "Lansia tinggi",
    "Lansia rendah"
)

panel_typology["kategori_kemiskinan"] = np.where(
    panel_typology["p0_miskin"] >= median_p0_miskin,
    "Kemiskinan tinggi",
    "Kemiskinan rendah"
)


def tentukan_tipologi(row):

    if (
        row["kategori_lansia"] == "Lansia tinggi"
        and row["kategori_kemiskinan"] == "Kemiskinan tinggi"
    ):
        return "Lansia tinggi - Kemiskinan tinggi"

    elif (
        row["kategori_lansia"] == "Lansia tinggi"
        and row["kategori_kemiskinan"] == "Kemiskinan rendah"
    ):
        return "Lansia tinggi - Kemiskinan rendah"

    elif (
        row["kategori_lansia"] == "Lansia rendah"
        and row["kategori_kemiskinan"] == "Kemiskinan tinggi"
    ):
        return "Lansia rendah - Kemiskinan tinggi"

    else:
        return "Lansia rendah - Kemiskinan rendah"


panel_typology["Tipologi"] = panel_typology.apply(
    tentukan_tipologi,
    axis=1
)


print("\nDistribusi tipologi:")
print(
    panel_typology["Tipologi"]
    .value_counts()
)


# ============================================================
# 12. DISTRIBUSI TIPOLOGI PER TAHUN
# ============================================================

print("\n" + "=" * 70)
print("DISTRIBUSI TIPOLOGI PER TAHUN")
print("=" * 70)

typology_year = (
    panel_typology
    .groupby(["Tahun", "Tipologi"])
    .size()
    .reset_index(name="jumlah_kab_kota")
)

typology_year["persentase"] = (
    typology_year["jumlah_kab_kota"]
    / 273
    * 100
)

print(
    typology_year.round(2).to_string(index=False)
)

typology_year.to_csv(
    TABEL_DIR / "tipologi_per_tahun.csv",
    index=False
)


# ============================================================
# 13. TABEL SILANG TIPOLOGI
# ============================================================

print("\n" + "=" * 70)
print("CROSS-TAB TIPOLOGI")
print("=" * 70)

typology_crosstab = pd.crosstab(
    panel_typology["kategori_lansia"],
    panel_typology["kategori_kemiskinan"]
)

print(typology_crosstab)

typology_crosstab.to_csv(
    TABEL_DIR / "crosstab_tipologi.csv"
)


# ============================================================
# 14. KOMPOSISI TIPOLOGI PER PULAU
# ============================================================

print("\n" + "=" * 70)
print("TIPOLOGI PER PULAU")
print("=" * 70)

typology_island = (
    panel_typology
    .groupby(["Pulau", "Tipologi"])
    .size()
    .reset_index(name="jumlah")
)

print(
    typology_island.to_string(index=False)
)

typology_island.to_csv(
    TABEL_DIR / "tipologi_per_pulau.csv",
    index=False
)


# ============================================================
# 15. PERUBAHAN TIPOLOGI 2020 → 2024
# ============================================================

print("\n" + "=" * 70)
print("PERUBAHAN TIPOLOGI 2020 → 2024")
print("=" * 70)

typology_2020 = panel_typology[
    panel_typology["Tahun"] == 2020
][
    [
        "Kab_kota",
        "Provinsi",
        "Pulau",
        "pct_lansia",
        "p0_miskin",
        "Tipologi"
    ]
].copy()

typology_2020 = typology_2020.rename(
    columns={
        "pct_lansia": "pct_lansia_2020",
        "p0_miskin": "p0_miskin_2020",
        "Tipologi": "Tipologi_2020"
    }
)


typology_2024 = panel_typology[
    panel_typology["Tahun"] == 2024
][
    [
        "Kab_kota",
        "pct_lansia",
        "p0_miskin",
        "Tipologi"
    ]
].copy()

typology_2024 = typology_2024.rename(
    columns={
        "pct_lansia": "pct_lansia_2024",
        "p0_miskin": "p0_miskin_2024",
        "Tipologi": "Tipologi_2024"
    }
)


typology_transition = typology_2020.merge(
    typology_2024,
    on="Kab_kota",
    how="inner",
    validate="one_to_one"
)


typology_transition["delta_pct_lansia"] = (
    typology_transition["pct_lansia_2024"]
    - typology_transition["pct_lansia_2020"]
)

typology_transition["delta_p0_miskin"] = (
    typology_transition["p0_miskin_2024"]
    - typology_transition["p0_miskin_2020"]
)


print(
    typology_transition[
        [
            "Kab_kota",
            "Provinsi",
            "Pulau",
            "Tipologi_2020",
            "Tipologi_2024",
            "delta_pct_lansia",
            "delta_p0_miskin"
        ]
    ]
    .head(20)
    .to_string(index=False)
)


typology_transition.to_csv(
    TABEL_DIR / "transisi_tipologi_2020_2024.csv",
    index=False
)


# ============================================================
# 16. MATRIKS TRANSISI TIPOLOGI
# ============================================================

print("\n" + "=" * 70)
print("MATRIKS TRANSISI TIPOLOGI")
print("=" * 70)

transition_matrix = pd.crosstab(
    typology_transition["Tipologi_2020"],
    typology_transition["Tipologi_2024"]
)

print(transition_matrix)

transition_matrix.to_csv(
    TABEL_DIR / "matriks_transisi_tipologi_2020_2024.csv"
)


# ============================================================
# 17. JUMLAH KAB/KOTA YANG BERUBAH TIPOLOGI
# ============================================================

typology_transition["berubah_tipologi"] = (
    typology_transition["Tipologi_2020"]
    != typology_transition["Tipologi_2024"]
)

jumlah_berubah = (
    typology_transition["berubah_tipologi"]
    .sum()
)

jumlah_tetap = (
    (~typology_transition["berubah_tipologi"])
    .sum()
)

print(
    f"\nKab/kota yang berubah tipologi : {jumlah_berubah}"
)

print(
    f"Kab/kota yang tetap tipologi   : {jumlah_tetap}"
)

print(
    f"Persentase berubah             : "
    f"{jumlah_berubah / 273 * 100:.2f}%"
)


# ============================================================
# 18. VISUALISASI DISTRIBUSI TIPOLOGI
# ============================================================

print("\n" + "=" * 70)
print("MEMBUAT GRAFIK TIPOLOGI")
print("=" * 70)

typology_plot = (
    typology_year
    .pivot(
        index="Tahun",
        columns="Tipologi",
        values="jumlah_kab_kota"
    )
    .fillna(0)
)

plt.figure(figsize=(12, 7))

typology_plot.plot(
    kind="bar",
    stacked=True
)

plt.title(
    "Distribusi Tipologi Ageing dan Kemiskinan\n"
    "Kabupaten/Kota Jawa dan Sumatera, 2020–2024"
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
    GRAFIK_DIR / "distribusi_tipologi_2020_2024.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 19. SAVE DATASET NB03
# ============================================================

panel_typology.to_csv(
    OUTPUT_DIR / "panel_nb03_typology.csv",
    index=False
)


# ============================================================
# 20. SAVE TRANSITION DATASET
# ============================================================

typology_transition.to_csv(
    OUTPUT_DIR / "typology_transition_2020_2024.csv",
    index=False
)


# ============================================================
# 21. RINGKASAN OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("NB03 SELESAI")
print("=" * 70)

print("\nOutput tabel:")
print(TABEL_DIR)

print("\nOutput grafik:")
print(GRAFIK_DIR)

print("\nDataset tipologi:")
print(OUTPUT_DIR / "panel_nb03_typology.csv")

print("\nDataset transisi:")
print(OUTPUT_DIR / "typology_transition_2020_2024.csv")