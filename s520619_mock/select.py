"""Select platform for S520619 Mock."""
from __future__ import annotations
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import S520619State
from .const import DOMAIN, SCHNEIDER_PILOT_MODES, TEMPERATURE_DISPLAY_MODES
from .entity import S520619Entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: S520619State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        S520619TemperatureDisplayModeSelect(entry, state),
        S520619SchneiderPilotModeSelect(entry, state),
    ])


class _BaseSelect(S520619Entity, SelectEntity):
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


class S520619TemperatureDisplayModeSelect(_BaseSelect):
    _attr_name = "Temperature Display Mode"
    _attr_options = TEMPERATURE_DISPLAY_MODES

    def __init__(self, entry, state):
        super().__init__(entry, state, "display_mode")

    @property
    def current_option(self):
        return self._state.temperature_display_mode

    def select_option(self, option: str) -> None:
        self._state.temperature_display_mode = option
        self._state.notify()


class S520619SchneiderPilotModeSelect(_BaseSelect):
    _attr_name = "Schneider pilot mode"
    _attr_options = SCHNEIDER_PILOT_MODES

    def __init__(self, entry, state):
        super().__init__(entry, state, "pilot_mode")

    @property
    def current_option(self):
        return self._state.schneider_pilot_mode

    def select_option(self, option: str) -> None:
        self._state.schneider_pilot_mode = option
        self._state.notify()

