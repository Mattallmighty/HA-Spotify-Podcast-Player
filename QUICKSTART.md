# Quick Start Guide - 5 Minutes to Your First Automation

Get Spotify Podcast Player running in 5 minutes!

## Step 1: Get Spotify Credentials (2 minutes)

1. Go to https://developer.spotify.com/dashboard
2. Click **"Create app"**
3. Fill in:
   - **App name**: Home Assistant Podcast
   - **App description**: Podcast automation
   - **Redirect URI**: Leave blank
   - **API**: Select "Web API"
4. Click **"Save"**
5. Copy your **Client ID** and **Client Secret**

## Step 2: Install Integration (1 minute)

### Option A: Via HACS (Recommended)
1. Open **HACS** → **Integrations**
2. Click **⋮** → **Custom repositories**
3. Add: `https://github.com/yourusername/spotify-podcast-player`
4. Category: **Integration**
5. Click **"Install"**
6. **Restart Home Assistant**

### Option B: Manual
1. Download and extract this repository
2. Copy `custom_components/spotify_podcast_player` to your Home Assistant's `config/custom_components/`
3. **Restart Home Assistant**

## Step 3: Configure (1 minute)

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search: **"Spotify Podcast Player"**
4. Enter your credentials:
   - Paste **Client ID**
   - Paste **Client Secret**
   - (Optional) Default podcast: `https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A`
   - (Optional) Keywords: `Headlines:`
5. Click **"Submit"**

## Step 4: Create Automation (1 minute)

### UI Method:
1. Go to **Settings** → **Automations & Scenes**
2. Click **"+ Create Automation"** → **"Create new automation"**
3. **Trigger**:
   - Type: **Time**
   - At: **07:00:00**
4. **Action**:
   - Action type: **Call service**
   - Service: **Spotify Podcast Player: Play Filtered Episode**
   - Media Player: Select your Sonos/speaker
   - Podcast URL: `https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A`
   - Filter Keywords: `Headlines:`
   - Start Time: `0`
5. Click **"Save"**

### YAML Method:
Add to `automations.yaml`:

```yaml
- alias: "Morning Headlines"
  trigger:
    - platform: time
      at: "07:00:00"
  action:
    - service: spotify_podcast_player.play_filtered_episode
      data:
        entity_id: media_player.sonos_kitchen  # Change to your device
        podcast_url: "https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A"
        filter_keywords: "Headlines:"
        start_time: 0
```

## Step 5: Test It! (30 seconds)

1. Go to **Developer Tools** → **Services**
2. Select: `spotify_podcast_player.play_filtered_episode`
3. Fill in:
   ```yaml
   entity_id: media_player.your_device
   podcast_url: "https://open.spotify.com/show/0onVY7weTsqjZLM8y3Tt9A"
   filter_keywords: "Headlines:"
   ```
4. Click **"Call Service"**
5. Listen to your speaker! 🎉

## Done! 🎊

You now have:
- ✅ Spotify integration configured
- ✅ Automation ready to run at 7 AM
- ✅ Ability to test anytime via Developer Tools

## Common First-Time Issues

### "No episode found"
- The podcast might not have recent episodes with "Headlines:" in the title
- Try `filter_keywords: "Daily"` instead
- Or increase `episodes_to_check: 10`

### "Invalid credentials"
- Double-check you copied the full Client ID and Client Secret
- No extra spaces
- Try creating a new Spotify app

### Device won't play
- Ensure your Sonos/speaker is online in Home Assistant
- For Sonos: Link Spotify in the Sonos app first
- Try playing regular Spotify content first to test

## Next Steps

Now that it's working:

1. **Customize your automation**:
   - Change the time
   - Add conditions (only weekdays)
   - Add multiple automations for different podcasts

2. **Explore more podcasts**:
   - Find podcast URLs in Spotify (Share → Copy link)
   - Test different filter keywords
   - Use `tools/test_podcast.py` to explore

3. **Advanced features**:
   - Skip intros: `start_time: 30`
   - Check more episodes: `episodes_to_check: 10`
   - Create button-triggered playback

## Get Help

- 📖 **Full docs**: See [README.md](README.md)
- 🔧 **Troubleshooting**: See [INSTALLATION.md](INSTALLATION.md)
- ❓ **FAQ**: See [FAQ.md](FAQ.md)
- 🐛 **Issues**: Open a GitHub issue

## More Automation Ideas

```yaml
# Weekday-only news
- alias: "Weekday News"
  trigger:
    - platform: time
      at: "07:00:00"
  condition:
    - condition: time
      weekday: [mon, tue, wed, thu, fri]
  action:
    - service: spotify_podcast_player.play_filtered_episode
      data:
        entity_id: media_player.bedroom
        filter_keywords: "Headlines:"

# Button-triggered
- alias: "News Button"
  trigger:
    - platform: state
      entity_id: input_button.play_news
  action:
    - service: spotify_podcast_player.play_filtered_episode
      data:
        entity_id: media_player.kitchen
        filter_keywords: "Headlines:"

# Multiple podcasts
- alias: "Evening Podcast"
  trigger:
    - platform: time
      at: "18:00:00"
  action:
    - service: spotify_podcast_player.play_filtered_episode
      data:
        entity_id: media_player.living_room
        podcast_url: "https://open.spotify.com/show/DIFFERENT_SHOW"
        filter_keywords: "Episode"
```

---

**Enjoy your automated podcast experience! 🎙️**
