"""SONOFF ZBMINIR2 Mock Switch."""
from __future__ import annotations
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
class ZBMINIR2State:
    delayed_power_on_state: bool = False
    delayed_power_on_time: float = 0.5
    detach_relay_mode: bool = False
    external_trigger_mode: str = "edge"
    linkquality: int = 255
    network_indicator: bool = True
    state: str = "OFF"
    power_on_behavior: str = "previous"
    turbo_mode: bool = False
    update: dict = field(default_factory=dict)  

    listeners: list = field(default_factory=list)

    def notify(self) -> None:
        for cb in self.listeners:
            cb()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = ZBMINIR2State()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
