"""Update platform for ZBMINIR2 Mock."""
from __future__ import annotations
from homeassistant.components.update import UpdateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import ZBMINIR2State
from .const import DOMAIN
from .entity import ZBMINIR2Entity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: ZBMINIR2State = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ZBMINIR2Update(entry, state)
    ])


class ZBMINIR2Update(ZBMINIR2Entity, UpdateEntity):
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state) -> None:
        self._entry = entry
        self._state = state
        self._attr_name = entry.title
        self._attr_unique_id = entry.entry_id
