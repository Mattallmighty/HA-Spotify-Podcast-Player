#!/usr/bin/env python3
"""
Helper script to find and test Spotify podcast information.

This script helps you:
1. Verify your Spotify API credentials
2. Find podcast shows
3. List recent episodes and their titles
4. Test filter keywords

Usage:
    python3 test_podcast.py
"""

import sys

try:
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
except ImportError:
    print("Error: spotipy not installed")
    print("Install with: pip install spotipy")
    sys.exit(1)


def main():
    print("=" * 60)
    print("HA Spotify Podcast Player - Helper Script")
    print("=" * 60)
    print()

    # Get credentials
    print("Step 1: Enter your Spotify API credentials")
    print("(Get them from https://developer.spotify.com/dashboard)")
    print()
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()

    if not client_id or not client_secret:
        print("Error: Both Client ID and Client Secret are required")
        sys.exit(1)

    # Test credentials
    print("\nTesting credentials...")
    try:
        auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        # Test with a simple search
        sp.search(q="test", type="show", limit=1)
        print("✓ Credentials valid!")
    except Exception as e:
        print(f"✗ Error: Invalid credentials - {e}")
        sys.exit(1)

    # Get podcast URL
    print("\n" + "=" * 60)
    print("Step 2: Enter podcast information")
    print("=" * 60)
    print()
    podcast_url = input(
        "Podcast URL (e.g., https://open.spotify.com/show/...): "
    ).strip()

    # Extract show ID
    if "/show/" not in podcast_url:
        print("Error: Invalid podcast URL")
        sys.exit(1)

    show_id = podcast_url.split("/show/")[-1].split("?")[0]

    # Get show info
    print(f"\nFetching podcast information for show ID: {show_id}")
    try:
        show = sp.show(show_id)
        print("\n" + "=" * 60)
        print("Podcast Information")
        print("=" * 60)
        print(f"Name: {show['name']}")
        print(f"Publisher: {show['publisher']}")
        print(f"Total Episodes: {show['total_episodes']}")
        print(f"Description: {show['description'][:100]}...")
    except Exception as e:
        print(f"✗ Error fetching show: {e}")
        sys.exit(1)

    # Get recent episodes
    episodes_to_check = input(
        "\nHow many recent episodes to check? (default: 10): "
    ).strip()
    episodes_to_check = int(episodes_to_check) if episodes_to_check else 10

    print(f"\nFetching last {episodes_to_check} episodes...")
    try:
        results = sp.show_episodes(show_id, limit=episodes_to_check)
        episodes = results["items"]

        print("\n" + "=" * 60)
        print(f"Recent Episodes (Latest {len(episodes)})")
        print("=" * 60)

        for i, episode in enumerate(episodes, 1):
            print(f"\n{i}. {episode['name']}")
            print(f"   Released: {episode['release_date']}")
            print(f"   Duration: {episode['duration_ms'] // 60000} minutes")
            print(f"   URI: {episode['uri']}")
            desc = episode.get("description", "")
            if desc:
                print(f"   Description: {desc[:100]}...")

    except Exception as e:
        print(f"✗ Error fetching episodes: {e}")
        sys.exit(1)

    # Test filter
    print("\n" + "=" * 60)
    print("Step 3: Test filter keywords")
    print("=" * 60)
    print()
    filter_keywords = input(
        "Enter filter keywords to search for (e.g., 'Headlines:'): "
    ).strip()

    if filter_keywords:
        print(f"\nSearching for episodes with '{filter_keywords}'...")
        matching_episodes = []

        for episode in episodes:
            name = episode.get("name", "").lower()
            desc = episode.get("description", "").lower()
            keywords_lower = filter_keywords.lower()

            if keywords_lower in name or keywords_lower in desc:
                matching_episodes.append(episode)

        if matching_episodes:
            print(f"\n✓ Found {len(matching_episodes)} matching episode(s):")
            for i, episode in enumerate(matching_episodes, 1):
                print(f"\n{i}. {episode['name']}")
                print(f"   Released: {episode['release_date']}")
                print(f"   URI: {episode['uri']}")

            print("\n" + "=" * 60)
            print("Configuration for Home Assistant")
            print("=" * 60)
            print("\nUse this in your automation:")
            print(
                f"""
service: HA_Spotify_Podcast_Player.play_filtered_episode
data:
  entity_id: media_player.your_device
  podcast_url: "{podcast_url}"
  filter_keywords: "{filter_keywords}"
  start_time: 0
  episodes_to_check: {episodes_to_check}
"""
            )
        else:
            print(f"\n✗ No episodes found with filter keywords '{filter_keywords}'")
            print(
                "\nTry using broader keywords or check the episode titles/descriptions above."
            )

    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
