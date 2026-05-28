"""Binary sensor platform for S520619 Mock."""
from __future__ import annotations
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import S520619State
from .const import DOMAIN
from .entity import S520619Entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: S520619State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        S520619KeypadLockoutSwitch(entry, state),
    ])


class _BaseSwitch(S520619Entity, SwitchEntity):
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


class S520619KeypadLockoutSwitch(_BaseSwitch):
    _attr_name = "Keypad lockout"

    def __init__(self, entry, state):
        super().__init__(entry, state, "keypad_lockout")
    
    @property
    def is_on(self):
        return self._state.keypad_lockout == "lock1"
    
    def turn_on(self):
        self._state.keypad_lockout = "lock1"
        self._state.notify()

    def turn_off(self):
        self._state.keypad_lockout = "unlock"
        self._state.notify()



