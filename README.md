# Cloud-Connected Hardware IoT Monitor

A real-time monitoring system for Azure File Share storage capacity using IoT agents, with a Streamlit dashboard for visualization and alerting.

## 📋 Project Overview

This project monitors disk usage on Azure File Shares through distributed IoT agents, collects metrics, and displays them in a web dashboard with threshold-based alerts.

### Key Features

- **Real-time Monitoring**: Track storage capacity across multiple Azure File Shares
- **IoT Agent Architecture**: Distributed agents collect and report metrics
- **Streamlit Dashboard**: Interactive web UI with KPIs, charts, and status indicators
- **Threshold Alerting**: Warning (70%) and Critical (85%) alerts
- **JSON Schema Validation**: Structured data format for consistent metrics collection
- **Azure Integration**: Native support for Azure Storage accounts and file shares

## 🏗️ Architecture

```
┌─────────────────────┐
│   IoT Agents        │  ← Collect metrics from Azure File Shares
│   (data collectors) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Azure File Share  │  ← Store latest_reading.json
│   (shared storage)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Streamlit App     │  ← Display dashboard with KPIs
│   (dashboard)       │
└─────────────────────┘
```

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
└── requirements.txt          # Python dependencies
```

## 🚀 Development Roadmap

### Phase 1: Core Infrastructure ✅ (Completed)
- [x] Project structure setup
- [x] Central configuration with Azure env vars
- [x] JSON schema definition for metrics
- [x] Threshold constants (warning: 70%, critical: 85%)
- [x] Basic Streamlit dashboard with KPI cards

### Phase 2: Data Collection (In Progress)
- [ ] Implement Azure File Share client in `monitor/core/`
- [ ] Create metrics collector that reads file share stats
- [ ] Build agent registration system
- [ ] Add timestamp and metadata handling
- [ ] Implement local file caching for offline mode

### Phase 3: Dashboard Enhancement
- [ ] Add historical charts (plotly/matplotlib)
- [ ] Implement auto-refresh with `st.rerun()`
- [ ] Add multi-agent comparison view
- [ ] Create alert history log
- [ ] Add export functionality (CSV/JSON)

### Phase 4: Advanced Features
- [ ] WebSocket real-time updates
- [ ] Email/Slack notifications for alerts
- [ ] Multi-region support
- [ ] Role-based access control
- [ ] API endpoints for external integrations

### Phase 5: Production Deployment
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Azure Container Instances deployment
- [ ] Monitoring and logging (Application Insights)
- [ ] Performance optimization

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- Azure Storage Account with File Share
- Azure credentials (account name + key)

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

### Configuration

Set environment variables:

```bash
# Windows PowerShell
$env:AZURE_STORAGE_ACCOUNT="your_account_name"
$env:AZURE_STORAGE_KEY="your_account_key"
$env:AZURE_FILE_SHARE_NAME="your_share_name"
$env:POLL_INTERVAL_SECONDS="300"
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
  "agent_id": "agent-001",
  "timestamp": "2026-07-24T10:00:00Z",
  "metrics": {
    "total_gb": 100.0,
    "used_gb": 72.5,
    "free_gb": 27.5,
    "usage_pct": 72.5
  },
  "tags": {
    "region": "westeurope",
    "env": "production",
    "share_name": "iot-data"
  },
  "suffix_status": "warning"
}
```

## 🎯 Alert Thresholds

| Status | Usage % | Color | Action |
|--------|---------|-------|--------|
| OK | < 70% | 🟢 Green | Normal operation |
| Warning | 70-85% | 🟠 Orange | Monitor closely |
| Critical | > 85% | 🔴 Red | Take action |

## 🔧 Development Commands

```bash
# Run dashboard
streamlit run app.py

# Run with debug logging
LOG_LEVEL=DEBUG streamlit run app.py

# Run entry point (for agent mode)
python main.py

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```

## 📝 Implementation Notes

### Core Module (`monitor/core/`)
- `azure_client.py` - Azure File Share API wrapper
- `collector.py` - Metrics collection logic
- `agent.py` - Agent lifecycle management

### UI Module (`monitor/ui/`)
- `components.py` - Reusable Streamlit widgets
- `charts.py` - Plotly/matplotlib chart functions
- `alerts.py` - Alert display components

### Utils Module (`monitor/utils/`)
- `validators.py` - JSON schema validation
- `formatters.py` - Number/date formatting
- `notifications.py` - Email/Slack integration

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
- Check the docs in `/docs` folder
- Review config.py for environment variables