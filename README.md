# Network Telemetry Manager (Python + SQLite)

A simple telemetry collection and analysis tool built to practice skills for network reliability/DevOps roles.

## Purpose
Demonstrates handling infrastructure telemetry data:
- Storing mock network metrics (latency, packet loss)
- Querying averages and high-latency events
- Exporting for dashboards/APIs
- Relevant to tools like Prometheus, Grafana, Solarwinds

## Features
- Initialize SQLite database with telemetry schema
- Insert random mock data for multiple devices
- Query average latency per device
- Find recent high-latency events (configurable threshold)
- Export full dataset to JSON
- Comprehensive logging and CLI interface

## Usage
```bash
python telemetry_manager.py --init --insert 100 --avg --high 80 --export
