"""Switch platform for ZBMINIL2 Mock."""
from __future__ import annotations
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import ZBMINIL2State
from .const import DOMAIN
from .entity import ZBMINIL2Entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: ZBMINIL2State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ZBMINIL2Switch(entry, state),
    ])


class ZBMINIL2Switch(ZBMINIL2Entity, SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, entry, state) -> None:
        self._entry = entry
        self._state = state
        self._attr_name = entry.title
        self._attr_unique_id = entry.entry_id

    async def async_added_to_hass(self) -> None:
        self._state.listeners.append(self._async_refresh)

    async def async_will_remove_from_hass(self) -> None:
        try:
            self._state.listeners.remove(self._async_refresh)
        except ValueError:
            pass

    @callback
    def _async_refresh(self) -> None:
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        return self._state.state == "ON"

    async def async_turn_on(self) -> None:
        self._state.state = "ON"
        self._state.notify()

    async def async_turn_off(self) -> None:
        self._state.state = "OFF"
        self._state.notify()

    async def async_toggle(self) -> None:
        self._state.state = "ON" if self._state.state == "OFF" else "OFF"
        self._state.notify()
