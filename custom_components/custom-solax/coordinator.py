"""Data update coordinator for the Solax integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any
import re

import aiohttp
import json
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_REALTIME_DATA, DEFAULT_TIMEOUT, DOMAIN, SENSOR_TYPES

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
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self._session = session
        self._host = host
        self._username = username
        self._password = password
        self._url = f"http://{host}{API_REALTIME_DATA}"
        self._processed_data = {}
        _LOGGER.info("Initialized Solax coordinator with URL: %s", self._url)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the Solax inverter."""
        try:
            _LOGGER.info("Attempting to fetch data from URL: %s", self._url)
            _LOGGER.debug("Using credentials - Username: %s, Password: %s", self._username, "***")
            
            async with self._session.get(
                self._url,
                auth=aiohttp.BasicAuth(self._username, self._password),
                timeout=DEFAULT_TIMEOUT,
            ) as response:
                _LOGGER.info("Response status: %s", response.status)
                _LOGGER.debug("Response headers: %s", response.headers)
                
                if response.status != 200:
                    error_text = await response.text()
                    _LOGGER.error(
                        "Error fetching data from Solax inverter. Status: %s, Response: %s",
                        response.status,
                        error_text,
                    )
                    raise UpdateFailed(f"Error fetching data: {response.status}")

                # Get the raw text response
                text_response = await response.text()
                _LOGGER.debug("Raw response: %s", text_response)
                
                # Extract the Data array content
                data_match = re.search(r'"Data":\[(.*?)\]', text_response)
                if not data_match:
                    raise UpdateFailed("Could not find Data array in response")
                
                # Split the data array into individual values
                data_values = data_match.group(1).split(',')
                
                # Replace empty values with null
                cleaned_values = ['null' if not value.strip() else value for value in data_values]
                
                # Reconstruct the JSON with cleaned data array
                cleaned_response = text_response.replace(
                    data_match.group(0),
                    f'"Data":[{",".join(cleaned_values)}]'
                )
                
                _LOGGER.debug("Cleaned response: %s", cleaned_response)
                
                # Try to parse as JSON
                try:
                    data = json.loads(cleaned_response)
                    _LOGGER.debug("Successfully parsed JSON data: %s", data)
                except json.JSONDecodeError as err:
                    _LOGGER.error("Error decoding JSON response: %s", err)
                    _LOGGER.error("Original response: %s", text_response)
                    _LOGGER.error("Cleaned response: %s", cleaned_response)
                    raise UpdateFailed("Invalid JSON response from inverter")
                
                if not data:
                    _LOGGER.error("Received empty response from inverter")
                    raise UpdateFailed("Empty response from inverter")
                
                # Process the data into the expected format
                self._processed_data = self._process_data(data)
                _LOGGER.debug("Processed data: %s", self._processed_data)
                
                return self._processed_data

        except aiohttp.ClientError as err:
            _LOGGER.error("Error connecting to Solax inverter: %s", err)
            raise UpdateFailed(f"Error communicating with inverter: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error fetching Solax data: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err

    def _process_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Process the JSON data into the expected format."""
        try:
            _LOGGER.debug("Processing data structure: %s", data)
            
            # Initialize the result dictionary
            result = {}
            
            # Add basic information
            for key in ["method", "version", "type", "SN", "Status"]:
                if key in data:
                    result[key] = data[key]
                    _LOGGER.debug("Added %s: %s", key, data[key])
            
            # Process the Data array
            if "Data" in data and isinstance(data["Data"], list):
                for i, value in enumerate(data["Data"]):
                    if value is not None:  # Skip None values
                        result[f"Data_{i}"] = value
                        _LOGGER.debug("Added Data_%d: %s", i, value)
            
            if not result:
                _LOGGER.error("No data was processed from the response")
            else:
                _LOGGER.info("Successfully processed %d data points", len(result))
            
            return result
            
        except Exception as err:
            _LOGGER.error("Error processing data: %s", err)
            raise UpdateFailed(f"Error processing data: {err}") from err 