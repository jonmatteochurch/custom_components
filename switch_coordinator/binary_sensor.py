"""BinarySensorEntity platform for Switch Coordinator."""
# from __future__ import annotations
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN, CONF_MASTER_SWITCHES, CONF_SLAVE_SWITCHES



async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([SwitchCoordinator(hass, entry)])


class SwitchCoordinator(BinarySensorEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, hass, entry) -> None:
        self._hass = hass
        self._entry = entry
        self._attr_unique_id = entry.entry_id
        self._masters = []
        self._slaves = []
        self._unsub = []

    async def async_added_to_hass(self) -> None:
        self._masters = self._entry.options.get(CONF_MASTER_SWITCHES)
        self._slaves = self._entry.options.get(CONF_SLAVE_SWITCHES)
        if self._masters:
            self._unsub.append(async_track_state_change_event(self._hass, self._masters, self._handle_master_state_change))
            
    async def async_will_remove_from_hass(self) -> None:
        for unsub in self._unsub:
            unsub()
        self._unsub.clear()

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            model="Switch Coordinator",
            manufacturer="Jon Matteo Church"
        )
        
    def _state(self, eid: str):
        st = self._hass.states.get(eid)
        return st.state if st else None

    @property
    def is_on(self) -> bool:
        return self._slaves and any(self._state(e) == STATE_ON for e in self._slaves)

    @callback
    async def _handle_master_state_change(self, event) -> None:
        eid = event.data.get("entity_id")
        assert(eid in self._masters)

        old_state = event.data.get("old_state")
        new_state = event.data.get("new_state")
        if old_state is None or new_state is None or new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return

        service = "turn_off" if self.is_on else "turn_on"
    
        for slave in self._slaves:
            await self.hass.services.async_call("switch", service, {"entity_id": slave})
