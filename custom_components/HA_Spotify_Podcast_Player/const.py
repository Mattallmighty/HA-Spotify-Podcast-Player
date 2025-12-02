"""Constants for the HA Spotify Podcast Player integration."""

DOMAIN = "ha_spotify_podcast_player"

# Configuration keys
CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_PODCAST_URL = "podcast_url"
CONF_FILTER_KEYWORDS = "filter_keywords"
CONF_START_TIME = "start_time"

# Default values
DEFAULT_FILTER_KEYWORDS = "Headlines:"
DEFAULT_START_TIME = 0
DEFAULT_EPISODES_TO_CHECK = 5

# Service names
SERVICE_PLAY_FILTERED_EPISODE = "play_filtered_episode"

# Attributes
ATTR_ENTITY_ID = "entity_id"
ATTR_PODCAST_URL = "podcast_url"
ATTR_FILTER_KEYWORDS = "filter_keywords"
ATTR_START_TIME = "start_time"
ATTR_EPISODES_TO_CHECK = "episodes_to_check"
