"""Switch platform for ZBMINIR2 Mock."""
from __future__ import annotations
from homeassistant.components.switch import SwitchEntity
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
        ZBMINIR2Switch(entry, state),
        ZBMINIR2DelayedPowerOnStateSwitch(entry, state),
        ZBMINIR2DetachRelayModeSwitch(entry, state),
        ZBMINIR2NetworkIndicatorSwitch(entry, state),
        ZBMINIR2TurboModeSwitch(entry, state),
    ])


class ZBMINIR2Switch(ZBMINIR2Entity, SwitchEntity):
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


class _BaseSwitch(ZBMINIR2Entity, SwitchEntity):
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


class ZBMINIR2DelayedPowerOnStateSwitch(_BaseSwitch):
    _attr_name = "Delayed power on state"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "delayed_power_on_state")

    @property
    def is_on(self):
        return self._state.delayed_power_on_state

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:timer-sand"
        return "mdi:timer-sand-empty"

    async def async_turn_on(self):
        self._state.delayed_power_on_state = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.delayed_power_on_state = False
        self._state.notify()


class ZBMINIR2DetachRelayModeSwitch(_BaseSwitch):
    _attr_name = "Detach relay mode"
    _attr_icon = "mdi:electric-switch"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "detach_relay_mode")

    @property
    def is_on(self):
        return self._state.detach_relay_mode

    async def async_turn_on(self):
        self._state.detach_relay_mode = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.detach_relay_mode = False
        self._state.notify()


class ZBMINIR2NetworkIndicatorSwitch(_BaseSwitch):
    _attr_name = "Network indicator"
    _attr_icon = "mdi:access-point-network"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "network_indicator")

    @property
    def is_on(self):
        return self._state.network_indicator

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:lightbulb-on-outline"
        return "mdi:lightbulb-outline"

    async def async_turn_on(self):
        self._state.network_indicator = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.network_indicator = False
        self._state.notify()


class ZBMINIR2TurboModeSwitch(_BaseSwitch):
    _attr_name = "Turbo mode"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "turbo_mode")

    @property
    def is_on(self):
        return self._state.turbo_mode

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:access-point-network"
        return "mdi:access-point-network-off"

    async def async_turn_on(self):
        self._state.turbo_mode = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.turbo_mode = False
        self._state.notify()
