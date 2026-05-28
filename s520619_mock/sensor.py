"""Number platform for S520619 Mock."""
from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import S520619State
from .const import DOMAIN
from .entity import S520619Entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: S520619State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        S520619LinkqualitySensor(entry, state),
        S520619PICoolingDemandSensor(entry, state),
        S520619PIHeatingDemandSensor(entry, state),
        S520619TemperatureSensor(entry, state),
    ])


class _BaseSensor(S520619Entity, SensorEntity):
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


class S520619LinkqualitySensor(_BaseSensor):
    _attr_name = "Linkquality"
    _attr_native_min_value = 0
    _attr_native_max_value = 255
    _attr_native_step = 1

    def __init__(self, entry, state):
        super().__init__(entry, state, "linkquality")

    @property
    def native_value(self):
        return self._state.linkquality


class S520619PICoolingDemandSensor(_BaseSensor):
    _attr_name = "PI cooling demand"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1

    def __init__(self, entry, state):
        super().__init__(entry, state, "pi_cooling_demand")

    @property
    def native_value(self):
        return self._state.pi_cooling_demand
    
    def set_native_value(self, value):
        try:
            self._state.pi_cooling_demand = int(value)
            self._state.notify()
        except ValueError:
            pass


class S520619PIHeatingDemandSensor(_BaseSensor):
    _attr_name = "PI heating demand"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1

    def __init__(self, entry, state):
        super().__init__(entry, state, "pi_heating_demand")

    @property
    def native_value(self):
        return self._state.pi_heating_demand


class S520619TemperatureSensor(_BaseSensor):
    _attr_name = "Temperature"

    def __init__(self, entry, state):
        super().__init__(entry, state, "temperature")
        self._attr_native_unit_of_measurement = self._entry.options.get("thermostat_unit", UnitOfTemperature.CELSIUS) 

    @property
    def native_value(self):
        return self._state.temperature
