"""Number platform for ZBMINIL2 Mock."""
from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import ZBMINIL2State
from .const import DOMAIN
from .entity import ZBMINIL2Entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: ZBMINIL2State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ZBMINIL2LinkqualitySensor(entry, state),
    ])


class _BaseSensor(ZBMINIL2Entity, SensorEntity):
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


class ZBMINIL2LinkqualitySensor(_BaseSensor):
    _attr_name = "Linkquality"
    _attr_native_min_value = 0
    _attr_native_max_value = 255
    _attr_native_step = 1

    def __init__(self, entry, state):
        super().__init__(entry, state, "linkquality")

    @property
    def native_value(self):
        return self._state.linkquality

    @property
    def icon(self) -> str:
        if self.native_value < 64:
            return "mdi:signal-cellular-outline"
        if self.native_value < 128:
            return "mdi:signal-cellular-1"
        if self.native_value < 192:
            return "mdi:signal-cellular-2"
        return "mdi:signal-cellular-3"
