# Menua di Tengah Perubahan

## Lansia dan Kesejahteraan di Jawa dan Sumatera, 2020–2024

Website interaktif yang mengeksplorasi perubahan proporsi penduduk lansia dan karakteristik kesejahteraan wilayah di kabupaten/kota Pulau Jawa dan Sumatera selama periode 2020–2024.

Proyek ini dikembangkan sebagai tugas Ujian Akhir Semester (UAS) mata kuliah Visualisasi Data dan Informasi di Politeknik Statistika STIS.

## Tujuan

Proyek ini bertujuan untuk mengeksplorasi bagaimana proses penuaan penduduk berlangsung di berbagai wilayah serta melihat karakteristik wilayah dari beberapa dimensi secara bersamaan.

Analisis difokuskan pada:

- perubahan proporsi penduduk lansia selama 2020–2024;
- pola spasial antarwilayah;
- hubungan antara proporsi lansia dan tingkat kemiskinan;
- perubahan karakteristik wilayah dari waktu ke waktu;
- struktur hierarki wilayah;
- serta pola multivariat berdasarkan indikator demografi, pendidikan, kesehatan, dan ekonomi.

## Cakupan Data

Analisis mencakup **273 kabupaten/kota di Pulau Jawa dan Sumatera** selama periode **2020–2024**.

Data utama bersumber dari **Badan Pusat Statistik (BPS)**.

Beberapa indikator yang digunakan antara lain:

- persentase penduduk lansia;
- jumlah penduduk;
- jumlah penduduk lansia;
- persentase anak;
- rata-rata lama sekolah;
- pengeluaran per kapita;
- angka harapan hidup;
- tingkat kemiskinan;
- serta perubahan proporsi lansia antara 2020 dan 2024.

## Metodologi

Analisis dan visualisasi dikembangkan melalui beberapa tahapan:

1. eksplorasi dan pemeriksaan data;
2. preprocessing dan penyusunan data panel;
3. pengolahan data spasial kabupaten/kota;
4. analisis statistik deskriptif;
5. analisis hubungan antara lansia dan kemiskinan;
6. analisis perubahan 2020–2024;
7. analisis struktur hierarki;
8. analisis multivariat menggunakan PCA dan UMAP;
9. visualisasi parallel coordinates;
10. integrasi seluruh hasil analisis ke dalam website interaktif.

## Visualisasi

Website menggunakan tiga kategori utama visualisasi sesuai kebutuhan proyek.

### 1. Geospatial

Visualisasi spasial digunakan untuk melihat distribusi indikator lansia dan karakteristik wilayah pada tingkat kabupaten/kota.

Fitur yang digunakan meliputi:

- peta choropleth interaktif (Leaflet);
- tooltip;
- zoom dan pan;
- serta pemetaan batas administrasi kabupaten/kota.

Data batas administrasi digunakan sebagai data pendukung untuk menghubungkan indikator BPS dengan wilayah geografis.

### 2. Hierarchical

Struktur wilayah divisualisasikan menggunakan:

- treemap;
- sunburst chart;
- drill-down;
- breadcrumb.

Dalam visualisasi hierarki:

- **ukuran** merepresentasikan jumlah penduduk;
- **warna** merepresentasikan persentase penduduk lansia.

Visualisasi ini digunakan untuk melihat struktur wilayah secara bertingkat sekaligus membandingkan besaran populasi dan tingkat penuaan.

### 3. Multivariate

Analisis multivariat menggunakan delapan variabel numerik:

1. jumlah penduduk;
2. jumlah lansia;
3. persentase lansia;
4. persentase anak;
5. rata-rata lama sekolah;
6. pengeluaran;
7. angka harapan hidup;
8. perubahan persentase lansia 2020–2024.

Beberapa teknik yang digunakan adalah:

- **Principal Component Analysis (PCA)** untuk merangkum variasi utama data;
- **UMAP** untuk melihat kedekatan profil multivariat antarwilayah;
- **Parallel Coordinates** untuk melihat karakteristik delapan indikator pada wilayah yang dipilih.

Tiga komponen utama PCA menjelaskan sekitar **84,60% variasi data**.

Website menyediakan interaksi pemilihan wilayah pada visualisasi PCA dan UMAP yang kemudian digunakan untuk melihat profil wilayah pada parallel coordinates.

## Hasil Utama

Beberapa temuan utama dari analisis adalah:

- Rata-rata proporsi penduduk lansia meningkat dari **9,89% pada 2020 menjadi 11,41% pada 2024**.
- Seluruh **273 kabupaten/kota** yang dianalisis mengalami peningkatan proporsi lansia.
- Rata-rata proporsi lansia meningkat sekitar **1,52 poin persentase** selama 2020–2024.
- Hubungan antara proporsi lansia dan tingkat kemiskinan pada masing-masing tahun relatif lemah.
- Karakteristik wilayah tidak dapat dijelaskan hanya melalui satu indikator karena terdapat kombinasi dimensi demografi, pendidikan, kesehatan, dan ekonomi.
- PCA menunjukkan bahwa tiga komponen utama mampu menjelaskan sekitar **84,60% variasi data multivariat**.

## Struktur Repository

```text
uas-visdat/
│
├── README.md
│
├── Data/                          # Data mentah (Excel + GeoJSON)
├── NB01_Preprocessing.py
├── NB02_EDA.py
├── NB03_EDA_AGEING_WELFARE.py
├── NB03_1_VALIDASI_TIPOLOGI.py
├── NB04_PCA_UMAP.py
├── NB05_FINAL_DATA.py
├── cek_shp.py
├── convert_shp_to_geojson.py
│
├── output/
│   ├── eda/
│   │   ├── grafik/
│   │   ├── peta/
│   │   └── tabel/
│   └── (CSV hasil analisis)
│
└── web/
    ├── index.html
    │
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── main.js
    │
    ├── libs/
    │   └── papaparse.min.js
    │
    ├── assets/
    │
    └── data/
        ├── web_panel_2020_2024.csv
        ├── web_multivariate_2024.csv
        ├── web_pca_scores_2024.csv
        ├── web_umap_2024.csv
        ├── mapping_kabkota_bps_shp.csv
        └── kabkota_bps_273.geojson
```

## Teknologi

Proyek ini menggunakan:

- **Python** untuk preprocessing, eksplorasi, dan analisis data;
- **HTML** untuk struktur halaman;
- **CSS** untuk tampilan dan responsive design;
- **JavaScript** (D3.js, Leaflet, PapaParse) untuk visualisasi dan interaksi;
- **GitHub** untuk version control dan repository;
- **GitHub Pages** untuk deployment website.

## Menjalankan Website Secara Lokal

File utama website adalah:

```text
web/index.html
```

Untuk hasil terbaik, jalankan menggunakan local web server agar file data CSV dan GeoJSON dapat dimuat dengan baik.

Contoh menggunakan Python:

```bash
python -m http.server 8000 --directory web
```

Kemudian buka:

```text
http://localhost:8000
```

## Sumber Data

**Sumber utama:**  
Badan Pusat Statistik (BPS).

Data digunakan untuk indikator demografi, kemiskinan, pendidikan, kesehatan, dan ekonomi yang dianalisis dalam proyek.

Data batas administrasi kabupaten/kota digunakan sebagai data pendukung untuk kebutuhan visualisasi geospasial.

## Deployment

Website dideploy secara publik menggunakan GitHub Pages.

**Website:**  
`[URL WEBSITE AKAN DITAMBAHKAN SETELAH DEPLOY]`

**Repository:**  
https://github.com/falizza/uas-visdat

## Author

**Faliza Maulidina Syarief**  
Politeknik Statistika STIS  
Mata Kuliah Visualisasi Data dan Informasi

## Catatan

Proyek ini dikembangkan untuk keperluan akademik sebagai bagian dari Ujian Akhir Semester mata kuliah Visualisasi Data dan Informasi.
