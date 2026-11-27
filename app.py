
import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo


# =====================================================
# 1. KONFIGURASI WEBSITE
# =====================================================

st.set_page_config(
    page_title="Environmental Monitoring System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

LAT = -8.1708
LON = 113.7156
BMKG_CODE = "35.09.21.1002"
TZ = "Asia/Jakarta"


# =====================================================
# 2. CSS DAN DESAIN WEBSITE
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

/* GLOBAL */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #f1f6f2 !important;
    color: #26382d !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 1450px !important;
    padding: 28px 35px 45px 35px !important;
}

h1, h2, h3, h4, h5 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #193d2b !important;
    letter-spacing: -0.5px;
}

.stMarkdown p {
    line-height: 1.7;
}

/* ANIMATION */

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(9px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* MAIN HEADER */

.hero {
    background: linear-gradient(
        125deg,
        #123c2a 0%,
        #1d6240 55%,
        #31845a 100%
    ) !important;
    padding: 36px 38px !important;
    border-radius: 20px !important;
    color: white !important;
    margin-bottom: 28px !important;
    box-shadow: 0 8px 24px rgba(20,65,43,0.15);
    animation: fadeIn 0.7s ease;
}

.hero h1 {
    color: white !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    margin: 0 0 12px 0 !important;
    letter-spacing: -1px;
}

.hero p {
    color: #e1f1e6 !important;
    font-size: 14px !important;
    margin: 6px 0 !important;
}

/* =========================================
   PARENT CARD MONITORING
========================================= */

/* Masing-masing container mempunyai class unik */

.st-key-iot-card,
.st-key-bmkg-card,
.st-key-openmeteo-card {
    background: #ffffff !important;
    border: 1px solid #dfeae2 !important;
    border-radius: 22px !important;
    padding: 20px 22px 18px 22px !important;
    margin: 20px 0 30px 0 !important;
    box-shadow: 0 7px 24px rgba(30,75,48,0.09) !important;
    overflow: hidden !important;
    animation: fadeIn 0.6s ease;
}

/* HEADER BANNER DI DALAM PARENT CARD */

.monitoring-group-header {
    display: block !important;
    width: 100% !important;
    box-sizing: border-box !important;
    padding: 23px 26px !important;
    border-radius: 15px !important;
    margin: 0 0 20px 0 !important;
    color: white !important;
}

.monitoring-group-header h3 {
    color: white !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 21px !important;
    font-weight: 800 !important;
    margin: 0 !important;
    line-height: 1.4 !important;
}

.monitoring-group-header p {
    color: #edf7f0 !important;
    font-size: 13px !important;
    margin: 7px 0 0 0 !important;
    line-height: 1.6 !important;
}

.iot-header {
    background: linear-gradient(120deg, #123c2a, #31845a) !important;
}

.bmkg-header {
    background: linear-gradient(120deg, #17547d, #398fc1) !important;
}

.openmeteo-header {
    background: linear-gradient(120deg, #50377e, #8965bd) !important;
}

/* JARAK ANTAR PARAMETER */

.st-key-iot-card [data-testid="stHorizontalBlock"],
.st-key-bmkg-card [data-testid="stHorizontalBlock"],
.st-key-openmeteo-card [data-testid="stHorizontalBlock"] {
    gap: 14px !important;
}

/* SENSOR CARD */

.sensor-card {
    background: #ffffff !important;
    padding: 23px !important;
    border-radius: 16px !important;
    border: 1px solid #e6eee8 !important;
    border-left: 5px solid #29945e !important;
    box-shadow: 0 4px 14px rgba(30,75,48,0.055);
    min-height: 155px !important;
    margin-bottom: 15px !important;
    transition: all 0.25s ease;
    animation: fadeIn 0.6s ease;
}

.sensor-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 9px 22px rgba(30,75,48,0.12);
}

.sensor-icon {
    font-size: 27px !important;
    margin-bottom: 9px;
}

.sensor-name {
    color: #687a6e !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-top: 7px !important;
}

.sensor-value {
    color: #174c30 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 29px !important;
    font-weight: 800 !important;
    margin-top: 8px !important;
    letter-spacing: -1px;
    word-break: break-word;
}

.sensor-value span {
    color: #4b7659 !important;
    font-size: 14px !important;
}

.sensor-device {
    color: #929e95 !important;
    font-size: 11px !important;
    margin-top: 7px !important;
}

/* WEATHER CARD */

.weather-card {
    background: #ffffff !important;
    padding: 22px !important;
    border-radius: 16px !important;
    border: 1px solid #e6eee8 !important;
    border-left: 5px solid #3988bd !important;
    box-shadow: 0 4px 14px rgba(30,75,48,0.055);
    min-height: 145px !important;
    margin-bottom: 15px !important;
    transition: all 0.25s ease;
    animation: fadeIn 0.6s ease;
}

.weather-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 9px 22px rgba(30,75,48,0.12);
}

.weather-name {
    color: #687a6e !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-top: 8px !important;
}

.weather-value {
    color: #174c30 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 25px !important;
    font-weight: 800 !important;
    margin-top: 9px !important;
    letter-spacing: -0.7px;
    word-break: break-word;
}

.weather-value span {
    color: #4b7659 !important;
    font-size: 13px !important;
}

.weather-source {
    color: #929e95 !important;
    font-size: 11px !important;
    margin-top: 7px !important;
}

/* STATUS BADGE */

.status-badge {
    display: inline-block !important;
    padding: 9px 16px !important;
    border-radius: 30px !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    margin: 5px 0 18px 0 !important;
}

.status-success {
    color: #187844 !important;
    background: #e4f6e9 !important;
}

.status-error {
    color: #c73737 !important;
    background: #ffeded !important;
}

.status-simulated {
    color: #946719 !important;
    background: #fff4d9 !important;
}

/* NOTICE BOX */

.notice-box {
    background: #fffaf0 !important;
    border: 1px solid #f0dfb9 !important;
    border-radius: 14px !important;
    padding: 17px 21px !important;
    color: #896329 !important;
    font-size: 13px !important;
    line-height: 1.8 !important;
    margin-top: 12px !important;
    margin-bottom: 8px !important;
}

.notice-box b {
    color: #80551a !important;
}

/* ERROR BOX */

.error-box {
    background: #fff8ed !important;
    border: 1px solid #f1d9ae !important;
    border-radius: 15px !important;
    padding: 21px !important;
    color: #79551f !important;
    margin-bottom: 18px !important;
    animation: fadeIn 0.5s ease;
}

.error-box h4 {
    color: #79551f !important;
    margin: 0 0 9px 0 !important;
    font-size: 16px !important;
}

/* SYSTEM INFORMATION */

.system-information-card {
    background: #ffffff !important;
    border: 1px solid #e4ece6 !important;
    border-radius: 18px !important;
    overflow: hidden !important;
    box-shadow: 0 5px 18px rgba(30,75,48,0.07);
    margin-top: 12px !important;
    margin-bottom: 22px !important;
}

.system-information-header {
    background: linear-gradient(120deg,#123c2a,#26734d) !important;
    color: white !important;
    padding: 25px 28px !important;
    border-radius: 14px !important;
}

.system-information-header h3 {
    color: white !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 21px !important;
    font-weight: 800 !important;
    margin: 0 !important;
}

.system-information-header p {
    color: #e0efe5 !important;
    font-size: 13px !important;
    margin: 7px 0 0 0 !important;
}

.system-information-content {
    display: grid !important;
    grid-template-columns: repeat(3,minmax(0,1fr)) !important;
    padding: 24px !important;
    gap: 0 !important;
}

.system-information-item {
    padding: 12px 21px !important;
    border-right: 1px solid #e8eee9 !important;
    min-width: 0;
}

.system-information-item:last-child {
    border-right: none !important;
}

.system-information-item h4 {
    color: #204b31 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    margin: 0 0 13px 0 !important;
}

.system-information-item p {
    color: #68786d !important;
    font-size: 12px !important;
    line-height: 1.8 !important;
    margin: 7px 0 !important;
}

/* EXPANDER */

[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e3ece5 !important;
    border-radius: 13px !important;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    color: #244b33 !important;
}

/* REFRESH BUTTON */

.stButton > button {
    background: linear-gradient(120deg,#23764b,#318b59) !important;
    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    padding: 11px 20px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: #185b38 !important;
    color: white !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 12px rgba(35,118,75,0.2);
}

/* CAPTION */

[data-testid="stCaptionContainer"] {
    color: #829087 !important;
    font-size: 11px !important;
}

/* FOOTER */

.footer {
    background: linear-gradient(120deg,#123c2a,#205e3d) !important;
    color: white !important;
    text-align: center !important;
    padding: 24px !important;
    border-radius: 15px !important;
    margin-top: 32px !important;
    font-size: 12px !important;
    line-height: 1.9 !important;
}

.footer b {
    color: white !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* RESPONSIVE */

@media (max-width: 900px) {
    .block-container {
        padding: 20px !important;
    }

    .system-information-content {
        grid-template-columns: 1fr !important;
    }

    .system-information-item {
        border-right: none !important;
        border-bottom: 1px solid #e8eee9 !important;
        padding: 18px 5px !important;
    }

    .system-information-item:last-child {
        border-bottom: none !important;
    }
}

@media (max-width: 600px) {
    .hero {
        padding: 25px 21px !important;
    }

    .hero h1 {
        font-size: 22px !important;
    }

    .monitoring-group-header {
        padding: 19px !important;
    }

    .monitoring-group-header h3 {
        font-size: 17px !important;
    }

    .sensor-value {
        font-size: 24px !important;
    }

    .weather-value {
        font-size: 21px !important;
    }

    .block-container {
        padding: 15px !important;
    }

    .st-key-iot-card,
    .st-key-bmkg-card,
    .st-key-openmeteo-card {
        padding: 13px !important;
        border-radius: 17px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. FUNGSI TAMPILAN
# =====================================================

def monitoring_header(title, subtitle, header_class):
    st.markdown(f"""
    <div class="monitoring-group-header {header_class}">
        <h3>{title}</h3>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def sensor_card(icon, name, value, unit, device):
    st.markdown(f"""
    <div class="sensor-card">
        <div class="sensor-icon">{icon}</div>
        <div class="sensor-name">{name}</div>
        <div class="sensor-value">
            {value} <span>{unit}</span>
        </div>
        <div class="sensor-device">Sensor: {device}</div>
    </div>
    """, unsafe_allow_html=True)


def weather_card(icon, name, value, unit, color, source):
    st.markdown(f"""
    <div class="weather-card" style="border-left-color:{color}">
        <div class="sensor-icon">{icon}</div>
        <div class="weather-name">{name}</div>
        <div class="weather-value">
            {value} <span>{unit}</span>
        </div>
        <div class="weather-source">Sumber: {source}</div>
    </div>
    """, unsafe_allow_html=True)


def show_status(text, status_type):
    st.markdown(
        f'<div class="status-badge {status_type}">● {text}</div>',
        unsafe_allow_html=True
    )


def display_value(value, default="-"):
    if value is None or value == "":
        return default
    return value


# =====================================================
# 4. DATA SENSOR IoT LOKAL
# =====================================================

sensor = {
    "Suhu Udara": {
        "icon": "🌡️",
        "value": 28.5,
        "unit": "°C",
        "device": "DHT22"
    },
    "Kelembapan Udara": {
        "icon": "💧",
        "value": 75,
        "unit": "%",
        "device": "DHT22"
    },
    "Intensitas Cahaya": {
        "icon": "☀️",
        "value": 850,
        "unit": "Lux",
        "device": "BH1750"
    },
    "Kelembapan Tanah": {
        "icon": "🌱",
        "value": 65,
        "unit": "%",
        "device": "Soil Moisture Sensor"
    },
    "Curah Hujan": {
        "icon": "🌧️",
        "value": 12,
        "unit": "mm",
        "device": "Tipping Bucket Rain Gauge"
    },
    "Kecepatan Angin": {
        "icon": "🌬️",
        "value": 8,
        "unit": "km/jam",
        "device": "Anemometer"
    }
}


# =====================================================
# 5. MENGAMBIL DATA BMKG
# =====================================================

@st.cache_data(ttl=900, show_spinner=False)
def get_bmkg():

    url = "https://api.bmkg.go.id/publik/prakiraan-cuaca"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(compatible; EnvironmentalMonitoringSystem/1.0)"
        ),
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            url,
            params={"adm4": BMKG_CODE},
            headers=headers,
            timeout=20
        )

        if response.status_code == 403:
            return {
                "_error": "Akses ke API BMKG ditolak (403 Forbidden)."
            }, []

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            return {"_error": "Format data BMKG tidak sesuai."}, []

        forecasts = []

        def extract(obj):
            if isinstance(obj, dict):
                if "local_datetime" in obj and "t" in obj:
                    forecasts.append(obj)

                for value in obj.values():
                    extract(value)

            elif isinstance(obj, list):
                for item in obj:
                    extract(item)

        extract(data)

        forecasts.sort(
            key=lambda x: x.get("local_datetime", "")
        )

        if not forecasts:
            return {
                "_error": "Data prakiraan BMKG belum ditemukan."
            }, []

        return data, forecasts

    except requests.exceptions.Timeout:
        return {"_error": "Koneksi ke BMKG mengalami timeout."}, []

    except requests.exceptions.HTTPError:
        return {
            "_error": f"Server BMKG memberikan respons HTTP {response.status_code}."
        }, []

    except requests.exceptions.RequestException:
        return {
            "_error": "Tidak dapat terhubung ke server BMKG."
        }, []

    except ValueError:
        return {"_error": "Respons BMKG bukan JSON yang valid."}, []

    except Exception:
        return {
            "_error": "Terjadi kesalahan saat mengolah data BMKG."
        }, []


def nearest_forecast(forecasts):

    now = datetime.now(ZoneInfo(TZ))
    valid = []

    for item in forecasts:
        try:
            dt = datetime.fromisoformat(item["local_datetime"])

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=ZoneInfo(TZ))

            valid.append((dt, item))

        except (ValueError, TypeError, KeyError):
            continue

    if not valid:
        return None

    future = [item for item in valid if item[0] >= now]

    if future:
        return min(future, key=lambda x: x[0])[1]

    return max(valid, key=lambda x: x[0])[1]


# =====================================================
# 6. MENGAMBIL DATA OPEN-METEO
# =====================================================

@st.cache_data(ttl=900, show_spinner=False)
def get_online_weather():

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LAT,
        "longitude": LON,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m,"
            "wind_direction_10m"
        ),
        "timezone": TZ,
        "wind_speed_unit": "kmh"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


# =====================================================
# 7. DESKRIPSI CUACA
# =====================================================

def weather_description(code):

    descriptions = {
        0: "Cerah",
        1: "Cerah Berawan",
        2: "Berawan Sebagian",
        3: "Berawan",
        45: "Kabut",
        48: "Kabut Tebal",
        51: "Gerimis Ringan",
        53: "Gerimis Sedang",
        55: "Gerimis Lebat",
        61: "Hujan Ringan",
        63: "Hujan Sedang",
        65: "Hujan Lebat",
        80: "Hujan Lokal",
        81: "Hujan Lokal Sedang",
        82: "Hujan Lokal Lebat",
        95: "Badai Petir"
    }

    try:
        code = int(code)
    except (ValueError, TypeError):
        return "Kondisi Cuaca Tidak Diketahui"

    return descriptions.get(
        code,
        "Kondisi Cuaca Tidak Diketahui"
    )


# =====================================================
# 8. HEADER WEBSITE
# =====================================================

now = datetime.now(ZoneInfo(TZ))

st.markdown(f"""
<div class="hero">
    <h1>🌿 ENVIRONMENTAL MONITORING SYSTEM</h1>
    <p>Integrated IoT Sensor & Weather Information Dashboard</p>
    <p>📍 Sumbersari, Kecamatan Sumbersari, Jember, Jawa Timur</p>
    <p>🕒 {now.strftime("%d %B %Y | %H:%M:%S WIB")}</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 9. TOMBOL REFRESH
# =====================================================

refresh_col1, refresh_col2 = st.columns([4, 1])

with refresh_col2:
    if st.button("🔄 REFRESH DATA", use_container_width=True):
        get_bmkg.clear()
        get_online_weather.clear()
        st.rerun()


# =====================================================
# 10. PENGAMBILAN DATA ONLINE
# =====================================================

try:
    bmkg_data, bmkg_forecasts = get_bmkg()

    if bmkg_data and not bmkg_data.get("_error"):
        bmkg_current = nearest_forecast(bmkg_forecasts)
        bmkg_error = None
    else:
        bmkg_current = None
        bmkg_error = (
            bmkg_data.get("_error", "Data BMKG tidak tersedia.")
            if bmkg_data else "Data BMKG tidak tersedia."
        )

except Exception:
    bmkg_current = None
    bmkg_error = "Terjadi kesalahan saat mengambil data BMKG."


try:
    online_data = get_online_weather()
    online_current = online_data.get("current", {})
    online_error = None

except Exception:
    online_data = None
    online_current = {}
    online_error = "Tidak dapat terhubung ke Open-Meteo."


# =====================================================
# 11. LOCAL IoT MONITORING
# =====================================================

with st.container(key="iot-card"):

    monitoring_header(
        "🌱 LOCAL IoT MONITORING",
        "Pemantauan kondisi lingkungan melalui enam parameter sensor IoT lokal",
        "iot-header"
    )

    show_status(
        "DATA SIMULASI - ESP32 BELUM TERHUBUNG",
        "status-simulated"
    )

    cols = st.columns(3, gap="medium")

    for i, (name, data) in enumerate(sensor.items()):
        with cols[i % 3]:
            sensor_card(
                data["icon"],
                name,
                data["value"],
                data["unit"],
                data["device"]
            )

    st.markdown("""
    <div class="notice-box">
        ℹ️ <b>Informasi:</b> Data Local IoT saat ini masih berupa
        simulasi. Nilai aktual akan ditampilkan setelah perangkat
        ESP32 terhubung dengan dashboard.
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 12. BMKG WEATHER INFORMATION
# =====================================================

with st.container(key="bmkg-card"):

    monitoring_header(
        "🌦️ BMKG WEATHER INFORMATION",
        "Informasi cuaca wilayah Sumbersari, Kabupaten Jember berdasarkan data BMKG",
        "bmkg-header"
    )

    if bmkg_current:

        show_status(
            "DATA BMKG BERHASIL DIMUAT",
            "status-success"
        )

        bmkg_cols = st.columns(3, gap="medium")

        bmkg_values = [
            (
                "🌤️",
                "Kondisi Cuaca",
                display_value(bmkg_current.get("weather_desc")),
                ""
            ),
            (
                "🌡️",
                "Suhu Udara",
                display_value(bmkg_current.get("t")),
                "°C"
            ),
            (
                "💧",
                "Kelembapan Udara",
                display_value(bmkg_current.get("hu")),
                "%"
            ),
            (
                "🌬️",
                "Kecepatan Angin",
                display_value(bmkg_current.get("ws")),
                "km/jam"
            ),
            (
                "🧭",
                "Arah Angin",
                display_value(bmkg_current.get("wd")),
                ""
            )
        ]

        for i, (icon, name, value, unit) in enumerate(bmkg_values):
            with bmkg_cols[i % 3]:
                weather_card(
                    icon,
                    name,
                    value,
                    unit,
                    "#2879ad",
                    "BMKG"
                )

        st.caption(
            "Waktu prakiraan: "
            + str(bmkg_current.get("local_datetime", "-"))
        )

    else:

        show_status(
            "DATA SEMENTARA TIDAK TERSEDIA",
            "status-error"
        )

        st.markdown(f"""
        <div class="error-box">
            <h4>⚠️ Koneksi BMKG belum berhasil</h4>
            <div>{bmkg_error or "Data BMKG belum tersedia."}</div>
            <div style="font-size:13px;margin-top:10px;">
                Silakan coba perbarui data beberapa saat lagi.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="notice-box">
        ℹ️ Data BMKG merupakan prakiraan cuaca pada waktu
        terdekat yang tersedia, bukan hasil pengukuran langsung
        dari sensor di lokasi.
        <br><br>
        Sumber: <b>BMKG - Badan Meteorologi, Klimatologi,
        dan Geofisika.</b>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 13. ELECTRONIC DEVICE WEATHER - OPEN-METEO
# =====================================================

with st.container(key="openmeteo-card"):

    monitoring_header(
        "📱 ELECTRONIC DEVICE WEATHER",
        "Informasi cuaca online wilayah Sumbersari, Jember melalui Open-Meteo API",
        "openmeteo-header"
    )

    if online_data:

        show_status(
            "DATA ONLINE BERHASIL DIMUAT",
            "status-success"
        )

        online_cols = st.columns(3, gap="medium")

        code = online_current.get("weather_code", -1)

        online_values = [
            (
                "🌤️",
                "Kondisi Cuaca",
                weather_description(code),
                ""
            ),
            (
                "🌡️",
                "Suhu Udara",
                display_value(online_current.get("temperature_2m")),
                "°C"
            ),
            (
                "💧",
                "Kelembapan Udara",
                display_value(online_current.get("relative_humidity_2m")),
                "%"
            ),
            (
                "🌧️",
                "Curah Hujan",
                display_value(online_current.get("precipitation")),
                "mm"
            ),
            (
                "🌬️",
                "Kecepatan Angin",
                display_value(online_current.get("wind_speed_10m")),
                "km/jam"
            ),
            (
                "🧭",
                "Arah Angin",
                display_value(online_current.get("wind_direction_10m")),
                "°"
            )
        ]

        for i, (icon, name, value, unit) in enumerate(online_values):
            with online_cols[i % 3]:
                weather_card(
                    icon,
                    name,
                    value,
                    unit,
                    "#7353a6",
                    "Open-Meteo"
                )

        st.caption(
            "Waktu data: "
            + str(online_current.get("time", "-"))
        )

    else:

        show_status(
            "DATA ONLINE TIDAK TERSEDIA",
            "status-error"
        )

        st.warning(
            online_error or "Data Open-Meteo belum tersedia."
        )

    st.markdown("""
    <div class="notice-box">
        ℹ️ Open-Meteo menyediakan informasi cuaca berbasis model
        untuk wilayah Sumbersari, Jember. Data ini bukan pembacaan
        langsung dari aplikasi cuaca pada perangkat elektronik.
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 14. SYSTEM INFORMATION
# =====================================================

with st.container(border=True):

    st.markdown("""
    <div class="system-information-header">
        <h3>⚙️ SYSTEM INFORMATION</h3>
        <p>
            Informasi sumber data, perangkat, dan sistem
            pemantauan lingkungan
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("### 🌱 LOCAL IoT SYSTEM")
        st.caption("LOCAL SENSOR")

        st.markdown("""
        - **ESP32** — Mikrokontroler
        - **DHT22** — Suhu dan kelembapan udara
        - **BH1750** — Intensitas cahaya
        - **Soil Moisture** — Kelembapan tanah
        - **Tipping Bucket** — Curah hujan
        - **Anemometer** — Kecepatan angin
        """)

    with col2:
        st.markdown("### 🌦️ BMKG WEATHER SYSTEM")
        st.caption("WEATHER API")

        st.markdown("""
        - **Sumber:** API resmi BMKG
        - **Kode wilayah:** 35.09.21.1002
        - **Jenis data:** Prakiraan cuaca
        - **Lokasi:** Sumbersari, Jember
        - **Cache aplikasi:** 15 menit
        """)

    with col3:
        st.markdown("### 📱 OPEN-METEO SYSTEM")
        st.caption("ONLINE WEATHER")

        st.markdown("""
        - **Sumber:** Open-Meteo API
        - **Jenis data:** Cuaca berbasis model
        - **Lokasi:** Sumbersari, Jember
        - **Latitude:** -8.1708
        - **Longitude:** 113.7156
        - **Cache aplikasi:** 15 menit
        """)


# =====================================================
# 15. CATATAN SISTEM
# =====================================================

with st.expander("📖 Catatan dan Keterbatasan Sistem"):

    st.write("""
    1. Data Local IoT masih berupa simulasi dan belum
       terhubung langsung dengan perangkat ESP32.

    2. Data BMKG merupakan prakiraan cuaca, bukan
       pengukuran langsung dari sensor di lokasi.

    3. Jika API BMKG memberikan respons 403 Forbidden,
       aplikasi akan menampilkan status data sementara
       tidak tersedia. Hal ini dapat disebabkan pembatasan
       akses dari server BMKG.

    4. Open-Meteo menyediakan informasi cuaca berbasis model,
       bukan data pengukuran langsung dari sensor lokal.

    5. Pembaruan data BMKG dan Open-Meteo mengikuti
       interval cache masing-masing selama 15 menit.

    6. BMP280 tidak ditampilkan sebagai parameter dashboard.

    7. Integrasi aplikasi cuaca pada perangkat elektronik
       membutuhkan API resmi dari penyedia layanan tersebut.
    """)


# =====================================================
# 16. FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    🌿 <b>ENVIRONMENTAL MONITORING SYSTEM</b>
    <br>
    Smart Agriculture & Environmental Monitoring
    <br>
    Sumbersari - Jember, Jawa Timur
    <br>
    Integrated Local IoT, BMKG & Open-Meteo
</div>
""", unsafe_allow_html=True)
