import geopandas as gpd
import pandas as pd
from pathlib import Path


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

SHP_PATH = BASE_DIR / "web" / "data" / "Administrasi_Kabupaten.shp"
MAPPING_PATH = BASE_DIR / "web" / "data" / "mapping_kabkota_bps_shp.csv"
OUTPUT_PATH = BASE_DIR / "web" / "data" / "kabkota_bps_273.geojson"


# ============================================================
# 1. BACA SHP
# ============================================================

print("MEMBACA SHP ADMINISTRASI KABUPATEN/KOTA")

gdf = gpd.read_file(SHP_PATH)

print(f"Jumlah polygon SHP : {len(gdf)}")
print(f"CRS                : {gdf.crs}")


# ============================================================
# 2. BACA MAPPING BPS → KODEKAB
# ============================================================

print("\nMEMBACA MAPPING BPS → KODEKAB")

mapping = pd.read_csv(MAPPING_PATH, dtype=str)

print(f"Jumlah baris mapping : {len(mapping)}")

# Pastikan kodekab berupa string
mapping["kodekab"] = mapping["kodekab"].astype(str).str.strip()

# Hilangkan .0 jika sebelumnya terbaca sebagai angka
mapping["kodekab"] = mapping["kodekab"].str.replace(
    r"\.0$",
    "",
    regex=True
)


# ============================================================
# 3. NORMALISASI KODEKAB SHP
# ============================================================

gdf["kodekab"] = (
    gdf["kodekab"]
    .astype(str)
    .str.strip()
    .str.replace(r"\.0$", "", regex=True)
)


# ============================================================
# 4. VALIDASI KODEKAB
# ============================================================

mapping_codes = set(mapping["kodekab"])
shp_codes = set(gdf["kodekab"])

missing_in_shp = sorted(mapping_codes - shp_codes)

print("\nVALIDASI KODEKAB")

print(f"Kodekab dari BPS mapping : {len(mapping_codes)}")
print(f"Kodekab di SHP            : {len(shp_codes)}")
print(f"Kodekab mapping tidak ada di SHP : {len(missing_in_shp)}")

if missing_in_shp:
    print("\nKodekab yang tidak ditemukan:")
    for code in missing_in_shp:
        print(f"  {code}")

    raise ValueError(
        "Ada kodekab BPS yang tidak ditemukan di SHP. "
        "Proses dihentikan."
    )


# ============================================================
# 5. FILTER SHP → HANYA 273 KAB/KOTA BPS
# ============================================================

gdf_273 = gdf[gdf["kodekab"].isin(mapping_codes)].copy()

print("\nFILTER POLYGON")

print(f"Polygon hasil filter : {len(gdf_273)}")


# ============================================================
# 6. CEK JUMLAH HARUS 273
# ============================================================

if len(gdf_273) != len(mapping_codes):
    raise ValueError(
        f"Jumlah polygon hasil filter ({len(gdf_273)}) "
        f"tidak sama dengan jumlah kodekab BPS ({len(mapping_codes)})."
    )


# ============================================================
# 7. CEK KODEKAB DUPLIKAT
# ============================================================

duplicate_codes = (
    gdf_273["kodekab"]
    .value_counts()
)

duplicate_codes = duplicate_codes[
    duplicate_codes > 1
]

print(f"Kodekab SHP duplikat : {len(duplicate_codes)}")

if len(duplicate_codes) > 0:
    print("\nKodekab duplikat:")
    print(duplicate_codes)

    raise ValueError(
        "Ada kodekab SHP yang memiliki lebih dari satu polygon."
    )


# ============================================================
# 8. SIMPLIFIKASI PROPERTY
# ============================================================

# Kita hanya menyimpan property yang berguna untuk web.
# Geometri tetap berasal langsung dari SHP.

keep_columns = [
    "kodekab",
    "kdkab",
    "kdprov",
    "nmkab",
    "nmprov",
    "periode",
    "sumber",
    "geometry",
]

existing_columns = [
    col for col in keep_columns
    if col in gdf_273.columns
]

gdf_273 = gdf_273[existing_columns].copy()


# ============================================================
# 9. CRS UNTUK WEB MAP
# ============================================================

if gdf_273.crs is None:
    raise ValueError("CRS SHP tidak ditemukan.")

# Leaflet menggunakan koordinat geografis WGS84
gdf_273 = gdf_273.to_crs(epsg=4326)


# ============================================================
# 10. VALIDASI GEOMETRI
# ============================================================

empty_geometry = gdf_273.geometry.is_empty.sum()
null_geometry = gdf_273.geometry.isna().sum()
invalid_geometry = (~gdf_273.geometry.is_valid).sum()

print("\nVALIDASI GEOMETRI")

print(f"Geometry kosong : {empty_geometry}")
print(f"Geometry NULL   : {null_geometry}")
print(f"Geometry invalid: {invalid_geometry}")

if empty_geometry > 0:
    raise ValueError("Ada geometry kosong.")

if null_geometry > 0:
    raise ValueError("Ada geometry NULL.")

if invalid_geometry > 0:
    print("\nMemperbaiki geometry invalid...")
    gdf_273["geometry"] = gdf_273.geometry.make_valid()

    invalid_after = (~gdf_273.geometry.is_valid).sum()

    if invalid_after > 0:
        raise ValueError(
            "Masih terdapat geometry invalid setelah make_valid()."
        )


# ============================================================
# 11. SIMPAN GEOJSON
# ============================================================

gdf_273.to_file(
    OUTPUT_PATH,
    driver="GeoJSON"
)


# ============================================================
# 12. VALIDASI HASIL AKHIR
# ============================================================

hasil = gpd.read_file(OUTPUT_PATH)

hasil["kodekab"] = (
    hasil["kodekab"]
    .astype(str)
    .str.strip()
)

print("\nVALIDASI GEOJSON HASIL")

print(f"Jumlah feature : {len(hasil)}")
print(f"Kodekab unik   : {hasil['kodekab'].nunique()}")
print(f"CRS            : {hasil.crs}")

print(
    f"Bounds         : "
    f"{hasil.total_bounds}"
)

print("\nSTATUS AKHIR")

if (
    len(hasil) == 273
    and hasil["kodekab"].nunique() == 273
):
    print("GEOJSON VALID 273/273")
    print("Semua kab/kota BPS memiliki polygon SHP.")
    print()
    print(f"File disimpan:")
    print(OUTPUT_PATH)
else:
    raise ValueError(
        "Validasi GeoJSON gagal."
    )