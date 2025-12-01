"""Config flow for HA Spotify Podcast Player integration."""
import logging
from typing import Any

import voluptuous as vol
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_FILTER_KEYWORDS,
    CONF_PODCAST_URL,
    CONF_START_TIME,
    DEFAULT_FILTER_KEYWORDS,
    DEFAULT_START_TIME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def validate_spotify_credentials(
    hass: HomeAssistant, client_id: str, client_secret: str
) -> bool:
    """Validate Spotify API credentials."""
    try:
        auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        # Try to make a simple API call to validate credentials
        await hass.async_add_executor_job(sp.current_user)
        return True
    except Exception as err:
        _LOGGER.error("Failed to validate Spotify credentials: %s", err)
        return False


class SpotifyPodcastPlayerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HA Spotify Podcast Player."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate Spotify credentials
            client_id = user_input[CONF_CLIENT_ID]
            client_secret = user_input[CONF_CLIENT_SECRET]

            if await validate_spotify_credentials(self.hass, client_id, client_secret):
                return self.async_create_entry(
                    title="HA Spotify Podcast Player",
                    data=user_input,
                )
            else:
                errors["base"] = "invalid_auth"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
                vol.Optional(
                    CONF_PODCAST_URL,
                    default="https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A",
                ): cv.string,
                vol.Optional(
                    CONF_FILTER_KEYWORDS, default=DEFAULT_FILTER_KEYWORDS
                ): cv.string,
                vol.Optional(CONF_START_TIME, default=DEFAULT_START_TIME): cv.positive_int,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_import(self, user_input: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input)
