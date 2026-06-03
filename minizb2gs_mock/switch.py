"""Switch platform for MINI-ZB2GS Mock."""
from __future__ import annotations
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import MINIZB2GSState
from .const import DOMAIN, CONF_NAME
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


class MINIZB2GSL1Switch(MINIZB2GSEntity, SwitchEntity):
    _attr_name = "L1"

    def __init__(self, entry, state) -> None:
        super().__init__(entry, state, "l1")

    @property
    def is_on(self) -> bool:
        return self._state.state_l1 == "ON"

    async def async_turn_on(self) -> None:
        self._state.state_l1 = "ON"
        self._state.notify()

    async def async_turn_off(self) -> None:
        self._state.state_l1 = "OFF"
        self._state.notify()

    async def async_toggle(self) -> None:
        self._state.state_l1 = "ON" if self._state.state_l1 == "OFF" else "OFF"
        self._state.notify()


class MINIZB2GSL2Switch(_BaseSwitch):
    _attr_name = "L2"

    def __init__(self, entry, state):
        super().__init__(entry, state, "l2")

    @property
    def is_on(self):
        return self._state.state_l2 == "ON"

    async def async_turn_on(self):
        self._state.state_l2 = "ON"
        self._state.notify()

    async def async_turn_off(self):
        self._state.state_l2 = "OFF"
        self._state.notify()

    async def async_toggle(self):
        self._state.state_l2 = "ON" if self._state.state_l2 == "OFF" else "OFF"
        self._state.notify()


class MINIZB2GSDelayedPowerOnStateChannel1L1Switch(_BaseSwitch):
    _attr_name = "Delayed power on state channel 1 l1"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "delayed_power_on_state_channel1_l1")

    @property
    def is_on(self):
        return self._state.delayed_power_on_state_channel1_l1

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:timer-sand"
        return "mdi:timer-sand-empty"

    async def async_turn_on(self):
        self._state.delayed_power_on_state_channel1_l1 = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.delayed_power_on_state_channel1_l1 = False
        self._state.notify()


class MINIZB2GSDelayedPowerOnStateChannel2L2Switch(_BaseSwitch):
    _attr_name = "Delayed power on state channel 2 l2"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "delayed_power_on_state_channel2_l2")

    @property
    def is_on(self):
        return self._state.delayed_power_on_state_channel2_l2

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:timer-sand"
        return "mdi:timer-sand-empty"

    async def async_turn_on(self):
        self._state.delayed_power_on_state_channel2_l2 = True
        self._state.notify()

    async def async_turn_off(self):
        self._state.delayed_power_on_state_channel2_l2 = False
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
