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

### Option 1: ESP32 (Recommended for Beginners)

| Component | Approx. Cost | Purpose |
|-----------|--------------|---------|
| ESP32 DevKit v1 | $5-10 | Microcontroller with WiFi |
| DHT22/SHT31 Sensor | $5-15 | Temperature & humidity |
| Breadboard + Wires | $5 | Prototyping |
| USB Cable | $3 | Power & programming |
| 3D Printed Case | $10 | Enclosure (optional) |

**Wiring (ESP32):**
```
ESP32          DHT22/SHT31
──────         ───────────
3.3V  ──────── VCC
GND   ──────── GND
GPIO4 ──────── DATA (with 10kΩ pull-up)
```

### Option 2: Raspberry Pi (Recommended for Advanced Users)

| Component | Approx. Cost | Purpose |
|-----------|--------------|---------|
| Raspberry Pi 4/5 (4GB) | $35-75 | Main controller with WiFi/Ethernet |
| DHT22 Sensor | $5-10 | Temperature & humidity |
| BMP280/BME280 Sensor | $5-15 | Pressure + altitude (optional) |
| MicroSD Card (32GB+) | $10 | OS and data storage |
| Breadboard + Wires | $5 | Prototyping |
| Power Supply (5V 3A) | $10 | Official Pi adapter |

**Wiring (Raspberry Pi):**
```
Raspberry Pi    DHT22 Sensor
──────────      ─────────────
Pin 1 (3.3V) ── VCC
Pin 6 (GND)  ── GND
Pin 7 (GPIO4)── DATA (with 10kΩ pull-up)

Raspberry Pi    BMP280 (I2C)
──────────      ─────────────
Pin 1 (3.3V) ── VCC
Pin 6 (GND)  ── GND
Pin 3 (GPIO2)── SDA (I2C Data)
Pin 5 (GPIO3)── SCL (I2C Clock)
```

**Raspberry Pi Advantages:**
- Full Linux OS for complex processing
- Multiple I2C/SPI sensors simultaneously
- Built-in WiFi/Ethernet connectivity
- GPIO header for easy prototyping
- Support for OLED displays and local logging
- Can run Flask/Streamlit dashboard locally

### Sensor Specifications

| Sensor | Temperature Range | Accuracy | Humidity | Best For |
|--------|-------------------|----------|----------|----------|
| DHT22 | -40°C to 80°C | ±0.5°C | 0-100% RH | Budget-friendly all-rounder |
| SHT31 | -40°C to 125°C | ±0.3°C | 0-100% RH | High precision |
| DS18B20 | -55°C to 125°C | ±0.5°C | N/A | Waterproof probes, 1-Wire |
| BME280 | -40°C to 85°C | ±1.0°C | 0-100% RH | All-in-one (temp+humidity+pressure) |

**Update Interval**: Configurable (10s - 5min)
**Power**: USB or battery (ESP32/Pi low-power modes available)

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
├── hardware/
│   ├── esp32_sensor/         # ESP32 Arduino/PlatformIO code
│   │   ├── src/
│   │   │   ├── main.cpp
│   │   │   └── azure_client.cpp
│   │   └── platformio.ini
│   ├── raspberry_pi/         # Raspberry Pi Python code
│   │   ├── sensor_reader.py
│   │   ├── azure_sender.py
│   │   └── requirements.txt
│   └── docs/                 # Wiring diagrams and hardware guides
│       ├── esp32_wiring.png
│       └── raspberry_pi_wiring.png
├── azure/                    # Azure ARM templates
│   ├── iot-hub.json
│   └── time-series.json
└── requirements.txt          # Python dependencies
```

## 🆚 ESP32 vs Raspberry Pi: Which to Choose?

| Feature | ESP32 | Raspberry Pi |
|---------|-------|--------------|
| **Cost** | $5-10 | $35-75 |
| **Power Consumption** | Very low (deep sleep available) | Higher (1-5W) |
| **Processing Power** | Limited (240MHz dual-core) | High (1.5GHz+ quad-core) |
| **Memory** | 520KB SRAM | 1-8GB RAM |
| **OS** | None (bare metal) | Full Linux |
| **Connectivity** | WiFi + Bluetooth | WiFi + Ethernet + Bluetooth |
| **GPIO** | 34 pins | 40 pins |
| **Best For** | Simple, battery-powered sensors | Complex processing, local dashboards |
| **Programming** | C++/Arduino or MicroPython | Python, Node.js, any Linux language |
| **Multiple Sensors** | Limited | Many (I2C/SPI bus support) |
| **Local Display** | OLED (small) | HDMI monitor, touchscreen |

**Choose ESP32 if:**
- You want low power consumption
- Budget is tight
- Simple temperature monitoring only
- Battery-powered deployment needed

**Choose Raspberry Pi if:**
- You need complex data processing
- Want to run dashboard locally
- Multiple sensors simultaneously
- Future expansion planned
- Educational purposes (learn Linux/networking)

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

**Hardware (Choose one):**

**Option A - ESP32:**
- ESP32 DevKit v1
- DHT22 or SHT31 temperature sensor
- Jumper wires and breadboard
- USB cable for programming

**Option B - Raspberry Pi:**
- Raspberry Pi 4/5 (4GB+ RAM)
- DHT22 or BME280 sensor
- MicroSD card (32GB+)
- Power supply (5V 3A)
- Breadboard and jumper wires

**Software:**
- Python 3.10+
- Arduino IDE/PlatformIO (ESP32) or Raspberry Pi OS (Pi)
- Azure account (free tier available)
- Azure CLI (optional)

### Hardware Assembly

**ESP32:**
```
ESP32          DHT22/SHT31
──────         ───────────
3.3V  ──────── VCC
GND   ──────── GND
GPIO4 ──────── DATA (with 10kΩ pull-up)
```

**Raspberry Pi:**
```
Raspberry Pi    DHT22 Sensor
──────────      ─────────────
Pin 1 (3.3V) ── VCC
Pin 6 (GND)  ── GND
Pin 7 (GPIO4)── DATA (with 10kΩ pull-up)
```

### Raspberry Pi Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Enable I2C and 1-Wire interfaces
sudo raspi-config
# Navigate to: Interface Options → I2C → Enable
# Navigate to: Interface Options → 1-Wire → Enable

# Reboot
sudo reboot

# Install Python dependencies
sudo apt install python3-pip python3-venv libgpiod2 -y

# Create project directory
mkdir ~/iot-monitor && cd ~/iot-monitor
python3 -m venv venv
source venv/bin/activate

# Install libraries
pip install adafruit-circuitpython-dht
pip install azure-iot-device
pip install streamlit
```

### ESP32 Setup

```bash
# Install PlatformIO
pip install platformio

# Create project
mkdir esp32_sensor && cd esp32_sensor
pio init --board esp32dev

# Install libraries
pio lib install "DHT sensor library"
pio lib install "Azure IoT Hub Arduino"
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

## 💡 Raspberry Pi Quick Start Code

### sensor_reader.py
```python
import time
import board
import adafruit_dht
from azure.iot.device import IoTHubDeviceClient, Message

# Initialize sensor
dht = adafruit_dht.DHT22(board.D4)

# Azure IoT Hub connection string
CONNECTION_STRING = "HostName=YourHub.azure-devices.net;DeviceId=YourDevice;SharedAccessKey=YourKey"

def read_temperature():
    try:
        temp = dht.temperature
        humidity = dht.humidity
        return {"temperature": temp, "humidity": humidity}
    except RuntimeError as e:
        print(f"Sensor error: {e}")
        return None

def send_to_azure(data):
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    message = Message(str(data))
    client.send_message(message)
    print(f"Sent to Azure: {data}")
    client.shutdown()

if __name__ == "__main__":
    while True:
        data = read_temperature()
        if data:
            send_to_azure(data)
        time.sleep(60)  # Send every 60 seconds
```

## 🔧 Development Commands

### Dashboard Commands
```bash
# Run dashboard
streamlit run app.py

# Run with debug logging
LOG_LEVEL=DEBUG streamlit run app.py

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```

### ESP32 Commands
```bash
# Flash ESP32 (with PlatformIO)
cd hardware/esp32_sensor
pio run --target upload

# Monitor serial output
pio device monitor

# Build without uploading
pio run
```

### Raspberry Pi Commands
```bash
# SSH into Raspberry Pi
ssh pi@<pi-ip-address>

# Run sensor reader
cd ~/iot-monitor
source venv/bin/activate
python sensor_reader.py

# Run as systemd service
sudo systemctl enable iot-monitor
sudo systemctl start iot-monitor

# View logs
sudo journalctl -u iot-monitor -f

# Enable I2C/SPI interfaces
sudo raspi-config
# Interface Options → I2C → Enable
# Interface Options → 1-Wire → Enable

# Check connected I2C devices
sudo i2cdetect -y 1
```

## 📝 Implementation Notes

### Hardware Module (`hardware/`)

**ESP32 (`esp32_sensor/`):**
- `src/main.cpp` - Main sensor loop
- `src/azure_client.cpp` - Azure IoT Hub connection
- `platformio.ini` - PlatformIO configuration

**Raspberry Pi (`raspberry_pi/`):**
- `sensor_reader.py` - DHT22/BME280 sensor reading
- `azure_sender.py` - Azure IoT Hub MQTT publisher
- `local_logger.py` - CSV/file logging
- `requirements.txt` - Pi-specific dependencies

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