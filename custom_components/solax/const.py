"""Constants for the Solax integration."""
from datetime import timedelta

DOMAIN = "solax"

DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)
DEFAULT_TIMEOUT = 10

CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# API endpoints
API_REALTIME_DATA = "/api/realTimeData.htm"

# Sensor types
SENSOR_TYPES = {
    "method": "Method",
    "version": "Version",
    "type": "Type",
    "SN": "Serial Number",
    "Status": "Status",
    "Data_0": "PV1 Voltage",
    "Data_1": "PV1 Current",
    "Data_2": "PV2 Voltage",
    "Data_3": "PV2 Current",
    "Data_4": "PV1 Power",
    "Data_5": "PV2 Power",
    "Data_6": "Grid Voltage",
    "Data_7": "Grid Current",
    "Data_8": "Grid Power",
    "Data_9": "Grid Frequency",
    "Data_10": "Inverter Temperature",
    "Data_11": "Today's Energy",
    "Data_12": "Total Energy",
    "Data_13": "Battery Voltage",
    "Data_14": "Battery Current",
    "Data_15": "Battery Power",
    "Data_16": "Battery Temperature",
    "Data_17": "Battery State of Charge",
} 