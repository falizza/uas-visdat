// SCROLL REVEAL

function setupScrollReveal() {

    const revealElements =
        document.querySelectorAll(".reveal");

    if (!revealElements.length) {
        return;
    }

    const observer =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        entry.target.classList.add(
                            "is-visible"
                        );

                    } else {

                        entry.target.classList.remove(
                            "is-visible"
                        );

                    }

                });

            },
            {
                threshold: 0.15
            }
        );

    revealElements.forEach((element) => {

        observer.observe(element);

    });

}


// NUMBER COUNTER

function setupCounters() {

    const counters =
        document.querySelectorAll(".counter");

    if (!counters.length) {
        return;
    }

    const activeCounters =
        new WeakSet();

    function animateCounter(counter) {

        if (activeCounters.has(counter)) {
            return;
        }

        activeCounters.add(counter);

        const start =
            Number(counter.dataset.start || 0);

        const end =
            Number(counter.dataset.end || 0);

        const decimal =
            Number(counter.dataset.decimal || 0);

        if (start === end) {

            counter.textContent =
                start.toLocaleString(
                    "id-ID",
                    {
                        minimumFractionDigits: decimal,
                        maximumFractionDigits: decimal
                    }
                );

            return;
        }

        const duration = 1400;

        const startTime =
            performance.now();

        function updateCounter(currentTime) {

            const elapsed =
                currentTime - startTime;

            const progress =
                Math.min(
                    elapsed / duration,
                    1
                );

            const eased =
                1 - Math.pow(
                    1 - progress,
                    3
                );

            const value =
                start +
                (end - start) * eased;

            counter.textContent =
                value.toLocaleString(
                    "id-ID",
                    {
                        minimumFractionDigits: decimal,
                        maximumFractionDigits: decimal
                    }
                );

            if (progress < 1) {

                requestAnimationFrame(
                    updateCounter
                );

            } else {

                counter.textContent =
                    end.toLocaleString(
                        "id-ID",
                        {
                            minimumFractionDigits: decimal,
                            maximumFractionDigits: decimal
                        }
                    );

            }

        }

        requestAnimationFrame(
            updateCounter
        );

    }

    const counterObserver =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        activeCounters.delete(
                            entry.target
                        );

                        animateCounter(
                            entry.target
                        );

                    } else {

                        activeCounters.delete(
                            entry.target
                        );

                    }

                });

            },
            {
                threshold: 0.45
            }
        );

    counters.forEach((counter) => {

        counterObserver.observe(counter);

    });

}


// INDICATOR CARD ANIMATION

function setupIndicatorAnimation() {

    const cards =
        document.querySelectorAll(
            ".indicator-card"
        );

    if (!cards.length) {
        return;
    }

    const observer =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    const line =
                        entry.target.querySelector(
                            ".indicator-line span"
                        );

                    if (!line) {
                        return;
                    }

                    if (entry.isIntersecting) {

                        line.style.animation =
                            "none";

                        void line.offsetWidth;

                        line.style.animation =
                            "indicatorGrow 1.2s cubic-bezier(.22,.61,.36,1) both";

                    }

                });

            },
            {
                threshold: 0.35
            }
        );

    cards.forEach((card) => {

        observer.observe(card);

    });

}


// OPENING REPLAY

function setupOpeningReplay() {

    const opening =
        document.querySelector(
            "#opening"
        );

    if (!opening) {
        return;
    }

    const animatedElements =
        opening.querySelectorAll(
            ".opening-center, .opening-character-left, .opening-character-right"
        );

    const observer =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (!entry.isIntersecting) {
                        return;
                    }

                    animatedElements.forEach(
                        (element) => {

                            element.style.animation =
                                "none";

                            void element.offsetWidth;

                            element.style.animation =
                                "";

                        }
                    );

                });

            },
            {
                threshold: 0.5
            }
        );

    observer.observe(opening);

}


// SMOOTH SCROLL DARI OPENING

function setupOpeningScroll() {

    const opening =
        document.querySelector(
            "#opening"
        );

    const scrollIndicator =
        document.querySelector(
            ".opening-scroll"
        );

    if (!opening || !scrollIndicator) {
        return;
    }

    scrollIndicator.addEventListener(
        "click",
        () => {

            const context =
                document.querySelector(
                    "#context"
                );

            if (!context) {
                return;
            }

            context.scrollIntoView({
                behavior: "smooth"
            });

        }
    );

}
function setupBackToTop() {
    const button = document.querySelector("#back-to-top");

    if (!button) return;

    button.addEventListener("click", () => {
        const opening = document.querySelector("#opening");

        if (opening) {
            opening.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        } else {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }
    });
}
function setupStoryNavigation() {
    const navItems = document.querySelectorAll(".story-nav-item");

    if (!navItems.length) return;

    navItems.forEach((item) => {
        item.addEventListener("click", () => {
            const targetId = item.dataset.target;
            const target = document.getElementById(targetId);

            if (!target) return;

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        });
    });
}
function setupStoryNavigationObserver() {
    const navItems = document.querySelectorAll(".story-nav-item");

    if (!navItems.length) return;

    const sections = Array.from(navItems)
        .map((item) => {
            const targetId = item.dataset.target;
            return document.getElementById(targetId);
        })
        .filter(Boolean);

    function updateActiveSection() {
        const viewportCenter = window.scrollY + (window.innerHeight / 2);

        let activeSection = sections[0];

        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            const sectionBottom = sectionTop + section.offsetHeight;

            if (
                viewportCenter >= sectionTop &&
                viewportCenter < sectionBottom
            ) {
                activeSection = section;
            }
        });

        navItems.forEach((item) => {
            item.classList.toggle(
                "active",
                item.dataset.target === activeSection.id
            );
        });
    }

    let ticking = false;

    window.addEventListener("scroll", () => {
        if (ticking) return;

        window.requestAnimationFrame(() => {
            updateActiveSection();
            ticking = false;
        });

        ticking = true;
    });

    window.addEventListener("resize", updateActiveSection);

    updateActiveSection();
}

// KONFIGURASI DATA PETA

const SPATIAL_CONFIG = {

    csvPath:
        "data/web_panel_2020_2024.csv",

    mappingPath:
        "data/mapping_kabkota_bps_shp.csv",

    geojsonPath:
        "data/kabkota_bps_273.geojson",

    defaultYear:
        2024,

    defaultIndicator:
        "pct_lansia"

};


// STATE PETA

let spatialMap = null;

let spatialGeojsonLayer = null;

let spatialPanelData = [];

let spatialMappingData = [];

let spatialGeojsonData = null;

let spatialCurrentYear =
    SPATIAL_CONFIG.defaultYear;

let spatialCurrentIndicator =
    SPATIAL_CONFIG.defaultIndicator;


// HELPER — NUMBER

function spatialNumber(
    value,
    decimal = 2
) {

    const number =
        Number(value);

    if (!Number.isFinite(number)) {
        return "—";
    }

    return number.toLocaleString(
        "id-ID",
        {
            minimumFractionDigits: decimal,
            maximumFractionDigits: decimal
        }
    );

}


// HELPER — NORMALISASI TEKS

function spatialNormalizeText(
    value
) {

    return String(value || "")
        .trim()
        .toLowerCase()
        .replace(/\s+/g, " ");

}


// HELPER — INDIKATOR

function getSpatialIndicatorLabel() {

    if (
        spatialCurrentIndicator ===
        "p0_miskin"
    ) {

        return "Tingkat Kemiskinan (%)";

    }

    return "Proporsi Lansia (%)";

}


function getSpatialIndicatorShortLabel() {

    if (
        spatialCurrentIndicator ===
        "p0_miskin"
    ) {

        return "Tingkat Kemiskinan";

    }

    return "Proporsi Lansia";

}


// HELPER — WARNA PETA

function getSpatialColor(
    value,
    min,
    max,
    indicator
) {

    if (
        !Number.isFinite(value) ||
        !Number.isFinite(min) ||
        !Number.isFinite(max)
    ) {

        return "#dfe4e6";

    }

    if (max === min) {

        if (indicator === "p0_miskin") {
            return "#c2410c";
        }

        return "#9333ea";

    }

    const ratio =
        Math.min(
            1,
            Math.max(
                0,
                (value - min) /
                (max - min)
            )
        );

    let palette;

    if (
        indicator ===
        "pct_lansia"
    ) {

        palette = [
            "#f3e8ff",
            "#e9d5ff",
            "#d8b4fe",
            "#c084fc",
            "#a855f7",
            "#7e22ce",
            "#581c87"
        ];

    } else if (
        indicator ===
        "p0_miskin"
    ) {

        palette = [
            "#fff7ed",
            "#ffedd5",
            "#fed7aa",
            "#fdba74",
            "#fb923c",
            "#ea580c",
            "#9a3412"
        ];

    } else {

        palette = [
            "#e8eef1",
            "#c8d8dd",
            "#a9c1ca",
            "#89a9b4",
            "#668b99",
            "#4d7180",
            "#355c7d"
        ];

    }

    const index =
        Math.min(
            palette.length - 1,
            Math.max(
                0,
                Math.floor(
                    ratio *
                    palette.length
                )
            )
        );

    return palette[index];

}


// AMBIL DATA TAHUN + INDIKATOR

function getSpatialYearData() {

    return spatialPanelData.filter(
        (row) => {

            return Number(row.Tahun) ===
                Number(spatialCurrentYear);

        }
    );

}


// BUAT LOOKUP DATA BPS BERDASARKAN KODEKAB

function createSpatialLookup() {

    const lookup =
        new Map();

    getSpatialYearData().forEach(
        (row) => {

            const kabKotaKey =
                spatialNormalizeText(
                    row.Kab_kota
                );

            const mapping =
                spatialMappingData.find(
                    (item) => {

                        return (
                            spatialNormalizeText(
                                item.Kab_kota
                            ) ===
                            kabKotaKey
                        );

                    }
                );

            if (!mapping) {
                return;
            }

            const kodekab =
                String(
                    mapping.kodekab || ""
                )
                .trim()
                .replace(
                    /\.0$/,
                    ""
                );

            if (!kodekab) {
                return;
            }

            lookup.set(
                kodekab,
                row
            );

        }
    );

    return lookup;

}


// HITUNG DOMAIN WARNA

function getSpatialDomain() {

    const rows =
        getSpatialYearData();

    const values =
        rows
            .map(
                (row) =>
                    Number(
                        row[
                            spatialCurrentIndicator
                        ]
                    )
            )
            .filter(
                (value) =>
                    Number.isFinite(value)
            );

    if (!values.length) {

        return {
            min: 0,
            max: 1
        };

    }

    return {
        min: Math.min(...values),
        max: Math.max(...values)
    };

}


// AMBIL KODEKAB DARI FEATURE SHP

function getSpatialFeatureKodekab(
    feature
) {

    const properties =
        feature.properties || {};

    const kodekab =
        properties.kodekab ||
        properties.KODEKAB ||
        properties.kodeKab ||
        "";

    return String(
        kodekab
    )
        .trim()
        .replace(
            /\.0$/,
            ""
        );

}


// STYLE GEOJSON

function spatialFeatureStyle(
    feature
) {

    const lookup =
        createSpatialLookup();

    const kodekab =
        getSpatialFeatureKodekab(
            feature
        );

    const row =
        lookup.get(
            kodekab
        );

    const value =
        row
            ? Number(
                row[
                    spatialCurrentIndicator
                ]
            )
            : NaN;

    const domain =
        getSpatialDomain();

    return {

        fillColor:
            getSpatialColor(
                value,
                domain.min,
                domain.max,
                spatialCurrentIndicator
            ),

        weight:
            0.7,

        opacity:
            1,

        color:
            "rgba(255,255,255,0.9)",

        fillOpacity:
            0.82

    };

}


// HIGHLIGHT WILAYAH

function spatialHighlightFeature(
    event
) {

    const layer =
        event.target;

    layer.setStyle({

        weight:
            2.5,

        color:
            "#1f2933",

        fillOpacity:
            0.95

    });

    if (
        !L.Browser.ie &&
        !L.Browser.opera &&
        !L.Browser.edge
    ) {

        layer.bringToFront();

    }

    spatialUpdateTooltip(
        layer
    );

}


// RESET HIGHLIGHT

function spatialResetHighlight(
    event
) {

    if (!spatialGeojsonLayer) {
        return;
    }

    spatialGeojsonLayer.resetStyle(
        event.target
    );

    event.target.closeTooltip();

}


// TOOLTIP

function spatialUpdateTooltip(
    layer
) {

    const properties =
        layer.feature.properties || {};

    const kodekab =
        getSpatialFeatureKodekab(
            layer.feature
        );

    const kabKota =
        properties.nmkab ||
        properties.NAMOBJ ||
        properties.Kab_kota ||
        properties.kab_kota ||
        "Kabupaten/Kota";

    const provinsi =
        properties.nmprov ||
        properties.Provinsi ||
        properties.provinsi ||
        "";

    const lookup =
        createSpatialLookup();

    const row =
        lookup.get(
            kodekab
        );

    const pctLansia =
        row
            ? Number(row.pct_lansia)
            : NaN;

    const p0Miskin =
        row
            ? Number(row.p0_miskin)
            : NaN;

    const rls =
        row
            ? Number(row.rls)
            : NaN;

    const pengeluaran =
        row
            ? Number(row.pengeluaran)
            : NaN;

    const lansiaText =
        Number.isFinite(pctLansia)
            ? spatialNumber(
                pctLansia,
                2
            ) + "%"
            : "–";

    const miskinText =
        Number.isFinite(p0Miskin)
            ? spatialNumber(
                p0Miskin,
                2
            ) + "%"
            : "–";

    const rlsText =
        Number.isFinite(rls)
            ? spatialNumber(
                rls,
                2
            ) + " tahun"
            : "–";

    const pengeluaranText =
        Number.isFinite(pengeluaran)
            ? "Rp " +
              spatialNumber(
                  pengeluaran / 1000,
                  2
              ) +
              " juta/orang/tahun"
            : "–";

    const html = `
        <div class="map-tooltip">

            <div class="map-tooltip-name">
                ${kabKota}
            </div>

            <div class="map-tooltip-location">
                ${provinsi}
                ${provinsi ? " · " : ""}
                ${spatialCurrentYear}
            </div>

            <div class="map-tooltip-divider"></div>

            <div class="map-tooltip-row">
                <span>
                    Proporsi Lansia
                </span>
                <strong>
                    ${lansiaText}
                </strong>
            </div>

            <div class="map-tooltip-row">
                <span>
                    Tingkat Kemiskinan
                </span>
                <strong>
                    ${miskinText}
                </strong>
            </div>

            <div class="map-tooltip-row">
                <span>
                    RLS
                </span>
                <strong>
                    ${rlsText}
                </strong>
            </div>

            <div class="map-tooltip-row">
                <span>
                    Pengeluaran per Kapita
                </span>
                <strong>
                    ${pengeluaranText}
                </strong>
            </div>

        </div>
    `;

    layer.bindTooltip(
        html,
        {
            sticky:
                true,

            direction:
                "top",

            opacity:
                0.97
        }
    );

    layer.openTooltip();

}


// EVENT GEOJSON

function spatialOnEachFeature(
    feature,
    layer
) {

    layer.on({

        mouseover:
            spatialHighlightFeature,

        mouseout:
            spatialResetHighlight,

        click:
            (event) => {

                spatialHighlightFeature(
                    event
                );

                spatialUpdateTooltip(
                    event.target
                );

            }

    });

}


// RENDER GEOJSON

function renderSpatialGeoJSON() {

    if (!spatialMap) {
        return;
    }

    if (spatialGeojsonLayer) {

        spatialMap.removeLayer(
            spatialGeojsonLayer
        );

    }

    spatialGeojsonLayer =
        L.geoJSON(
            spatialGeojsonData,
            {

                style:
                    spatialFeatureStyle,

                onEachFeature:
                    spatialOnEachFeature

            }
        );

    spatialGeojsonLayer.addTo(
        spatialMap
    );

    updateSpatialLegend();

}


// UPDATE LEGEND

function updateSpatialLegend() {

    const title =
        document.querySelector(
            "#map-legend-title"
        );

    const minLabel =
        document.querySelector(
            "#legend-min"
        );

    const maxLabel =
        document.querySelector(
            "#legend-max"
        );

    const gradient =
        document.querySelector(
            "#map-gradient"
        );

    if (
        !title ||
        !minLabel ||
        !maxLabel
    ) {

        return;

    }

    const domain =
        getSpatialDomain();

    title.textContent =
        getSpatialIndicatorLabel();

    minLabel.textContent =
        spatialNumber(
            domain.min,
            2
        ) + "%";

    maxLabel.textContent =
        spatialNumber(
            domain.max,
            2
        ) + "%";

    if (!gradient) {
        return;
    }

    if (
        spatialCurrentIndicator ===
        "pct_lansia"
    ) {

        gradient.style.background =
            "linear-gradient(" +
            "90deg," +
            "#f3e8ff 0%," +
            "#d8b4fe 35%," +
            "#a855f7 70%," +
            "#581c87 100%" +
            ")";

    } else if (
        spatialCurrentIndicator ===
        "p0_miskin"
    ) {

        gradient.style.background =
            "linear-gradient(" +
            "90deg," +
            "#fff7ed 0%," +
            "#fed7aa 35%," +
            "#fb923c 70%," +
            "#9a3412 100%" +
            ")";

    }

}


// UPDATE MAP

function updateSpatialMap() {

    if (
        !spatialMap ||
        !spatialGeojsonData
    ) {

        return;

    }

    renderSpatialGeoJSON();

}


// LOAD CSV BPS

function loadSpatialCSV() {

    return new Promise(
        (
            resolve,
            reject
        ) => {

            console.log(
                "[PETA] Memuat CSV:",
                SPATIAL_CONFIG.csvPath
            );

            if (
                typeof Papa ===
                "undefined"
            ) {

                reject(
                    new Error(
                        "Papa Parse tidak ditemukan."
                    )
                );

                return;

            }

            Papa.parse(
                SPATIAL_CONFIG.csvPath,
                {

                    download:
                        true,

                    header:
                        true,

                    skipEmptyLines:
                        true,

                    dynamicTyping:
                        true,

                    complete:
                        (results) => {

                            console.log(
                                "[PETA] CSV berhasil dimuat."
                            );

                            console.log(
                                "[PETA] Jumlah baris:",
                                results.data.length
                            );

                            console.log(
                                "[PETA] Kolom:",
                                results.meta.fields
                            );

                            if (
                                !results.meta.fields ||
                                !results.meta.fields.includes(
                                    "Kab_kota"
                                )
                            ) {

                                reject(
                                    new Error(
                                        "Kolom Kab_kota tidak ditemukan pada CSV."
                                    )
                                );

                                return;

                            }

                            if (
                                !results.meta.fields.includes(
                                    "Tahun"
                                )
                            ) {

                                reject(
                                    new Error(
                                        "Kolom Tahun tidak ditemukan pada CSV."
                                    )
                                );

                                return;

                            }

                            spatialPanelData =
                                results.data.filter(
                                    (row) =>
                                        row.Kab_kota
                                );

                            console.log(
                                "[PETA] Data CSV siap:",
                                spatialPanelData.length,
                                "baris"
                            );

                            resolve(
                                spatialPanelData
                            );

                        },

                    error:
                        (error) => {

                            console.error(
                                "[PETA] CSV ERROR:",
                                error
                            );

                            reject(
                                new Error(
                                    "CSV gagal dimuat: " +
                                    (
                                        error.message ||
                                        "kesalahan tidak diketahui"
                                    )
                                )
                            );

                        }

                }
            );

        }
    );

}


// LOAD MAPPING BPS → KODEKAB

function loadSpatialMapping() {

    return new Promise(
        (
            resolve,
            reject
        ) => {

            console.log(
                "[PETA] Memuat mapping:",
                SPATIAL_CONFIG.mappingPath
            );

            if (
                typeof Papa ===
                "undefined"
            ) {

                reject(
                    new Error(
                        "Papa Parse tidak ditemukan."
                    )
                );

                return;

            }

            Papa.parse(
                SPATIAL_CONFIG.mappingPath,
                {

                    download:
                        true,

                    header:
                        true,

                    skipEmptyLines:
                        true,

                    dynamicTyping:
                        false,

                    complete:
                        (results) => {

                            console.log(
                                "[PETA] Mapping berhasil dimuat."
                            );

                            console.log(
                                "[PETA] Jumlah mapping:",
                                results.data.length
                            );

                            console.log(
                                "[PETA] Kolom mapping:",
                                results.meta.fields
                            );

                            if (
                                !results.meta.fields ||
                                !results.meta.fields.includes(
                                    "Kab_kota"
                                )
                            ) {

                                reject(
                                    new Error(
                                        "Kolom Kab_kota tidak ditemukan pada mapping."
                                    )
                                );

                                return;

                            }

                            if (
                                !results.meta.fields.includes(
                                    "kodekab"
                                )
                            ) {

                                reject(
                                    new Error(
                                        "Kolom kodekab tidak ditemukan pada mapping."
                                    )
                                );

                                return;

                            }

                            spatialMappingData =
                                results.data.filter(
                                    (row) =>
                                        row.Kab_kota &&
                                        row.kodekab
                                );

                            console.log(
                                "[PETA] Mapping siap:",
                                spatialMappingData.length,
                                "kab/kota"
                            );

                            resolve(
                                spatialMappingData
                            );

                        },

                    error:
                        (error) => {

                            console.error(
                                "[PETA] MAPPING ERROR:",
                                error
                            );

                            reject(
                                new Error(
                                    "Mapping gagal dimuat: " +
                                    (
                                        error.message ||
                                        "kesalahan tidak diketahui"
                                    )
                                )
                            );

                        }

                }
            );

        }
    );

}


// LOAD GEOJSON

async function loadSpatialGeoJSON() {

    console.log(
        "[PETA] Memuat GeoJSON:",
        SPATIAL_CONFIG.geojsonPath
    );

    const response =
        await fetch(
            SPATIAL_CONFIG.geojsonPath
        );

    console.log(
        "[PETA] Status GeoJSON:",
        response.status,
        response.statusText
    );

    if (!response.ok) {

        throw new Error(
            "GeoJSON gagal dimuat. HTTP " +
            response.status +
            " " +
            response.statusText
        );

    }

    let geojson;

    try {

        geojson =
            await response.json();

    } catch (error) {

        throw new Error(
            "File GeoJSON ditemukan tetapi isinya bukan JSON yang valid."
        );

    }

    if (
        !geojson ||
        !geojson.features ||
        !Array.isArray(
            geojson.features
        )
    ) {

        throw new Error(
            "Struktur GeoJSON tidak valid. Property features tidak ditemukan."
        );

    }

    console.log(
        "[PETA] GeoJSON berhasil dimuat."
    );

    console.log(
        "[PETA] Jumlah polygon:",
        geojson.features.length
    );

    if (
        geojson.features.length === 0
    ) {

        throw new Error(
            "GeoJSON berhasil dibaca tetapi tidak memiliki polygon."
        );

    }

    if (
        geojson.features[0].properties
    ) {

        console.log(
            "[PETA] Contoh properties GeoJSON:",
            geojson.features[0].properties
        );

    }

    spatialGeojsonData =
        geojson;

    return spatialGeojsonData;

}


// VALIDASI JOIN

function validateSpatialJoin() {

    if (
        !spatialGeojsonData ||
        !spatialGeojsonData.features
    ) {

        return;

    }

    const geojsonCodes =
        new Set();

    spatialGeojsonData.features.forEach(
        (feature) => {

            const kodekab =
                getSpatialFeatureKodekab(
                    feature
                );

            if (kodekab) {

                geojsonCodes.add(
                    kodekab
                );

            }

        }
    );

    const mappingCodes =
        new Set();

    spatialMappingData.forEach(
        (row) => {

            const kodekab =
                String(
                    row.kodekab || ""
                )
                    .trim()
                    .replace(
                        /\.0$/,
                        ""
                    );

            if (kodekab) {

                mappingCodes.add(
                    kodekab
                );

            }

        }
    );

    let matched =
        0;

    spatialPanelData.forEach(
        (row) => {

            const kabKotaKey =
                spatialNormalizeText(
                    row.Kab_kota
                );

            const mapping =
                spatialMappingData.find(
                    (item) => {

                        return (
                            spatialNormalizeText(
                                item.Kab_kota
                            ) ===
                            kabKotaKey
                        );

                    }
                );

            if (!mapping) {
                return;
            }

            const kodekab =
                String(
                    mapping.kodekab || ""
                )
                    .trim()
                    .replace(
                        /\.0$/,
                        ""
                    );

            if (
                geojsonCodes.has(
                    kodekab
                )
            ) {

                matched++;

            }

        }
    );

    console.log(
        "[PETA] Validasi join"
    );

    console.log(
        "[PETA] Polygon GeoJSON:",
        geojsonCodes.size
    );

    console.log(
        "[PETA] Mapping kodekab:",
        mappingCodes.size
    );

    console.log(
        "[PETA] Baris BPS yang berhasil terhubung:",
        matched,
        "/",
        spatialPanelData.length
    );

}


// INISIALISASI MAP

async function setupSpatialMap() {

    const mapElement =
        document.querySelector(
            "#spatial-map"
        );

    if (!mapElement) {
        return;
    }

    const loading =
        document.querySelector(
            "#map-loading"
        );

    try {

        spatialMap =
            L.map(
                "spatial-map",
                {

                    zoomControl:
                        true,

                    scrollWheelZoom:
                        true

                }
            );

        spatialMap.setView(
            [
                -2.5,
                105.0
            ],
            5
        );

        L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            {

                maxZoom:
                    12,

                attribution:
                    "&copy; OpenStreetMap contributors"

            }
        ).addTo(
            spatialMap
        );

        await Promise.all(
            [

                loadSpatialCSV(),

                loadSpatialMapping(),

                loadSpatialGeoJSON()

            ]
        );

        validateSpatialJoin();

        renderSpatialGeoJSON();

        if (
            spatialGeojsonLayer &&
            spatialGeojsonLayer.getBounds().isValid()
        ) {

            spatialMap.fitBounds(
                spatialGeojsonLayer.getBounds(),
                {

                    padding:
                        [
                            20,
                            20
                        ]

                }
            );

        }

        if (loading) {

            loading.classList.add(
                "loaded"
            );

        }

    } catch (error) {

        console.error(
            "[PETA] Gagal memuat peta:",
            error
        );

        if (loading) {

            loading.innerHTML =
                "Peta belum dapat dimuat.<br><br>" +
                "<small>" +
                (
                    error.message ||
                    "Kesalahan tidak diketahui."
                ) +
                "</small>";

            loading.classList.remove(
                "loaded"
            );

        }

    }

}


// YEAR BUTTON

function setupSpatialYearButtons() {

    const buttons =
        document.querySelectorAll(
            ".year-button"
        );

    if (!buttons.length) {
        return;
    }

    buttons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                () => {

                    const year =
                        Number(
                            button.dataset.year
                        );

                    if (!year) {
                        return;
                    }

                    spatialCurrentYear =
                        year;

                    buttons.forEach(
                        (item) => {

                            item.classList.toggle(
                                "active",
                                item === button
                            );

                        }
                    );

                    updateSpatialMap();

                }
            );

        }
    );

}


// INDICATOR BUTTON

function setupSpatialIndicatorButtons() {

    const buttons =
        document.querySelectorAll(
            ".map-indicator-button"
        );

    if (!buttons.length) {
        return;
    }

    buttons.forEach(
        (button) => {

            button.addEventListener(
                "click",
                () => {

                    const indicator =
                        button.dataset.indicator;

                    if (!indicator) {
                        return;
                    }

                    spatialCurrentIndicator =
                        indicator;

                    buttons.forEach(
                        (item) => {

                            item.classList.toggle(
                                "active",
                                item === button
                            );

                        }
                    );

                    updateSpatialMap();

                }
            );

        }
    );

}


// SECTION 02 INITIALIZATION

function setupSpatialSection() {

    const spatialSection =
        document.querySelector(
            "#spatial"
        );

    if (!spatialSection) {
        return;
    }

    setupSpatialYearButtons();

    setupSpatialIndicatorButtons();

    setupSpatialMap();

}

// SECTION 03 — LANSIA × KESEJAHTERAAN
const WELFARE_CONFIG = {

    csvPath:
        "data/web_panel_2020_2024.csv",

    defaultYear:
        2024

};


let welfareData = [];

let welfareCurrentYear =
    WELFARE_CONFIG.defaultYear;

let welfareSvg = null;

let welfareXScale = null;

let welfareYScale = null;

let welfarePointSelection = null;

let welfareMedianX = null;

let welfareMedianY = null;


// WARNA TIPOLOGI

const WELFARE_COLORS = {

    "Tinggi-Tinggi":
        "#c2410c",

    "Tinggi-Rendah":
        "#7c3aed",

    "Rendah-Tinggi":
        "#f59e0b",

    "Rendah-Rendah":
        "#0f766e"

};


// FORMAT ANGKA

function welfareNumber(
    value,
    digits = 2
) {

    if (
        !Number.isFinite(value)
    ) {

        return "–";

    }

    return value.toLocaleString(
        "id-ID",
        {
            minimumFractionDigits:
                digits,

            maximumFractionDigits:
                digits
        }
    );

}


// HITUNG MEDIAN

function welfareMedian(
    values
) {

    const clean =
        values
            .filter(
                value =>
                    Number.isFinite(value)
            )
            .sort(
                (a, b) =>
                    a - b
            );

    if (!clean.length) {
        return NaN;
    }

    const middle =
        Math.floor(
            clean.length / 2
        );

    if (
        clean.length % 2 === 0
    ) {

        return (
            clean[middle - 1] +
            clean[middle]
        ) / 2;

    }

    return clean[middle];

}


// TIPOLOGI BERDASARKAN MEDIAN TAHUNAN

function welfareGetTypology(
    row,
    medianX,
    medianY
) {

    const x =
        Number(
            row.pct_lansia
        );

    const y =
        Number(
            row.p0_miskin
        );

    const lansiaHigh =
        x >= medianX;

    const miskinHigh =
        y >= medianY;

    if (
        lansiaHigh &&
        miskinHigh
    ) {

        return "Tinggi-Tinggi";

    }

    if (
        lansiaHigh &&
        !miskinHigh
    ) {

        return "Tinggi-Rendah";

    }

    if (
        !lansiaHigh &&
        miskinHigh
    ) {

        return "Rendah-Tinggi";

    }

    return "Rendah-Rendah";

}


// LOAD DATA SECTION 03

function loadWelfareData() {

    console.log(
        "[WELFARE] Memuat data:",
        WELFARE_CONFIG.csvPath
    );

    Papa.parse(
        WELFARE_CONFIG.csvPath,
        {

            download:
                true,

            header:
                true,

            skipEmptyLines:
                true,

            dynamicTyping:
                true,

            complete:
                function(results) {

                    welfareData =
                        results.data
                            .map(
                                row => ({

                                    ...row,

                                    Tahun:
                                        Number(
                                            row.Tahun
                                        ),

                                    pct_lansia:
                                        Number(
                                            row.pct_lansia
                                        ),

                                    p0_miskin:
                                        Number(
                                            row.p0_miskin
                                        ),

                                    rls:
                                        Number(
                                            row.rls
                                        ),

                                    pengeluaran:
                                        Number(
                                            row.pengeluaran
                                        )

                                })
                            )
                            .filter(
                                row =>
                                    Number.isFinite(
                                        row.Tahun
                                    ) &&
                                    Number.isFinite(
                                        row.pct_lansia
                                    ) &&
                                    Number.isFinite(
                                        row.p0_miskin
                                    )
                            );

                    console.log(
                        "[WELFARE] Data siap:",
                        welfareData.length,
                        "baris"
                    );

                    initWelfareScatter();

                },

            error:
                function(error) {

                    console.error(
                        "[WELFARE] Gagal memuat data:",
                        error
                    );

                    const loading =
                        document.getElementById(
                            "welfare-loading"
                        );

                    if (loading) {

                        loading.textContent =
                            "Data gagal dimuat.";

                    }

                }

        }
    );

}


// INISIALISASI SCATTERPLOT

function initWelfareScatter() {

    const container =
        document.getElementById(
            "welfare-scatter"
        );

    const loading =
        document.getElementById(
            "welfare-loading"
        );

    if (
        !container ||
        typeof d3 === "undefined"
    ) {

        console.warn(
            "[WELFARE] Container atau D3 tidak tersedia."
        );

        return;

    }

    const width =
        container.clientWidth;

    const height =
        container.clientHeight;

    const margin = {

        top:
            30,

        right:
            30,

        bottom:
            65,

        left:
            70

    };

    const innerWidth =
        width -
        margin.left -
        margin.right;

    const innerHeight =
        height -
        margin.top -
        margin.bottom;

    welfareSvg =
        d3
            .select(container)
            .append("svg")
            .attr(
                "viewBox",
                `0 0 ${width} ${height}`
            )
            .attr(
                "preserveAspectRatio",
                "xMidYMid meet"
            );

    const chart =
        welfareSvg
            .append("g")
            .attr(
                "transform",
                `translate(${margin.left},${margin.top})`
            );


    welfareXScale =
        d3
            .scaleLinear()
            .domain(
                [
                    0,
                    d3.max(
                        welfareData,
                        d =>
                            d.pct_lansia
                    ) * 1.05
                ]
            )
            .nice()
            .range(
                [
                    0,
                    innerWidth
                ]
            );


    welfareYScale =
        d3
            .scaleLinear()
            .domain(
                [
                    0,
                    d3.max(
                        welfareData,
                        d =>
                            d.p0_miskin
                    ) * 1.05
                ]
            )
            .nice()
            .range(
                [
                    innerHeight,
                    0
                ]
            );


    // GRID

    chart
        .append("g")
        .attr(
            "class",
            "grid welfare-grid-x"
        )
        .attr(
            "transform",
            `translate(0,${innerHeight})`
        )
        .call(
            d3
                .axisBottom(
                    welfareXScale
                )
                .tickSize(
                    -innerHeight
                )
                .tickFormat("")
        );

    chart
        .append("g")
        .attr(
            "class",
            "grid welfare-grid-y"
        )
        .call(
            d3
                .axisLeft(
                    welfareYScale
                )
                .tickSize(
                    -innerWidth
                )
                .tickFormat("")
        );


    // X AXIS

    chart
        .append("g")
        .attr(
            "class",
            "axis welfare-x-axis"
        )
        .attr(
            "transform",
            `translate(0,${innerHeight})`
        )
        .call(
            d3
                .axisBottom(
                    welfareXScale
                )
                .ticks(7)
                .tickFormat(
                    d => `${d}%`
                )
        );


    // Y AXIS

    chart
        .append("g")
        .attr(
            "class",
            "axis welfare-y-axis"
        )
        .call(
            d3
                .axisLeft(
                    welfareYScale
                )
                .ticks(7)
                .tickFormat(
                    d => `${d}%`
                )
        );


    // LABEL X

    chart
        .append("text")
        .attr(
            "class",
            "axis-label"
        )
        .attr(
            "x",
            innerWidth / 2
        )
        .attr(
            "y",
            innerHeight + 52
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .text(
            "Proporsi Lansia (%)"
        );


    // LABEL Y

    chart
        .append("text")
        .attr(
            "class",
            "axis-label"
        )
        .attr(
            "transform",
            "rotate(-90)"
        )
        .attr(
            "x",
            -innerHeight / 2
        )
        .attr(
            "y",
            -50
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .text(
            "Tingkat Kemiskinan (%)"
        );


    // GARIS MEDIAN

    chart
        .append("line")
        .attr(
            "class",
            "median-line welfare-median-x"
        );

    chart
        .append("line")
        .attr(
            "class",
            "median-line welfare-median-y"
        );

    chart
        .append("text")
        .attr(
            "class",
            "median-label welfare-median-x-label"
        );

    chart
        .append("text")
        .attr(
            "class",
            "median-label welfare-median-y-label"
        );


    // TOOLTIP

    const tooltip =
        d3
            .select(container)
            .append("div")
            .attr(
                "class",
                "welfare-tooltip"
            );


    // POINTS

    welfarePointSelection =
        chart
            .append("g")
            .attr(
                "class",
                "welfare-points"
            );


    // UPDATE TAHUN PERTAMA

    welfareUpdateYear(
        welfareCurrentYear,
        false,
        tooltip,
        container
    );


    if (loading) {

        loading.style.display =
            "none";

    }


    // BUTTON TAHUN

    document
        .querySelectorAll(
            ".welfare-year-button"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    function() {

                        const year =
                            Number(
                                this.dataset.year
                            );

                        document
                            .querySelectorAll(
                                ".welfare-year-button"
                            )
                            .forEach(
                                btn =>
                                    btn.classList.remove(
                                        "active"
                                    )
                            );

                        this.classList.add(
                            "active"
                        );

                        welfareUpdateYear(
                            year,
                            true,
                            tooltip,
                            container
                        );

                    }
                );

            }
        );


    // RESIZE

    window.addEventListener(
        "resize",
        welfareResize
    );

}


// UPDATE TAHUN

function welfareUpdateYear(
    year,
    animate = true,
    tooltip = null,
    container = null
) {

    welfareCurrentYear =
        year;

    const yearData =
        welfareData.filter(
            d =>
                d.Tahun ===
                year
        );

    if (!yearData.length) {
        return;
    }


    welfareMedianX =
        welfareMedian(
            yearData.map(
                d =>
                    d.pct_lansia
            )
        );

    welfareMedianY =
        welfareMedian(
            yearData.map(
                d =>
                    d.p0_miskin
            )
        );


    // UPDATE GARIS MEDIAN

    const medianXLine =
        welfareSvg
            .select(
                ".welfare-median-x"
            );

    const medianYLine =
        welfareSvg
            .select(
                ".welfare-median-y"
            );

    const xRange =
        welfareXScale.range();

    const yRange =
        welfareYScale.range();


    medianXLine
        .attr(
            "x1",
            welfareXScale(
                welfareMedianX
            )
        )
        .attr(
            "x2",
            welfareXScale(
                welfareMedianX
            )
        )
        .attr(
            "y1",
            yRange[1]
        )
        .attr(
            "y2",
            yRange[0]
        );


    medianYLine
        .attr(
            "x1",
            xRange[0]
        )
        .attr(
            "x2",
            xRange[1]
        )
        .attr(
            "y1",
            welfareYScale(
                welfareMedianY
            )
        )
        .attr(
            "y2",
            welfareYScale(
                welfareMedianY
            )
        );


    // LABEL MEDIAN

    welfareSvg
        .select(
            ".welfare-median-x-label"
        )
        .attr(
            "x",
            welfareXScale(
                welfareMedianX
            ) + 6
        )
        .attr(
            "y",
            16
        )
        .text(
            `Median lansia ${welfareNumber(
                welfareMedianX
            )}%`
        );


    welfareSvg
        .select(
            ".welfare-median-y-label"
        )
        .attr(
            "x",
            welfareXScale.range()[1] - 5
        )
        .attr(
            "y",
            welfareYScale(
                welfareMedianY
            ) - 7
        )
        .attr(
            "text-anchor",
            "end"
        )
        .text(
            `Median kemiskinan ${welfareNumber(
                welfareMedianY
            )}%`
        );


    // UPDATE POINT

    const points =
        welfarePointSelection
            .selectAll("circle")
            .data(
                yearData,
                d =>
                    `${d.Kab_kota}-${d.Tahun}`
            );


    points.join(

        enter =>
            enter
                .append("circle")
                .attr(
                    "class",
                    "welfare-point"
                )
                .attr(
                    "r",
                    animate ? 0 : 5
                )
                .attr(
                    "cx",
                    d =>
                        welfareXScale(
                            d.pct_lansia
                        )
                )
                .attr(
                    "cy",
                    d =>
                        welfareYScale(
                            d.p0_miskin
                        )
                )
                .attr(
                    "fill",
                    d =>
                        WELFARE_COLORS[
                            welfareGetTypology(
                                d,
                                welfareMedianX,
                                welfareMedianY
                            )
                        ]
                )
                .call(
                    selection => {

                        if (animate) {

                            selection
                                .transition()
                                .duration(500)
                                .attr(
                                    "r",
                                    5
                                );

                        }

                    }
                ),

        update => {

            if (animate) {

                return update
                    .transition()
                    .duration(650)
                    .attr(
                        "cx",
                        d =>
                            welfareXScale(
                                d.pct_lansia
                            )
                    )
                    .attr(
                        "cy",
                        d =>
                            welfareYScale(
                                d.p0_miskin
                            )
                    )
                    .attr(
                        "fill",
                        d =>
                            WELFARE_COLORS[
                                welfareGetTypology(
                                    d,
                                    welfareMedianX,
                                    welfareMedianY
                                )
                            ]
                    );

            }

            return update
                .attr(
                    "cx",
                    d =>
                        welfareXScale(
                            d.pct_lansia
                        )
                )
                .attr(
                    "cy",
                    d =>
                        welfareYScale(
                            d.p0_miskin
                        )
                )
                .attr(
                    "fill",
                    d =>
                        WELFARE_COLORS[
                            welfareGetTypology(
                                d,
                                welfareMedianX,
                                welfareMedianY
                            )
                        ]
                );

        },

        exit => {

            if (animate) {

                return exit
                    .transition()
                    .duration(350)
                    .attr(
                        "r",
                        0
                    )
                    .remove();

            }

            return exit.remove();

        }

    );


    // PASANG EVENT TOOLTIP

    const currentPoints =
        welfarePointSelection
            .selectAll("circle");


    currentPoints
        .on(
            "mouseenter",
            function(event, d) {

                if (!tooltip) {
                    return;
                }

                d3.select(this)
                    .raise()
                    .attr(
                        "r",
                        8
                    )
                    .style(
                        "opacity",
                        1
                    );

                const typology =
                    welfareGetTypology(
                        d,
                        welfareMedianX,
                        welfareMedianY
                    );

                tooltip
                    .style(
                        "display",
                        "block"
                    )
                    .html(`
                        <div class="welfare-tooltip-title">
                            ${d.Kab_kota || "Kab/Kota"}
                        </div>

                        <div class="welfare-tooltip-subtitle">
                            ${d.Provinsi || "–"} · ${d.Tahun}
                        </div>

                        <div class="welfare-tooltip-row">
                            <span>Proporsi lansia</span>
                            <span>${welfareNumber(
                                d.pct_lansia
                            )}%</span>
                        </div>

                        <div class="welfare-tooltip-row">
                            <span>Kemiskinan</span>
                            <span>${welfareNumber(
                                d.p0_miskin
                            )}%</span>
                        </div>

                        <div class="welfare-tooltip-row">
                            <span>RLS</span>
                            <span>${welfareNumber(
                                d.rls
                            )} tahun</span>
                        </div>

                        <div class="welfare-tooltip-row">
                            <span>Pengeluaran</span>
                            <span>
                                ${
                                    Number.isFinite(
                                        d.pengeluaran
                                    )
                                        ? "Rp " +
                                          welfareNumber(
                                              d.pengeluaran /
                                              1000
                                          ) +
                                          " juta"
                                        : "–"
                                }
                            </span>
                        </div>

                        <div class="welfare-tooltip-row">
                            <span>Tipologi</span>
                            <span>${typology}</span>
                        </div>
                    `);

            }
        )
        .on(
            "mousemove",
            function(event) {

                if (
                    !tooltip ||
                    !container
                ) {
                    return;
                }

                const bounds =
                    container.getBoundingClientRect();

                tooltip
                    .style(
                        "left",
                        `${event.clientX - bounds.left + 15}px`
                    )
                    .style(
                        "top",
                        `${event.clientY - bounds.top - 20}px`
                    );

            }
        )
        .on(
            "mouseleave",
            function() {

                if (!tooltip) {
                    return;
                }

                d3.select(this)
                    .attr(
                        "r",
                        5
                    )
                    .style(
                        "opacity",
                        null
                    );

                tooltip.style(
                    "display",
                    "none"
                );

            }
        );


    // UPDATE INSIGHT

    const insightTitle =
        document.getElementById(
            "welfare-insight-title"
        );

    const insightText =
        document.getElementById(
            "welfare-insight-text"
        );

    if (
        insightTitle &&
        insightText
    ) {

        insightTitle.textContent =
            `Pada ${year}, median proporsi lansia adalah ${welfareNumber(
                welfareMedianX
            )}%, sedangkan median kemiskinan ${welfareNumber(
                welfareMedianY
            )}%.`;

        insightText.textContent =
            "Titik yang berada di atas garis median kemiskinan menunjukkan wilayah dengan tingkat kemiskinan relatif lebih tinggi pada tahun tersebut. Sementara itu, posisi terhadap garis median lansia menunjukkan apakah proporsi lansia relatif tinggi atau rendah.";

    }

}


// RESPONSIVE SECTION 03

function welfareResize() {

    const container =
        document.getElementById(
            "welfare-scatter"
        );

    if (
        !container ||
        !welfareSvg
    ) {

        return;

    }

    const width =
        container.clientWidth;

    const height =
        container.clientHeight;

    welfareSvg
        .attr(
            "viewBox",
            `0 0 ${width} ${height}`
        );

}


// INITIALIZATION

document.addEventListener(
    "DOMContentLoaded",
    () => {

        setupScrollReveal();

        setupCounters();

        setupIndicatorAnimation();

        setupOpeningReplay();

        setupOpeningScroll();
        setupBackToTop();
        setupSpatialSection();
        setupStoryNavigation();
        setupStoryNavigationObserver();

        if (
            document.getElementById(
                "welfare-scatter"
            )
        ) {

            loadWelfareData();

        }

    }
);
// SECTION 04 — DINAMIKA 2020–2024

const DYNAMICS_CONFIG = {
    csvPath: "data/web_panel_2020_2024.csv"
};

let dynamicsData = [];

let dynamicsSvg = null;

let dynamicsXScale = null;

let dynamicsYScale = null;


function loadDynamicsData() {

    const container =
        document.getElementById(
            "dynamics-scatter"
        );

    if (
        !container ||
        typeof d3 === "undefined"
    ) {
        return;
    }

    Papa.parse(
        DYNAMICS_CONFIG.csvPath,
        {
            download: true,
            header: true,
            skipEmptyLines: true,
            dynamicTyping: true,

            complete: function(results) {

                dynamicsData =
                    results.data
                        .filter(
                            row =>
                                row.Kab_kota &&
                                Number.isFinite(
                                    Number(row.Tahun)
                                ) &&
                                Number.isFinite(
                                    Number(row.pct_lansia)
                                )
                        )
                        .map(
                            row => ({
                                ...row,

                                Tahun:
                                    Number(
                                        row.Tahun
                                    ),

                                pct_lansia:
                                    Number(
                                        row.pct_lansia
                                    )
                            })
                        );

                initDynamicsScatter();

            },

            error: function(error) {

                console.error(
                    "[DYNAMICS] Gagal memuat data:",
                    error
                );

                const loading =
                    document.getElementById(
                        "dynamics-loading"
                    );

                if (loading) {

                    loading.textContent =
                        "Data gagal dimuat.";

                }

            }
        }
    );

}


function initDynamicsScatter() {

    const container =
        document.getElementById(
            "dynamics-scatter"
        );

    const loading =
        document.getElementById(
            "dynamics-loading"
        );

    if (!container) {
        return;
    }

    const width =
        container.clientWidth;

    const height =
        container.clientHeight;

    const margin = {
        top: 30,
        right: 35,
        bottom: 65,
        left: 70
    };

    const innerWidth =
        width -
        margin.left -
        margin.right;

    const innerHeight =
        height -
        margin.top -
        margin.bottom;


    dynamicsSvg =
        d3
            .select(container)
            .append("svg")
            .attr(
                "viewBox",
                `0 0 ${width} ${height}`
            )
            .attr(
                "preserveAspectRatio",
                "xMidYMid meet"
            );


    const chart =
        dynamicsSvg
            .append("g")
            .attr(
                "transform",
                `translate(${margin.left},${margin.top})`
            );


    const data2020 =
        dynamicsData.filter(
            d =>
                d.Tahun === 2020
        );

    const data2024 =
        dynamicsData.filter(
            d =>
                d.Tahun === 2024
        );


    const dataMap2024 =
        new Map(
            data2024.map(
                d => [
                    d.Kab_kota,
                    d
                ]
            )
        );


    const pairedData =
        data2020
            .map(
                start => {

                    const end =
                        dataMap2024.get(
                            start.Kab_kota
                        );

                    if (!end) {
                        return null;
                    }

                    return {
                        Kab_kota:
                            start.Kab_kota,

                        Provinsi:
                            start.Provinsi,

                        start:
                            start.pct_lansia,

                        end:
                            end.pct_lansia
                    };

                }
            )
            .filter(
                d => d !== null
            );


    const allValues =
        pairedData.flatMap(
            d => [
                d.start,
                d.end
            ]
        );


    const minValue =
        Math.min(
            ...allValues
        );

    const maxValue =
        Math.max(
            ...allValues
        );


    dynamicsXScale =
        d3
            .scaleLinear()
            .domain(
                [
                    minValue - 0.5,
                    maxValue + 0.5
                ]
            )
            .nice()
            .range(
                [
                    0,
                    innerWidth
                ]
            );


    dynamicsYScale =
        d3
            .scaleLinear()
            .domain(
                [
                    minValue - 0.5,
                    maxValue + 0.5
                ]
            )
            .nice()
            .range(
                [
                    innerHeight,
                    0
                ]
            );


    // GRID

    chart
        .append("g")
        .attr(
            "class",
            "dynamics-grid"
        )
        .attr(
            "transform",
            `translate(0,${innerHeight})`
        )
        .call(
            d3
                .axisBottom(
                    dynamicsXScale
                )
                .tickSize(
                    -innerHeight
                )
                .tickFormat("")
        );


    chart
        .append("g")
        .attr(
            "class",
            "dynamics-grid"
        )
        .call(
            d3
                .axisLeft(
                    dynamicsYScale
                )
                .tickSize(
                    -innerWidth
                )
                .tickFormat("")
        );


    // AXIS

    chart
        .append("g")
        .attr(
            "class",
            "dynamics-axis"
        )
        .attr(
            "transform",
            `translate(0,${innerHeight})`
        )
        .call(
            d3
                .axisBottom(
                    dynamicsXScale
                )
                .ticks(7)
                .tickFormat(
                    d => `${d}%`
                )
        );


    chart
        .append("g")
        .attr(
            "class",
            "dynamics-axis"
        )
        .call(
            d3
                .axisLeft(
                    dynamicsYScale
                )
                .ticks(7)
                .tickFormat(
                    d => `${d}%`
                )
        );


    // LABEL X

    chart
        .append("text")
        .attr(
            "class",
            "dynamics-axis-label"
        )
        .attr(
            "x",
            innerWidth / 2
        )
        .attr(
            "y",
            innerHeight + 50
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .text(
            "Proporsi Lansia 2020 (%)"
        );


    // LABEL Y

    chart
        .append("text")
        .attr(
            "class",
            "dynamics-axis-label"
        )
        .attr(
            "transform",
            "rotate(-90)"
        )
        .attr(
            "x",
            -innerHeight / 2
        )
        .attr(
            "y",
            -50
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .text(
            "Proporsi Lansia 2024 (%)"
        );


    // DIAGONAL

    chart
        .append("line")
        .attr(
            "class",
            "dynamics-connection"
        )
        .attr(
            "x1",
            dynamicsXScale(
                minValue
            )
        )
        .attr(
            "y1",
            dynamicsYScale(
                minValue
            )
        )
        .attr(
            "x2",
            dynamicsXScale(
                maxValue
            )
        )
        .attr(
            "y2",
            dynamicsYScale(
                maxValue
            )
        )
        .style(
            "stroke-dasharray",
            "5 5"
        )
        .style(
            "opacity",
            0.2
        );


    // CONNECTION

    chart
        .selectAll(
            ".dynamics-change-line"
        )
        .data(
            pairedData
        )
        .join("line")
        .attr(
            "class",
            "dynamics-connection"
        )
        .attr(
            "x1",
            d =>
                dynamicsXScale(
                    d.start
                )
        )
        .attr(
            "y1",
            d =>
                dynamicsYScale(
                    d.start
                )
        )
        .attr(
            "x2",
            d =>
                dynamicsXScale(
                    d.end
                )
        )
        .attr(
            "y2",
            d =>
                dynamicsYScale(
                    d.end
                )
        );


    // START POINT

    chart
        .selectAll(
            ".dynamics-start-point"
        )
        .data(
            pairedData
        )
        .join("circle")
        .attr(
            "class",
            "dynamics-start-point"
        )
        .attr(
            "r",
            4
        )
        .attr(
            "cx",
            d =>
                dynamicsXScale(
                    d.start
                )
        )
        .attr(
            "cy",
            d =>
                dynamicsYScale(
                    d.start
                )
        );


    // END POINT

    chart
        .selectAll(
            ".dynamics-end-point"
        )
        .data(
            pairedData
        )
        .join("circle")
        .attr(
            "class",
            "dynamics-end-point"
        )
        .attr(
            "r",
            5
        )
        .attr(
            "cx",
            d =>
                dynamicsXScale(
                    d.end
                )
        )
        .attr(
            "cy",
            d =>
                dynamicsYScale(
                    d.end
                )
        )
        .on(
            "mouseenter",
            function(event, d) {

                d3.select(this)
                    .attr(
                        "r",
                        8
                    );

                const tooltip =
                    d3
                        .select(container)
                        .append("div")
                        .attr(
                            "class",
                            "welfare-tooltip dynamics-temp-tooltip"
                        )
                        .style(
                            "display",
                            "block"
                        )
                        .html(`
                            <div class="welfare-tooltip-title">
                                ${d.Kab_kota}
                            </div>

                            <div class="welfare-tooltip-subtitle">
                                ${d.Provinsi || "–"}
                            </div>

                            <div class="welfare-tooltip-row">
                                <span>2020</span>
                                <span>${welfareNumber(
                                    d.start
                                )}%</span>
                            </div>

                            <div class="welfare-tooltip-row">
                                <span>2024</span>
                                <span>${welfareNumber(
                                    d.end
                                )}%</span>
                            </div>

                            <div class="welfare-tooltip-row">
                                <span>Perubahan</span>
                                <span>${welfareNumber(
                                    d.end - d.start
                                )} poin</span>
                            </div>
                        `);


                const bounds =
                    container.getBoundingClientRect();

                tooltip
                    .style(
                        "left",
                        `${event.clientX - bounds.left + 15}px`
                    )
                    .style(
                        "top",
                        `${event.clientY - bounds.top - 20}px`
                    );

            }
        )
        .on(
            "mousemove",
            function(event) {

                const tooltip =
                    container.querySelector(
                        ".dynamics-temp-tooltip"
                    );

                if (!tooltip) {
                    return;
                }

                const bounds =
                    container.getBoundingClientRect();

                tooltip.style.left =
                    `${event.clientX - bounds.left + 15}px`;

                tooltip.style.top =
                    `${event.clientY - bounds.top - 20}px`;

            }
        )
        .on(
            "mouseleave",
            function() {

                d3.select(this)
                    .attr(
                        "r",
                        5
                    );

                const tooltip =
                    container.querySelector(
                        ".dynamics-temp-tooltip"
                    );

                if (tooltip) {
                    tooltip.remove();
                }

            }
        );


    // INSIGHT

    const changes =
        pairedData.map(
            d =>
                d.end - d.start
        );


    const averageChange =
        d3.mean(
            changes
        );


    const increased =
        changes.filter(
            d =>
                d > 0
        ).length;


    const decreased =
        changes.filter(
            d =>
                d < 0
        ).length;


    const unchanged =
        changes.filter(
            d =>
                d === 0
        ).length;


    const title =
        document.getElementById(
            "dynamics-insight-title"
        );

    const text =
        document.getElementById(
            "dynamics-insight-text"
        );


    if (title) {

    title.textContent =
        "Seluruh kabupaten/kota mengalami peningkatan proporsi lansia.";
    }

    if (text) {

        text.textContent =
            `Rata-rata proporsi lansia bertambah ${welfareNumber(
                averageChange
            )} poin persentase antara 2020 dan 2024. Namun, besar perubahan berbeda antarwilayah, menunjukkan bahwa proses penuaan penduduk berlangsung dengan intensitas yang tidak seragam.`;

    }


        if (loading) {

            loading.style.display =
                "none";

        }

    }
document.addEventListener(
    "DOMContentLoaded",
    () => {

        if (
            document.getElementById(
                "dynamics-scatter"
            )
        ) {

            loadDynamicsData();

        }

    }
);

/* SECTION 05 — STRUKTUR HIERARKI WILAYAH */

const HIERARCHY_CONFIG = {
    csvPath: "data/web_panel_2020_2024.csv",
    year: 2024
};

let hierarchyData = [];
let hierarchyRoot = null;
let hierarchyCurrentNode = null;
let hierarchyColorScale = null;

async function loadHierarchyData() {

    const treemapContainer =
        document.getElementById("hierarchy-treemap");

    const sunburstContainer =
        document.getElementById("hierarchy-sunburst");

    if (!treemapContainer || !sunburstContainer) {
        return;
    }

    try {

        const rows = await d3.csv(
            HIERARCHY_CONFIG.csvPath
        );

        hierarchyData = rows
            .filter(d =>
                +d.Tahun === HIERARCHY_CONFIG.year &&
                d.Kab_kota &&
                d.Provinsi
            )
            .map(d => ({
                kabkota: d.Kab_kota,
                provinsi: d.Provinsi,
                pulau: normalizeIsland(d.Provinsi),
                penduduk: +d.jumlah_penduduk || 0,
                pctLansia: +d.pct_lansia || 0
            }))
            .filter(d =>
                d.pulau &&
                d.penduduk > 0
            );

        if (!hierarchyData.length) {
            throw new Error(
                "Data hierarki tidak ditemukan."
            );
        }

        hierarchyRoot =
            buildHierarchyTree(hierarchyData);

        hierarchyCurrentNode =
            hierarchyRoot;

        const minLansia =
            d3.min(
                hierarchyData,
                d => d.pctLansia
            );

        const maxLansia =
            d3.max(
                hierarchyData,
                d => d.pctLansia
            );

        hierarchyColorScale =
            d3.scaleSequential()
                .domain([
                    minLansia,
                    maxLansia
                ])
                .interpolator(
                    d3.interpolateRgb(
                        "#d9d9e8",
                        "#54278f"
                    )
                );

        renderHierarchy();

    } catch (error) {

        console.error(
            "Gagal memuat Section 05:",
            error
        );

        treemapContainer.innerHTML =
            "<p>Visualisasi hierarki tidak dapat dimuat.</p>";

        sunburstContainer.innerHTML =
            "<p>Visualisasi hierarki tidak dapat dimuat.</p>";
    }
}

function normalizeIsland(province) {

    const name =
        String(province)
            .toLowerCase()
            .trim();

    const sumatra = [
        "aceh",
        "sumatera utara",
        "sumatera barat",
        "riau",
        "jambi",
        "sumatera selatan",
        "bengkulu",
        "lampung",
        "kepulauan bangka belitung",
        "kepulauan riau"
    ];

    const java = [
        "dki jakarta",
        "jawa barat",
        "jawa tengah",
        "di yogyakarta",
        "jawa timur",
        "banten"
    ];

    if (sumatra.includes(name)) {
        return "Sumatera";
    }

    if (java.includes(name)) {
        return "Jawa";
    }

    return null;
}
function buildHierarchyTree(rows) {

    const root = {
        name: "Jawa & Sumatera",
        type: "root",
        children: []
    };

    const islandNames = [
        "Jawa",
        "Sumatera"
    ];

    islandNames.forEach(
        islandName => {

            const islandRows =
                rows.filter(
                    d => d.pulau === islandName
                );

            const islandNode = {
                name: islandName,
                type: "island",
                children: [],
                parent: root
            };

            const provinces =
                d3.group(
                    islandRows,
                    d => d.provinsi
                );

            provinces.forEach(
                (provinceRows, provinceName) => {

                    const provinceNode = {
                        name: provinceName,
                        type: "province",
                        children: [],
                        parent: islandNode
                    };

                    provinceRows.forEach(d => {

                        provinceNode.children.push({
                            name: d.kabkota,
                            type: "kabkota",
                            value: d.penduduk,
                            pctLansia: d.pctLansia,
                            provinsi: d.provinsi,
                            pulau: d.pulau,
                            parent: provinceNode
                        });

                    });

                    islandNode.children.push(
                        provinceNode
                    );
                }
            );

            root.children.push(
                islandNode
            );
        }
    );

    return root;
}
function hierarchyNodeValue(node) {

    if (
        node.value !== undefined
    ) {
        return node.value;
    }

    if (
        !node.children ||
        !node.children.length
    ) {
        return 0;
    }

    return d3.sum(
        node.children,
        child =>
            hierarchyNodeValue(child)
    );
}

function hierarchyNodePctLansia(node) {

    if (
        node.pctLansia !== undefined
    ) {
        return node.pctLansia;
    }

    if (
        !node.children ||
        !node.children.length
    ) {
        return 0;
    }

    const total =
        hierarchyNodeValue(node);

    if (!total) {
        return 0;
    }

    return d3.sum(
        node.children,
        child =>
            hierarchyNodePctLansia(child) *
            hierarchyNodeValue(child)
    ) / total;
}

function renderHierarchy() {
    renderHierarchyBreadcrumb();
    renderHierarchyTreemap();
    renderHierarchySunburst();
    updateHierarchyInsight();
}

function renderHierarchyBreadcrumb() {

    const container =
        document.getElementById(
            "hierarchy-breadcrumb"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const path =
        getHierarchyPath(
            hierarchyCurrentNode
        );

    path.forEach(
        (node, index) => {

            const button =
                document.createElement(
                    "button"
                );

            button.type = "button";

            button.className =
                "hierarchy-breadcrumb-button" +
                (
                    index === path.length - 1
                        ? " active"
                        : ""
                );

            button.textContent =
                node.name;

            button.addEventListener(
                "click",
                () => {

                    hierarchyCurrentNode =
                        node;

                    renderHierarchy();

                }
            );

            container.appendChild(
                button
            );

            if (
                index <
                path.length - 1
            ) {

                const separator =
                    document.createElement(
                        "span"
                    );

                separator.textContent =
                    "›";

                separator.style.color =
                    "var(--text-muted)";

                container.appendChild(
                    separator
                );
            }
        }
    );
}

function getHierarchyPath(node) {

    const path = [];

    let current =
        node;

    while (current) {

        path.unshift(
            current
        );

        current =
            current.parent;
    }

    return path;
}

function renderHierarchyTreemap() {

    const container =
        document.getElementById(
            "hierarchy-treemap"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const width =
        container.clientWidth || 700;

    const height =
        window.innerWidth <= 600
            ? 340
            : window.innerWidth <= 900
                ? 420
                : 470;

    const current =
        hierarchyCurrentNode;

    const children =
        current.children || [];

    if (!children.length) {

        renderHierarchyTreemapLeaf(
            container,
            current,
            width,
            height
        );

        return;
    }

    const treemapData = {
        name: current.name,
        children: children.map(
            child => ({
                name: child.name,
                type: child.type,
                value:
                    hierarchyNodeValue(
                        child
                    ),
                pctLansia:
                    hierarchyNodePctLansia(
                        child
                    ),
                originalNode:
                    child
            })
        )
    };

    const root =
        d3.hierarchy(
            treemapData
        )
            .sum(
                d => d.value || 0
            )
            .sort(
                (a, b) =>
                    b.value - a.value
            );

    d3.treemap()
        .size([
            width,
            height
        ])
        .paddingOuter(5)
        .paddingInner(3)
        .round(true)(
            root
        );

    const svg =
        d3.select(container)
            .append("svg")
            .attr(
                "viewBox",
                `0 0 ${width} ${height}`
            )
            .attr(
                "role",
                "img"
            )
            .attr(
                "aria-label",
                `Struktur ${current.name}`
            );

    const groups =
        svg.selectAll(
            ".hierarchy-treemap-group"
        )
            .data(
                root.children || []
            )
            .join("g")
            .attr(
                "class",
                "hierarchy-treemap-group"
            )
            .attr(
                "transform",
                d =>
                    `translate(${d.x0},${d.y0})`
            );

    groups.append("rect")
        .attr(
            "class",
            "hierarchy-treemap-rect"
        )
        .attr(
            "width",
            d =>
                Math.max(
                    0,
                    d.x1 - d.x0
                )
        )
        .attr(
            "height",
            d =>
                Math.max(
                    0,
                    d.y1 - d.y0
                )
        )
        .attr(
            "fill",
            d =>
                hierarchyColorScale(
                    d.data.pctLansia
                )
        )
        .on(
            "click",
            function(event, d) {

                hierarchyCurrentNode =
                    d.data.originalNode;

                renderHierarchy();

            }
        )
        .on(
            "mouseenter",
            function(event, d) {

                showHierarchyTooltip(
                    event,
                    d.data.originalNode
                );

            }
        )
        .on(
            "mousemove",
            function(event) {

                moveHierarchyTooltip(
                    event
                );

            }
        )
        .on(
            "mouseleave",
            function() {

                hideHierarchyTooltip();

            }
        );

    groups.append("text")
        .attr(
            "class",
            "hierarchy-treemap-label"
        )
        .attr(
            "x",
            7
        )
        .attr(
            "y",
            17
        )
        .style(
            "display",
            d =>
                d.x1 - d.x0 > 75 &&
                d.y1 - d.y0 > 35
                    ? null
                    : "none"
        )
        .text(
            d =>
                d.data.name
        );

    groups.append("text")
        .attr(
            "class",
            "hierarchy-treemap-value"
        )
        .attr(
            "x",
            7
        )
        .attr(
            "y",
            32
        )
        .style(
            "display",
            d =>
                d.x1 - d.x0 > 100 &&
                d.y1 - d.y0 > 52
                    ? null
                    : "none"
        )
        .text(
            d =>
                `${d3.format(",.3s")(
                    d.data.value
                )} jiwa`
        );
}

function renderHierarchyTreemapLeaf(
    container,
    node,
    width,
    height
) {

    const svg =
        d3.select(container)
            .append("svg")
            .attr(
                "viewBox",
                `0 0 ${width} ${height}`
            );

    svg.append("rect")
        .attr(
            "x",
            5
        )
        .attr(
            "y",
            5
        )
        .attr(
            "width",
            width - 10
        )
        .attr(
            "height",
            height - 10
        )
        .attr(
            "rx",
            6
        )
        .attr(
            "fill",
            hierarchyColorScale(
                node.pctLansia
            )
        );

    svg.append("text")
        .attr(
            "x",
            width / 2
        )
        .attr(
            "y",
            height / 2 - 10
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .attr(
            "class",
            "hierarchy-treemap-label"
        )
        .text(
            node.name
        );

    svg.append("text")
        .attr(
            "x",
            width / 2
        )
        .attr(
            "y",
            height / 2 + 12
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .attr(
            "class",
            "hierarchy-treemap-value"
        )
        .text(
            `${welfareNumber(
                node.pctLansia
            )}% lansia`
        );
}

function renderHierarchySunburst() {

    const container =
        document.getElementById(
            "hierarchy-sunburst"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const width =
        container.clientWidth || 420;

    const height =
        window.innerWidth <= 600
            ? 340
            : window.innerWidth <= 900
                ? 420
                : 470;

    const radius =
        Math.min(
            width,
            height
        ) / 2 - 8;

    const root =
        d3.hierarchy(
            hierarchyCurrentNode
        )
            .sum(
                d =>
                    d.children
                        ? 0
                        : d.value || 0
            )
            .sort(
                (a, b) =>
                    b.value - a.value
            );

    d3.partition()
        .size([
            2 * Math.PI,
            radius
        ])(
            root
        );

    const svg =
        d3.select(container)
            .append("svg")
            .attr(
                "viewBox",
                `0 0 ${width} ${height}`
            )
            .attr(
                "role",
                "img"
            )
            .attr(
                "aria-label",
                "Sunburst hierarki wilayah"
            );

    const group =
        svg.append("g")
            .attr(
                "transform",
                `translate(
                    ${width / 2},
                    ${height / 2}
                )`
            );

    const arc =
        d3.arc()
            .startAngle(
                d => d.x0
            )
            .endAngle(
                d => d.x1
            )
            .innerRadius(
                d => d.y0
            )
            .outerRadius(
                d => d.y1
            )
            .padAngle(0.008)
            .padRadius(radius);

    const nodes =
        root.descendants()
            .filter(
                d => d.depth > 0
            );

    group.selectAll(
        ".hierarchy-sunburst-path"
    )
        .data(nodes)
        .join("path")
        .attr(
            "class",
            "hierarchy-sunburst-path"
        )
        .attr(
            "d",
            arc
        )
        .attr(
            "fill",
            d =>
                hierarchyColorScale(
                    hierarchyNodePctLansia(
                        d.data
                    )
                )
        )
        .on(
            "click",
            function(event, d) {

                if (
                    d.data.children &&
                    d.data.children.length
                ) {

                    hierarchyCurrentNode =
                        d.data;

                    renderHierarchy();

                }

            }
        )
        .on(
            "mouseenter",
            function(event, d) {

                showHierarchyTooltip(
                    event,
                    d.data
                );

            }
        )
        .on(
            "mousemove",
            function(event) {

                moveHierarchyTooltip(
                    event
                );

            }
        )
        .on(
            "mouseleave",
            function() {

                hideHierarchyTooltip();

            }
        );

    const center =
        group.append("g")
            .attr(
                "class",
                "hierarchy-center-label"
            );

    center.append("text")
        .attr(
            "class",
            "hierarchy-center-title"
        )
        .attr(
            "y",
            -5
        )
        .text(
            hierarchyCurrentNode.name
        );

    center.append("text")
        .attr(
            "class",
            "hierarchy-center-value"
        )
        .attr(
            "y",
            13
        )
        .text(
            `${d3.format(",.3s")(
                hierarchyNodeValue(
                    hierarchyCurrentNode
                )
            )} jiwa`
        );
}

function updateHierarchyInsight() {

    const title =
        document.getElementById(
            "hierarchy-insight-title"
        );

    const text =
        document.getElementById(
            "hierarchy-insight-text"
        );

    if (!title || !text) {
        return;
    }

    const node =
        hierarchyCurrentNode;

    const value =
        hierarchyNodeValue(node);

    const pct =
        hierarchyNodePctLansia(node);

    if (
        node.type === "root"
    ) {

        title.textContent =
            "Mulai dari pulau, lalu telusuri struktur wilayah di bawahnya.";

        text.textContent =
            `Pada 2024, ${hierarchyData.length} kabupaten/kota membentuk dua struktur wilayah utama: Jawa dan Sumatera. Klik salah satu pulau untuk melihat provinsi yang membentuknya.`;

        return;
    }

    if (
        node.type === "island"
    ) {

        title.textContent =
            `${node.name} → provinsi → kabupaten/kota.`;

        text.textContent =
            `${node.name} terdiri dari ${node.children.length} provinsi dengan sekitar ${d3.format(",.3s")(
                value
            )} penduduk. Klik salah satu provinsi untuk melihat kabupaten/kota di dalamnya.`;

        return;
    }

    if (
        node.type === "province"
    ) {

        title.textContent =
            `${node.name} → ${node.children.length} kabupaten/kota.`;

        text.textContent =
            `Sekitar ${d3.format(",.3s")(
                value
            )} penduduk berada di ${node.name}, dengan proporsi lansia tertimbang sekitar ${welfareNumber(
                pct
            )}%. Klik kabupaten/kota untuk melihat karakteristiknya.`;

        return;
    }

    title.textContent =
        node.name;

    text.textContent =
        `${node.name} memiliki sekitar ${d3.format(",.3s")(
            value
        )} penduduk, dengan proporsi lansia sebesar ${welfareNumber(
            pct
        )}%.`;
}

function getHierarchyTooltip() {

    let tooltip =
        document.getElementById(
            "hierarchy-tooltip"
        );

    if (tooltip) {
        return tooltip;
    }

    tooltip =
        document.createElement(
            "div"
        );

    tooltip.id =
        "hierarchy-tooltip";

    tooltip.className =
        "hierarchy-tooltip";

    tooltip.style.display =
        "none";

    document.body.appendChild(
        tooltip
    );

    return tooltip;
}

function showHierarchyTooltip(
    event,
    node
) {

    const tooltip =
        getHierarchyTooltip();

    tooltip.innerHTML = `
        <div class="hierarchy-tooltip-title">
            ${escapeHierarchyHtml(
                node.name
            )}
        </div>

        <div class="hierarchy-tooltip-value">
            Penduduk:
            ${d3.format(",")(
                hierarchyNodeValue(node)
            )} jiwa
        </div>

        <div class="hierarchy-tooltip-value">
            Proporsi lansia:
            ${welfareNumber(
                hierarchyNodePctLansia(node)
            )}%
        </div>
    `;

    tooltip.style.display =
        "block";

    moveHierarchyTooltip(
        event
    );
}

function moveHierarchyTooltip(
    event
) {

    const tooltip =
        document.getElementById(
            "hierarchy-tooltip"
        );

    if (!tooltip) {
        return;
    }

    tooltip.style.left =
        `${event.pageX + 14}px`;

    tooltip.style.top =
        `${event.pageY + 14}px`;
}

function hideHierarchyTooltip() {

    const tooltip =
        document.getElementById(
            "hierarchy-tooltip"
        );

    if (tooltip) {
        tooltip.style.display =
            "none";
    }
}

function escapeHierarchyHtml(
    value
) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}

function initHierarchy() {

    const section =
        document.getElementById(
            "hierarchy"
        );

    if (!section) {
        return;
    }

    loadHierarchyData();
}

let hierarchyResizeTimer = null;

window.addEventListener(
    "resize",
    () => {

        if (
            !hierarchyCurrentNode
        ) {
            return;
        }

        clearTimeout(
            hierarchyResizeTimer
        );

        hierarchyResizeTimer =
            setTimeout(
                () => {

                    renderHierarchy();

                },
                150
            );
    }
);

if (
    document.readyState ===
    "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        initHierarchy,
        {
            once: true
        }
    );

} else {

    initHierarchy();

}
// SECTION 06 — POLA MULTIVARIAT

const MULTIVARIATE_CONFIG = {
    multivariatePath: "data/web_multivariate_2024.csv",
    pcaPath: "data/web_pca_scores_2024.csv",
    umapPath: "data/web_umap_2024.csv"
};

let multivariateData = [];
let multivariatePcaData = [];
let multivariateUmapData = [];

let multivariateSelectedId = null;

const MULTIVARIATE_VARIABLES = [
    "jumlah_penduduk",
    "jumlah_lansia",
    "pct_lansia",
    "pct_anak",
    "rls",
    "pengeluaran",
    "ahh_rata2",
    "delta_pct_lansia"
];

function multivariateFindColumn(row, candidates) {

    const keys = Object.keys(row);

    for (const candidate of candidates) {

        const exact =
            keys.find(
                key => key.toLowerCase() === candidate.toLowerCase()
            );

        if (exact) {
            return exact;
        }
    }

    return null;
}

function multivariateGetId(row) {

    const column =
        multivariateFindColumn(
            row,
            [
                "Kab_kota",
                "kab_kota",
                "kabkota",
                "KabKota"
            ]
        );

    return column ? row[column] : "";
}

function multivariateGetProvince(row) {

    const column =
        multivariateFindColumn(
            row,
            [
                "Provinsi",
                "provinsi"
            ]
        );

    return column ? row[column] : "";
}

function multivariateGetNumeric(row, variable) {

    const column =
        multivariateFindColumn(
            row,
            [variable]
        );

    if (!column) {
        return 0;
    }

    const value =
        String(row[column])
            .replace(/,/g, "");

    const number =
        Number(value);

    return Number.isFinite(number)
        ? number
        : 0;
}

function multivariateNormalizeVariable(variable) {

    const values =
        multivariateData
            .map(d => d[variable])
            .filter(Number.isFinite);

    const min =
        d3.min(values);

    const max =
        d3.max(values);

    if (
        !Number.isFinite(min) ||
        !Number.isFinite(max) ||
        max === min
    ) {
        return () => 0.5;
    }

    return value =>
        (value - min) /
        (max - min);
}

async function loadMultivariateData() {

    const pcaContainer =
        document.getElementById("multivariate-pca");

    const umapContainer =
        document.getElementById("multivariate-umap");

    const parallelContainer =
        document.getElementById("multivariate-parallel");

    if (
        !pcaContainer ||
        !umapContainer ||
        !parallelContainer
    ) {
        return;
    }

    try {

        const [
            multivariateRows,
            pcaRows,
            umapRows
        ] = await Promise.all([
            d3.csv(
                MULTIVARIATE_CONFIG.multivariatePath
            ),
            d3.csv(
                MULTIVARIATE_CONFIG.pcaPath
            ),
            d3.csv(
                MULTIVARIATE_CONFIG.umapPath
            )
        ]);

        multivariateData =
            multivariateRows
                .map(row => {

                    const id =
                        multivariateGetId(row);

                    if (!id) {
                        return null;
                    }

                    const item = {
                        id: id,
                        provinsi:
                            multivariateGetProvince(row)
                    };

                    MULTIVARIATE_VARIABLES.forEach(
                        variable => {

                            item[variable] =
                                multivariateGetNumeric(
                                    row,
                                    variable
                                );
                        }
                    );

                    return item;

                })
                .filter(Boolean);

        multivariatePcaData =
            pcaRows
                .map(row => {

                    const id =
                        multivariateGetId(row);

                    const pc1Column =
                        multivariateFindColumn(
                            row,
                            [
                                "PC1",
                                "pc1"
                            ]
                        );

                    const pc2Column =
                        multivariateFindColumn(
                            row,
                            [
                                "PC2",
                                "pc2"
                            ]
                        );

                    const pc3Column =
                        multivariateFindColumn(
                            row,
                            [
                                "PC3",
                                "pc3"
                            ]
                        );

                    return {
                        id: id,
                        pc1:
                            Number(
                                row[pc1Column]
                            ),
                        pc2:
                            Number(
                                row[pc2Column]
                            ),
                        pc3:
                            Number(
                                row[pc3Column]
                            )
                    };

                })
                .filter(
                    d =>
                        d.id &&
                        Number.isFinite(d.pc1) &&
                        Number.isFinite(d.pc2)
                );

        multivariateUmapData =
            umapRows
                .map(row => {

                    const id =
                        multivariateGetId(row);

                    const xColumn =
                        multivariateFindColumn(
                            row,
                            [
                                "UMAP1",
                                "umap1",
                                "UMAP_1",
                                "x"
                            ]
                        );

                    const yColumn =
                        multivariateFindColumn(
                            row,
                            [
                                "UMAP2",
                                "umap2",
                                "UMAP_2",
                                "y"
                            ]
                        );

                    return {
                        id: id,
                        x:
                            Number(
                                row[xColumn]
                            ),
                        y:
                            Number(
                                row[yColumn]
                            )
                    };

                })
                .filter(
                    d =>
                        d.id &&
                        Number.isFinite(d.x) &&
                        Number.isFinite(d.y)
                );

        if (
            !multivariateData.length ||
            !multivariatePcaData.length ||
            !multivariateUmapData.length
        ) {
            throw new Error(
                "Data multivariat tidak lengkap."
            );
        }

        renderMultivariatePCA();
        renderMultivariateUMAP();
        renderMultivariateParallel();

        updateMultivariateProfile();

    } catch (error) {

        console.error(
            "Gagal memuat Section 06:",
            error
        );

        pcaContainer.innerHTML =
            "<p>Visualisasi PCA tidak dapat dimuat.</p>";

        umapContainer.innerHTML =
            "<p>Visualisasi UMAP tidak dapat dimuat.</p>";

        parallelContainer.innerHTML =
            "<p>Profil wilayah tidak dapat dimuat.</p>";
    }
}

function createMultivariateTooltip(container) {

    let tooltip =
        container.querySelector(
            ".multivariate-tooltip"
        );

    if (!tooltip) {

        tooltip =
            document.createElement("div");

        tooltip.className =
            "multivariate-tooltip";

        tooltip.style.display =
            "none";

        container.appendChild(
            tooltip
        );
    }

    return tooltip;
}

function showMultivariateTooltip(
    tooltip,
    event,
    title,
    lines
) {

    tooltip.innerHTML =
        `
        <div class="multivariate-tooltip-title">
            ${title}
        </div>

        ${lines.map(
            line =>
                `<div class="multivariate-tooltip-value">${line}</div>`
        ).join("")}
        `;

    tooltip.style.display =
        "block";

    const rect =
        tooltip.parentElement.getBoundingClientRect();

    const x =
        event.clientX -
        rect.left +
        14;

    const y =
        event.clientY -
        rect.top +
        14;

    tooltip.style.left =
        `${x}px`;

    tooltip.style.top =
        `${y}px`;
}

function hideMultivariateTooltip(
    tooltip
) {

    tooltip.style.display =
        "none";
}

function getMultivariatePointColor(
    item
) {

    if (
        item.provinsi &&
        normalizeIsland(item.provinsi) === "Sumatera"
    ) {
        return "#756bb1";
    }

    return "#54278f";
}

function selectMultivariateRegion(
    id
) {

    multivariateSelectedId =
        id;

    d3.selectAll(
        ".multivariate-point"
    )
        .classed(
            "is-selected",
            function() {
                return (
                    d3.select(this)
                        .attr("data-id") === id
                );
            }
        )
        .classed(
            "is-muted",
            function() {
                return (
                    d3.select(this)
                        .attr("data-id") !== id
                );
            }
        );

    d3.selectAll(
        ".multivariate-parallel-line"
    )
        .classed(
            "is-selected",
            function() {
                return (
                    d3.select(this)
                        .attr("data-id") === id
                );
            }
        )
        .classed(
            "is-muted",
            function() {
                return (
                    d3.select(this)
                        .attr("data-id") !== id
                );
            }
        );

    updateMultivariateProfile();
}

function clearMultivariateSelection() {

    multivariateSelectedId =
        null;

    d3.selectAll(
        ".multivariate-point"
    )
        .classed(
            "is-selected",
            false
        )
        .classed(
            "is-muted",
            false
        );

    d3.selectAll(
        ".multivariate-parallel-line"
    )
        .classed(
            "is-selected",
            false
        )
        .classed(
            "is-muted",
            false
        );

    updateMultivariateProfile();
}

function renderMultivariatePCA() {

    const container =
        document.getElementById(
            "multivariate-pca"
        );

    if (!container) {
        return;
    }

    container.innerHTML =
        "";

    const width =
        container.clientWidth || 760;

    const height =
        500;

    const margin = {
        top: 24,
        right: 24,
        bottom: 52,
        left: 58
    };

    const innerWidth =
        width -
        margin.left -
        margin.right;

    const innerHeight =
        height -
        margin.top -
        margin.bottom;

    const svg =
        d3.select(container)
            .append("svg")
            .attr(
                "viewBox",
                `0 0 ${width} ${height}`
            );

    const x =
        d3.scaleLinear()
            .domain(
                d3.extent(
                    multivariatePcaData,
                    d => d.pc1
                )
            )
            .nice()
            .range([
                margin.left,
                width - margin.right
            ]);

    const y =
        d3.scaleLinear()
            .domain(
                d3.extent(
                    multivariatePcaData,
                    d => d.pc2
                )
            )
            .nice()
            .range([
                height - margin.bottom,
                margin.top
            ]);

    const xAxis =
        d3.axisBottom(x)
            .ticks(6);

    const yAxis =
        d3.axisLeft(y)
            .ticks(6);

    svg.append("g")
        .attr(
            "class",
            "multivariate-axis"
        )
        .attr(
            "transform",
            `translate(0,${height - margin.bottom})`
        )
        .call(xAxis);

    svg.append("g")
        .attr(
            "class",
            "multivariate-axis"
        )
        .attr(
            "transform",
            `translate(${margin.left},0)`
        )
        .call(yAxis);

    svg.append("text")
        .attr(
            "class",
            "multivariate-axis-label"
        )
        .attr(
            "x",
            width / 2
        )
        .attr(
            "y",
            height - 10
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .text(
            "PC1 — 47,54%"
        );

    svg.append("text")
        .attr(
            "class",
            "multivariate-axis-label"
        )
        .attr(
            "transform",
            "rotate(-90)"
        )
        .attr(
            "x",
            -height / 2
        )
        .attr(
            "y",
            16
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .text(
            "PC2 — 22,09%"
        );

    const tooltip =
        createMultivariateTooltip(
            container
        );

    const points =
        svg.append("g")
            .selectAll("circle")
            .data(
                multivariatePcaData,
                d => d.id
            )
            .join("circle")
            .attr(
                "class",
                "multivariate-point"
            )
            .attr(
                "data-id",
                d => d.id
            )
            .attr(
                "cx",
                d => x(d.pc1)
            )
            .attr(
                "cy",
                d => y(d.pc2)
            )
            .attr(
                "r",
                4
            )
            .attr(
                "fill",
                d => {

                    const match =
                        multivariateData.find(
                            item =>
                                item.id === d.id
                        );

                    return match
                        ? getMultivariatePointColor(match)
                        : "#54278f";
                }
            )
            .on(
                "mouseenter",
                function(event, d) {

                    const match =
                        multivariateData.find(
                            item =>
                                item.id === d.id
                        );

                    showMultivariateTooltip(
                        tooltip,
                        event,
                        d.id,
                        [
                            match
                                ? match.provinsi
                                : "",
                            `PC1: ${d.pc1.toFixed(3)}`,
                            `PC2: ${d.pc2.toFixed(3)}`
                        ]
                    );
                }
            )
            .on(
                "mousemove",
                function(event) {

                    const rect =
                        container.getBoundingClientRect();

                    tooltip.style.left =
                        `${event.clientX - rect.left + 14}px`;

                    tooltip.style.top =
                        `${event.clientY - rect.top + 14}px`;
                }
            )
            .on(
                "mouseleave",
                function() {
                    hideMultivariateTooltip(
                        tooltip
                    );
                }
            )
            .on(
                "click",
                function(event, d) {

                    event.stopPropagation();

                    selectMultivariateRegion(
                        d.id
                    );
                }
            );

    svg.on(
        "click",
        function() {
            clearMultivariateSelection();
        }
    );

    points
        .attr(
            "opacity",
            1
        );
}

function renderMultivariateUMAP() {
    const container = document.getElementById("multivariate-umap");

    if (!container) return;

    container.innerHTML = "";

    if (!multivariateUmapData || multivariateUmapData.length === 0) {
        container.innerHTML = `
            <div class="multivariate-empty">
                Data UMAP tidak tersedia.
            </div>
        `;
        return;
    }

    const xColumn = "x";
    const yColumn = "y";

    console.log("Jumlah data UMAP:", multivariateUmapData.length);
    console.log("Kolom UMAP:", xColumn, yColumn);
    console.log("Contoh data UMAP:", multivariateUmapData[0]);
    console.log("UMAP1 mentah:", multivariateUmapData[0].UMAP1);
    console.log("UMAP2 mentah:", multivariateUmapData[0].UMAP2);

    const points = multivariateUmapData
        .map(row => ({
            ...row,
            x: Number(String(row[xColumn]).replace(",", ".")),
            y: Number(String(row[yColumn]).replace(",", "."))
        }))
        .filter(row =>
            Number.isFinite(row.x) &&
            Number.isFinite(row.y)
        );

    console.log("Jumlah koordinat UMAP valid:", points.length);

    if (points.length === 0) {
        container.innerHTML = `
            <div class="multivariate-empty">
                Tidak ada koordinat UMAP yang valid.
            </div>
        `;
        return;
    }

    const width = Math.max(
        container.clientWidth || 700,
        320
    );

    const height = 500;

    const margin = {
        top: 30,
        right: 30,
        bottom: 45,
        left: 50
    };

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const svg = d3
        .select(container)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("role", "img")
        .attr(
            "aria-label",
            "Scatter plot UMAP kabupaten dan kota"
        );

    const chart = svg
        .append("g")
        .attr(
            "transform",
            `translate(${margin.left},${margin.top})`
        );

    const xExtent = d3.extent(points, d => d.x);
    const yExtent = d3.extent(points, d => d.y);

    const xPadding = (xExtent[1] - xExtent[0]) * 0.08 || 1;
    const yPadding = (yExtent[1] - yExtent[0]) * 0.08 || 1;

    const xScale = d3
        .scaleLinear()
        .domain([
            xExtent[0] - xPadding,
            xExtent[1] + xPadding
        ])
        .range([0, innerWidth]);

    const yScale = d3
        .scaleLinear()
        .domain([
            yExtent[0] - yPadding,
            yExtent[1] + yPadding
        ])
        .range([innerHeight, 0]);

    chart
        .append("g")
        .attr("class", "multivariate-axis")
        .attr(
            "transform",
            `translate(0,${innerHeight})`
        )
        .call(d3.axisBottom(xScale).ticks(6));

    chart
        .append("g")
        .attr("class", "multivariate-axis")
        .call(d3.axisLeft(yScale).ticks(6));

    chart
        .append("text")
        .attr("class", "multivariate-axis-label")
        .attr("x", innerWidth / 2)
        .attr("y", innerHeight + 38)
        .attr("text-anchor", "middle")
        .text("UMAP 1");

    chart
        .append("text")
        .attr("class", "multivariate-axis-label")
        .attr("transform", "rotate(-90)")
        .attr("x", -innerHeight / 2)
        .attr("y", -36)
        .attr("text-anchor", "middle")
        .text("UMAP 2");

    const contourData = points.map(d => [
        xScale(d.x),
        yScale(d.y)
    ]);

    if (contourData.length >= 10) {
        const density = d3
            .contourDensity()
            .x(d => d[0])
            .y(d => d[1])
            .size([innerWidth, innerHeight])
            .bandwidth(35)
            .thresholds(8);

        const contours = density(contourData);

        chart
            .append("g")
            .attr("class", "multivariate-density")
            .selectAll("path")
            .data(contours)
            .join("path")
            .attr("class", "multivariate-density-contour")
            .attr("d", d3.geoPath())
            .attr("fill", "var(--viz-series-2)")
            .attr("fill-opacity", 0.08)
            .attr("stroke", "var(--viz-series-2)")
            .attr("stroke-opacity", 0.2)
            .attr("stroke-width", 1);
    }

    const pointGroup = chart
        .append("g")
        .attr("class", "multivariate-points");
    let tooltip =
        container.querySelector(
            ".multivariate-tooltip"
        );

    if (!tooltip) {
        tooltip =
            document.createElement("div");

        tooltip.className =
            "multivariate-tooltip";

        tooltip.style.display =
            "none";

        container.appendChild(tooltip);
    }
    pointGroup
        .selectAll("circle")
        .data(points)
        .join("circle")
        .attr("class", "multivariate-point")
        .attr("cx", d => xScale(d.x))
        .attr("cy", d => yScale(d.y))
        .attr("r", 4.5)
        .attr("fill", d => getMultivariatePointColor(d))
        .attr("fill-opacity", 0.78)
        .attr("stroke", "var(--background)")
        .attr("stroke-width", 1)
        .style("cursor", "pointer")

        .on("mouseenter", function(event, d) {

            const title =
                d.id ||
                d.Kab_kota ||
                d.KabKota ||
                d.kab_kota ||
                "Wilayah";

            const province =
                d.Provinsi ||
                d.provinsi ||
                "";

            showMultivariateTooltip(
                tooltip,
                event,
                title,
                [
                    province,
                    `UMAP 1: ${d.x.toFixed(3)}`,
                    `UMAP 2: ${d.y.toFixed(3)}`,
                    "Klik untuk melihat profil wilayah."
                ]
            );

            d3.select(this)
                .raise()
                .attr("r", 7)
                .attr(
                    "stroke",
                    "var(--text)"
                )
                .attr(
                    "stroke-width",
                    2
                );
        })

        .on("mousemove", function(event) {

            const rect =
                container.getBoundingClientRect();

            tooltip.style.left =
                `${event.clientX - rect.left + 14}px`;

            tooltip.style.top =
                `${event.clientY - rect.top + 14}px`;
        })

        .on("mouseleave", function() {

            tooltip.style.display =
                "none";

            d3.select(this)
                .attr("r", 4.5)
                .attr(
                    "stroke",
                    "var(--background)"
                )
                .attr(
                    "stroke-width",
                    1
                );
        })

        .on("click", function(event, d) {

            event.stopPropagation();

            const id =
                d.id ||
                multivariateGetId(d);

            if (!id) return;

            selectMultivariateRegion(id);
        });

    if (multivariateSelectedId) {
        updateMultivariateSelectionStyles();
    }
}
function renderMultivariateParallel() {

    const container =
        document.getElementById(
            "multivariate-parallel"
        );

    if (!container) {
        return;
    }

    container.innerHTML =
        "";

    const width =
        Math.max(
            container.clientWidth || 760,
            760
        );

    const height =
        390;

    const margin = {
        top: 28,
        right: 20,
        bottom: 42,
        left: 20
    };

    const svg =
        d3.select(container)
            .append("svg")
            .attr(
                "viewBox",
                `0 0 ${width} ${height}`
            );

    const x =
        d3.scalePoint()
            .domain(
                MULTIVARIATE_VARIABLES
            )
            .range([
                margin.left,
                width - margin.right
            ]);

    const scales = {};

    MULTIVARIATE_VARIABLES.forEach(
        variable => {

            const values =
                multivariateData.map(
                    d => d[variable]
                );

            scales[variable] =
                d3.scaleLinear()
                    .domain(
                        d3.extent(values)
                    )
                    .nice()
                    .range([
                        height - margin.bottom,
                        margin.top
                    ]);
        }
    );

    const line =
        d3.line();

    function pathFor(d) {

        return line(
            MULTIVARIATE_VARIABLES.map(
                variable => [
                    x(variable),
                    scales[variable](
                        d[variable]
                    )
                ]
            )
        );
    }

    svg.selectAll(
        ".parallel-axis"
    )
        .data(
            MULTIVARIATE_VARIABLES
        )
        .join("line")
        .attr(
            "class",
            "multivariate-parallel-axis"
        )
        .attr(
            "x1",
            d => x(d)
        )
        .attr(
            "x2",
            d => x(d)
        )
        .attr(
            "y1",
            margin.top
        )
        .attr(
            "y2",
            height - margin.bottom
        );

    svg.selectAll(
        ".parallel-label"
    )
        .data(
            MULTIVARIATE_VARIABLES
        )
        .join("text")
        .attr(
            "class",
            "multivariate-parallel-label"
        )
        .attr(
            "x",
            d => x(d)
        )
        .attr(
            "y",
            height - 15
        )
        .attr(
            "text-anchor",
            "middle"
        )
        .text(
            d => {

                const labels = {
                    jumlah_penduduk: "Penduduk",
                    jumlah_lansia: "Lansia",
                    pct_lansia: "% Lansia",
                    pct_anak: "% Anak",
                    rls: "RLS",
                    pengeluaran: "Pengeluaran",
                    ahh_rata2: "AHH",
                    delta_pct_lansia: "Δ % Lansia"
                };

                return labels[d] || d;
            }
        );

    svg.selectAll(
        ".multivariate-parallel-line"
    )
        .data(
            multivariateData,
            d => d.id
        )
        .join("path")
        .attr(
            "class",
            "multivariate-parallel-line"
        )
        .attr(
            "data-id",
            d => d.id
        )
        .attr(
            "d",
            pathFor
        )
        .attr(
            "stroke",
            d => getMultivariatePointColor(d)
        );
}

function updateMultivariateProfile() {

    const title =
        document.getElementById(
            "multivariate-profile-title"
        );

    const description =
        document.getElementById(
            "multivariate-profile-description"
        );

    const insightTitle =
        document.getElementById(
            "multivariate-insight-title"
        );

    const insightText =
        document.getElementById(
            "multivariate-insight-text"
        );

    if (!title) {
        return;
    }

    if (!multivariateSelectedId) {

        title.textContent =
            "Pilih satu wilayah";

        description.textContent =
            "Pilih titik pada PCA atau UMAP untuk melihat profil delapan indikator.";

        if (insightTitle) {
            insightTitle.textContent =
                "Kedekatan posisi menunjukkan kemiripan profil.";
        }

        if (insightText) {
            insightText.textContent =
                "Pilih sebuah kabupaten/kota pada PCA atau UMAP. Wilayah yang sama akan disorot pada visualisasi lainnya.";
        }

        return;
    }

    const selected =
        multivariateData.find(
            d =>
                d.id ===
                multivariateSelectedId
        );

    if (!selected) {
        return;
    }

    title.textContent =
        selected.id;

    description.textContent =
        selected.provinsi ||
        "Profil delapan indikator wilayah.";

    if (insightTitle) {
        insightTitle.textContent =
            `${selected.id} memiliki profil multivariat tersendiri.`;
    }

    if (insightText) {
        insightText.textContent =
            "Garis yang disorot menunjukkan posisi wilayah terpilih pada delapan indikator. PCA dan UMAP membantu melihat kedekatannya dengan wilayah lain.";
    }
}

loadMultivariateData();
