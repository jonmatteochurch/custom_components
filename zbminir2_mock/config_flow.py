"""Config flow for ZBMINIR2 Mock."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector


from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_INCHING_CONTROL,
    CONF_INCHING_TIME,
    CONF_INCHING_MODE,
    INCHING_CONTROLS,
    INCHING_MODES,
)


def _data_schema() -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_NAME): str
    })


def _options_schema() -> vol.Schema:
    return vol.Schema({
        vol.Optional(CONF_INCHING_CONTROL): selector.SelectSelector(
            selector.SelectSelectorConfig(options=INCHING_CONTROLS)
        ),
        vol.Optional(CONF_INCHING_TIME): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=0.5, max=3599.5, step=0.5, mode=selector.NumberSelectorMode.BOX)
        ),
        vol.Optional(CONF_INCHING_MODE): selector.SelectSelector(
            selector.SelectSelectorConfig(options=INCHING_MODES)
        )
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

    if CONF_INCHING_CONTROL in user_input:
        config[CONF_INCHING_CONTROL] = user_input[CONF_INCHING_CONTROL]
    if CONF_INCHING_TIME in user_input:
        config[CONF_INCHING_TIME] = user_input[CONF_INCHING_TIME]
    if CONF_INCHING_MODE in user_input:
        config[CONF_INCHING_MODE] = user_input.get(CONF_INCHING_MODE)

    return config, errors


class ZBMINIR2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
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
        return ZBMINIR2OptionsFlow(config_entry)
    

class ZBMINIR2OptionsFlow(config_entries.OptionsFlow):

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
            errors=errors
        )