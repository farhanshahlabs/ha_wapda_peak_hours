# WAPDA Peak Hours — Home Assistant Integration

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/farhanshahlabs/ha_wapda_peak_hours?style=flat-square)](https://github.com/farhanshahlabs/ha_wapda_peak_hours/releases)
[![Validate](https://github.com/farhanshahlabs/ha_wapda_peak_hours/actions/workflows/validate.yml/badge.svg)](https://github.com/farhanshahlabs/ha_wapda_peak_hours/actions/workflows/validate.yml)

A **100% offline** Home Assistant integration that tracks electricity peak hours for Pakistani distribution companies (DISCOs). No internet connection required after setup.

---

## Features

- Select your DISCO from a dropdown during setup
- 7 sensors updated every 30 seconds
- Fully offline — all schedules are hardcoded per NEPRA/DISCO published data
- HACS compatible

---

## Supported DISCOs

| DISCO | Region |
|---|---|
| IESCO | Islamabad |
| GEPCO | Gujranwala |
| LESCO | Lahore |
| MEPCO | Multan |
| PESCO | Peshawar |
| HESCO | Hyderabad |
| QESCO | Quetta |
| SEPCO | Sukkur |
| KE | Karachi |
| TESCO | Tribal Areas |

---

## Peak Hour Schedules

| DISCO | Months | Peak Hours |
|---|---|---|
| IESCO / GEPCO / LESCO | Dec–Feb | 5:00 PM – 9:00 PM |
| IESCO / GEPCO / LESCO | Mar–May, Sep–Nov | 6:00 PM – 10:00 PM |
| IESCO / GEPCO / LESCO | Jun–Aug | 7:00 PM – 11:00 PM |
| MEPCO / PESCO / HESCO / QESCO / SEPCO / KE | Nov–Mar | 6:00 PM – 10:00 PM |
| MEPCO / PESCO / HESCO / QESCO / SEPCO / KE | Apr–Oct | 6:30 PM – 10:30 PM |
| TESCO | All year | 6:00 PM – 10:00 PM |

---

## Sensors

| Entity | Type | Description |
|---|---|---|
| `binary_sensor.<disco>_is_peak_hour` | Binary | `on` during peak hours |
| `binary_sensor.<disco>_is_off_peak` | Binary | `on` outside peak hours |
| `sensor.<disco>_tariff_period` | Sensor | `Peak` or `Off-Peak` |
| `sensor.<disco>_time_until_peak_ends` | Sensor | HH:MM until peak ends (peak only) |
| `sensor.<disco>_time_until_peak_starts` | Sensor | HH:MM until next peak (off-peak only) |
| `sensor.<disco>_peak_start_today` | Timestamp | Today's peak start time |
| `sensor.<disco>_peak_end_today` | Timestamp | Today's peak end time |

---

## Installation

### Via HACS (Recommended)

1. Open HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/farhanshahlabs/ha_wapda_peak_hours` as **Integration**
3. Install **WAPDA Peak Hours**
4. Restart Home Assistant
5. Go to **Settings → Devices & Services → Add Integration** → search **WAPDA Peak Hours**
6. Select your DISCO from the dropdown

### Manual

1. Copy `custom_components/wapda_peak_hours` into your HA `custom_components` folder
2. Restart Home Assistant
3. Add integration via UI

---

## Automation / Notification Templates

### Notify 30 minutes before peak starts

```yaml
automation:
  - alias: "Notify before peak hours"
    trigger:
      - platform: template
        value_template: >
          {{ states('sensor.gepco_time_until_peak_starts') == '00:30' }}
    action:
      - service: notify.mobile_app
        data:
          title: "⚡ Peak Hours Soon"
          message: "Electricity peak hours start in 30 minutes. Turn off heavy appliances."
```

### Notify when peak ends

```yaml
automation:
  - alias: "Notify peak hours ended"
    trigger:
      - platform: state
        entity_id: binary_sensor.gepco_is_peak_hour
        from: "on"
        to: "off"
    action:
      - service: notify.mobile_app
        data:
          title: "✅ Peak Hours Ended"
          message: "Off-peak hours have started. You can run heavy appliances now."
```

### Auto turn off AC during peak hours

```yaml
automation:
  - alias: "Turn off AC during peak"
    trigger:
      - platform: state
        entity_id: binary_sensor.gepco_is_peak_hour
        to: "on"
    action:
      - service: climate.turn_off
        target:
          entity_id: climate.living_room_ac
```

---

## License

GPL-3.0 license © [farhanshahlabs](https://github.com/farhanshahlabs)
