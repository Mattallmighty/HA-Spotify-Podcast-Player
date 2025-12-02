# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-12-02

### Fixed
- **CRITICAL**: Fixed Spotify API returning stale/cached episode data
- Disabled credential and response caching by adding `cache_handler=None`
- Fixed incorrect parameter passing to `sp.show_episodes()`
- Episodes now correctly fetched with `limit` and `offset=0` parameters
- Integration now always fetches the latest episodes from Spotify

## [1.0.2] - 2025-12-02

### Added
- Enhanced logging to show all episodes checked during filtering
- Detailed episode selection debugging (episode names, release dates, match status)

### Changed
- Updated README with HACS store installation instructions
- Improved automation examples with current Home Assistant YAML format
- Added visual editor (UI) automation setup instructions
- Updated service call format in documentation

### Fixed
- Service now correctly displays input fields in Home Assistant visual editor
- Episode selection now always chooses the latest matching episode

## [1.0.0] - 2024-12-02

### Added

- Initial release of HA Spotify Podcast Player integration
- Play filtered podcast episodes on Home Assistant media players
- Support for filtering by keywords in episode title or description
- Configurable start time (seek to specific timestamp)
- UI configuration flow for Spotify API credentials
- Service: `HA_Spotify_Podcast_Player.play_filtered_episode`
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
2. Find "HA Spotify Podcast Player"
3. Click "Update"
4. Restart Home Assistant

Manual:

1. Replace the `custom_components/HA_Spotify_Podcast_Player` folder
2. Restart Home Assistant
