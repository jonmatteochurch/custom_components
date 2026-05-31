"""Select platform for SNZB-02D Mock."""
from __future__ import annotations
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import SNZB02DState
from .const import DOMAIN, TEMPERATURE_UNITS
from .entity import SNZB02DEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: SNZB02DState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SNZB02DTemperatureUnitsSelect(entry, state),
    ])


class _BaseSelect(SNZB02DEntity, SelectEntity):
    _attr_has_entity_name = True

    def __init__(self, entry, state, key):
        self._entry = entry
        self._state = state
        self._attr_unique_id = f"{entry.entry_id}_{key}"

    async def async_added_to_hass(self):
        self._state.listeners.append(self._async_refresh)

    async def async_will_remove_from_hass(self):
        try:
            self._state.listeners.remove(self._async_refresh)
        except ValueError:
            pass

    @callback
    def _async_refresh(self):
        self.async_write_ha_state()


class SNZB02DTemperatureUnitsSelect(_BaseSelect):
    _attr_name = "Temperature units"
    _attr_options = TEMPERATURE_UNITS
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "temperature_units")

    @property
    def current_option(self):
        return self._state.temperature_units


    async def async_select_option(self, option: str) -> None:
        self._state.temperature_units = option
        self._state.notify()
