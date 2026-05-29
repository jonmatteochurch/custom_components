"""Schneider Electric S520619 Mock Setpoint."""
from __future__ import annotations
from dataclasses import dataclass, field
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN

PLATFORMS = [
    Platform.CLIMATE, 
    Platform.SWITCH,
    Platform.SELECT,
    Platform.BINARY_SENSOR,
    Platform.SENSOR, 
    Platform.NUMBER,
]


@dataclass
class S520619State:
    keypad_lockout: bool
    occupancy: bool
    linkquality: int
    pi_heating_demand: int
    pi_cooling_demand: int
    local_temperature: float
    temperature: float
    occupied_cooling_setpoint: float
    occupied_heating_setpoint: float
    running_state: str
    schneider_pilot_mode: str
    system_mode: str
    temperature_display_mode: str

    listeners: list = field(default_factory=list)

    def update(self):
        too_cold = self.system_mode == "heat" and self.local_temperature < self.occupied_heating_setpoint
        too_hot = self.system_mode == "cool" and self.local_temperature > self.occupied_cooling_setpoint
        self.running_state = "heat" if too_cold else "idle"
        self.pi_cooling_demand = 100 if too_hot else 0
        self.pi_heating_demand = 100 if too_cold else 0

    def notify(self):
        for cb in self.listeners:
            cb()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = S520619State(False, True, 255, 0, 0, 20.0, None, 30.0, 4.0, "idle", "pilot", "off", "celsius")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
