# Cloud-Connected Hardware & AI Monitoring

A Raspberry Pi and ESP32 monitoring project that connects physical devices, cloud telemetry and practical operations dashboards.

This is Vahid Rahmani's Raspberry Pi project. The repository combines two connected tracks:

1. **Environmental IoT monitoring** - temperature and humidity telemetry from ESP32/Raspberry Pi devices through MQTT or HTTPS into Azure IoT Hub and a Streamlit dashboard.
2. **AI-assisted system monitoring** - a planned edge-monitoring layer for Raspberry Pi health, performance metrics, baseline learning, anomaly detection and actionable incident explanations.

## Environmental IoT monitoring

- Temperature and humidity sensing for server rooms or lab environments
- ESP32 and Raspberry Pi hardware options
- DHT22, SHT31, DS18B20 and BME280 sensor support planning
- MQTT/HTTPS telemetry
- Azure IoT Hub connectivity
- Streamlit visualisation, history and threshold-based alerts
- Multi-zone monitoring roadmap

## AI-assisted Raspberry Pi monitoring

The next development track extends the same Raspberry Pi project to monitor the device itself:

- CPU, memory, disk, temperature and uptime metrics
- Network reachability, latency and interface health
- Process and service checks
- Local SQLite history
- Baseline learning and lightweight anomaly detection
- Evidence-based alert severity
- Optional AI-assisted explanations of detected incidents
- FastAPI health endpoints and a lightweight local dashboard

The AI layer is designed as an explanation and prioritisation aid. Core monitoring remains measurable, local and useful without a paid AI service.

## Architecture

~~~text
Sensors / Raspberry Pi system metrics
              ↓
     Edge collector and validation
              ↓
   MQTT or HTTPS / local SQLite history
              ↓
Azure IoT Hub telemetry + local monitoring APIs
              ↓
Streamlit dashboard + anomaly detection
              ↓
Optional AI incident explanation + alerts
~~~

## Hardware options

| Platform | Best fit |
|---|---|
| ESP32 | Low-cost sensor telemetry and low-power deployments |
| Raspberry Pi 4/5 | Linux-based collection, local processing, dashboards and system monitoring |

## Planned stack

Python · C++ / MicroPython · Raspberry Pi OS · MQTT · Azure IoT Hub · Streamlit · FastAPI · SQLite · lightweight anomaly detection

## Roadmap

- [x] Establish the hardware and telemetry project foundation
- [x] Define the Azure IoT and dashboard direction
- [ ] Complete ESP32/Raspberry Pi sensor telemetry
- [ ] Add local Raspberry Pi system metrics
- [ ] Add SQLite history and health endpoints
- [ ] Implement baseline learning and anomaly detection
- [ ] Add the first local monitoring dashboard
- [ ] Add optional AI incident explanations
- [ ] Document service installation, security and deployment

## Scope boundary

This repository is intentionally the single Raspberry Pi project. It is separate from the Windows Server and Active Directory work in [Automated Hybrid Network Monitoring Dashboard](https://github.com/Vahid-Rahmani/Automated-Hybrid-Network-Monitoring-Dashboard).

## Author

Designed and developed by [Vahid Rahmani](https://github.com/Vahid-Rahmani).

## License

Project licensing and hardware documentation will be defined as the implementation is stabilised.