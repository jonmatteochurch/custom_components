"""Number platform for S520619 Mock."""
from __future__ import annotations
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import S520619State
from .const import DOMAIN
from .entity import S520619Entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: S520619State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        S520619LocalTemperatureNumber(entry, state),
    ])


class _BaseNumber(S520619Entity, NumberEntity):
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


class S520619LocalTemperatureNumber(_BaseNumber):
    _attr_name = "Local temperature"
    _attr_native_min_value = -20
    _attr_native_max_value = 100
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, entry, state):
        super().__init__(entry, state, "local_temperature")
        self._attr_icon = "mdi:temperature-fahrenheit" if entry.options.get(
            "thermostat_unit") == "fahrenheit" else "mdi:temperature-celsius"

    @property
    def native_value(self):
        return self._state.local_temperature

    @property
    def native_step(self) -> float:
        return 10 ** -self._entry.options.get("temperature_precision", 3)
    
    async def async_set_native_value(self, value: float) -> None:
        self._state.local_temperature = value
        self._state.update()
        self._state.notify()
