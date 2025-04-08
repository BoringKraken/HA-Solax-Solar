"""Sensor platform for the Solax integration."""
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
    """Set up Solax sensors based on a config entry."""
    coordinator: SolaxDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for key, name in SENSOR_TYPES.items():
        if key in coordinator.data:
            entities.append(SolaxSensor(coordinator, key, name))
    
    async_add_entities(entities)

class SolaxSensor(SolaxEntity, SensorEntity):
    """Representation of a Solax sensor."""

    def __init__(
        self,
        coordinator: SolaxDataUpdateCoordinator,
        key: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Solax {name}"
        self._attr_unique_id = f"{coordinator._host}_{key}"
        
        # Set device class and unit of measurement based on the sensor type
        if "Voltage" in name:
            self._attr_device_class = SensorDeviceClass.VOLTAGE
            self._attr_native_unit_of_measurement = ELECTRIC_POTENTIAL_VOLT
        elif "Current" in name:
            self._attr_device_class = SensorDeviceClass.CURRENT
            self._attr_native_unit_of_measurement = ELECTRIC_CURRENT_AMPERE
        elif "Power" in name:
            self._attr_device_class = SensorDeviceClass.POWER
            self._attr_native_unit_of_measurement = POWER_WATT
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif "Energy" in name:
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif "Frequency" in name:
            self._attr_device_class = SensorDeviceClass.FREQUENCY
            self._attr_native_unit_of_measurement = FREQUENCY_HERTZ
        elif "Temperature" in name:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = TEMP_CELSIUS
        elif "Charge" in name:
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        value = self.coordinator.data.get(self._key)
        try:
            return float(value) if value is not None else None
        except (TypeError, ValueError):
            return value 