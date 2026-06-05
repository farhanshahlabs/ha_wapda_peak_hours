"""Config flow for WAPDA Peak Hours."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_DISCO, DISCO_NAMES, DOMAIN


class WapdaPeakHoursConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            disco = user_input[CONF_DISCO]
            await self.async_set_unique_id(disco)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=DISCO_NAMES[disco],
                data={CONF_DISCO: disco},
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_DISCO): vol.In(DISCO_NAMES),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)
