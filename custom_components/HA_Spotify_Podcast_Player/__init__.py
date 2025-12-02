"""The HA Spotify Podcast Player integration."""
import logging
import re
from datetime import timedelta
from typing import Any

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTR_ENTITY_ID,
    ATTR_EPISODES_TO_CHECK,
    ATTR_FILTER_KEYWORDS,
    ATTR_PODCAST_URL,
    ATTR_START_TIME,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_FILTER_KEYWORDS,
    CONF_PODCAST_URL,
    CONF_START_TIME,
    DEFAULT_EPISODES_TO_CHECK,
    DEFAULT_FILTER_KEYWORDS,
    DEFAULT_START_TIME,
    DOMAIN,
    SERVICE_PLAY_FILTERED_EPISODE,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = []

# Service schema
SERVICE_PLAY_FILTERED_EPISODE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_ENTITY_ID): cv.entity_id,
        vol.Optional(ATTR_PODCAST_URL): cv.string,
        vol.Optional(ATTR_FILTER_KEYWORDS): cv.string,
        vol.Optional(ATTR_START_TIME, default=DEFAULT_START_TIME): cv.positive_int,
        vol.Optional(
            ATTR_EPISODES_TO_CHECK, default=DEFAULT_EPISODES_TO_CHECK
        ): cv.positive_int,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HA Spotify Podcast Player component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA Spotify Podcast Player from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_CLIENT_ID: entry.data[CONF_CLIENT_ID],
        CONF_CLIENT_SECRET: entry.data[CONF_CLIENT_SECRET],
        CONF_PODCAST_URL: entry.data.get(CONF_PODCAST_URL, ""),
        CONF_FILTER_KEYWORDS: entry.data.get(
            CONF_FILTER_KEYWORDS, DEFAULT_FILTER_KEYWORDS
        ),
        CONF_START_TIME: entry.data.get(CONF_START_TIME, DEFAULT_START_TIME),
    }

    async def handle_play_filtered_episode(call: ServiceCall) -> None:
        """Handle the service call to play a filtered podcast episode."""
        entity_id = call.data[ATTR_ENTITY_ID]
        podcast_url = call.data.get(ATTR_PODCAST_URL) or entry.data.get(
            CONF_PODCAST_URL, ""
        )
        filter_keywords = call.data.get(ATTR_FILTER_KEYWORDS) or entry.data.get(
            CONF_FILTER_KEYWORDS, DEFAULT_FILTER_KEYWORDS
        )
        start_time = call.data.get(ATTR_START_TIME, DEFAULT_START_TIME)
        episodes_to_check = call.data.get(
            ATTR_EPISODES_TO_CHECK, DEFAULT_EPISODES_TO_CHECK
        )

        if not podcast_url:
            _LOGGER.error("No podcast URL provided")
            return

        # Extract show ID from Spotify URL
        show_id_match = re.search(r"show/([a-zA-Z0-9]+)", podcast_url)
        if not show_id_match:
            _LOGGER.error("Invalid Spotify podcast URL: %s", podcast_url)
            return

        show_id = show_id_match.group(1)

        # Get Spotify credentials
        client_id = entry.data[CONF_CLIENT_ID]
        client_secret = entry.data[CONF_CLIENT_SECRET]

        try:
            # Authenticate with Spotify
            auth_manager = SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
            sp = spotipy.Spotify(auth_manager=auth_manager)

            # Get show episodes
            _LOGGER.info("Fetching episodes for show: %s", show_id)
            results = await hass.async_add_executor_job(
                sp.show_episodes, show_id, None, episodes_to_check
            )

            if not results or "items" not in results:
                _LOGGER.error("No episodes found for show: %s", show_id)
                return

            # Log all episodes found for debugging
            _LOGGER.info("Found %d episodes, checking for filter: '%s'", len(results["items"]), filter_keywords)
            for idx, ep in enumerate(results["items"]):
                _LOGGER.info("Episode %d: '%s' (Released: %s)", idx + 1, ep.get("name", ""), ep.get("release_date", ""))

            # Find the first episode matching the filter
            matching_episode = None
            for episode in results["items"]:
                episode_name = episode.get("name", "")
                episode_description = episode.get("description", "")

                # Check if filter keywords are in the episode name or description
                if filter_keywords.lower() in episode_name.lower() or filter_keywords.lower() in episode_description.lower():
                    matching_episode = episode
                    _LOGGER.info("✓ MATCHED episode: '%s' (Released: %s)", episode_name, episode.get("release_date", ""))
                    break
                else:
                    _LOGGER.debug("✗ Skipped episode: '%s' - does not contain '%s'", episode_name, filter_keywords)

            if not matching_episode:
                _LOGGER.warning(
                    "No episode found with filter keywords: %s", filter_keywords
                )
                return

            episode_uri = matching_episode["uri"]
            episode_name = matching_episode["name"]

            _LOGGER.info(
                "Playing episode: %s on device: %s at %s seconds",
                episode_name,
                entity_id,
                start_time,
            )

            # Play the episode on the specified media player
            # First, play the episode
            await hass.services.async_call(
                "media_player",
                "play_media",
                {
                    "entity_id": entity_id,
                    "media_content_id": episode_uri,
                    "media_content_type": "episode",
                },
                blocking=True,
            )

            # Wait a moment for playback to start, then seek if needed
            if start_time > 0:
                await hass.async_add_executor_job(
                    lambda: hass.loop.call_later(
                        2,
                        lambda: hass.async_create_task(
                            hass.services.async_call(
                                "media_player",
                                "media_seek",
                                {
                                    "entity_id": entity_id,
                                    "seek_position": start_time,
                                },
                            )
                        ),
                    )
                )

        except Exception as err:
            _LOGGER.error("Error playing filtered episode: %s", err, exc_info=True)

    # Register the service
    hass.services.async_register(
        DOMAIN,
        SERVICE_PLAY_FILTERED_EPISODE,
        handle_play_filtered_episode,
        schema=SERVICE_PLAY_FILTERED_EPISODE_SCHEMA,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)

    # Unregister service if no more entries
    if not hass.data[DOMAIN]:
        hass.services.async_remove(DOMAIN, SERVICE_PLAY_FILTERED_EPISODE)

    return True
