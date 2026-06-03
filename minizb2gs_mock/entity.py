from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, CONF_NAME

class MINIZB2GSEntity:
    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.options.get(CONF_NAME),
            model="Sonoff MINI-ZB2GS (Mock Double Switch)",
            manufacturer="Jon Matteo Church"
        )