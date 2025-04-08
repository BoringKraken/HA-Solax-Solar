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

# Set up logging
_LOGGER = logging.getLogger(__name__)

class SolaxDataUpdateCoordinator(DataUpdateCoordinator):
    """
    Class to manage fetching Solax data.
    
    This coordinator handles:
    - Fetching data from the inverter at regular intervals
    - Processing the raw data into a usable format
    - Providing the data to all sensors
    - Error handling and retries
    """

    def __init__(
        self,
        hass: HomeAssistant,
        session: aiohttp.ClientSession,
        host: str,
        username: str,
        password: str,
    ) -> None:
        """
        Initialize the coordinator.
        
        Args:
            hass: Home Assistant instance
            session: aiohttp session for making HTTP requests
            host: IP address or hostname of the inverter
            username: Username for authentication
            password: Password for authentication
        """
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        # Store connection details
        self._session = session
        self._host = host
        self._username = username
        self._password = password
        self._auth = aiohttp.BasicAuth(username, password)

    async def _async_update_data(self) -> dict[str, Any]:
        """
        Fetch and process data from the inverter.
        
        This method is called by the coordinator at regular intervals.
        It:
        1. Makes an HTTP request to the inverter
        2. Processes the response
        3. Returns the processed data
        
        Returns:
            dict: Processed data from the inverter
            
        Raises:
            UpdateFailed: If there's an error fetching or processing the data
        """
        try:
            # Make HTTP request to the inverter
            async with self._session.get(
                f"http://{self._host}{API_REALTIME_DATA}",
                auth=self._auth,
                timeout=DEFAULT_TIMEOUT,
            ) as response:
                # Check if the request was successful
                if response.status != 200:
                    raise UpdateFailed(f"Invalid response from Solax inverter: {response.status}")

                # Get the raw data from the response
                data = await response.text()
                
                # Process the data similar to the bash script
                # Replace empty values with 0 to handle missing data
                data = data.replace(",,", ",0,")
                
                try:
                    # Split the data into lines and process each line
                    lines = data.split("\n")
                    result = {}
                    
                    # Process each line of the response
                    for line in lines:
                        # Look for key=value pairs
                        if "=" in line:
                            # Split the line into key and value
                            key, value = line.split("=", 1)
                            # Store the processed data
                            result[key.strip()] = value.strip()
                    
                    return result
                    
                except Exception as err:
                    # Handle any errors during data processing
                    raise UpdateFailed(f"Error parsing Solax data: {err}")

        except aiohttp.ClientError as err:
            # Handle network/connection errors
            raise UpdateFailed(f"Error communicating with Solax inverter: {err}")
        except Exception as err:
            # Handle any other unexpected errors
            raise UpdateFailed(f"Unexpected error: {err}") 