"""Base entity for the Solax integration."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SolaxDataUpdateCoordinator

class SolaxEntity(CoordinatorEntity):
    """Defines a base Solax entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: SolaxDataUpdateCoordinator) -> None:
        """Initialize the Solax entity."""
        super().__init__(coordinator)
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator._host)},
            manufacturer="Solax",
            name="Solax Inverter",
            model=coordinator.data.get("type", "Unknown"),
            sw_version=coordinator.data.get("version", "Unknown"),
        ) 