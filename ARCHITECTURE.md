# Architecture & How It Works

This document explains the technical architecture and workflow of the HA Spotify Podcast Player integration.

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Component Overview](#component-overview)
3. [Data Flow](#data-flow)
4. [Sequence Diagrams](#sequence-diagrams)
5. [Technical Details](#technical-details)

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Home Assistant                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         HA Spotify Podcast Player Integration              │  │
│  │                                                          │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌───────────────┐  │  │
│  │  │Config Flow │  │ Service Layer│  │ Spotify API   │  │  │
│  │  │   (UI)     │  │              │  │   Client      │  │  │
│  │  └────────────┘  └──────────────┘  └───────────────┘  │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              │ Commands                         │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Media Player Integration                    │  │
│  │        (Sonos, Google Home, Spotify, etc.)              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ API Calls
                              ▼
                 ┌─────────────────────────┐
                 │     Spotify Web API     │
                 │  (developer.spotify.com) │
                 └─────────────────────────┘
```

## Component Overview

### 1. Configuration Flow (`config_flow.py`)

**Purpose**: Handles the UI-based setup of the integration

**Responsibilities**:

- Collects Spotify API credentials (Client ID, Client Secret)
- Validates credentials by testing connection to Spotify
- Stores configuration in Home Assistant's encrypted storage
- Provides default values for podcast URL, filter keywords, and start time

**User Interaction**:

```
User → Settings → Add Integration → HA Spotify Podcast Player
     → Enter credentials → Validation → Save
```

### 2. Core Integration (`__init__.py`)

**Purpose**: Main integration logic and service registration

**Responsibilities**:

- Initializes the integration when Home Assistant starts
- Registers the `play_filtered_episode` service
- Handles service calls from automations
- Manages Spotify API authentication
- Orchestrates the episode search and playback process

**Key Functions**:

```python
async_setup_entry()         # Setup integration
handle_play_filtered_episode()  # Main service handler
async_unload_entry()        # Cleanup on removal
```

### 3. Constants (`const.py`)

**Purpose**: Centralized configuration and constant values

**Contains**:

- Domain name
- Configuration keys
- Default values
- Service names
- Attribute names

### 4. Services Definition (`services.yaml`)

**Purpose**: Describes the service for Home Assistant's UI

**Defines**:

- Service name and description
- Input parameters and their types
- Parameter validation rules
- UI selectors for parameters

### 5. Translations (`strings.json`, `translations/en.json`)

**Purpose**: Internationalization support

**Contains**:

- UI text for configuration flow
- Error messages
- Service descriptions
- Help text

## Data Flow

### Initialization Flow

```
Home Assistant Startup
        │
        ▼
Load Integration (async_setup_entry)
        │
        ├─→ Read stored configuration
        │   (Client ID, Client Secret, defaults)
        │
        ├─→ Register service
        │   (HA_Spotify_Podcast_Player.play_filtered_episode)
        │
        └─→ Ready to handle service calls
```

### Service Call Flow

```
Automation Trigger (e.g., 7:00 AM)
        │
        ▼
Call Service: play_filtered_episode
        │
        ├─→ Parameters
        │   ├─ entity_id: media_player.sonos
        │   ├─ podcast_url: https://open.spotify.com/...
        │   ├─ filter_keywords: "Headlines:"
        │   ├─ start_time: 0
        │   └─ episodes_to_check: 5
        │
        ▼
Service Handler (handle_play_filtered_episode)
        │
        ├─→ Extract show ID from URL
        │
        ├─→ Authenticate with Spotify API
        │   (using Client Credentials flow)
        │
        ├─→ Fetch recent episodes
        │   (sp.show_episodes)
        │
        ├─→ Filter episodes
        │   (search for keywords in title/description)
        │
        ├─→ Get first matching episode URI
        │
        ├─→ Call media_player.play_media
        │   (play episode on specified device)
        │
        └─→ Call media_player.media_seek
            (skip to start_time if > 0)
```

## Sequence Diagrams

### Setup Sequence

```
User          Home Assistant    Config Flow    Spotify API
 │                  │                │              │
 │ Add Integration  │                │              │
 ├─────────────────►│                │              │
 │                  │ Show UI        │              │
 │                  ├───────────────►│              │
 │                  │                │              │
 │ Enter Creds      │                │              │
 ├──────────────────┼───────────────►│              │
 │                  │                │ Validate     │
 │                  │                ├─────────────►│
 │                  │                │ ✓ OK         │
 │                  │                │◄─────────────┤
 │                  │ Save Config    │              │
 │                  │◄───────────────┤              │
 │ Success          │                │              │
 │◄─────────────────┤                │              │
```

### Playback Sequence

```
Automation    Integration    Spotify API    Media Player
    │              │              │               │
    │ Trigger      │              │               │
    │ (7:00 AM)    │              │               │
    │              │              │               │
    │ Call Service │              │               │
    ├─────────────►│              │               │
    │              │ Auth         │               │
    │              ├─────────────►│               │
    │              │ Token        │               │
    │              │◄─────────────┤               │
    │              │              │               │
    │              │ Get Episodes │               │
    │              ├─────────────►│               │
    │              │ Episode List │               │
    │              │◄─────────────┤               │
    │              │              │               │
    │              │ Filter       │               │
    │              │ (Keywords)   │               │
    │              │              │               │
    │              │ Play Media   │               │
    │              ├──────────────┼──────────────►│
    │              │              │    Playing    │
    │              │◄─────────────┼───────────────┤
    │              │              │               │
    │              │ Seek         │               │
    │              ├──────────────┼──────────────►│
    │              │              │    Seeked     │
    │              │◄─────────────┼───────────────┤
    │ Complete     │              │               │
    │◄─────────────┤              │               │
```

## Technical Details

### Authentication

The integration uses **Spotify Client Credentials Flow**:

1. **No User Login Required**: Uses app credentials only
2. **Token Management**: Spotipy library handles token refresh automatically
3. **Scope**: Read-only access to public podcast data

```python
auth_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)
```

### Episode Filtering Logic

```python
def find_matching_episode(episodes, filter_keywords):
    """
    Search logic:
    1. Iterate through episodes (most recent first)
    2. Check episode name (case-insensitive)
    3. Check episode description (case-insensitive)
    4. Return first match
    """
    keywords_lower = filter_keywords.lower()

    for episode in episodes:
        name = episode.get("name", "").lower()
        description = episode.get("description", "").lower()

        if keywords_lower in name or keywords_lower in description:
            return episode

    return None
```

### Media Player Commands

#### Play Media

```python
await hass.services.async_call(
    "media_player",
    "play_media",
    {
        "entity_id": entity_id,
        "media_content_id": episode_uri,  # spotify:episode:XXXXX
        "media_content_type": "episode",
    },
    blocking=True,
)
```

#### Seek

```python
await hass.services.async_call(
    "media_player",
    "media_seek",
    {
        "entity_id": entity_id,
        "seek_position": start_time,  # in seconds
    },
)
```

### Error Handling

The integration implements comprehensive error handling:

```python
try:
    # Spotify API operations
    results = sp.show_episodes(show_id)
except Exception as err:
    _LOGGER.error("Error: %s", err, exc_info=True)
    return
```

**Error Categories**:

1. **Authentication Errors**: Invalid credentials
2. **Network Errors**: Connection timeout, API unavailable
3. **Data Errors**: Invalid podcast URL, no episodes found
4. **Playback Errors**: Media player unavailable, unsupported format

### Logging

The integration provides detailed logging:

```python
# Info level: Normal operations
_LOGGER.info("Playing episode: %s", episode_name)

# Debug level: Detailed information
_LOGGER.debug("Checking episode: %s", episode_name)

# Error level: Problems
_LOGGER.error("No episodes found for show: %s", show_id)
```

**Enable Debug Logging**:

```yaml
logger:
  logs:
    custom_components.HA_Spotify_Podcast_Player: debug
```

### Asynchronous Operations

Home Assistant requires async operations for performance:

```python
# Run blocking Spotify calls in executor
results = await hass.async_add_executor_job(
    sp.show_episodes, show_id, None, episodes_to_check
)

# Async service calls
await hass.services.async_call(...)
```

### State Management

The integration is **stateless** by design:

- No persistent state between calls
- Each service call is independent
- Configuration stored in Home Assistant's config entry
- No background polling or continuous monitoring

## Performance Considerations

### API Calls per Service Invocation

1. **Authentication**: ~1 call (cached by spotipy)
2. **Fetch Episodes**: 1 call
3. **Play Media**: 1 local call to media player
4. **Seek**: 1 local call to media player

**Total external API calls**: ~2 per automation trigger

### Optimization Strategies

1. **Limited Episode Fetch**: Only fetch `episodes_to_check` (default: 5)
2. **Early Return**: Stop searching after first match
3. **Token Caching**: Spotipy handles token caching automatically
4. **Async Operations**: Non-blocking execution

### Rate Limits

**Spotify API Limits**:

- Free tier: ~180 requests per minute
- Daily limit: ~10,000+ requests

**Integration Usage**:

- Typical automation: 2 API calls
- Daily automation (once/day): ~60 calls/month
- Well below Spotify limits

## Extension Points

The integration is designed for extensibility:

### 1. Additional Filters

```python
# Current: keyword matching
# Possible: regex, date-based, duration filters
```

### 2. Multi-Podcast Support

```python
# Store multiple podcast configurations
# Switch between them in automations
```

### 3. Caching Layer

```python
# Cache episode lists to reduce API calls
# Invalidate cache periodically
```

### 4. Queue Management

```python
# Build episode queues
# Play multiple episodes sequentially
```

## Security Considerations

### Credential Storage

- **Encrypted**: Stored in Home Assistant's encrypted storage
- **Not Logged**: Credentials never appear in logs
- **Local Only**: Never transmitted except to Spotify API

### API Permissions

- **Read-Only**: Cannot modify Spotify account
- **Public Data**: Only accesses public podcast information
- **No User Data**: Doesn't access user playlists or history

### Network Security

- **HTTPS**: All API calls use HTTPS
- **No External Services**: Only communicates with Spotify API
- **No Telemetry**: No data sent to third parties

## Testing Strategy

### Unit Tests (Future Enhancement)

```python
# test_filter.py
def test_episode_filtering():
    episodes = [...]
    result = find_matching_episode(episodes, "Headlines:")
    assert result["name"] == "Headlines: Test"
```

### Integration Tests

```python
# test_service.py
async def test_service_call(hass):
    await hass.services.async_call(
        DOMAIN,
        SERVICE_PLAY_FILTERED_EPISODE,
        {...}
    )
    # Assert media player received commands
```

### Manual Testing Checklist

- [ ] Configuration flow accepts valid credentials
- [ ] Configuration flow rejects invalid credentials
- [ ] Service plays correct episode
- [ ] Service filters episodes correctly
- [ ] Service seeks to correct timestamp
- [ ] Service handles missing episodes gracefully
- [ ] Error logging works correctly

## Troubleshooting Tools

### 1. Test Script

Use `tools/test_podcast.py` to:

- Verify credentials
- List recent episodes
- Test filter keywords

### 2. Debug Logging

Enable detailed logs:

```yaml
logger:
  logs:
    custom_components.HA_Spotify_Podcast_Player: debug
    spotipy: debug
```

### 3. Developer Tools

Use Home Assistant's Developer Tools:

- **Services**: Test service calls manually
- **States**: Check media player states
- **Logs**: View real-time logs

## Future Enhancements

Potential improvements:

1. **Episode Caching**: Reduce API calls
2. **Advanced Filtering**: Regex, date ranges
3. **Playlist Support**: Play multiple episodes
4. **Notifications**: Alert when episode plays
5. **Statistics**: Track played episodes
6. **Multiple Accounts**: Support multiple Spotify accounts
7. **UI Dashboard**: Visual episode browser
8. **Episode History**: Track what's been played

## Contributing

To contribute to the architecture:

1. **Understand the flow**: Study the sequence diagrams
2. **Maintain patterns**: Follow existing async patterns
3. **Add tests**: Include tests for new features
4. **Document changes**: Update this document
5. **Follow conventions**: Use Home Assistant best practices

## References

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [Spotipy Documentation](https://spotipy.readthedocs.io/)
- [Home Assistant Service Calls](https://www.home-assistant.io/docs/scripts/service-calls/)
