# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-02

### Added
- Initial release of Spotify Podcast Player integration
- Play filtered podcast episodes on Home Assistant media players
- Support for filtering by keywords in episode title or description
- Configurable start time (seek to specific timestamp)
- UI configuration flow for Spotify API credentials
- Service: `spotify_podcast_player.play_filtered_episode`
- HACS compatibility
- Support for all Home Assistant media players
- Configurable number of episodes to check (default: 5)
- Debug logging support
- Comprehensive documentation and examples

### Features
- Fetch latest episodes from any Spotify podcast
- Filter episodes by keywords
- Start playback at specific timestamps
- Perfect for daily news podcasts
- Easy automation integration
- Sonos and other media player support

### Documentation
- README.md with quick start guide
- INSTALLATION.md with detailed setup instructions
- Example automations for common use cases
- Troubleshooting guide

## [Unreleased]

### Planned
- Support for multiple podcast configurations
- Episode caching to reduce API calls
- More advanced filtering options (regex, date-based)
- Playlist support
- Episode queue management
- Integration with Home Assistant notifications

---

## Version History

### How to Upgrade

Via HACS:
1. Go to HACS → Integrations
2. Find "Spotify Podcast Player"
3. Click "Update"
4. Restart Home Assistant

Manual:
1. Replace the `custom_components/spotify_podcast_player` folder
2. Restart Home Assistant
