"""Streamlit dashboard for Cloud-Connected-Hardware-IoT-Monitor."""

import json
import os
from datetime import datetime, timezone

import streamlit as st

from monitor.config import (
    AZURE_FILE_SHARE_NAME,
    AZURE_IOT_HUB_CONNECTION_STRING,
    MONITOR_SCHEMA,
    POLL_INTERVAL_SECONDS,
    TEMPERATURE_CRITICAL,
    TEMPERATURE_WARNING,
    get_temperature_status,
)
from monitor.utils.formatters import (
    format_humidity,
    format_location,
    format_status_emoji,
    format_temperature,
    format_timestamp,
)


def load_reading() -> dict | None:
    """Load the latest reading from file."""
    data_file = os.path.join(os.path.dirname(__file__), "monitor", "latest_reading.json")
    if not os.path.exists(data_file):
        return None
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        st.error(f"Error reading data file: {e}")
        return None


def get_sample_reading() -> dict:
    """Get sample data for preview."""
    return {
        "device_id": "ESP32-Sensor-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": 26.5,
        "humidity": 52.3,
        "location": {
            "room": "Server Room A",
            "rack_id": "Rack-01",
            "zone": "Zone-1",
        },
        "device_info": {
            "type": "esp32",
            "sensor_type": "dht22",
            "firmware_version": "1.0.0",
        },
        "status": "warning",
    }


# Page configuration
st.set_page_config(
    page_title="IoT Temperature Monitor",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ Cloud-Connected Hardware IoT Monitor")
st.markdown("*Real-time temperature monitoring for server rooms*")

# --- Sidebar: Connection Info -----------------------------------------------
with st.sidebar:
    st.header("⚙️ Connection")

    iot_hub_status = "🟢 Connected" if AZURE_IOT_HUB_CONNECTION_STRING else "🔴 Not Configured"
    st.text_input("Azure IoT Hub", value=iot_hub_status, disabled=True)
    st.text_input("File Share", value=AZURE_FILE_SHARE_NAME or "(not set)", disabled=True)
    st.number_input("Poll Interval (s)", value=POLL_INTERVAL_SECONDS, disabled=True)

    st.divider()
    st.header("📊 Thresholds")
    st.metric("Warning", f"{TEMPERATURE_WARNING}°C")
    st.metric("Critical", f"{TEMPERATURE_CRITICAL}°C")

# --- Load Data -------------------------------------------------------------
reading = load_reading()

if reading is None:
    st.info(
        "No monitoring data found yet.  \n"
        "Connect a hardware sensor or start the simulator to populate the dashboard."
    )
    st.subheader("📱 Sample Data (Preview)")
    reading = get_sample_reading()
    st.caption("Showing simulated data — connect a real sensor for live metrics.")

# --- Main Dashboard --------------------------------------------------------

# Status banner
status = reading.get("status", "ok")
temperature = reading.get("temperature", 0)

if status == "critical":
    st.error(f"🔴 **CRITICAL ALERT** - Temperature {temperature:.1f}°C exceeds {TEMPERATURE_CRITICAL}°C threshold!")
elif status == "warning":
    st.warning(f"🟠 **WARNING** - Temperature {temperature:.1f}°C exceeds {TEMPERATURE_WARNING}°C threshold!")
else:
    st.success("🟢 All systems operating normally")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    status_label, status_color = get_temperature_status(temperature)
    st.metric(
        "Temperature",
        format_temperature(temperature),
        delta=status_label.upper(),
        delta_color="inverse" if status_label != "ok" else "off",
    )

with col2:
    humidity = reading.get("humidity")
    st.metric("Humidity", format_humidity(humidity))

with col3:
    location = reading.get("location", {})
    st.metric("Location", location.get("room", "Unknown"))

with col4:
    device_info = reading.get("device_info", {})
    st.metric("Device", device_info.get("type", "Unknown").upper())

# Temperature Gauge
st.subheader("🌡️ Temperature Reading")

# Create a visual gauge using progress bar
temp_min = -10.0
temp_max = 50.0
temp_range = temp_max - temp_min
temp_normalized = (temperature - temp_min) / temp_range

col_gauge1, col_gauge2 = st.columns([2, 1])

with col_gauge1:
    st.progress(min(max(temp_normalized, 0.0), 1.0))
    st.caption(f"Range: {temp_min}°C to {temp_max}°C")

with col_gauge2:
    st.markdown(f"### {format_temperature(temperature)}")
    status_emoji = "🟢" if status == "ok" else "🟠" if status == "warning" else "🔴"
    st.markdown(f"{status_emoji} Status: **{status.upper()}**")

# Detailed Info
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("📍 Location Details")
    st.json(location)

with col_info2:
    st.subheader("🔧 Device Information")
    st.json(device_info)

# Tags and Metadata
st.subheader("🏷️ Metadata")
tags = reading.get("tags", {})
if tags:
    st.json(tags)

# Timestamp
ts = reading.get("timestamp", "")
if ts:
    st.caption(f"Last reading: {format_timestamp(ts)}")

# Schema Reference
with st.expander("📋 JSON Schema Reference"):
    st.json(MONITOR_SCHEMA)

# Footer
st.divider()
st.caption("Cloud-Connected Hardware IoT Monitor | Real-time Server Room Temperature Monitoring")
