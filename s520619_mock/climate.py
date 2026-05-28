"""Climate platform for S520619 Mock."""
from __future__ import annotations
from homeassistant.components.climate import (
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
    UnitOfTemperature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import S520619State
from .const import CONF_TEMPERATURE_PRECISION, CONF_THERMOSTAT_UNIT, DOMAIN
from .entity import S520619Entity


TEMPERATURE_DISPLAY_MODE_MAP = {
    "celsius": UnitOfTemperature.CELSIUS,
    "fahrenheit": UnitOfTemperature.FAHRENHEIT,
}

SYSTEM_MODE_MAP = {
    "off": HVACMode.OFF,
    "heat": HVACMode.HEAT,
    "cool": HVACMode.COOL
}
HVAC_MODE_MAP = {v: k for k, v in SYSTEM_MODE_MAP.items()}

RUNNING_STATE_MAP = {
    "idle": HVACAction.IDLE,
    "heat": HVACAction.HEATING,
    "cool": HVACAction.COOLING,
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: S520619State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        S520619Climate(entry, state)
    ])


class S520619Climate(S520619Entity, ClimateEntity):
    _attr_has_entity_name = True
    _attr_target_temperature_step = 0.5
    _attr_min_temp = 4.0
    _attr_max_temp = 30.0
    _attr_hvac_modes = list(SYSTEM_MODE_MAP.values())
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE_RANGE |
        ClimateEntityFeature.TURN_OFF |
        ClimateEntityFeature.TURN_ON
    )

    def __init__(self, entry: ConfigEntry, state: S520619State) -> None:
        self._entry = entry
        self._state = state
        self._attr_name = self._entry.title
        self._attr_unique_id = entry.entry_id

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

    @property
    def precision(self) -> float:
        return self._entry.options.get(CONF_TEMPERATURE_PRECISION, 3)

    @property
    def temperature_unit(self) -> str:
        return self._entry.options.get(CONF_THERMOSTAT_UNIT, UnitOfTemperature.CELSIUS)

    @property
    def hvac_mode(self) -> HVACMode:
        return SYSTEM_MODE_MAP.get(self._state.system_mode)

    @property
    def hvac_action(self) -> HVACAction:
        return RUNNING_STATE_MAP.get(self._state.running_state)

    @property
    def current_temperature(self) -> float:
        return self._state.local_temperature

    @property
    def target_temperature_low(self) -> float:
        return self._state.occupied_cooling_setpoint

    @property
    def target_temperature_high(self) -> float:
        return self._state.occupied_heating_setpoint


    def set_temperature(self, **kwargs) -> None:
        if (temp := kwargs.get(ATTR_TARGET_TEMP_HIGH)) is not None:
            self._state.occupied_heating_setpoint = temp
        elif (temp := kwargs.get(ATTR_TARGET_TEMP_LOW)) is not None:
            self._state.occupied_cooling_setpoint = temp
        self._state.notify()

    def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        self._state.system_mode = HVAC_MODE_MAP.get(hvac_mode)
        self._state.notify()

