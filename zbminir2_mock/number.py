"""Number platform for ZBMINIR2 Mock."""
from __future__ import annotations
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import ZBMINIR2State
from .const import DOMAIN
from .entity import ZBMINIR2Entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: ZBMINIR2State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ZBMINIR2DelayedPowerOnNumber(entry, state),
    ])


class _BaseNumber(ZBMINIR2Entity, NumberEntity):
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


class ZBMINIR2DelayedPowerOnNumber(_BaseNumber):
    _attr_name = "Delayed power on time"
    _attr_native_min_value = 0.5
    _attr_native_max_value = 3599.5
    _attr_native_step = .5
    _attr_icon = "mdi:camera-timer"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "delayed_power_on_time")

    @property
    def native_value(self):
        return self._state.delayed_power_on_time

    async def async_set_native_value(self, value: float) -> None:
        self._state.delayed_power_on_time = value
        self._state.notify()
