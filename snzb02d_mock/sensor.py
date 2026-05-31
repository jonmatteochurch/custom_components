"""Sensor platform for SNZB-02D Mock."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import SNZB02DState
from .const import DOMAIN
from .entity import SNZB02DEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: SNZB02DState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SNZB02DLinkqualitySensor(entry, state),
        SNZB02DTemperatureSensor(entry, state),
        SNZB02DHumiditySensor(entry, state),
        SNZB02DBattery(entry, state),
    ])


class _BaseSensor(SNZB02DEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, entry, state, key):
        self._entry = entry
        self._state = state
        self._attr_unique_id = f"{entry.entry_id}_{key}"

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


class SNZB02DLinkqualitySensor(_BaseSensor):
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
    

class SNZB02DTemperatureSensor(_BaseSensor):
    _attr_name = "Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, entry, state):
        super().__init__(entry, state, "temperature")

    def _temperature(self):
        return self._state.temperature + self._state.temperature_calibration

    @property
    def native_value(self):
        if self._state.temperature_units == "fahrenheit":
            return self._temperature() * 9 / 5 + 32
        return self._temperature()

    @property
    def native_unit_of_measurement(self):
        if self._state.temperature_units == "fahrenheit":
            return UnitOfTemperature.FAHRENHEIT
        return UnitOfTemperature.CELSIUS

    @property
    def icon(self) -> str:
        if self._temperature() < self._state.comfort_temperature_min:
            return "mdi:snowflake"
        if self._temperature() > self._state.comfort_temperature_max:
            return "mdi:fire"
        return "mdi:blank"
    

class SNZB02DHumiditySensor(_BaseSensor):
    _attr_name = "Humidity"
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, entry, state):
        super().__init__(entry, state, "humidity")

    def _humidity(self):
        return self._state.humidity + self._state.humidity_calibration

    @property
    def native_value(self):
        return self._humidity()

    @property
    def icon(self) -> str:
        if self._humidity() < self._state.comfort_humidity_min:
            return "mdi:weather-sunny"
        if self._humidity() > self._state.comfort_humidity_max:
            return "mdi:water-outline"
        return "mdi:blank"
    

class SNZB02DBattery(_BaseSensor):
    _attr_name = "Battery"
    _attr_icon = "mdi:battery"
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, entry, state):
        super().__init__(entry, state, "battery")

    @property
    def native_value(self):
        return self._state.battery