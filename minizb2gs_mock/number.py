"""Number platform for MINI-ZB2GS Mock."""
from __future__ import annotations
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import MINIZB2GState
from .const import DOMAIN, CONF_NAME
from .entity import MINIZB2GSEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: MINIZB2GState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MINIZB2GSDelayedPowerOnTimeL1Number(entry, state),
        MINIZB2GSDelayedPowerOnTimeL2Number(entry, state),
    ])


class _BaseNumber(MINIZB2GSEntity, NumberEntity):
    _attr_has_entity_name = True

    def __init__(self, entry, state, key):
        self._entry = entry
        self._state = state
        self._attr_unique_id = f"{entry.options.get(CONF_NAME)}_{key}"

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


class MINIZB2GSDelayedPowerOnTimeL1Number(_BaseNumber):
    _attr_name = "Delayed power on time l1"
    _attr_native_min_value = 0.5
    _attr_native_max_value = 3599.5
    _attr_native_step = .5
    _attr_icon = "mdi:camera-timer"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "delayed_power_on_time_l1")

    @property
    def native_value(self):
        return self._state.delayed_power_on_time_l1

    async def async_set_native_value(self, value: float) -> None:
        self._state.delayed_power_on_time_l1 = value
        self._state.notify()


class MINIZB2GSDelayedPowerOnTimeL2Number(_BaseNumber):
    _attr_name = "Delayed power on time l2"
    _attr_native_min_value = 0.5
    _attr_native_max_value = 3599.5
    _attr_native_step = .5
    _attr_icon = "mdi:camera-timer"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "delayed_power_on_time_l2")

    @property
    def native_value(self):
        return self._state.delayed_power_on_time_l2

    async def async_set_native_value(self, value: float) -> None:
        self._state.delayed_power_on_time_l2 = value
        self._state.notify()
