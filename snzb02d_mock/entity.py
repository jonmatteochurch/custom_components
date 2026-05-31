from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN

class SNZB02DEntity:
    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            model="Sonoff SNZB-02D (Mock Temp/Humidity Sensor)",
            manufacturer="Jon Matteo Church"
        )