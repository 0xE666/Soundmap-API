
# Soundmap API

![Soundmap API Logo](https://e-e.tools/soundmap.png)

This Python library allows you to interact with the Soundmap API to manage songs, trades, and quests.

I will be lightly monitoring this, any questions? Discord: eric.cpp

## Features

- Search for songs
- Fetch songs from a profile
- Create, delete, and manage trade offers
- Fetch and parse trade data
- Get notification counts
- Accept and reject trade offers with optional emojis or notes
- Claim daily lootboxes and coins
- Change user bio
- Fetch and manage artist quests

## Installation

Clone the repository:

```sh
git clone https://github.com/yourusername/soundmap-api.git
```

Navigate to the project directory:

```sh
cd soundmap-api
```

Install the required dependencies:

```sh
pip install requests urllib3
```

## Usage

### Initialization

To use the API, first create an instance of the `Soundmap` class:

```python
from soundmap import Soundmap

api = Soundmap()
```

### Search for a Song

```python
song_data = api.search_song("song_id")
print(song_data)
```

### Fetch specfic song data

```python
song = api.search_song_details("song_name", "artist", "rarity **shiny")
print(song)
```

### Fetch Songs from a Profile

```python
songs = api.fetch_songs("profile_owner_id")
print(songs)
```

### Create a Trade Offer

```python
song_ids = ["song_id1", "song_id2"]
result, offer_id = api.create_trade_offer(song_ids, note="Trade note here")
print(result, offer_id)
```

### Delete a Trade Offer

```python
result = api.delete_trade_offer("offer_id")
print(result)
```

### Fetch and Parse Trade Data

```python
active_trades = api.fetch_trade_data()
parsed_trades = api.parse_trades(active_trades)
print(parsed_trades)
```

### Get Notification Count

```python
count = api.notification_count()
print(count)
```

### Accept a Trade Offer

```python
result = api.accept_trade("trade_id", emoji="🤝", note="Thank you!")
print(result)
```

### Reject a Trade Offer

```python
result = api.reject_trade("trade_id", emoji="😐", note="Not interested")
print(result)
```

### Claim Daily Lootbox

```python
result = api.claim_lootbox("genre")
print(result)
```

### Claim Daily Coins

```python
result = api.claim_coins()
print(result)
```

### Change User Bio

```python
result = api.change_bio("New bio content")
print(result)
```

### Fetch Artist Quests

```python
all_quests = api.fetch_quests()
print(all_quests)

specific_artist_quest = api.fetch_quests(artist="The Weeknd")
print(specific_artist_quest)
```

### Fetch Trade Data for Quest Requirements

```python
trade_requirements = {
    "type": "trade",
    "username": "w"
}
trade_data = api.get_quest_trade_data(trade_requirements)
print(trade_data)
```

## Configuring an iOS Device for Burp Suite

To configure your iOS device to work with Burp Suite, follow these steps:

1. **Install Burp Suite**: Download and install Burp Suite on your computer from the [official website](https://portswigger.net/burp).

2. **Configure Burp Suite Proxy**:
   - Open Burp Suite and go to the "Proxy" tab.
   - Click on "Options" and ensure the interface is set to listen on 127.0.0.1:8080 (or another desired port).

3. **Configure iOS Device to Use Burp as a Proxy**:
   - On your iOS device, go to `Settings` > `Wi-Fi`.
   - Tap the `i` icon next to the connected Wi-Fi network.
   - Scroll down to `HTTP Proxy` and select `Manual`.
   - Enter your computer's IP address in the `Server` field and `8080` (or the port set in Burp) in the `Port` field.

4. **Install Burp Suite CA Certificate on iOS**:
   - Open Safari on your iOS device and navigate to `http://burp` (or `http://<your-computer-ip>:<port>`).
   - Download the CA certificate and follow the prompts to install it.
   - Go to `Settings` > `General` > `Profile` (or `Profile & Device Management`) to install the certificate.
   - Enable full trust for the Burp Suite certificate under `Settings` > `General` > `About` > `Certificate Trust Settings`.

5. **Start Intercepting Traffic**:
   - Go back to Burp Suite, ensure intercept is on in the "Proxy" > "Intercept" tab.
   - Browse on your iOS device, and you should see traffic being captured in Burp Suite.

For detailed instructions and troubleshooting, refer to the [Burp Suite documentation](https://portswigger.net/burp/documentation/desktop/mobile/config-ios-device).
