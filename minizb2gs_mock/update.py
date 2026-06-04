"""Update platform for MINI-ZB2GS Mock."""
from __future__ import annotations
from homeassistant.components.update import UpdateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import MINIZB2GSState
from .const import  DOMAIN
from .entity import MINIZB2GSEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: MINIZB2GSState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MINIZB2GSUpdate(entry, state)
    ])


class MINIZB2GSUpdate(MINIZB2GSEntity, UpdateEntity):
    _attr_has_entity_name = True
    _attr_name = None
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state) -> None:
        self._entry = entry
        self._state = state
        self._attr_unique_id = entry.entry_id
