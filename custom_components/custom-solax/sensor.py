"""Sensor platform for the Solax integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES
from .coordinator import SolaxDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Solax sensors based on a config entry."""
    coordinator: SolaxDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    _LOGGER.debug("Setting up Solax sensors for entry %s", entry.entry_id)
    _LOGGER.debug("Available data keys: %s", list(coordinator.data.keys()))
    
    entities = []
    for key, name in SENSOR_TYPES.items():
        if key in coordinator.data:
            _LOGGER.debug("Creating sensor for %s (key: %s)", name, key)
            entities.append(SolaxSensor(coordinator, key, name))
        else:
            _LOGGER.warning("Skipping sensor %s (key: %s) - data not available", name, key)
    
    _LOGGER.debug("Adding %d Solax sensors to Home Assistant", len(entities))
    if not entities:
        _LOGGER.error("No sensors were created! Available data: %s", coordinator.data)
    async_add_entities(entities)

class SolaxSensor(CoordinatorEntity, SensorEntity):
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
        
        # Configure the sensor based on its type
        if "Voltage" in name:
            self._attr_device_class = SensorDeviceClass.VOLTAGE
            self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        elif "Current" in name:
            self._attr_device_class = SensorDeviceClass.CURRENT
            self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        elif "Power" in name:
            self._attr_device_class = SensorDeviceClass.POWER
            self._attr_native_unit_of_measurement = UnitOfPower.WATT
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif "Energy" in name:
            self._attr_device_class = SensorDeviceClass.ENERGY
            self._attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        elif "Frequency" in name:
            self._attr_device_class = SensorDeviceClass.FREQUENCY
            self._attr_native_unit_of_measurement = UnitOfFrequency.HERTZ
        elif "Temperature" in name:
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
            self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        elif "Charge" in name:
            self._attr_device_class = SensorDeviceClass.BATTERY
            self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key) 