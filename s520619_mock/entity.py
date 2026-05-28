from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN

class S520619Entity:
    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            model="Schneider Electric S520619 (mock setpoint)",
            manufacturer="Jon Matteo Church"
        )