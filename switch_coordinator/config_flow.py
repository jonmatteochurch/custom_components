"""Config flow for Switch Coordinator."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_MASTER_SWITCHES,
    CONF_SLAVE_SWITCHES
)


def _data_schema() -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_NAME): str
    })


def _options_schema() -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_MASTER_SWITCHES): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="switch", multiple=True)
        ),
        vol.Required(CONF_SLAVE_SWITCHES): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="switch", multiple=True)
        )},
    )


def _parse_data(user_input: dict) -> dict:
    config = {}
    errors = {}

    config[CONF_NAME] = user_input.get(CONF_NAME, "").strip()

    if not config[CONF_NAME]:
        errors[CONF_NAME] = "invalid_name"

    return config, errors


def _parse_options(user_input: dict) -> dict:
    config = user_input.copy()
    errors = {}

    if any(master in config[CONF_SLAVE_SWITCHES] for master in config[CONF_MASTER_SWITCHES]):
        errors[CONF_SLAVE_SWITCHES] = "master_in_slaves"

    return config, errors


class SwitchCoordinatorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
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
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SwitchCoordinatorOptionsFlow(config_entry)


class SwitchCoordinatorOptionsFlow(config_entries.OptionsFlow):

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