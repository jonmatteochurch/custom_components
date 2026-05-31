from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN

class ZBMINIR2Entity:
    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            model="Sonoff ZBMINIR2 (Mock Switch)",
            manufacturer="Jon Matteo Church"
        )