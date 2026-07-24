# Cloud-Connected Hardware IoT Monitor

A DIY temperature monitoring system for server rooms using custom hardware sensors connected to Azure IoT Hub, with a Streamlit dashboard for real-time visualization and alerts.

## 📋 Project Overview

This project builds a **DIY hardware device** that measures temperature in computer/server rooms and sends the data to Azure for monitoring and visualization. The system consists of:

1. **Hardware Component**: Custom-built temperature sensor (ESP32/Arduino + DHT22/SHT31)
2. **Azure IoT Hub**: Cloud platform for receiving and storing sensor data
3. **Streamlit Dashboard**: Real-time web interface for monitoring temperatures

### Key Features

- **DIY Hardware**: Build your own temperature sensor using affordable components
- **Azure IoT Hub**: Secure, scalable cloud connection for IoT devices
- **Real-time Dashboard**: Live temperature readings with charts and alerts
- **Multi-zone Monitoring**: Track multiple server rooms or rack locations
- **Alert System**: Email/webhook notifications when temperature exceeds thresholds
- **Historical Data**: Store and visualize temperature trends over time

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Hardware Sensor (DIY)             │
│   - ESP32/Arduino + DHT22/SHT31    │
│   - Measures temperature            │
│   - Sends data via WiFi            │
└──────────────┬──────────────────────┘
               │ (MQTT/HTTPS)
               ▼
┌─────────────────────────────────────┐
│   Azure IoT Hub                    │
│   - Receives sensor telemetry      │
│   - Stores in Time Series Insights│
│   - Triggers alerts                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Streamlit Dashboard              │
│   - Real-time temperature display  │
│   - Historical charts              │
│   - Alert management               │
└─────────────────────────────────────┘
```

## 🔧 Hardware Components

### Required Parts

| Component | Approx. Cost | Purpose |
|-----------|--------------|---------|
| ESP32 DevKit | $5-10 | Microcontroller with WiFi |
| DHT22/SHT31 Sensor | $5-15 | Temperature & humidity |
| Breadboard + Wires | $5 | Prototyping |
| USB Cable | $3 | Power & programming |
| 3D Printed Case | $10 | Enclosure (optional) |

### Sensor Specifications

- **Temperature Range**: -40°C to 80°C
- **Accuracy**: ±0.5°C (DHT22) / ±0.3°C (SHT31)
- **Update Interval**: Configurable (10s - 5min)
- **Power**: USB or battery (ESP32 low-power modes)

## 📁 Project Structure

```
Cloud-Connected-Hardware-IoT-Monitor/
├── app.py                    # Streamlit dashboard application
├── main.py                   # Application entry point
├── monitor/
│   ├── __init__.py
│   ├── config.py             # Central configuration & schema
│   ├── core/                 # Core business logic
│   │   └── __init__.py
│   ├── ui/                   # UI components (Streamlit widgets)
│   │   └── __init__.py
│   └── utils/                # Utility functions
│       └── __init__.py
├── hardware/                 # Hardware firmware code
│   ├── esp32_sensor/         # ESP32 Arduino/PlatformIO code
│   └── docs/                 # Wiring diagrams
├── azure/                    # Azure ARM templates
│   ├── iot-hub.json
│   └── time-series.json
└── requirements.txt          # Python dependencies
```

## 🚀 Development Roadmap

### Phase 1: Hardware Prototype ✅ (Completed)
- [x] Project structure setup
- [x] Central configuration with Azure env vars
- [x] JSON schema definition for metrics
- [x] Threshold constants (warning: 28°C, critical: 35°C)
- [x] Basic Streamlit dashboard with KPI cards

### Phase 2: Hardware Development (In Progress)
- [ ] ESP32 firmware with DHT22/SHT31 support
- [ ] WiFi connection management
- [ ] Azure IoT Hub device provisioning
- [ ] MQTT/HTTPS telemetry sending
- [ ] Battery power management (optional)

### Phase 3: Azure Integration
- [ ] Create Azure IoT Hub resource
- [ ] Set up device authentication (X.509/SAS)
- [ ] Configure Time Series Insights
- [ ] Set up alert rules and action groups
- [ ] Implement direct methods for remote config

### Phase 4: Dashboard Enhancement
- [ ] Real-time temperature charts (plotly)
- [ ] Multi-sensor comparison view
- [ ] Historical data analysis
- [ ] Alert history and notifications
- [ ] Mobile-responsive design

### Phase 5: Production Deployment
- [ ] 3D print sensor enclosure
- [ ] Deploy sensors in server room
- [ ] Set up monitoring and alerting
- [ ] Documentation and user guide
- [ ] Open-source hardware designs

## ⚙️ Setup Instructions

### Prerequisites

**Hardware:**
- ESP32 DevKit v1
- DHT22 or SHT31 temperature sensor
- Jumper wires and breadboard
- USB cable for programming

**Software:**
- Python 3.10+
- Arduino IDE or PlatformIO
- Azure account (free tier available)
- Azure CLI (optional)

### Hardware Assembly

```
ESP32          DHT22/SHT31
──────         ───────────
3.3V  ──────── VCC
GND   ──────── GND
GPIO4 ──────── DATA (with 10kΩ pull-up)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/Cloud-Connected-Hardware-IoT-Monitor.git
cd Cloud-Connected-Hardware-IoT-Monitor

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Azure Setup

```bash
# Login to Azure
az login

# Create resource group
az group create --name IoTMonitorRG --location westeurope

# Create IoT Hub
az iot hub create --name MyIoTHub --resource-group IoTMonitorRG --sku S1

# Register device
az iot hub device-identity create --hub-name MyIoTHub --device-id ESP32-Sensor-001

# Get connection string
az iot hub device-identity connection-string show --hub-name MyIoTHub --device-id ESP32-Sensor-001
```

### Configuration

Set environment variables:

```bash
# Windows PowerShell
$env:AZURE_IOT_HUB_CONNECTION_STRING="HostName=MyIoTHub.azure-devices.net;DeviceId=ESP32-Sensor-001;SharedAccessKey=..."
$env:TEMPERATURE_WARNING_THRESHOLD="28"
$env:TEMPERATURE_CRITICAL_THRESHOLD="35"
$env:LOG_LEVEL="INFO"
```

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 📊 Metrics Schema

```json
{
  "device_id": "ESP32-Sensor-001",
  "timestamp": "2026-07-24T10:00:00Z",
  "temperature": 24.5,
  "humidity": 45.2,
  "location": "Server Room A",
  "rack_id": "Rack-01",
  "status": "ok"
}
```

## 🎯 Alert Thresholds

| Status | Temperature | Color | Action |
|--------|-------------|-------|--------|
| OK | < 28°C | 🟢 Green | Normal operation |
| Warning | 28-35°C | 🟠 Orange | Monitor closely |
| Critical | > 35°C | 🔴 Red | Take action immediately |

## 🔧 Development Commands

```bash
# Run dashboard
streamlit run app.py

# Run with debug logging
LOG_LEVEL=DEBUG streamlit run app.py

# Flash ESP32 (with PlatformIO)
cd hardware/esp32_sensor
pio run --target upload

# Monitor serial output
pio device monitor

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```

## 📝 Implementation Notes

### Hardware Module (`hardware/`)
- `esp32_sensor/` - Arduino/PlatformIO firmware
- `src/main.cpp` - Main sensor loop
- `src/azure_client.cpp` - Azure IoT Hub connection
- `docs/wiring.png` - Connection diagram

### Core Module (`monitor/core/`)
- `azure_client.py` - Azure IoT Hub SDK wrapper
- `telemetry.py` - Telemetry processing
- `alerts.py` - Alert management

### UI Module (`monitor/ui/`)
- `components.py` - Reusable Streamlit widgets
- `charts.py` - Temperature visualization
- `gauges.py` - Real-time temperature gauges

### Utils Module (`monitor/utils/`)
- `validators.py` - Telemetry validation
- `formatters.py` - Temperature/date formatting
- `notifications.py` - Email/webhook alerts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- Create an issue on GitHub
- Check the hardware docs in `/hardware/docs`
- Review config.py for environment variables
- Azure IoT Hub documentation: https://docs.microsoft.com/azure/iot-hub/