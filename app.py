"""Streamlit dashboard for Cloud-Connected-Hardware-IoT-Monitor."""

import json
import os
from datetime import datetime, timezone

import streamlit as st

from monitor.config import (
    AZURE_FILE_SHARE_NAME,
    AZURE_STORAGE_ACCOUNT,
    MONITOR_SCHEMA,
    POLL_INTERVAL_SECONDS,
    THRESHOLD_CRITICAL,
    THRESHOLD_WARNING,
)


def get_status(usage_pct: float) -> tuple[str, str]:
    if usage_pct >= THRESHOLD_CRITICAL:
        return "critical", "red"
    if usage_pct >= THRESHOLD_WARNING:
        return "warning", "orange"
    return "ok", "green"


st.set_page_config(
    page_title="IoT Monitor Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Cloud-Connected Hardware IoT Monitor")

# --- Connection info -------------------------------------------------------
with st.sidebar:
    st.header("Connection")
    st.text_input("Storage Account", value=AZURE_STORAGE_ACCOUNT or "(not set)", disabled=True)
    st.text_input("File Share", value=AZURE_FILE_SHARE_NAME or "(not set)", disabled=True)
    st.number_input("Poll Interval (s)", value=POLL_INTERVAL_SECONDS, disabled=True)

# --- Placeholder: load monitoring data -------------------------------------
DATA_FILE = os.path.join(os.path.dirname(__file__), "monitor", "latest_reading.json")


@st.cache_data(ttl=10)
def load_reading() -> dict | None:
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


reading = load_reading()

if reading is None:
    st.info(
        "No monitoring data found yet.  \n"
        f"Place a JSON file at `{DATA_FILE}` or start the collector to populate the dashboard."
    )
    st.subheader("Sample Data (for preview)")
    reading = {
        "agent_id": "agent-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "total_gb": 100.0,
            "used_gb": 72.5,
            "free_gb": 27.5,
            "usage_pct": 72.5,
        },
        "tags": {
            "region": "westeurope",
            "env": "production",
            "share_name": "iot-data",
        },
        "suffix_status": "warning",
    }
    st.caption("Showing simulated data — connect a real collector for live metrics.")

# --- KPI cards -------------------------------------------------------------
metrics = reading.get("metrics", {})
status_label, status_color = get_status(metrics.get("usage_pct", 0))

col1, col2, col3, col4 = st.columns(4)
col1.metric("Agent ID", reading.get("agent_id", "—"))
col2.metric("Usage", f"{metrics.get('usage_pct', 0):.1f}%", delta=status_label.upper(), delta_color=status_color if status_label != "ok" else "off")
col3.metric("Used / Total", f"{metrics.get('used_gb', 0):.1f} / {metrics.get('total_gb', 0):.1f} GB")
col4.metric("Free", f"{metrics.get('free_gb', 0):.1f} GB")

st.progress(min(metrics.get("usage_pct", 0) / 100, 1.0))

# --- Tags ------------------------------------------------------------------
st.subheader("Tags")
tags = reading.get("tags", {})
if tags:
    st.json(tags)
else:
    st.caption("No tags recorded.")

# --- Schema reference ------------------------------------------------------
with st.expander("JSON Schema Reference"):
    st.json(MONITOR_SCHEMA)

# --- Timestamp -------------------------------------------------------------
ts = reading.get("timestamp", "")
if ts:
    st.caption(f"Last reading: {ts}")
