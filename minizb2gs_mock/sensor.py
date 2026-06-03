"""Sensor platform for MINI-ZB2GS Mock."""
from __future__ import annotations
from homeassistant.components.sensor import EntityCategory, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import MINIZB2GSState
from .const import DOMAIN, CONF_NAME
from .entity import MINIZB2GSEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: MINIZB2GSState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MINIZB2GSLinkqualitySensor(entry, state),
    ])


class _BaseSensor(MINIZB2GSEntity, SensorEntity):
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


class MINIZB2GSLinkqualitySensor(_BaseSensor):
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


class MINIZB2GSDetachRelayModeSensor(_BaseSensor):
    _attr_name = "Detach relay mode"
    _attr_icon = "mdi:electric-switch"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "detach_relay_mode")

    @property
    def native_value(self):
        return self._state.detach_relay_mode


class MINIZB2GSProgrammableStepperSeq1Sensor(_BaseSensor):
    _attr_name = "Programmable stepper seq1"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "programmable_stepper_seq1")

    @property
    def native_value(self):
        return self._state.programmable_stepper_seq1
    

class MINIZB2GSProgrammableStepperSeq2Sensor(_BaseSensor):
    _attr_name = "Programmable stepper seq2"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "programmable_stepper_seq2")

    @property
    def native_value(self):
        return self._state.programmable_stepper_seq2
    

class MINIZB2GSProgrammableStepperSeq3Sensor(_BaseSensor):
    _attr_name = "Programmable stepper seq3"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "programmable_stepper_seq3")

    @property
    def native_value(self):
        return self._state.programmable_stepper_seq3


class MINIZB2GSProgrammableStepperSeq4Sensor(_BaseSensor):
    _attr_name = "Programmable stepper seq4"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "programmable_stepper_seq4")

    @property
    def native_value(self):
        return self._state.programmable_stepper_seq4