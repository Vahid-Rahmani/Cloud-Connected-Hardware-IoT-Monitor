from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from collector import collect_status


app = FastAPI(
    title="Windows Infrastructure Monitor"
)


@app.get("/api/devices")
def api_devices():
    return collect_status()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    devices = collect_status()

    online_count = sum(
        1 for device in devices
        if device["online"]
    )

    total_count = len(devices)

    rows = ""

    for device in devices:
        status = (
            "🟢 ONLINE"
            if device["online"]
            else "🔴 OFFLINE"
        )

        cpu = (
            device["cpu"]
            if device["cpu"] is not None
            else "-"
        )

        ram = (
            device["ram"]
            if device["ram"] is not None
            else "-"
        )

        disk = (
            device["disk"]
            if device["disk"] is not None
            else "-"
        )

        uptime = (
            device["uptime"]
            if device["uptime"] is not None
            else "-"
        )

        rows += f"""
        <tr>
            <td>{device["name"]}</td>
            <td>{device["type"]}</td>
            <td>{device["ip"]}</td>
            <td>{status}</td>
            <td>{cpu}%</td>
            <td>{ram}%</td>
            <td>{disk}%</td>
            <td>{uptime} h</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <meta
            http-equiv="refresh"
            content="30"
        >

        <title>
            Windows Infrastructure Monitor
        </title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 40px;
                font-family:
                    Arial,
                    Helvetica,
                    sans-serif;
                background: #0f172a;
                color: #f8fafc;
            }}

            .container {{
                max-width: 1400px;
                margin: auto;
            }}

            h1 {{
                margin-bottom: 5px;
            }}

            .subtitle {{
                color: #94a3b8;
                margin-bottom: 30px;
            }}

            .summary-grid {{
                display: grid;
                grid-template-columns:
                    repeat(
                        auto-fit,
                        minmax(200px, 1fr)
                    );
                gap: 20px;
                margin-bottom: 30px;
            }}

            .card {{
                background: #1e293b;
                border-radius: 12px;
                padding: 20px;
            }}

            .card-title {{
                color: #94a3b8;
                font-size: 14px;
                margin-bottom: 10px;
            }}

            .card-value {{
                font-size: 28px;
                font-weight: bold;
            }}

            .table-container {{
                overflow-x: auto;
                background: #1e293b;
                border-radius: 12px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th {{
                text-align: left;
                padding: 16px;
                background: #334155;
                color: #f8fafc;
            }}

            td {{
                padding: 16px;
                border-bottom:
                    1px solid #334155;
            }}

            tr:hover {{
                background: #263449;
            }}

            .footer {{
                margin-top: 20px;
                color: #64748b;
                font-size: 13px;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>
                Windows Infrastructure Monitor
            </h1>

            <div class="subtitle">
                Domain: kurs.intern
            </div>

            <div class="summary-grid">

                <div class="card">
                    <div class="card-title">
                        Total Devices
                    </div>

                    <div class="card-value">
                        {total_count}
                    </div>
                </div>

                <div class="card">
                    <div class="card-title">
                        Online Devices
                    </div>

                    <div class="card-value">
                        {online_count}
                    </div>
                </div>

                <div class="card">
                    <div class="card-title">
                        Offline Devices
                    </div>

                    <div class="card-value">
                        {total_count - online_count}
                    </div>
                </div>

            </div>

            <div class="table-container">

                <table>

                    <thead>

                        <tr>
                            <th>Device</th>
                            <th>Role</th>
                            <th>IP Address</th>
                            <th>Status</th>
                            <th>CPU</th>
                            <th>RAM</th>
                            <th>Disk</th>
                            <th>Uptime</th>
                        </tr>

                    </thead>

                    <tbody>
                        {rows}
                    </tbody>

                </table>

            </div>

            <div class="footer">
                Auto-discovered from Active Directory.
                Refresh interval: 30 seconds.
            </div>

        </div>

    </body>

    </html>
    """

    return html