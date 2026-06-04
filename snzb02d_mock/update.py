"""Update platform for SNZB-02D Mock."""
from __future__ import annotations
from homeassistant.components.update import UpdateEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import SNZB02DState
from .const import DOMAIN
from .entity import SNZB02DEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    state: SNZB02DState = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        SNZB02DUpdate(entry, state)
    ])


class SNZB02DUpdate(SNZB02DEntity, UpdateEntity):
    _attr_has_entity_name = True
    _attr_name = None
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry, state) -> None:
        self._entry = entry
        self._state = state
        self._attr_unique_id = entry.entry_id
