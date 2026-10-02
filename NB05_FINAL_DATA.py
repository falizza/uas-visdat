from pathlib import Path
import pandas as pd


# ============================================================
# NB05 - FINAL DATASET UNTUK WEB STORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
EDA_TABLE_DIR = OUTPUT_DIR / "eda" / "tabel"

PANEL_FILE = OUTPUT_DIR / "panel_clean.csv"
MULTIVARIATE_FILE = OUTPUT_DIR / "nb04_multivariate_2024.csv"
PCA_FILE = OUTPUT_DIR / "nb04_pca_scores_2024.csv"
UMAP_FILE = OUTPUT_DIR / "nb04_umap_2024.csv"
PCA_VAR_FILE = EDA_TABLE_DIR / "nb04_pca_explained_variance.csv"
PCA_LOADINGS_FILE = EDA_TABLE_DIR / "nb04_pca_loadings.csv"

print("=" * 70)
print("NB05 - FINAL DATASET UNTUK WEB STORY")
print("=" * 70)


# ============================================================
# 1. BACA DATA
# ============================================================

print("\n[1] MEMBACA DATA")
print("-" * 70)

panel = pd.read_csv(PANEL_FILE)
multivariate = pd.read_csv(MULTIVARIATE_FILE)
pca = pd.read_csv(PCA_FILE)
umap = pd.read_csv(UMAP_FILE)
pca_var = pd.read_csv(PCA_VAR_FILE)
pca_loadings = pd.read_csv(PCA_LOADINGS_FILE)

print(f"Panel utama       : {panel.shape}")
print(f"Multivariate 2024 : {multivariate.shape}")
print(f"PCA scores        : {pca.shape}")
print(f"UMAP              : {umap.shape}")
print(f"PCA variance      : {pca_var.shape}")
print(f"PCA loadings      : {pca_loadings.shape}")


# ============================================================
# 2. VALIDASI PANEL UTAMA
# ============================================================

print("\n[2] VALIDASI PANEL UTAMA")
print("-" * 70)

required_panel = [
    "Kab_kota",
    "Provinsi",
    "Tahun",
    "pct_lansia",
    "p0_miskin",
    "rls",
    "pengeluaran",
    "ahh_rata2",
    "tpt_total"
]

missing_panel = [c for c in required_panel if c not in panel.columns]

if missing_panel:
    raise ValueError(
        f"Kolom panel yang dibutuhkan tidak ditemukan: {missing_panel}"
    )

print("Kolom utama tersedia.")

print(f"Tahun : {sorted(panel['Tahun'].unique().tolist())}")
print(f"Kab/kota : {panel['Kab_kota'].nunique()}")
print(f"Jumlah baris : {len(panel)}")

duplicate_panel = panel.duplicated(
    subset=["Kab_kota", "Tahun"]
).sum()

print(f"Duplikasi Kab_kota-Tahun : {duplicate_panel}")

if duplicate_panel > 0:
    raise ValueError("Terdapat duplikasi Kab_kota-Tahun.")


# ============================================================
# 3. VALIDASI DATA MULTIVARIAT 2024
# ============================================================

print("\n[3] VALIDASI MULTIVARIAT 2024")
print("-" * 70)

required_multi = [
    "Kab_kota",
    "Provinsi",
    "Tahun",
    "PC1",
    "PC2",
    "PC3",
    "PC4",
    "PC5",
    "PC6",
    "Tipologi_Lansia",
    "pct_lansia",
    "p0_miskin",
    "rls",
    "pengeluaran",
    "ahh_rata2",
    "tpt_total",
    "UMAP1",
    "UMAP2"
]

missing_multi = [c for c in required_multi if c not in multivariate.columns]

if missing_multi:
    raise ValueError(
        f"Kolom multivariat tidak ditemukan: {missing_multi}"
    )

multi_2024 = multivariate[
    multivariate["Tahun"] == 2024
].copy()

print(f"Baris multivariat 2024 : {len(multi_2024)}")
print(f"Kab/kota               : {multi_2024['Kab_kota'].nunique()}")

duplicate_multi = multi_2024.duplicated(
    subset=["Kab_kota"]
).sum()

print(f"Duplikasi kab/kota : {duplicate_multi}")

if duplicate_multi > 0:
    raise ValueError(
        "Terdapat lebih dari satu baris untuk kab/kota pada data multivariat 2024."
    )


# ============================================================
# 4. BUAT DATA PANEL FINAL
# ============================================================

print("\n[4] MEMBUAT PANEL FINAL 2020-2024")
print("-" * 70)

# Salin agar data asli tidak berubah
panel_final = panel.copy()

# Urutkan
panel_final = panel_final.sort_values(
    ["Kab_kota", "Tahun"]
).reset_index(drop=True)

print(f"Shape panel final : {panel_final.shape}")


# ============================================================
# 5. BUAT DATA MULTIVARIAT FINAL 2024
# ============================================================

print("\n[5] MEMBUAT DATA MULTIVARIAT FINAL 2024")
print("-" * 70)

web_multivariate = multi_2024.copy()

# Urutkan berdasarkan provinsi dan kab/kota
web_multivariate = web_multivariate.sort_values(
    ["Provinsi", "Kab_kota"]
).reset_index(drop=True)

print(f"Shape multivariat final : {web_multivariate.shape}")


# ============================================================
# 6. VALIDASI KESESUAIAN PANEL DAN MULTIVARIAT
# ============================================================

print("\n[6] VALIDASI KESESUAIAN DATA")
print("-" * 70)

panel_2024 = panel_final[
    panel_final["Tahun"] == 2024
].copy()

keys_panel = set(panel_2024["Kab_kota"])
keys_multi = set(web_multivariate["Kab_kota"])

only_panel = keys_panel - keys_multi
only_multi = keys_multi - keys_panel

print(f"Kab/kota hanya di panel      : {len(only_panel)}")
print(f"Kab/kota hanya di multivariat: {len(only_multi)}")

if only_panel:
    print("Contoh hanya di panel:", sorted(only_panel)[:10])

if only_multi:
    print("Contoh hanya di multivariat:", sorted(only_multi)[:10])

if only_panel or only_multi:
    raise ValueError(
        "Daftar kab/kota panel 2024 dan multivariat tidak sama."
    )

print("✓ Daftar kab/kota 2024 konsisten.")


# ============================================================
# 7. VALIDASI NILAI INDIKATOR 2024
# ============================================================

print("\n[7] VALIDASI NILAI INDIKATOR 2024")
print("-" * 70)

indicator_cols = [
    "pct_lansia",
    "p0_miskin",
    "rls",
    "pengeluaran",
    "ahh_rata2",
    "tpt_total"
]

check = panel_2024[
    ["Kab_kota"] + indicator_cols
].merge(
    web_multivariate[
        ["Kab_kota"] + indicator_cols
    ],
    on="Kab_kota",
    suffixes=("_panel", "_multi"),
    validate="one_to_one"
)

for col in indicator_cols:

    diff = (
        check[f"{col}_panel"] -
        check[f"{col}_multi"]
    ).abs()

    max_diff = diff.max()

    print(
        f"{col:15s} | maksimum selisih = {max_diff:.10f}"
    )

    if max_diff > 1e-8:
        raise ValueError(
            f"Nilai {col} berbeda antara panel dan multivariat."
        )

print("✓ Semua indikator 2024 konsisten.")


# ============================================================
# 8. VALIDASI PCA
# ============================================================

print("\n[8] VALIDASI PCA")
print("-" * 70)

pca_components = [
    "PC1",
    "PC2",
    "PC3",
    "PC4",
    "PC5",
    "PC6"
]

print(
    "Explained variance kumulatif PC2 : "
    f"{pca_var.loc[pca_var['Komponen'] == 'PC2', 'Cumulative_Variance'].iloc[0]:.2f}%"
)

print(
    "Explained variance kumulatif PC3 : "
    f"{pca_var.loc[pca_var['Komponen'] == 'PC3', 'Cumulative_Variance'].iloc[0]:.2f}%"
)

print("✓ Data PCA tersedia.")


# ============================================================
# 9. VALIDASI UMAP
# ============================================================

print("\n[9] VALIDASI UMAP")
print("-" * 70)

if {"UMAP1", "UMAP2"}.issubset(web_multivariate.columns):

    print("UMAP1 tersedia : Ya")
    print("UMAP2 tersedia : Ya")

    print(
        "Missing UMAP1 :",
        web_multivariate["UMAP1"].isna().sum()
    )

    print(
        "Missing UMAP2 :",
        web_multivariate["UMAP2"].isna().sum()
    )

else:
    raise ValueError("Kolom UMAP1/UMAP2 tidak ditemukan.")

print("✓ Data UMAP tersedia.")


# ============================================================
# 10. SIMPAN DATASET FINAL
# ============================================================

print("\n[10] MENYIMPAN DATASET FINAL")
print("-" * 70)

final_panel_file = OUTPUT_DIR / "web_panel_2020_2024.csv"
final_multi_file = OUTPUT_DIR / "web_multivariate_2024.csv"
final_pca_file = OUTPUT_DIR / "web_pca_scores_2024.csv"
final_umap_file = OUTPUT_DIR / "web_umap_2024.csv"

panel_final.to_csv(
    final_panel_file,
    index=False
)

web_multivariate.to_csv(
    final_multi_file,
    index=False
)

pca.to_csv(
    final_pca_file,
    index=False
)

umap.to_csv(
    final_umap_file,
    index=False
)

print(f"1. {final_panel_file}")
print(f"2. {final_multi_file}")
print(f"3. {final_pca_file}")
print(f"4. {final_umap_file}")


# ============================================================
# 11. RINGKASAN FINAL
# ============================================================

print("\n" + "=" * 70)
print("NB05 SELESAI")
print("=" * 70)

print("\nDataset yang siap digunakan untuk web story:")
print()
print("A. web_panel_2020_2024.csv")
print("   → tren 2020-2024")
print("   → perubahan indikator")
print("   → analisis longitudinal")
print()
print("B. web_multivariate_2024.csv")
print("   → peta 2024")
print("   → tipologi")
print("   → PCA")
print("   → UMAP")
print("   → visualisasi multivariat")
print()
print("C. web_pca_scores_2024.csv")
print("   → PCA biplot / analisis komponen")
print()
print("D. web_umap_2024.csv")
print("   → visualisasi UMAP")
print()
print("Semua proses NB05 berhasil.")