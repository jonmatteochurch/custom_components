"""Select platform for MINI-ZB2GS Mock."""
from __future__ import annotations
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MINIZB2GSState
from .const import DOMAIN, CONF_NAME, EXTERNAL_TRIGGER_MODES, POWER_ON_BEHAVIORS
from .entity import MINIZB2GSEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: MINIZB2GSState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MINIZB2GSExternalTriggerModeL1Select(entry, state),
        MINIZB2GSExternalTriggerModeL2Select(entry, state),
        MINIZB2GSPowerOnBehaviorL1Select(entry, state),
        MINIZB2GSPowerOnBehaviorL2Select(entry, state),
    ])


class _BaseSelect(MINIZB2GSEntity, SelectEntity):
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


class MINIZB2GSExternalTriggerModeL1Select(_BaseSelect):
    _attr_name = "External trigger mode l1"
    _attr_options = EXTERNAL_TRIGGER_MODES
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "external_trigger_mode_l1")

    @property
    def current_option(self):
        return self._state.external_trigger_mode_l1


    async def async_select_option(self, option: str) -> None:
        self._state.external_trigger_mode_l1 = option
        self._state.notify()


class MINIZB2GSPowerOnBehaviorL1Select(_BaseSelect):
    _attr_name = "Power on behavior l1"
    _attr_options = POWER_ON_BEHAVIORS
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "power_on_behavior_l1")

    @property
    def current_option(self):
        return self._state.power_on_behavior_l1

    async def async_select_option(self, option: str) -> None:
        self._state.power_on_behavior_l1 = option
        self._state.notify()


class MINIZB2GSExternalTriggerModeL2Select(_BaseSelect):
    _attr_name = "External trigger mode l2"
    _attr_options = EXTERNAL_TRIGGER_MODES
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "external_trigger_mode_l2")

    @property
    def current_option(self):
        return self._state.external_trigger_mode_l2

    async def async_select_option(self, option: str) -> None:
        self._state.external_trigger_mode_l2 = option
        self._state.notify()


class MINIZB2GSPowerOnBehaviorL2Select(_BaseSelect):
    _attr_name = "Power on behavior l2"
    _attr_options = POWER_ON_BEHAVIORS
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "power_on_behavior_l2")

    @property
    def current_option(self):
        return self._state.power_on_behavior_l2

    async def async_select_option(self, option: str) -> None:
        self._state.power_on_behavior_l2 = option
        self._state.notify()