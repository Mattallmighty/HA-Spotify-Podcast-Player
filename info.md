# Spotify Podcast Player

Play filtered Spotify podcast episodes on your Home Assistant media players.

## Quick Start

1. **Get Spotify API Credentials**
   - Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create an app and get your Client ID and Client Secret

2. **Configure Integration**
   - Go to Settings → Devices & Services
   - Add "Spotify Podcast Player"
   - Enter your credentials

3. **Create Automation**
   - Use the `spotify_podcast_player.play_filtered_episode` service
   - Filter episodes by keywords
   - Play on any media player

## Perfect For

- 🎙️ Daily news podcasts
- 📻 Specific segments like "Headlines"
- ⏰ Morning routines
- 🔊 Sonos and other smart speakers

## Example

Play "The Daily Aus" headlines at 7 AM:

```yaml
automation:
  - alias: "Morning Headlines"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      service: spotify_podcast_player.play_filtered_episode
      data:
        entity_id: media_player.sonos_kitchen
        podcast_url: "https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A"
        filter_keywords: "Headlines:"
```

See README for full documentation.
