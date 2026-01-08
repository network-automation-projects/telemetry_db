# Telemetry DB

A Python-based network telemetry database manager for storing, querying, and analyzing network device performance metrics. Uses SQLite to store telemetry data including latency and packet loss measurements.

## Features

- **Database Management**: Initialize and manage SQLite database for network telemetry data
- **Mock Data Generation**: Generate random telemetry data for testing and demonstration
- **Query Capabilities**: 
  - Average latency per device
  - High latency event detection with configurable thresholds
- **Data Export**: Export telemetry data to JSON format
- **Logging**: Comprehensive logging to `logs/telemetry.log`

## Requirements

- Python 3.9+
- Standard library only (no external dependencies)

## Installation

1. Clone or navigate to the project directory:
```bash
cd telemetry_db
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Usage

The script uses command-line arguments to perform various operations:

### Initialize Database

Create the database and table structure:
```bash
python telemetry_manager.py --init
```

### Insert Mock Data

Insert random mock telemetry records:
```bash
python telemetry_manager.py --insert 50
```

### Query Average Latency

Display average latency per device:
```bash
python telemetry_manager.py --avg
```

### Query High Latency Events

Find recent events exceeding a latency threshold (default: 100ms):
```bash
python telemetry_manager.py --high 80
```

### Export to JSON

Export all telemetry data to JSON:
```bash
python telemetry_manager.py --export
```

### Combined Operations

You can combine multiple operations in a single command:
```bash
python telemetry_manager.py --init --insert 50 --avg --high 80 --export
```

## Database Schema

The `telemetry` table contains the following fields:

- `id`: Primary key (auto-increment)
- `device`: Device name/hostname (TEXT)
- `latency_ms`: Latency in milliseconds (REAL)
- `packet_loss`: Packet loss percentage (REAL)
- `timestamp`: ISO format timestamp (TEXT)

## Project Structure

```
telemetry_db/
├── telemetry_manager.py    # Main script
├── data/                    # Database and exports
│   ├── network_telemetry.db
│   └── latest_telemetry.json
└── logs/                    # Application logs
    └── telemetry.log
```

## Example Output

### Average Latency Query
```
Average Latency per Device:
Device               Avg Latency (ms)
-----------------------------------
router-nyc-01        125.43
switch-lax-02        98.21
fw-ams-01            87.65
```

### High Latency Events
```
Recent High Latency Events (> 100.0 ms):
Device               Latency (ms)    Timestamp
--------------------------------------------------
router-nyc-01        156.78          2024-01-15T10:30:45
switch-lax-02        134.22          2024-01-15T10:29:12
```

## Logging

All operations are logged to `logs/telemetry.log` with timestamps and log levels. The log file is automatically created if it doesn't exist.

## Notes

- The database file (`data/network_telemetry.db`) is created automatically on first use
- Mock data includes devices: `router-nyc-01`, `switch-lax-02`, `fw-ams-01`, `ap-sfo-03`, `core-router-01`
- Latency values in mock data range from 1.0 to 200.0 ms
- Packet loss values in mock data range from 0.0 to 5.0%

## Future Enhancements

Potential improvements:
- Real-time telemetry collection from network devices
- Additional query types (packet loss analysis, time-series trends)
- Web dashboard for visualization
- Alerting for threshold violations
- Support for multiple database backends
