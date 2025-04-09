"""Constants for the Solax integration."""
from datetime import timedelta

# The unique identifier for this integration in Home Assistant
# This must match the domain in manifest.json
DOMAIN = "custom-solax"

# How often to poll the inverter for new data
# Default is every 30 seconds
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)

# How long to wait for a response from the inverter before timing out
DEFAULT_TIMEOUT = 10

# Configuration keys used in the config flow and options
CONF_HOST = "host"        # IP address or hostname of the inverter
CONF_USERNAME = "username"  # Username for authentication
CONF_PASSWORD = "password"  # Password for authentication

# API endpoints for the Solax inverter
# This is the endpoint that provides real-time data
API_REALTIME_DATA = "/api/realTimeData.htm"

# Mapping of raw data keys to friendly sensor names
# This defines what sensors will be created and how they'll be named
SENSOR_TYPES = {
    # System information
    "method": "Method",           # API method used
    "version": "Version",         # Firmware version
    "type": "Type",              # Inverter type/model
    "SN": "Serial Number",       # Inverter serial number
    "Status": "Status",          # Current system status
    
    # PV (Solar Panel) Data - String 1
    "Data_0": "PV1 Voltage",     # Voltage from first PV string
    "Data_1": "PV1 Current",     # Current from first PV string
    "Data_4": "PV1 Power",       # Power from first PV string
    
    # PV (Solar Panel) Data - String 2
    "Data_2": "PV2 Voltage",     # Voltage from second PV string
    "Data_3": "PV2 Current",     # Current from second PV string
    "Data_5": "PV2 Power",       # Power from second PV string
    
    # Grid Data
    "Data_6": "Grid Voltage",    # Grid voltage
    "Data_7": "Grid Current",    # Grid current
    "Data_8": "Grid Power",      # Grid power (positive = export, negative = import)
    "Data_9": "Grid Frequency",  # Grid frequency
    
    # System Data
    "Data_10": "Inverter Temperature",  # Inverter temperature
    "Data_11": "Today's Energy",        # Energy produced today
    "Data_12": "Total Energy",          # Total energy produced
    
    # Battery Data
    "Data_13": "Battery Voltage",       # Battery voltage
    "Data_14": "Battery Current",       # Battery current (positive = charging, negative = discharging)
    "Data_15": "Battery Power",         # Battery power
    "Data_16": "Battery Temperature",   # Battery temperature
    "Data_17": "Battery State of Charge",  # Battery charge percentage
} 