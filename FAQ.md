# Frequently Asked Questions (FAQ)

## General Questions

### What is HA Spotify Podcast Player?

HA Spotify Podcast Player is a Home Assistant integration that allows you to automatically play specific podcast episodes on your media players based on filter criteria. It's perfect for automating daily news podcasts or specific segments.

### Do I need a Spotify Premium account?

No! A free Spotify account is sufficient. However, you do need to create a Spotify Developer account (also free) to get API credentials.

### Does this work with any media player?

Yes, it works with any media player that supports Spotify playback in Home Assistant, including:

- Sonos
- Google Home/Nest
- Amazon Echo (with Spotify linked)
- Spotify Connect devices
- And more

### Can I use this with multiple podcasts?

Absolutely! You can create multiple automations, each targeting different podcasts with different filter keywords.

## Setup Questions

### Where do I get Spotify API credentials?

1. Go to https://developer.spotify.com/dashboard
2. Create a free developer account
3. Create a new app
4. Copy the Client ID and Client Secret

See [INSTALLATION.md](INSTALLATION.md) for detailed steps.

### Do I need to add redirect URIs?

No! This integration uses client credentials flow, so redirect URIs are not needed.

### Can I change the default settings after setup?

Currently, you need to reconfigure the integration:

1. Go to Settings → Devices & Services
2. Find "HA Spotify Podcast Player"
3. Click "Configure"
4. Update your settings

### How do I find a podcast's Spotify URL?

1. Open Spotify (web, desktop, or mobile)
2. Navigate to the podcast
3. Click the "..." menu → Share → Copy Podcast Link
4. The URL will look like: `https://open.spotify.com/show/XXXXXXXXXXX`

## Usage Questions

### How do filter keywords work?

The integration searches for your keywords in both the episode **title** and **description**. The search is case-insensitive.

For example:

- Keywords: `Headlines:` will match "Headlines: December 2nd" or any description containing "headlines:"
- Keywords: `Full Episode` will match episodes with that phrase
- Keywords: `Monday` will match episodes with Monday in the title or description

### What if multiple episodes match my keywords?

The integration plays the **most recent** episode that matches. It checks the latest N episodes (default: 5, configurable).

### Can I skip the intro/ads?

Yes! Use the `start_time` parameter to skip ahead:

```yaml
start_time: 30 # Skip first 30 seconds
```

### Why isn't the seek working?

Some media players need a moment to start playback before seeking. The integration waits 2 seconds before seeking. If your player still doesn't seek, it may not support the `media_seek` service.

### Can I play just one episode and stop?

Yes! The integration only plays the single matching episode. It won't continue to the next episode automatically. You can also create an automation to stop playback after a certain time:

```yaml
- delay:
    minutes: 5
- service: media_player.media_stop
  target:
    entity_id: media_player.your_sonos
```

## Troubleshooting Questions

### "No episode found with filter keywords" - What do I do?

1. **Check the podcast has recent episodes**: The integration only checks the latest N episodes (default: 5)
2. **Try broader keywords**: Instead of "Daily News Headlines", try just "Headlines"
3. **Increase episodes to check**: Set `episodes_to_check: 10` or higher
4. **Verify the podcast URL**: Make sure you're using the correct Spotify show URL
5. **Check episode names**: Look at recent episodes in Spotify to see how they're titled

### "Invalid Spotify API credentials" - What's wrong?

1. **Double-check credentials**: Copy them again from https://developer.spotify.com/dashboard
2. **No extra spaces**: Make sure there are no spaces before/after the credentials
3. **App is active**: Verify your Spotify app is not in "development mode" with restrictions
4. **Create new app**: Try creating a new Spotify app and use those credentials

### Media player doesn't start - What could it be?

1. **Check player is online**: Verify in Home Assistant that your media player is responsive
2. **Test manually**: Try playing regular Spotify content on the player first
3. **Link Spotify account**: For Sonos, ensure your Spotify account is linked in the Sonos app
4. **Check entity_id**: Make sure you're using the correct entity_id (e.g., `media_player.sonos_kitchen`)
5. **Check logs**: Go to Settings → System → Logs and look for errors

### The episode plays but from the beginning, not at my start_time

1. **Wait longer**: Some players need 3-5 seconds before they accept seek commands
2. **Check player support**: Not all players support `media_seek` service
3. **Try different player**: Test with a different media player to confirm
4. **Check logs**: Enable debug logging to see if seek command is being sent

### How do I enable debug logging?

Add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.HA_Spotify_Podcast_Player: debug
```

Then restart Home Assistant and check Settings → System → Logs.

## Advanced Questions

### Can I use multiple Spotify API apps?

Yes, but you'd need to set up separate Home Assistant instances or manually manage credentials. The integration currently supports one set of credentials per Home Assistant instance.

### Can I filter by date or episode number?

Not currently. The integration filters by keywords only. However, you can:

- Set `episodes_to_check: 1` to always get the absolute latest episode
- Use date-specific keywords like "December 2nd" if the podcast titles include dates

### Can I create a queue of episodes?

Not with this integration. It's designed to play a single matching episode. For queues, you'd need to use Home Assistant's native Spotify integration or create multiple sequential automation steps.

### Can I use this with non-Spotify podcasts?

No, this integration specifically uses the Spotify API. For other podcast sources, you'd need different integrations or RSS feed parsers.

### How often does it check for new episodes?

It checks every time the service is called. It doesn't continuously monitor for new episodes. If you want to check regularly, create a time-based automation.

### Does this use my Spotify API quota?

Yes, each service call makes 1-2 API requests:

- 1 request to fetch episodes
- 1 request to play the episode

Spotify's free tier has generous limits (typically thousands of requests per day), so normal home automation use won't be an issue.

## Integration Questions

### Can I integrate this with voice assistants?

Yes! Example with Alexa:

```yaml
automation:
  - alias: "Alexa Play News"
    trigger:
      - platform: event
        event_type: alexa_actionable_notification
        event_data:
          event_id: play_news
    action:
      - service: HA_Spotify_Podcast_Player.play_filtered_episode
        data:
          entity_id: media_player.echo_kitchen
          filter_keywords: "Headlines:"
```

### Can I use this with other Home Assistant automations?

Absolutely! You can combine it with:

- Time triggers (play at 7 AM)
- Presence detection (play when I arrive home)
- Button presses
- Other automation conditions
- Scenes and scripts

### Can I get notifications when an episode plays?

Yes, add a notification action to your automation:

```yaml
action:
  - service: HA_Spotify_Podcast_Player.play_filtered_episode
    data:
      entity_id: media_player.sonos
      filter_keywords: "Headlines:"
  - service: notify.mobile_app
    data:
      message: "Playing today's headlines on Sonos"
```

### Can this work offline?

No, it requires internet access to:

- Authenticate with Spotify API
- Fetch episode information
- Stream content to your media player

## Update Questions

### How do I update the integration?

**Via HACS:**

1. Go to HACS → Integrations
2. Find "HA Spotify Podcast Player"
3. Click "Update" if available
4. Restart Home Assistant

**Manual:**

1. Download the latest release
2. Replace the `custom_components/HA_Spotify_Podcast_Player` folder
3. Restart Home Assistant

### Will updates break my automations?

We follow semantic versioning:

- Major versions (2.0.0): May have breaking changes
- Minor versions (1.1.0): New features, backward compatible
- Patch versions (1.0.1): Bug fixes, backward compatible

### How do I know what changed in an update?

Check the [CHANGELOG.md](CHANGELOG.md) file for detailed release notes.

## Support Questions

### Where can I get help?

1. **Check this FAQ** first
2. **Read the [INSTALLATION.md](INSTALLATION.md)** guide
3. **Enable debug logging** and check logs
4. **Open a GitHub issue** with:
   - Your Home Assistant version
   - Error messages from logs
   - Your configuration (without credentials)
   - Media player type

### How can I contribute?

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Can I request features?

Yes! Open a GitHub issue with:

- Clear description of the feature
- Use case/example
- Why it would be useful

### Is there a community forum?

Check the Home Assistant Community forums for discussions:

- Tag: `HA-Spotify-Podcast-Player`
- Category: Custom Integrations

## Privacy & Security Questions

### What data does this integration collect?

The integration:

- **Does NOT** collect or store any personal data
- **Does NOT** send data to third parties (except Spotify API calls)
- Only stores your Spotify credentials locally in Home Assistant
- Only accesses podcasts you configure

### Are my Spotify credentials secure?

Yes:

- Credentials are stored in Home Assistant's encrypted storage
- They're never logged or transmitted except to Spotify's API
- Use Home Assistant's security best practices (HTTPS, strong passwords)

### Can this integration control my Spotify account?

No! It only has permission to:

- Read podcast information
- Send playback commands to your media players

It cannot:

- Access your personal playlists
- See your listening history
- Modify your Spotify account
- Share content on your behalf

## License & Legal Questions

### What license is this under?

MIT License - see [LICENSE](LICENSE) file. This means you can freely use, modify, and distribute this integration.

### Is this official from Spotify?

No, this is an unofficial, community-created integration. It uses Spotify's public Web API.

### Can I use this commercially?

Yes, the MIT license allows commercial use. However, ensure you comply with Spotify's API Terms of Service.

---

## Still Have Questions?

If your question isn't answered here:

1. Check the [README.md](README.md)
2. Read [INSTALLATION.md](INSTALLATION.md)
3. Look at [examples/automations.yaml](examples/automations.yaml)
4. Open a GitHub issue with your question
