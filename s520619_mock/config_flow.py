"""Config flow for S520619 Mock."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

import logging
_LOGGER = logging.getLogger(__name__)

from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_MEASUREMENT_POLL_INTERVAL,
    CONF_TEMPERATURE_CALIBRATION,
    CONF_TEMPERATURE_PRECISION,
    CONF_THERMOSTAT_UNIT,
    CONF_NO_OCCUPANCY_SINCE,
    THERMOSTAT_UNITS,
)

def _data_schema() -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_NAME): str
    })

def _options_schema() -> vol.Schema:
    return vol.Schema({
        vol.Optional(CONF_MEASUREMENT_POLL_INTERVAL): selector.NumberSelector(
            selector.NumberSelectorConfig(step=1, min=-1, mode=selector.NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_TEMPERATURE_CALIBRATION): selector.NumberSelector(
            selector.NumberSelectorConfig(step=0.1, mode=selector.NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_TEMPERATURE_PRECISION): selector.NumberSelector(
            selector.NumberSelectorConfig(step=1, min=0, max=3, mode=selector.NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_THERMOSTAT_UNIT): selector.SelectSelector(
            selector.SelectSelectorConfig(options=THERMOSTAT_UNITS)
        ),
        vol.Optional(CONF_NO_OCCUPANCY_SINCE): str
    })

def _parse_data(user_input: dict) -> dict:
    config = {}
    errors = {}

    config[CONF_NAME] = user_input.get(CONF_NAME, "").strip()
    if not config[CONF_NAME]:
        errors[CONF_NAME] = "invalid_name"

    return config, errors


def _parse_options(user_input: dict) -> dict:
    config = {}
    errors = {}

    config[CONF_MEASUREMENT_POLL_INTERVAL] = user_input.get(CONF_MEASUREMENT_POLL_INTERVAL)
    config[CONF_TEMPERATURE_CALIBRATION] = user_input.get(CONF_TEMPERATURE_CALIBRATION)
    config[CONF_TEMPERATURE_PRECISION] = user_input.get(CONF_TEMPERATURE_PRECISION)
    config[CONF_THERMOSTAT_UNIT] = user_input.get(CONF_THERMOSTAT_UNIT)
    try:
        config[CONF_NO_OCCUPANCY_SINCE] = [int(x) for x in user_input.get(CONF_NO_OCCUPANCY_SINCE, "").strip().split(",") if x.strip()]
    except ValueError:
        errors[CONF_NO_OCCUPANCY_SINCE] = "invalid_no_occupancy_since"

    return config, errors


class S520619ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            config, errors = _parse_data(user_input)
            if not errors:
                id = config[CONF_NAME].lower().replace(" ", "_")
                await self.async_set_unique_id(id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=config[CONF_NAME], data={})

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(data_schema=_data_schema(), suggested_values=user_input),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return S520619OptionsFlow(config_entry)
    

class S520619OptionsFlow(config_entries.OptionsFlow):
    """Allow changing parameters after initial setup."""

    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        print(self._config_entry.title)
        print(self._config_entry.data)
        print(self._config_entry.options)
        errors = {}
        if user_input is not None:
            config, errors = _parse_options(user_input)
            if not errors:
                return self.async_create_entry(data=config)

        if errors:
            defaults = user_input
        else:
            defaults = dict(self._config_entry.options)
            defaults[CONF_NO_OCCUPANCY_SINCE] = ",".join(str(x) for x in self._config_entry.options.get(CONF_NO_OCCUPANCY_SINCE, []))
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(data_schema=_options_schema(), suggested_values=defaults),
            description_placeholders={"name": self._config_entry.title},
            errors=errors
        )
