import sqlite3
from pathlib import Path
from datetime import datetime
import logging
import argparse
import json
import random

# Setup directories and logging
Path('data').mkdir(exist_ok=True)
Path('logs').mkdir(exist_ok=True)

logging.basicConfig(
    filename='logs/telemetry.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_PATH = 'data/network_telemetry.db'

def init_db():
    """Create the database and table if they don't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device TEXT NOT NULL,
                latency_ms REAL,
                packet_loss REAL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        logging.info("Database initialized successfully")
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {e}")
        raise

def insert_mock_data(num_records: int = 20):
    """Insert random mock telemetry data."""
    devices = ['router-nyc-01', 'switch-lax-02', 'fw-ams-01', 'ap-sfo-03', 'core-router-01']
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for _ in range(num_records):
            device = random.choice(devices)
            latency = random.uniform(1.0, 200.0)  # ms
            packet_loss = random.uniform(0.0, 5.0)  # %
            timestamp = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO telemetry (device, latency_ms, packet_loss, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (device, latency, packet_loss, timestamp))
        conn.commit()
        logging.info(f"Inserted {num_records} mock records")
        conn.close()
    except sqlite3.Error as e:
        logging.error(f"Insert failed: {e}")
        raise

def query_average_latency():
    """Query average latency per device."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT device, AVG(latency_ms) as avg_latency
            FROM telemetry
            GROUP BY device
            ORDER BY avg_latency DESC
        ''')
        results = cursor.fetchall()
        conn.close()
        
        logging.info("Queried average latency per device")
        print("\nAverage Latency per Device:")
        print("Device".ljust(20), "Avg Latency (ms)")
        print("-" * 35)
        for row in results:
            print(f"{row[0].ljust(20)} {row[1]:.2f}")
        return results
    except sqlite3.Error as e:
        logging.error(f"Query failed: {e}")
        raise

def query_high_latency_events(threshold: float = 100.0):
    """Find recent events with high latency."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT device, latency_ms, timestamp
            FROM telemetry
            WHERE latency_ms > ?
            ORDER BY timestamp DESC
            LIMIT 10
        ''', (threshold,))
        results = cursor.fetchall()
        conn.close()
        
        logging.info(f"Queried high latency events (> {threshold} ms)")
        print(f"\nRecent High Latency Events (> {threshold} ms):")
        if results:
            print("Device".ljust(20), "Latency (ms)".ljust(15), "Timestamp")
            print("-" * 50)
            for row in results:
                print(f"{row[0].ljust(20)} {row[1]:.2f}".ljust(35), row[2])
        else:
            print("No high latency events found.")
        return results
    except sqlite3.Error as e:
        logging.error(f"Query failed: {e}")
        raise

def export_to_json(filename: str = "data/latest_telemetry.json"):
    """Export all data to JSON."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM telemetry ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        conn.close()
        
        Path(filename).parent.mkdir(exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logging.info(f"Exported telemetry data to {filename}")
        print(f"\nData exported to {filename}")
    except Exception as e:
        logging.error(f"Export failed: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Telemetry Manager")
    parser.add_argument('--init', action='store_true', help="Initialize database")
    parser.add_argument('--insert', type=int, default=0, help="Insert N mock records")
    parser.add_argument('--avg', action='store_true', help="Show average latency per device")
    parser.add_argument('--high', type=float, default=100.0, help="Show high latency events (threshold in ms)")
    parser.add_argument('--export', action='store_true', help="Export all data to JSON")
    
    args = parser.parse_args()
    
    try:
        if args.init:
            init_db()
        
        if args.insert > 0:
            init_db()  # Ensure DB exists
            insert_mock_data(args.insert)
        
        if args.avg:
            init_db()
            query_average_latency()
        
        if args.high:
            init_db()
            query_high_latency_events(args.high)
        
        if args.export:
            init_db()
            export_to_json()
        
        if not any(vars(args).values()):
            print("No action specified. Use --help for options.")
            print("Example: python telemetry_manager.py --init --insert 50 --avg --high 80 --export")
    
    except Exception as e:
        print(f"Error: {e}")