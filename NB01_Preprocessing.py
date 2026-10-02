# Impor Library
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
pd.set_option("display.float_format", lambda x: f"{x:,.3f}")

#Load Data
DATA_DIR = Path("Data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

excel_path = DATA_DIR / "Data_UAS.xlsx"
geojson_path = DATA_DIR / "peta_kabkota_jawa_sumatera.geojson"
xls = pd.ExcelFile(excel_path)
print("Daftar sheet:")
print(xls.sheet_names)

data_dict = {}

for year in xls.sheet_names:
    data_dict[int(year)] = pd.read_excel(excel_path, sheet_name=year)

for year, df in data_dict.items():
    print(year, df.shape)

for year, df in data_dict.items():
    print(f"\n===== {year} =====")
    print(df.columns.tolist())

for year, df in data_dict.items():
    print(
        year,
        "jumlah baris =", len(df),
        "| kab/kota unik =", df["Kab_kota"].nunique()
    )

for year, df in data_dict.items():
    dup = df["Kab_kota"].duplicated().sum()
    print(year, "duplikasi Kab_kota:", dup)

panel_list = []

for year, df in data_dict.items():
    temp = df.copy()
    temp["Tahun"] = year
    panel_list.append(temp)

panel = pd.concat(panel_list, ignore_index=True)

print("Ukuran panel:", panel.shape)

print(
    "Kab/kota:",
    panel["Kab_kota"].nunique()
)

print(
    "Tahun:",
    sorted(panel["Tahun"].unique())
)

print(
    "Observasi:",
    len(panel)
)
panel.groupby("Tahun")["Kab_kota"].nunique()

missing = (
    panel.isna()
    .sum()
    .sort_values(ascending=False)
)

missing

missing_table = pd.DataFrame({
    "missing": panel.isna().sum(),
    "persen_missing": panel.isna().mean() * 100
}).sort_values("missing", ascending=False)

missing_table

panel.dtypes
panel.info()

numeric_cols = panel.select_dtypes(
    include=np.number
).columns

panel[numeric_cols].describe().T

# ============================================================
# AUDIT MISSING VALUE
# ============================================================

missing_table = pd.DataFrame({
    "missing": panel.isna().sum(),
    "persen_missing": panel.isna().mean() * 100
}).sort_values("missing", ascending=False)

print("\n=== Missing Value ===")
print(missing_table)

# ============================================================
# CEK BALANCED PANEL
# ============================================================

panel_count = (
    panel.groupby("Kab_kota")["Tahun"]
    .agg(["count", "nunique", "min", "max"])
)

print("\n=== Struktur Panel ===")
print(panel_count["count"].value_counts())

print("\nJumlah kab/kota dengan 5 tahun:")
print((panel_count["count"] == 5).sum())

print("\nJumlah kab/kota dengan tahun unik = 5:")
print((panel_count["nunique"] == 5).sum())

# ============================================================
# CEK BALANCED PANEL
# ============================================================

panel_count = (
    panel.groupby("Kab_kota")["Tahun"]
    .agg(["count", "nunique", "min", "max"])
)

print("\n=== Struktur Panel ===")
print(panel_count["count"].value_counts())

print("\nJumlah kab/kota dengan 5 tahun:")
print((panel_count["count"] == 5).sum())

print("\nJumlah kab/kota dengan tahun unik = 5:")
print((panel_count["nunique"] == 5).sum())

print("\n=== Pulau ===")
print(panel["Pulau"].value_counts())
print(
    panel.groupby("Pulau")["Kab_kota"]
    .nunique()
)

province_count = (
    panel.groupby("Pulau")["Provinsi"]
    .nunique()
)

print("\nJumlah provinsi per pulau:")
print(province_count)
province_list = (
    panel[["Pulau", "Provinsi"]]
    .drop_duplicates()
    .sort_values(["Pulau", "Provinsi"])
)

print("\nDaftar provinsi:")
print(province_list.to_string(index=False))

# ============================================================
# RANGE DATA NUMERIK
# ============================================================

numeric_cols = panel.select_dtypes(
    include=np.number
).columns

range_table = pd.DataFrame({
    "min": panel[numeric_cols].min(),
    "max": panel[numeric_cols].max(),
    "mean": panel[numeric_cols].mean(),
    "median": panel[numeric_cols].median()
})

print("\n=== Range Variabel Numerik ===")
print(range_table)

comparison = pd.DataFrame({
    "pct_lansia": panel["pct_lansia"],
    "rasio_lansia": panel["rasio_lansia"],
})

comparison["selisih"] = (
    comparison["pct_lansia"] -
    comparison["rasio_lansia"]
)

print(comparison["selisih"].describe())
print(
    "Jumlah nilai yang identik:",
    np.isclose(
        panel["pct_lansia"],
        panel["rasio_lansia"]
    ).sum()
)

print(
    "Jumlah observasi:",
    len(panel)
)

print(
    "Jumlah nilai yang identik:",
    np.isclose(
        panel["pct_lansia"],
        panel["rasio_lansia"]
    ).sum()
)

print(
    "Jumlah observasi:",
    len(panel)
)

plt.figure(figsize=(8, 6))

sns.scatterplot(
    data=panel.sample(
        min(1000, len(panel)),
        random_state=42
    ),
    x="jumlah_lansia",
    y="pct_lansia",
    hue="Pulau",
    alpha=0.6
)

plt.title("Jumlah Lansia vs Persentase Lansia")
plt.xlabel("Jumlah Lansia")
plt.ylabel("Persentase Lansia (%)")
plt.tight_layout()
plt.show()

# LOAD GEOJSON
gdf = gpd.read_file(geojson_path)

print("\n=== GEOJSON ===")
print("Shape:", gdf.shape)
print("CRS:", gdf.crs)
print("Geometry types:")
print(gdf.geometry.geom_type.value_counts())
# ============================================================
# LOAD GEOJSON
# ============================================================

gdf = gpd.read_file(geojson_path)

print("\n=== GEOJSON ===")
print("Shape:", gdf.shape)
print("CRS:", gdf.crs)
print("Geometry types:")
print(gdf.geometry.geom_type.value_counts())

excel_names = set(panel["Kab_kota"].unique())
geo_names = set(gdf["Kab_kota"].unique())

print("\n=== Excel tetapi tidak ada di GeoJSON ===")
print(sorted(excel_names - geo_names))

print("\n=== GeoJSON tetapi tidak ada di Excel ===")
print(sorted(geo_names - excel_names))

excel_geo_check = (
    panel[["Kab_kota", "Provinsi"]]
    .drop_duplicates()
    .merge(
        gdf[["Kab_kota", "Provinsi"]].drop_duplicates(),
        on="Kab_kota",
        how="outer",
        suffixes=("_excel", "_geo")
    )
)

province_mismatch = excel_geo_check[
    excel_geo_check["Provinsi_excel"] !=
    excel_geo_check["Provinsi_geo"]
]

print("\n=== Province Mismatch ===")
print(province_mismatch)

print("\nGeometry kosong:", gdf.geometry.is_empty.sum())
print("Geometry missing:", gdf.geometry.isna().sum())
print("Geometry invalid:", (~gdf.geometry.is_valid).sum())

data_2024 = panel[
    panel["Tahun"] == 2024
].copy()

geo_master = gdf[
    ["Kab_kota", "Provinsi", "geometry"]
].copy()

map_2024 = geo_master.merge(
    data_2024,
    on=["Kab_kota", "Provinsi"],
    how="left",
    validate="one_to_one"
)

map_2024 = gpd.GeoDataFrame(
    map_2024,
    geometry="geometry",
    crs=gdf.crs
)

print("Shape:", map_2024.shape)
print("Missing pct_lansia:", map_2024["pct_lansia"].isna().sum())

fig, ax = plt.subplots(figsize=(10, 10))

map_2024.plot(
    column="pct_lansia",
    cmap="viridis",
    legend=True,
    linewidth=0.2,
    edgecolor="white",
    ax=ax
)

ax.set_title(
    "Persentase Penduduk Lansia Kabupaten/Kota\n"
    "Jawa dan Sumatera, 2024"
)

ax.axis("off")

plt.tight_layout()
plt.show()

panel.to_csv(
    OUTPUT_DIR / "panel_clean.csv",
    index=False
)

print("Saved:", OUTPUT_DIR / "panel_clean.csv")

map_2024.to_file(
    OUTPUT_DIR / "map_2024.geojson",
    driver="GeoJSON"
)

print("Saved:", OUTPUT_DIR / "map_2024.geojson")