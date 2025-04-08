"""Sensor platform for the Custom Solax integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    FREQUENCY_HERTZ,
    POWER_WATT,
    TEMP_CELSIUS,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, SENSOR_TYPES
from .coordinator import SolaxDataUpdateCoordinator
from .entity import SolaxEntity

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """
    Set up Solax sensors based on a config entry.
    
    This function is called by Home Assistant when the integration is set up.
    It creates a sensor for each data point available from the inverter.
    
    Args:
        hass: Home Assistant instance
        entry: Configuration entry for this integration
        async_add_entities: Callback to add entities to Home Assistant
    """
    # Get the coordinator for this config entry
    coordinator: SolaxDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Create a list to store all sensors
    entities = []
    
    # Create a sensor for each data point defined in SENSOR_TYPES
    for key, name in SENSOR_TYPES.items():
        # Only create sensors for data that's actually available
        if key in coordinator.data:
            entities.append(SolaxSensor(coordinator, key, name))
    
    # Add all created sensors to Home Assistant
    async_add_entities(entities)

class SolaxSensor(SolaxEntity, SensorEntity):
    """
    Representation of a Solax sensor.
    
    This class represents a single sensor in Home Assistant.
    It handles:
    - Setting up the sensor with the correct name and unique ID
    - Configuring the appropriate device class and units
    - Providing the current value of the sensor
    """

    def __init__(
        self,
        coordinator: SolaxDataUpdateCoordinator,
        key: str,
        name: str,
    ) -> None:
        """
        Initialize the sensor.
        
        Args:
            coordinator: The coordinator that provides the data
            key: The key used to get the value from the coordinator's data
            name: The friendly name of the sensor
        """
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Solax {name}"
        self._attr_unique_id = f"{coordinator._host}_{key}"
        
        # Configure the sensor based on its type
        if "Voltage" in name:
            # Voltage sensors (PV, Grid, Battery)
            self._attr_device_class = SensorDeviceClass.VOLTAGE
            self._attr_native_unit_of_measurement = ELECTRIC_POTENTIAL_VOLT
        elif "Current" in name:
            # Current sensors (PV, Grid, Battery)
            self._attr_device_class = SensorDeviceClass.CURRENT
            self._attr_native_unit_of_measurement = ELECTRIC_CURRENT_AMPERE
        elif "Power" in name:
            # Power sensors (PV, Grid, Battery)
            self._attr_device_class = SensorDeviceClass.POWER
            self._attr_native_unit_of_measurement = POWER_WATT
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif "Energy" in name:
            # Energy sensors (Today's, Total)
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif "Frequency" in name:
            # Grid frequency sensor
            self._attr_device_class = SensorDeviceClass.FREQUENCY
            self._attr_native_unit_of_measurement = FREQUENCY_HERTZ
        elif "Temperature" in name:
            # Temperature sensors (Inverter, Battery)
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = TEMP_CELSIUS
        elif "Charge" in name:
            # Battery state of charge sensor
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self) -> StateType:
        """
        Return the current value of the sensor.
        
        This property is called by Home Assistant to get the current value.
        It:
        1. Gets the raw value from the coordinator's data
        2. Converts it to a float if possible
        3. Returns None if the value is not available
        
        Returns:
            The current value of the sensor, or None if not available
        """
        # Get the value from the coordinator's data
        value = self.coordinator.data.get(self._key)
        try:
            # Try to convert to float for numerical values
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            # Return as-is for non-numerical values
            return value 