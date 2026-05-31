"""SONOFF SNZB-02D Mock — temperature & humidity sensor with screen."""
from __future__ import annotations
from dataclasses import dataclass, field
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN

PLATFORMS: list[Platform] = [
    Platform.SENSOR, 
    Platform.NUMBER,
    Platform.SELECT,
    Platform.UPDATE,
]


@dataclass
class SNZB02DState:
    battery: int = 100
    comfort_humidity_max: float = 60.0
    comfort_humidity_min: float = 40.0
    comfort_temperature_max: float = 24.0
    comfort_temperature_min: float = 18.0
    humidity: float = 50.0
    humidity_calibration: float = 0.0
    linkquality: int = 255
    temperature: float = 20.0
    temperature_calibration: float = 0.0
    temperature_units: str = "celsius"
    update: dict = field(default_factory=dict)  

    listeners: list = field(default_factory=list)

    def notify(self):
        for cb in self.listeners:
            cb()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = SNZB02DState()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
