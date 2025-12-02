# HA Spotify Podcast Player for Home Assistant

Play filtered Spotify podcast episodes on your Home Assistant media players with the ability to skip to specific timestamps.

## Features

- 🎙️ Fetch latest episodes from any Spotify podcast
- 🔍 Filter episodes by keywords in title or description
- ⏰ Start playback at specific timestamps
- 🔊 Play on any Home Assistant media player (Sonos, etc.)
- 🎛️ Configurable via UI
- 🔄 Perfect for daily news podcasts or specific segments

## Use Case

Ideal for automations like:

- Play "The Daily Aus" headlines episode at 7:00 AM
- Automatically play the latest episode with specific keywords
- Skip intros and go straight to content

## Installation

### Via HACS (Recommended)

**Option 1: Install from HACS Store (Easiest)**
1. Open HACS in your Home Assistant
2. Go to "Integrations"
3. Search for "HA Spotify Podcast Player"
4. Click "Download"
5. Restart Home Assistant

**Option 2: Install as Custom Repository (If not in store)**
1. Open HACS in your Home Assistant
2. Click on "Integrations"
3. Click the 3 dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/Mattallmighty/HA-Spotify-Podcast-Player`
6. Select category: "Integration"
7. Click "Add"
8. Click "Download" on the HA Spotify Podcast Player card
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/HA_Spotify_Podcast_Player` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Getting Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in the app name and description
5. Accept the terms and click "Create"
6. You'll see your **Client ID** and **Client Secret** (click "Show Client Secret")
7. Copy both values - you'll need them for configuration

## Configuration

### Step 1: Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "HA Spotify Podcast Player"
4. Enter your Spotify API credentials:
   - **Client ID**: Your Spotify app client ID
   - **Client Secret**: Your Spotify app client secret
   - **Default Podcast URL**: (Optional) Default podcast URL
   - **Default Filter Keywords**: (Optional) Default keywords to filter episodes
   - **Default Start Time**: (Optional) Default start time in seconds

### Step 2: Create Automation

#### Example 1: UI Automation (Visual Editor)

1. Go to **Settings** → **Automations & Scenes**
2. Click **+ Create Automation** → **Create new automation**
3. Set up the trigger:
   - Click **Add Trigger**
   - Select **Time**
   - Set time to **07:00:00**
   - (Optional) Set weekdays: Mon, Tue, Wed, Thu, Fri
4. Set up the action:
   - Click **Add Action**
   - Select **Call service**
   - Search for and select: `HA Spotify Podcast Player: Play Filtered Episode`
   - Fill in the fields:
     - **Media Player**: Select your media player from dropdown (e.g., media_player.kitchen)
     - **Podcast URL**: `https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A`
     - **Filter Keywords**: `Headlines:`
     - **Start Time**: `0` (or number of seconds to skip intro)
     - **Episodes to Check**: `5`
5. Click **Save**

#### Example 2: YAML Automation

```yaml
description: "Play Daily Aus Headlines on weekday mornings"
mode: single
triggers:
  - trigger: time
    at: "07:00:00"
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri
conditions: []
actions:
  - action: ha_spotify_podcast_player.play_filtered_episode
    data:
      entity_id: media_player.kitchen
      podcast_url: "https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A"
      filter_keywords: "Headlines:"
      start_time: 0
      episodes_to_check: 5
```

## Service Details

### `HA_Spotify_Podcast_Player.play_filtered_episode`

Plays the latest podcast episode matching the filter keywords.

**Parameters:**

- `entity_id` (required): Media player entity to play on
- `podcast_url` (optional): Spotify podcast URL (uses default if not provided)
- `filter_keywords` (optional): Keywords to filter episodes (uses default if not provided)
- `start_time` (optional): Start time in seconds (default: 0)
- `episodes_to_check` (optional): Number of recent episodes to check (default: 5)

## How It Works

1. Connects to Spotify API using your credentials
2. Fetches the latest N episodes from the specified podcast
3. Searches for the first episode where the title or description contains your filter keywords
4. Plays that episode on your specified media player
5. Optionally seeks to the specified start time

## Finding Podcast URLs

1. Open Spotify (web or desktop app)
2. Navigate to the podcast you want
3. Click the "..." menu → Share → Copy Podcast Link
4. The URL will look like: `https://open.spotify.com/show/XXXXXXXXX`

## Troubleshooting

### "No episode found with filter keywords"

- Check that your filter keywords exactly match what's in the episode title or description
- Try increasing `episodes_to_check` (the podcast might not publish matching episodes frequently)
- Check the podcast has recent episodes

### "Invalid Spotify API credentials"

- Verify your Client ID and Client Secret are correct
- Make sure you're using credentials from a Spotify app (not user credentials)
- Check that your app is not in "development mode" restrictions

### Media player doesn't start playing

- Ensure your media player is connected to Home Assistant
- Verify the media player entity ID is correct
- Check that Spotify is properly linked to your media player (e.g., Sonos account linked to Spotify)

## Example Podcasts

- **The Daily Aus**: `https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A`
- Find your favorite podcast on Spotify and copy its URL!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Support

If you encounter any issues, please [open an issue](https://github.com/Mattallmighty/HA-Spotify-Podcast-Player/issues) on GitHub.
