"""Config flow for SNZB-02D Mock."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_NAME, 
    CONF_TEMPERATURE_PRECISION,
    CONF_HUMIDITY_PRECISION
)


def _data_schema() -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_NAME): str
    })


def _options_schema() -> vol.Schema:
    return vol.Schema({
        vol.Optional(CONF_TEMPERATURE_PRECISION): selector.NumberSelector(
            selector.NumberSelectorConfig(
                step=1, min=0, max=3, mode=selector.NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_HUMIDITY_PRECISION): selector.NumberSelector(
            selector.NumberSelectorConfig(
                step=1, min=0, max=3, mode=selector.NumberSelectorMode.BOX)
        ),
    })


def _parse_data(user_input: dict) -> tuple[dict, dict]:
    config = {}
    errors = {}

    config[CONF_NAME] = user_input.get(CONF_NAME, "").strip()
    if not config[CONF_NAME]:
        errors[CONF_NAME] = "invalid_name"

    return config, errors


def _parse_options(user_input: dict) -> tuple[dict, dict]:
    config = {}
    errors = {}

    if CONF_TEMPERATURE_PRECISION in user_input:
        config[CONF_TEMPERATURE_PRECISION] = user_input[CONF_TEMPERATURE_PRECISION]
    if CONF_HUMIDITY_PRECISION in user_input:
        config[CONF_HUMIDITY_PRECISION] = user_input[CONF_HUMIDITY_PRECISION]

    return config, errors


class SNZB02DConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
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
            data_schema=self.add_suggested_values_to_schema(
                data_schema=_data_schema(), suggested_values=user_input),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SNZB02DOptionsFlow(config_entry)
    

class SNZB02DOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            config, errors = _parse_options(user_input)
            if not errors:
                return self.async_create_entry(data=config)

        if errors:
            defaults = user_input
        else:
            defaults = dict(self._config_entry.options)
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                data_schema=_options_schema(), suggested_values=defaults),
                description_placeholders={"name": self._config_entry.title},
            errors=errors,
        )