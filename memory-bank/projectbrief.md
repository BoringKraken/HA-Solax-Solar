# Project Brief: Home Assistant Custom Solax Solar Integration

## Project Overview
This project is a custom Home Assistant integration for Solax solar inverters that enables real-time monitoring of solar system performance. The integration connects to Solax inverters over the local network, retrieves data, and exposes it as sensors in Home Assistant.

## Project Goals
1. Provide reliable, real-time monitoring of Solax solar inverters in Home Assistant
2. Create a user-friendly integration that follows Home Assistant standards
3. Support various Solax inverter models
4. Expose comprehensive sensor data for solar production, battery status, grid metrics, and more
5. Enable integration with Home Assistant's Energy Dashboard

## Requirements
1. The integration must connect to Solax inverters over the local network
2. Data should be polled at regular intervals (default: 30 seconds)
3. The integration must handle different response formats from Solax inverters
4. All data must be properly processed and exposed as sensors
5. The integration must be configurable through the Home Assistant UI
6. Proper error handling and logging must be implemented

## Constraints
1. The integration must work with Home Assistant version 2023.10.1 or newer
2. All communication is done over HTTP/HTTPS with the inverter's local API
3. Must follow Home Assistant integration standards
4. The integration must be installable via HACS

## Current Status
The integration is functional but has issues processing certain response formats from Solax inverters. The main challenge is parsing the JSON response correctly when it contains empty values in arrays. We have been working on improving the parsing logic to handle these cases.

## Key Files
- `__init__.py`: Core integration setup
- `coordinator.py`: Data update coordinator that handles fetching and processing data
- `sensor.py`: Defines sensor entities based on the processed data
- `config_flow.py`: Handles configuration through the UI
- `const.py`: Constants used throughout the integration
- `entity.py`: Base entity implementation
- `manifest.json`: Integration metadata

## Immediate Focus
Resolving issues with JSON parsing in the coordinator to handle various response formats from Solax inverters. 