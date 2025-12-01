# Installation Guide - HA Spotify Podcast Player

This guide will walk you through installing and configuring the HA Spotify Podcast Player integration for Home Assistant.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Spotify API Credentials](#getting-spotify-api-credentials)
3. [Installation Methods](#installation-methods)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- Home Assistant 2023.1.0 or newer
- A Spotify account (free or premium)
- A media player connected to Home Assistant (Sonos, etc.)
- Internet connection

## Getting Spotify API Credentials

### Step-by-Step Guide

1. **Go to Spotify Developer Dashboard**

   - Open https://developer.spotify.com/dashboard
   - Log in with your Spotify account

2. **Create a New App**

   - Click the "Create app" button
   - Fill in the required fields:
     - **App Name**: `Home Assistant Podcast Player` (or any name you prefer)
     - **App Description**: `Integration for playing podcasts in Home Assistant`
     - **Redirect URIs**: Leave blank (not needed for this integration)
     - **Which API/SDKs are you planning to use?**: Select "Web API"

3. **Accept Terms and Create**

   - Check the boxes to agree to Spotify's terms
   - Click "Save"

4. **Get Your Credentials**
   - You'll see your **Client ID** immediately
   - Click "Settings" to reveal your **Client Secret**
   - **IMPORTANT**: Copy both values - you'll need them for configuration
   - Keep these credentials secure - treat them like passwords

### Example Credentials Format

```
Client ID: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
Client Secret: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

## Installation Methods

### Method 1: Via HACS (Recommended)

HACS (Home Assistant Community Store) makes installation and updates easy.

#### Prerequisites for HACS

- HACS must be installed in your Home Assistant
- If you don't have HACS, install it first: https://hacs.xyz/docs/setup/download

#### Installation Steps

1. **Open HACS**

   - Go to Home Assistant
   - Click on "HACS" in the sidebar

2. **Add Custom Repository**

   - Click the 3 dots menu in the top right
   - Select "Custom repositories"
   - Add repository URL: `https://github.com/Mattallmighty/HA-Spotify-Podcast-Player`
   - Category: "Integration"
   - Click "Add"

3. **Install Integration**

   - Search for "HA Spotify Podcast Player" in HACS
   - Click on it
   - Click "Download"
   - Click "Download" again to confirm

4. **Restart Home Assistant**
   - Go to Settings → System → Restart
   - Click "Restart Home Assistant"

### Method 2: Manual Installation

If you prefer not to use HACS or want more control:

1. **Download Files**

   - Download or clone this repository
   - You need the `custom_components/HA_Spotify_Podcast_Player` folder

2. **Copy to Home Assistant**

   ```bash
   # On your Home Assistant system
   cd /config
   mkdir -p custom_components
   cp -r HA_Spotify_Podcast_Player custom_components/
   ```

3. **Directory Structure**
   Your `config` directory should look like:

   ```
   config/
   ├── custom_components/
   │   └── HA_Spotify_Podcast_Player/
   │       ├── __init__.py
   │       ├── config_flow.py
   │       ├── const.py
   │       ├── manifest.json
   │       ├── services.yaml
   │       ├── strings.json
   │       └── translations/
   │           └── en.json
   └── configuration.yaml
   ```

4. **Restart Home Assistant**
   - Go to Settings → System → Restart
   - Click "Restart Home Assistant"

## Configuration

### Step 1: Add Integration

1. **Navigate to Integrations**

   - Go to Settings → Devices & Services
   - Click "+ Add Integration" (bottom right)

2. **Search and Select**

   - Type "HA Spotify Podcast Player"
   - Click on it

3. **Enter Configuration**

   - **Spotify Client ID**: Paste your Client ID from Spotify Developer Dashboard
   - **Spotify Client Secret**: Paste your Client Secret
   - **Default Podcast URL** (optional): `https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A`
   - **Default Filter Keywords** (optional): `Headlines:`
   - **Default Start Time** (optional): `0`

4. **Submit**
   - Click "Submit"
   - If credentials are valid, you'll see "Success!"

### Step 2: Verify Installation

1. **Check Developer Tools**
   - Go to Developer Tools → Services
   - Search for `HA_Spotify_Podcast_Player.play_filtered_episode`
   - If you see it, installation was successful!

### Step 3: Test the Service

1. **In Developer Tools → Services**

   - Service: `HA_Spotify_Podcast_Player.play_filtered_episode`
   - Fill in:
     ```yaml
     entity_id: media_player.your_sonos
     podcast_url: "https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A"
     filter_keywords: "Headlines:"
     start_time: 0
     episodes_to_check: 5
     ```
   - Click "Call Service"

2. **Check Your Media Player**
   - The podcast should start playing
   - If it doesn't, check [Troubleshooting](#troubleshooting)

## Testing

### Test Script 1: Basic Playback

Create a test automation to verify everything works:

```yaml
# configuration.yaml or automations.yaml
automation:
  - alias: "Test Podcast Player"
    trigger:
      - platform: state
        entity_id: input_boolean.test_podcast
        to: "on"
    action:
      - service: HA_Spotify_Podcast_Player.play_filtered_episode
        data:
          entity_id: media_player.your_sonos
          podcast_url: "https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A"
          filter_keywords: "Headlines:"
```

### Test Script 2: Check Logs

Enable debug logging to see what's happening:

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.HA_Spotify_Podcast_Player: debug
```

Restart Home Assistant and check:

- Settings → System → Logs
- Look for messages from `custom_components.HA_Spotify_Podcast_Player`

## Troubleshooting

### Issue: "Invalid Spotify API credentials"

**Solution:**

- Verify your Client ID and Client Secret are copied correctly
- Make sure there are no extra spaces
- Try creating a new Spotify app and use those credentials
- Check that your Spotify account is active

### Issue: "No episode found with filter keywords"

**Solution:**

- Check the podcast has recent episodes with your keywords
- Try broader keywords (e.g., "Daily" instead of "Daily Headlines")
- Increase `episodes_to_check` to 10 or more
- Verify the podcast URL is correct

### Issue: Media player doesn't respond

**Solution:**

- Check your media player is online in Home Assistant
- Verify the entity_id is correct
- For Sonos: Ensure Spotify is linked to your Sonos account
  - Open Sonos app → Settings → Services → Add Spotify
- Test playing regular Spotify content on the media player first

### Issue: Episode plays but seek doesn't work

**Solution:**

- Some media players don't support seeking immediately after starting
- The integration waits 2 seconds before seeking
- Try increasing the delay in the code if needed
- Not all media players support the media_seek service

### Issue: Integration doesn't appear after installation

**Solution:**

1. Check file structure is correct
2. Restart Home Assistant completely (not just reload)
3. Check Home Assistant logs for errors:
   ```
   Settings → System → Logs
   ```
4. Verify `manifest.json` is valid JSON

### Issue: "Could not connect to Spotify"

**Solution:**

- Check your internet connection
- Verify Spotify's API is accessible (https://status.developer.spotify.com/)
- Check Home Assistant can access external URLs
- Look at firewall settings

### Getting Help

If you're still having issues:

1. **Check Logs**

   - Settings → System → Logs
   - Look for errors from `HA_Spotify_Podcast_Player`

2. **Enable Debug Logging**

   ```yaml
   logger:
     logs:
       custom_components.HA_Spotify_Podcast_Player: debug
   ```

3. **Open an Issue**
   - Go to GitHub issues
   - Include:
     - Home Assistant version
     - Error messages from logs
     - Configuration (without credentials)
     - Media player type

## Next Steps

Once installed and tested:

1. Create your morning automation (see [examples/automations.yaml](examples/automations.yaml))
2. Customize filter keywords for your podcasts
3. Set up multiple automations for different times/podcasts
4. Explore advanced features like conditional playback

## Advanced Configuration

### Multiple Podcast Configurations

You can configure different podcasts with different settings by calling the service with different parameters:

```yaml
# Morning news
- service: HA_Spotify_Podcast_Player.play_filtered_episode
  data:
    entity_id: media_player.kitchen
    podcast_url: "https://open.spotify.com/show/NEWS_SHOW_ID"
    filter_keywords: "Headlines:"
    start_time: 0

# Evening discussion
- service: HA_Spotify_Podcast_Player.play_filtered_episode
  data:
    entity_id: media_player.living_room
    podcast_url: "https://open.spotify.com/show/DISCUSSION_SHOW_ID"
    filter_keywords: "Full Episode"
    start_time: 30
```

### Integration with Other Automations

Combine with other Home Assistant features:

```yaml
automation:
  - alias: "Smart Morning Routine"
    trigger:
      - platform: time
        at: "07:00:00"
    condition:
      # Only on weekdays
      - condition: time
        weekday: [mon, tue, wed, thu, fri]
      # Only if someone is home
      - condition: state
        entity_id: binary_sensor.someone_home
        state: "on"
    action:
      # Turn on lights
      - service: light.turn_on
        target:
          entity_id: light.kitchen
      # Play podcast
      - service: HA_Spotify_Podcast_Player.play_filtered_episode
        data:
          entity_id: media_player.sonos_kitchen
          filter_keywords: "Headlines:"
      # Make coffee (if you have a smart coffee maker)
      - service: switch.turn_on
        target:
          entity_id: switch.coffee_maker
```
