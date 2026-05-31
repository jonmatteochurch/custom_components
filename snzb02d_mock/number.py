"""Number platform for SNZB-02D Mock."""
from __future__ import annotations
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import SNZB02DState
from .const import DOMAIN
from .entity import SNZB02DEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: SNZB02DState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SNZB02DConfortHumidityMaxNumber(entry, state),
        SNZB02DComfortHumidityMinNumber(entry, state),
        SNZB02DComfortTemperatureMaxNumber(entry, state),
        SNZB02DComfortTemperatureMinNumber(entry, state),
        SNZB02DHumidityCalibrationNumber(entry, state),
        SNZB02DTemperatureCalibrationNumber(entry, state),
        SNZB02DTemperatureNumber(entry, state),
        SNZB02DHumidityNumber(entry, state),
    ])


class _BaseNumber(SNZB02DEntity, NumberEntity):
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


class SNZB02DConfortHumidityMaxNumber(_BaseNumber):
    _attr_name = "Comfort humidity max"
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:water-percent"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "comfort_humidity_max")

    @property
    def native_value(self):
        return self._state.comfort_humidity_max

    async def async_set_native_value(self, value: float) -> None:
        self._state.comfort_humidity_max = value
        self._state.notify()


class SNZB02DComfortHumidityMinNumber(_BaseNumber):
    _attr_name = "Comfort humidity min"
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:water-percent"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "comfort_humidity_min")

    @property
    def native_value(self):
        return self._state.comfort_humidity_min

    async def async_set_native_value(self, value: float) -> None:
        self._state.comfort_humidity_min = value
        self._state.notify()


class SNZB02DComfortTemperatureMaxNumber(_BaseNumber):
    _attr_name = "Comfort temperature max"
    _attr_native_min_value = -20
    _attr_native_max_value = 60
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:thermometer-high"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "comfort_temperature_max")

    @property
    def native_value(self):
        return self._state.comfort_temperature_max

    async def async_set_native_value(self, value: float) -> None:
        self._state.comfort_temperature_max = value
        self._state.notify()


class SNZB02DComfortTemperatureMinNumber(_BaseNumber):
    _attr_name = "Comfort temperature min"
    _attr_native_min_value = -20
    _attr_native_max_value = 60
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:thermometer-low"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "comfort_temperature_min")

    @property
    def native_value(self):
        return self._state.comfort_temperature_min

    async def async_set_native_value(self, value: float) -> None:
        self._state.comfort_temperature_min = value
        self._state.notify()


class SNZB02DHumidityCalibrationNumber(_BaseNumber):
    _attr_name = "Humidity calibration"
    _attr_native_min_value = -10
    _attr_native_max_value = 10
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:tune"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "humidity_calibration")

    @property
    def native_value(self):
        return self._state.humidity_calibration

    async def async_set_native_value(self, value: float) -> None:
        self._state.humidity_calibration = value
        self._state.notify()


class SNZB02DTemperatureCalibrationNumber(_BaseNumber):
    _attr_name = "Temperature calibration"
    _attr_native_min_value = -10
    _attr_native_max_value = 10
    _attr_native_step = 0.1
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:tune"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state):
        super().__init__(entry, state, "temperature_calibration")

    @property
    def native_value(self):
        return self._state.temperature_calibration

    async def async_set_native_value(self, value: float) -> None:
        self._state.temperature_calibration = value
        self._state.notify()


class SNZB02DTemperatureNumber(_BaseNumber):
    _attr_name = "Temperature"
    _attr_native_min_value = -20
    _attr_native_max_value = 60
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:thermometer"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, entry, state):
        super().__init__(entry, state, "temperature")

    @property
    def native_value(self):
        return self._state.temperature

    async def async_set_native_value(self, value: float) -> None:
        self._state.temperature = value
        self._state.notify()


class SNZB02DHumidityNumber(_BaseNumber):
    _attr_name = "Humidity"
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = "mdi:water-percent"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, entry, state):
        super().__init__(entry, state, "humidity")

    @property
    def native_value(self):
        return self._state.humidity

    async def async_set_native_value(self, value: float) -> None:
        self._state.humidity = value
        self._state.notify()