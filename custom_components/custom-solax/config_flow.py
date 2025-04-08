"""Config flow for the Custom Solax integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_REALTIME_DATA, DEFAULT_TIMEOUT, DOMAIN

# Set up logging
_LOGGER = logging.getLogger(__name__)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> None:
    """
    Validate the user input allows us to connect.
    
    This function tests the connection to the inverter using the provided credentials.
    
    Args:
        hass: Home Assistant instance
        data: Dictionary containing the user input (host, username, password)
        
    Raises:
        ValueError: If the connection fails or credentials are invalid
    """
    # Get an aiohttp session
    session = async_get_clientsession(hass)
    
    # Try to connect to the inverter
    async with session.get(
        f"http://{data[CONF_HOST]}{API_REALTIME_DATA}",
        auth=aiohttp.BasicAuth(data[CONF_USERNAME], data[CONF_PASSWORD]),
        timeout=DEFAULT_TIMEOUT,
    ) as response:
        # Check if the connection was successful
        if response.status != 200:
            raise ValueError("Invalid credentials or host")

class SolaxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """
    Handle a config flow for Solax.
    
    This class manages the configuration flow in the Home Assistant UI.
    It:
    - Shows the configuration form
    - Validates user input
    - Creates the config entry
    """

    # Version of the config flow
    # Increment this when the config flow changes
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """
        Handle the initial step of the config flow.
        
        This is called when the user starts configuring the integration.
        It:
        1. Shows the configuration form
        2. Validates the input
        3. Creates the config entry if successful
        
        Args:
            user_input: Dictionary containing the user input, or None if this is the first step
            
        Returns:
            FlowResult: The result of the config flow step
        """
        # Dictionary to store any errors
        errors: dict[str, str] = {}

        # If we have user input, process it
        if user_input is not None:
            try:
                # Validate the connection
                await validate_input(self.hass, user_input)
            except ValueError:
                # Invalid credentials or host
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                # Any other error
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Success! Create the config entry
                return self.async_create_entry(
                    title=f"Solax Inverter ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        # Show the configuration form
        return self.async_show_form(
            step_id="user",
            # Define the form fields
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            # Show any errors
            errors=errors,
        ) 