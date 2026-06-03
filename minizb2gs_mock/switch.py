"""Switch platform for MINI-ZB2GS Mock."""
from __future__ import annotations
from asyncio import get_event_loop
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import MINIZB2GSState
from .const import DOMAIN, CONF_NAME, CONF_INCHING_CONTROL_L1, CONF_INCHING_MODE_L1, CONF_INCHING_TIME_L1
from .entity import MINIZB2GSEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: MINIZB2GSState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MINIZB2GSL1Switch(entry, state),
        MINIZB2GSL2Switch(entry, state),
        MINIZB2GSDelayedPowerOnStateChannel1L1Switch(entry, state),
        MINIZB2GSDelayedPowerOnStateChannel2L2Switch(entry, state),
        MINIZB2GSDetachRelayModeL1Switch(entry, state),
        MINIZB2GSDetachRelayModeL2Switch(entry, state),
        MINIZB2GSNetworkIndicatorSwitch(entry, state),
        MINIZB2GSTurboModeSwitch(entry, state),
    ])


class _BaseSwitch(MINIZB2GSEntity, SwitchEntity):
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


class MINIZB2GSL1Switch(_BaseSwitch):
    _attr_name = "L1"

    def __init__(self, entry, state) -> None:
        super().__init__(entry, state, "l1")

    @property
    def is_on(self) -> bool:
        return self._state.state_l1 == "ON"

    def turn_on(self):
        self._state.state_l1 = "ON"
        self._state.notify()

    async def async_turn_on(self) -> None:
        self._state.cancel_pending("l1")
        delay = self.delayed_power_on_time_l1 if self._state.delayed_power_on_state_channel_1_l1 else 0
        inching = self._entry.options.get(CONF_INCHING_TIME_L1, 0) if self._entry.options.get(CONF_INCHING_CONTROL_L1, "") == "ENABLE" and self._entry.options.get(CONF_INCHING_MODE_L1, "") == "OFF" else 0
        if delay and inching:
            self._state.pending_l1 = (
                get_event_loop().call_later(delay, self.turn_on),
                get_event_loop().call_later(delay+inching, self._turn_off)
            )
        elif delay:
            self._state.pending_l1 = (
                get_event_loop().call_later(delay, self.turn_on)
            )
        elif inching:
            self._state.pending_l1 = (
                get_event_loop().call_later(inching, self._turn_off)
            )
            self.turn_on()
        else:
            self.turn_on()

    def turn_off(self) -> None:
        self._state.state_l1 = "OFF"
        self._state.notify()

    async def async_turn_off(self) -> None:
        self._state.cancel_pending("l1")
        inching = self._entry.options.get(CONF_INCHING_TIME_L1, 0) if self._entry.options.get(CONF_INCHING_CONTROL_L1, "") == "ENABLE" and self._entry.options.get(CONF_INCHING_MODE_L1, "") == "ON" else 0
        if inching:
            self._state.pending_l1 = (
                get_event_loop().call_later(inching, self.turn_on)
            )
        self.turn_off()

    async def async_toggle(self) -> None:
        if self._state.state_l1 == "ON":
            await self.async_turn_off()
        else:
            await self.async_turn_on()


class MINIZB2GSL2Switch(_BaseSwitch):
    _attr_name = "L2"

    def __init__(self, entry, state):
        super().__init__(entry, state, "l2")

    @property
    def is_on(self):
        return self._state.state_l2 == "ON"

    async def async_turn_on(self):
        self._state.cancel_pending("l2")
        delay = self.delayed_power_on_time_l2 if self._state.delayed_power_on_state_channel_2_l2 else 0
        inching = self._entry.options.get(CONF_INCHING_TIME_L2, 0) if self._entry.options.get(CONF_INCHING_CONTROL_L2, "") ==
        if delay and inching:
            self._state.pending_l2 = (
                get_event_loop().call_later(delay, self.turn_on),
                get_event_loop().call_later(delay+inching, self._turn_off)
            )
        elif delay:
            self._state.pending_l2 = (
                get_event_loop().call_later(delay, self.turn_on)
            )
        elif inching:
            self._state.pending_l2 = (
                get_event_loop().call_later(inching, self._turn_off)
            )
            self.turn_on()
        else:
            self.turn_on()

    async def async_turn_off(self):
        self._state.cancel_pending("l2")
        inching = self._entry.options.get(CONF_INCHING_TIME_L2, 0) if self._entry.options.get(CONF_INCHING_CONTROL_L2, "") == "ENABLE" and self._entry.options.get(CONF_INCHING_MODE_L2, "") == "ON" else 0
        if inching:
            self._state.pending_l2 = (
                get_event_loop().call_later(inching, self.turn_on)
            )
        self.turn_off()

    async def async_toggle(self):
        if self._state.state_l2 == "ON":
            await self.async_turn_off()
        else:
            await self.async_turn_on()


class MINIZB2GSDelayedPowerOnStateChannel1L1Switch(_BaseSwitch):
    _attr_name = "Delayed power on state channel 1 l1"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "delayed_power_on_state_channel_1_l1")

    @property
    def is_on(self):
        return self._state.delayed_power_on_state_channel_1_l1

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:timer-sand"
        return "mdi:timer-sand-empty"

    async def async_turn_on(self):
        self._state.delayed_power_on_state_channel_1_l1 = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.delayed_power_on_state_channel_1_l1 = False
        self._state.notify()


class MINIZB2GSDelayedPowerOnStateChannel2L2Switch(_BaseSwitch):
    _attr_name = "Delayed power on state channel 2 l2"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "delayed_power_on_state_channel_2_l2")

    @property
    def is_on(self):
        return self._state.delayed_power_on_state_channel_2_l2

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:timer-sand"
        return "mdi:timer-sand-empty"

    async def async_turn_on(self):
        self._state.delayed_power_on_state_channel_2_l2 = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.delayed_power_on_state_channel_2_l2 = False
        self._state.notify()


class MINIZB2GSDetachRelayModeL1Switch(_BaseSwitch):
    _attr_name = "Detach relay mode l1"
    _attr_icon = "mdi:electric-switch"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "detach_relay_mode_l1")

    @property
    def is_on(self):
        return self._state.detach_relay_mode_l1

    async def async_turn_on(self):
        self._state.detach_relay_mode_l1 = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.cancel_pending("l1")
        self._state.detach_relay_mode_l1 = False
        self._state.notify()


class MINIZB2GSDetachRelayModeL2Switch(_BaseSwitch):
    _attr_name = "Detach relay mode l2"
    _attr_icon = "mdi:electric-switch"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "detach_relay_mode_l2")

    @property
    def is_on(self):
        return self._state.detach_relay_mode_l2

    async def async_turn_on(self):
        self._state.detach_relay_mode_l2 = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.detach_relay_mode_l2 = False
        self._state.notify()


class MINIZB2GSNetworkIndicatorSwitch(_BaseSwitch):
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


class MINIZB2GSTurboModeSwitch(_BaseSwitch):
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
