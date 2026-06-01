"""Number platform for S520619 Mock."""
from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
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
        S520619DisplaySensor(entry, state),
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

    @property
    def icon(self) -> str:
        if self.native_value < 64:
            return "mdi:signal-cellular-outline"
        if self.native_value < 128:
            return "mdi:signal-cellular-1"
        if self.native_value < 192:
            return "mdi:signal-cellular-2"
        return "mdi:signal-cellular-3"


class S520619PICoolingDemandSensor(_BaseSensor):
    _attr_name = "PI cooling demand"
    _attr_icon = "mdi:air-conditioner"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1

    def __init__(self, entry, state):
        super().__init__(entry, state, "pi_cooling_demand")

    @property
    def native_value(self):
        return self._state.pi_cooling_demand


class S520619PIHeatingDemandSensor(_BaseSensor):
    _attr_name = "PI heating demand"
    _attr_icon = "mdi:radiator"
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
    _attr_icon = "mdi:thermometer"

    def __init__(self, entry, state):
        super().__init__(entry, state, "temperature")
        self._attr_native_unit_of_measurement = self._entry.options.get(
            "thermostat_unit", UnitOfTemperature.CELSIUS)
        self._attr_icon = "mdi:temperature-fahrenheit" if entry.options.get(
            "thermostat_unit") == "fahrenheit" else "mdi:temperature-celsius"

    @property
    def native_value(self):
        return self._state.temperature


class S520619DisplaySensor(_BaseSensor):
    _attr_name = "Display"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, entry, state):
        super().__init__(entry, state, "display")

    @property
    def icon(self) -> str:
        too_cold = self._state.system_mode == "heat" and self._state.local_temperature < self._state.occupied_heating_setpoint
        too_hot = self._state.system_mode == "cool" and self._state.local_temperature > self._state.occupied_cooling_setpoint
        if too_cold:
            return "mdi:radiator"
        if too_hot:
            return "mdi:snowflake"
        return "mdi:blank"

    @property
    def native_unit_of_measurement_compat(self):
        if self._state.temperature_display_mode == "fahrenheit":
            return UnitOfTemperature.FAHRENHEIT
        return UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        if self._state.temperature_display_mode == "fahrenheit":
            return round(self._state.local_temperature * 18/5 + 64) / 2
        return round(self._state.local_temperature * 2) / 2
