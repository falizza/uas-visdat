from pathlib import Path
import geopandas as gpd
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "web" / "data"

SHP_PATH = DATA_DIR / "Administrasi_Kabupaten.shp"
CSV_PATH = DATA_DIR / "web_panel_2020_2024.csv"

print("MEMBUAT MAPPING FINAL KAB/KOTA BPS → KODEKAB SHP")
print()

# =========================================================
# BACA DATA
# =========================================================

gdf = gpd.read_file(SHP_PATH)
df = pd.read_csv(CSV_PATH)

bps = (
    df[
        [
            "Pulau",
            "Provinsi",
            "Kab_kota"
        ]
    ]
    .drop_duplicates()
    .sort_values(
        [
            "Provinsi",
            "Kab_kota"
        ]
    )
    .reset_index(drop=True)
)

# =========================================================
# NORMALISASI PROVINSI
# =========================================================

def normalize_province(name):

    if pd.isna(name):
        return ""

    name = str(name).upper().strip()

    province_map = {
        "KEP. BANGKA BELITUNG":
            "KEPULAUAN BANGKA BELITUNG",

        "KEP BANGKA BELITUNG":
            "KEPULAUAN BANGKA BELITUNG",

        "KEP. RIAU":
            "KEPULAUAN RIAU",

        "KEP RIAU":
            "KEPULAUAN RIAU"
    }

    return province_map.get(
        name,
        name
    )


# =========================================================
# NORMALISASI NAMA KAB/KOTA
# =========================================================

def normalize_name(name):

    if pd.isna(name):
        return ""

    name = str(name).upper().strip()

    name = re.sub(
        r"^KABUPATEN\s+",
        "",
        name
    )

    name = re.sub(
        r"^KAB\.\s+",
        "",
        name
    )

    name = re.sub(
        r"^KOTA\s+",
        "",
        name
    )

    name = re.sub(
        r"[^A-Z0-9\s]",
        " ",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    ).strip()

    return name


# =========================================================
# NORMALISASI DATA
# =========================================================

bps["prov_norm"] = bps[
    "Provinsi"
].apply(
    normalize_province
)

bps["nama_norm"] = bps[
    "Kab_kota"
].apply(
    normalize_name
)

gdf["prov_norm"] = gdf[
    "nmprov"
].apply(
    normalize_province
)

gdf["nama_norm"] = gdf[
    "nmkab"
].apply(
    normalize_name
)

# =========================================================
# ALIAS NAMA KHUSUS
# =========================================================

alias_nama = {

    # DKI Jakarta
    (
        "DKI JAKARTA",
        "KEP. SERIBU"
    ): "KEPULAUAN SERIBU",

    # Kepulauan Riau
    (
        "KEPULAUAN RIAU",
        "KOTA BATAM"
    ): "B A T A M",

    # Riau
    (
        "RIAU",
        "KOTA DUMAI"
    ): "D U M A I",

    (
        "RIAU",
        "SIAK"
    ): "S I A K",

    # Sumatera Utara
    (
        "SUMATERA UTARA",
        "TOBA SAMOSIR / TOBA"
    ): "TOBA SAMOSIR"
}


# =========================================================
# CARI KANDIDAT
# =========================================================

def cari_kandidat(
    prov_norm,
    nama_norm,
    kab_kota
):

    alias_key = (
        prov_norm,
        kab_kota.upper().strip()
    )

    # -----------------------------------------------------
    # Alias khusus
    # -----------------------------------------------------

    if alias_key in alias_nama:

        nama_alias = alias_nama[
            alias_key
        ]

        nama_alias_norm = normalize_name(
            nama_alias
        )

        kandidat = gdf[
            (gdf["prov_norm"] == prov_norm) &
            (gdf["nama_norm"] == nama_alias_norm)
        ].copy()

        return kandidat

    # -----------------------------------------------------
    # Match normal
    # -----------------------------------------------------

    kandidat = gdf[
        (gdf["prov_norm"] == prov_norm) &
        (gdf["nama_norm"] == nama_norm)
    ].copy()

    return kandidat


# =========================================================
# PROSES MAPPING
# =========================================================

hasil = []

for _, row in bps.iterrows():

    prov_norm = row["prov_norm"]
    nama_norm = row["nama_norm"]
    kab_kota = row["Kab_kota"]

    kandidat = cari_kandidat(
        prov_norm,
        nama_norm,
        kab_kota
    )

    # -----------------------------------------------------
    # Tidak ditemukan
    # -----------------------------------------------------

    if len(kandidat) == 0:

        hasil.append(
            {
                "Pulau": row["Pulau"],
                "Provinsi": row["Provinsi"],
                "Kab_kota": kab_kota,
                "kodekab": None,
                "nmprov_shp": None,
                "nmkab_shp": None,
                "status": "TIDAK_MATCH"
            }
        )

        continue

    # -----------------------------------------------------
    # Satu kandidat
    # -----------------------------------------------------

    if len(kandidat) == 1:

        shp = kandidat.iloc[0]

        hasil.append(
            {
                "Pulau": row["Pulau"],
                "Provinsi": row["Provinsi"],
                "Kab_kota": kab_kota,
                "kodekab": str(
                    shp["kodekab"]
                ),
                "nmprov_shp": shp["nmprov"],
                "nmkab_shp": shp["nmkab"],
                "status": "MATCH_UNIK"
            }
        )

        continue

    # -----------------------------------------------------
    # Kandidat ganda
    # -----------------------------------------------------

    is_kota = kab_kota.upper().startswith(
        "KOTA "
    )

    kandidat = kandidat.copy()

    kandidat["kode_akhir"] = (
        kandidat["kodekab"]
        .astype(str)
        .str[-2:]
    )

    # Kota = kode 71–79
    if is_kota:

        kandidat_kota = kandidat[
            kandidat["kode_akhir"].astype(int).between(
                71,
                79
            )
        ].copy()

        if len(kandidat_kota) == 1:
            kandidat = kandidat_kota

    # Kabupaten = kode selain 71–79
    else:

        kandidat_kab = kandidat[
            ~kandidat["kode_akhir"].astype(int).between(
                71,
                79
            )
        ].copy()

        if len(kandidat_kab) == 1:
            kandidat = kandidat_kab

    # -----------------------------------------------------
    # Hasil setelah resolusi
    # -----------------------------------------------------

    if len(kandidat) == 1:

        shp = kandidat.iloc[0]

        hasil.append(
            {
                "Pulau": row["Pulau"],
                "Provinsi": row["Provinsi"],
                "Kab_kota": kab_kota,
                "kodekab": str(
                    shp["kodekab"]
                ),
                "nmprov_shp": shp["nmprov"],
                "nmkab_shp": shp["nmkab"],
                "status": "MATCH_RESOLVED"
            }
        )

    else:

        kode_list = ", ".join(
            kandidat["kodekab"]
            .astype(str)
            .tolist()
        )

        nama_list = " | ".join(
            kandidat["nmkab"]
            .astype(str)
            .tolist()
        )

        hasil.append(
            {
                "Pulau": row["Pulau"],
                "Provinsi": row["Provinsi"],
                "Kab_kota": kab_kota,
                "kodekab": None,
                "nmprov_shp": None,
                "nmkab_shp": (
                    f"KANDIDAT: {nama_list} "
                    f"({kode_list})"
                ),
                "status": "AMBIGU"
            }
        )


mapping = pd.DataFrame(hasil)

# =========================================================
# VALIDASI
# =========================================================

print("VALIDASI MAPPING")
print()

print(
    mapping["status"]
    .value_counts()
    .to_string()
)

print()

print(
    f"Total BPS        : {len(mapping)}"
)

print(
    f"Kodekab terisi   : "
    f"{mapping['kodekab'].notna().sum()}"
)

print(
    f"Kodekab kosong   : "
    f"{mapping['kodekab'].isna().sum()}"
)

# =========================================================
# CEK KODEKAB DUPLIKAT
# =========================================================

duplikat_kode = (
    mapping[
        mapping["kodekab"].notna()
    ]
    .groupby("kodekab")
    .size()
)

duplikat_kode = duplikat_kode[
    duplikat_kode > 1
]

print()

print(
    f"Kodekab dipakai >1 BPS : "
    f"{len(duplikat_kode)}"
)

if len(duplikat_kode) > 0:

    print()
    print("KODEKAB DUPLIKAT")
    print()

    print(
        mapping[
            mapping["kodekab"].isin(
                duplikat_kode.index
            )
        ]
        [
            [
                "Provinsi",
                "Kab_kota",
                "kodekab"
            ]
        ]
        .sort_values("kodekab")
        .to_string(index=False)
    )

# =========================================================
# CEK TIDAK MATCH
# =========================================================

tidak_match = mapping[
    mapping["status"] == "TIDAK_MATCH"
]

if not tidak_match.empty:

    print()
    print("TIDAK MATCH")
    print()

    print(
        tidak_match[
            [
                "Provinsi",
                "Kab_kota"
            ]
        ].to_string(index=False)
    )

# =========================================================
# CEK AMBIGU
# =========================================================

ambigu = mapping[
    mapping["status"] == "AMBIGU"
]

if not ambigu.empty:

    print()
    print("AMBIGU")
    print()

    print(
        ambigu[
            [
                "Provinsi",
                "Kab_kota",
                "nmkab_shp"
            ]
        ].to_string(index=False)
    )

# =========================================================
# VALIDASI AKHIR
# =========================================================

valid_final = (
    len(mapping) == 273
    and mapping["kodekab"].notna().all()
    and len(duplikat_kode) == 0
    and mapping["status"].isin(
        [
            "MATCH_UNIK",
            "MATCH_RESOLVED"
        ]
    ).all()
)

print()

if valid_final:

    print("STATUS AKHIR: MAPPING VALID 273/273")
    print("Semua kab/kota BPS memiliki kodekab unik.")

else:

    print("STATUS AKHIR: MAPPING BELUM VALID")
    print("Jangan gunakan mapping ini untuk web dulu.")

# =========================================================
# SIMPAN MAPPING FINAL
# =========================================================

output_path = (
    DATA_DIR /
    "mapping_kabkota_bps_shp.csv"
)

mapping.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print()

print("File mapping disimpan:")
print(output_path)