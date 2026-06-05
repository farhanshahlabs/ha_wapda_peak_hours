"""Sensors for WAPDA Peak Hours."""
from __future__ import annotations

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval

from .const import CONF_DISCO, DISCO_NAMES, DOMAIN
from .peak_hours import get_peak_info

SCAN_INTERVAL = timedelta(seconds=30)


def _device_info(disco: str) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, disco)},
        name=f"Electricity Grid ({disco})",
        manufacturer="WAPDA / NEPRA",
        model=DISCO_NAMES[disco],
        entry_type="service",
    )


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    disco = entry.data[CONF_DISCO]
    entities = [
        IsPeakHourSensor(disco, entry.entry_id),
        IsOffPeakSensor(disco, entry.entry_id),
        TariffPeriodSensor(disco, entry.entry_id),
        TimeUntilPeakEndsSensor(disco, entry.entry_id),
        TimeUntilPeakStartsSensor(disco, entry.entry_id),
        PeakStartTodaySensor(disco, entry.entry_id),
        PeakEndTodaySensor(disco, entry.entry_id),
    ]
    async_add_entities(entities, update_before_add=True)

    def _refresh(_now=None):
        for e in entities:
            e.schedule_update_ha_state(True)

    entry.async_on_unload(
        async_track_time_interval(hass, _refresh, SCAN_INTERVAL)
    )


class _BaseSensor(SensorEntity):
    _attr_should_poll = False

    def __init__(self, disco: str, entry_id: str, key: str, name: str) -> None:
        self._disco = disco
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_device_info = _device_info(disco)
        self._data: dict = {}

    def update(self) -> None:
        self._data = get_peak_info(self._disco)

    @property
    def extra_state_attributes(self):
        return {"disco": self._disco}


class IsPeakHourSensor(_BaseSensor):
    _attr_icon = "mdi:lightning-bolt"

    def __init__(self, disco, entry_id):
        super().__init__(disco, entry_id, "is_peak_hour", "Peak Hours Active")

    @property
    def native_value(self):
        return "True" if self._data.get("is_peak", False) else "False"


class IsOffPeakSensor(_BaseSensor):
    _attr_icon = "mdi:lightning-bolt-outline"

    def __init__(self, disco, entry_id):
        super().__init__(disco, entry_id, "is_off_peak", "Off-Peak Active")

    @property
    def native_value(self):
        return "False" if self._data.get("is_peak", False) else "True"


class TariffPeriodSensor(_BaseSensor):
    _attr_icon = "mdi:transmission-tower"

    def __init__(self, disco, entry_id):
        super().__init__(disco, entry_id, "tariff_period", "Tariff Period")

    @property
    def native_value(self):
        return self._data.get("tariff_period")


class TimeUntilPeakEndsSensor(_BaseSensor):
    _attr_icon = "mdi:timer-off-outline"

    def __init__(self, disco, entry_id):
        super().__init__(disco, entry_id, "time_until_peak_ends", "Time Until Peak Ends")

    @property
    def native_value(self):
        return self._data.get("time_until_peak_ends") or "N/A"


class TimeUntilPeakStartsSensor(_BaseSensor):
    _attr_icon = "mdi:timer-outline"

    def __init__(self, disco, entry_id):
        super().__init__(disco, entry_id, "time_until_peak_starts", "Time Until Peak Starts")

    @property
    def native_value(self):
        return self._data.get("time_until_peak_starts") or "N/A"


class PeakStartTodaySensor(_BaseSensor):
    _attr_icon = "mdi:clock-start"
    _attr_device_class = "timestamp"

    def __init__(self, disco, entry_id):
        super().__init__(disco, entry_id, "peak_start_today", "Peak Start Today")

    @property
    def native_value(self):
        val = self._data.get("peak_start_today")
        if val:
            return datetime.fromisoformat(val)
        return None


class PeakEndTodaySensor(_BaseSensor):
    _attr_icon = "mdi:clock-end"
    _attr_device_class = "timestamp"

    def __init__(self, disco, entry_id):
        super().__init__(disco, entry_id, "peak_end_today", "Peak End Today")

    @property
    def native_value(self):
        val = self._data.get("peak_end_today")
        if val:
            return datetime.fromisoformat(val)
        return None
