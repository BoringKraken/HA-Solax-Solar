"""Base entity for the Custom Solax integration."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SolaxDataUpdateCoordinator

class SolaxEntity(CoordinatorEntity):
    """
    Defines a base Solax entity.
    
    This is the base class for all entities in this integration.
    It provides common functionality and device information.
    
    Attributes:
        _attr_has_entity_name: Whether the entity name should be prefixed with the device name
    """

    # Don't prefix entity names with the device name
    _attr_has_entity_name = True

    def __init__(self, coordinator: SolaxDataUpdateCoordinator) -> None:
        """
        Initialize the Solax entity.
        
        Args:
            coordinator: The coordinator that provides the data
        """
        super().__init__(coordinator)
        
        # Set up device information
        # This creates a device in Home Assistant that all sensors will be grouped under
        self._attr_device_info = DeviceInfo(
            # Unique identifier for the device
            identifiers={(DOMAIN, coordinator._host)},
            # Manufacturer name
            manufacturer="Solax",
            # Device name
            name="Solax Inverter",
            # Device model (from inverter data)
            model=coordinator.data.get("type", "Unknown"),
            # Firmware version (from inverter data)
            sw_version=coordinator.data.get("version", "Unknown"),
        ) 