"""Data update coordinator for the Custom Solax integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_REALTIME_DATA,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

class SolaxDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Solax data."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        host: str,
        username: str,
        password: str,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self._session = session
        self._host = host
        self._username = username
        self._password = password
        self._auth = aiohttp.BasicAuth(username, password)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            async with self._session.get(
                f"http://{self._host}{API_REALTIME_DATA}",
                auth=self._auth,
                timeout=DEFAULT_TIMEOUT,
            ) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Invalid response from Solax inverter: {response.status}")

                data = await response.text()
                
                # Process the data similar to the bash script
                # Replace empty values with 0
                data = data.replace(",,", ",0,")
                
                # Convert to JSON-like structure
                import json
                try:
                    # Split the data into lines and process each line
                    lines = data.split("\n")
                    result = {}
                    for line in lines:
                        if "=" in line:
                            key, value = line.split("=", 1)
                            result[key.strip()] = value.strip()
                    
                    return result
                except Exception as err:
                    raise UpdateFailed(f"Error parsing Solax data: {err}")

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with Solax inverter: {err}")
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") 