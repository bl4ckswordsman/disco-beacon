# Disco Beacon

A project consisting of a Python monitor app and a Svelte web app for Discord notifications.
## Monitor App (Python)

- Track game server status in real-time
- Send automated Discord notifications for server state changes
- Integrate with Steam API for game information
- Configurable check intervals

### Download

Download the latest Windows or Linux build from the Releases page:

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bl4ckswordsman/disco-beacon)](https://github.com/bl4ckswordsman/disco-beacon/releases/latest)

### Setup and Configuration

1. **Steam API Key**: Obtain from [Steam Dev Portal](https://steamcommunity.com/dev/apikey)
2. **Steam ID**:
    <details>
    <summary>Find your Steam ID (click to expand)</summary>

     1. Open the Steam client
     2. Click on your profile name
     3. Click on Account Details
     4. Your Steam ID is displayed below your profile name
   </details>

3. **Discord Webhook**:
    <details>
    <summary>Create a Discord webhook (click to expand)</summary>

   1. Open Discord
   2. Go to Server Settings
   3. Click on Integrations
   4. Click on Webhooks
   5. Create a new webhook or copy an existing one
    </details>

4. **Check Interval**: Set how often to check server status (in seconds)
5. **Monitor Mode**: Choose 'Both' for game and server, or 'Server Only'

Enter these settings in the app's configuration dialog to get started. You can also configure the app by editing the `settings.json` file directly.

## Web App (Svelte)

- Send notifications to Discord via webhooks
- Manage webhook URL and payload (notification content)

## Game Compatibility

Currently supported games:

- Valheim

More games to be added in future updates.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/89b803681f5d42d3b5b2b5a9f983cb0d)](https://app.codacy.com/gh/bl4ckswordsman/disco-beacon?utm_source=github.com&utm_medium=referral&utm_content=bl4ckswordsman/disco-beacon&utm_campaign=Badge_Grade)

[![Visits Badge](https://badges.pufler.dev/visits/bl4ckswordsman/disco-beacon)](https://github.com/bl4ckswordsman)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fbl4ckswordsman%2Fdisco-beacon&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Daily+hits&edge_flat=false)](https://hits.seeyoufarm.com/api/count/graph/dailyhits.svg?url=https://github.com/bl4ckswordsman/disco-beacon) <!-- 2024-09-13 -->
