# 🔆 Custom Solax Solar Integration for Home Assistant

A custom Home Assistant integration for Solax solar inverters that provides real-time monitoring of your solar system's performance.

## 🌟 Features

- Real-time monitoring of solar production
- Battery status and performance tracking
- Grid import/export monitoring
- Temperature monitoring
- Energy production statistics
- Support for multiple inverter models
- Configurable update intervals
- Home Assistant Energy Dashboard integration

## 📊 Available Sensors

- PV Voltage and Current (both strings)
- Grid Voltage, Current, Power, and Frequency
- Inverter Temperature
- Today's and Total Energy Production
- Battery Voltage, Current, Power, Temperature, and State of Charge
- System Status and Information

## 🚀 Installation

### Via HACS:

1. Open the HACS tab in Home Assistant
2. Click the "Three Dots" in the top Right Hand corner
3. Click "Custom repositories"
4. Choose Type: Integration
5. Copy in the link to this repository: https://github.com/BoringKraken/HA-Solax-Solar
6. Click "Add"
7. Find "Custom Solax" in the integrations list
8. Click "Install"

### Manual Installation:

1. Download or clone this repository
2. Copy the `custom-solax` directory into the `custom_components` directory in your Home Assistant configuration directory
3. Restart Home Assistant

## ⚙️ Configuration

After installation, you can configure the integration through the Home Assistant UI:

1. Go to Settings -> Devices & Services
2. Click "Add Integration"
3. Search for "Custom Solax"
4. Enter your inverter's details:
   - Host/IP Address
   - Username
   - Password

## 🔧 Troubleshooting

If you encounter any issues:

1. Check your inverter's network connectivity
2. Verify your credentials are correct
3. Check the Home Assistant logs for any error messages
4. Ensure your inverter's firmware is up to date

## 📝 Notes

- The integration polls the inverter every 30 seconds by default
- All sensors support long-term statistics for historical data
- The integration is designed to work with local network access to the inverter
- Some features may not be available depending on your inverter model

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is a custom integration and is not officially supported by Solax. Use at your own risk.

## Debugging

If you encounter issues with the integration, you can enable debug logging to get more detailed information. To do this:

1. Open your Home Assistant configuration file (`configuration.yaml`)
2. Add the following logger configuration:
   ```yaml
   logger:
     default: info
     logs:
       custom_components.custom_solax: debug
   ```
3. Restart Home Assistant for the changes to take effect

This will enable detailed logging for the Custom Solax integration, which can help diagnose any issues you might encounter.
