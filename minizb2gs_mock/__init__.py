"""MINI-ZB2GS Mock Double Switch."""
from __future__ import annotations
from asyncio import Task
from dataclasses import dataclass, field

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN


PLATFORMS: list[Platform] = [
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.UPDATE,
]


@dataclass
class MINIZB2GSState:
    delayed_power_on_state_channel_1_l1: bool = False
    delayed_power_on_state_channel_2_l2: bool = False
    delayed_power_on_time_l1: float = 0.5
    delayed_power_on_time_l2: float = 0.5
    detach_relay_mode: dict = field(default_factory=dict)
    external_trigger_mode: str = "edge"
    external_trigger_mode_l1: str = None
    external_trigger_mode_l2: str = None
    linkquality: int = 255
    network_indicator: bool = True
    power_on_behavior_l1: str = "previous"
    power_on_behavior_l2: str = "previous"
    programmable_stepper_seq1: dict = field(default_factory=dict)
    programmable_stepper_seq2: dict = field(default_factory=dict)
    programmable_stepper_seq3: dict = field(default_factory=dict)
    programmable_stepper_seq4: dict = field(default_factory=dict)
    state_l1: str = "OFF"
    state_l2: str = "OFF"
    turbo_mode: bool = False
    update: dict = field(default_factory=dict)

    listeners: list = field(default_factory=list)

    def notify(self) -> None:
        for cb in self.listeners:
            cb()

    pending_l1: list[Task] = field(default_factory=list)
    pending_l2: list[Task] = field(default_factory=list)

    def cancel_pending(self, channel: str) -> None:
        attr = f"pending_{channel}"
        tasks = getattr(self, attr)
        for task in tasks:
            if task and not task.done():
                task.cancel()
        setattr(self, attr, list())


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = MINIZB2GSState()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
