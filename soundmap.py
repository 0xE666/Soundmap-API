from urllib.parse import urlencode
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import cloudscraper, json, socket, time, uuid, datetime, logging, urllib.parse, requests

logging.basicConfig(level=logging.DEBUG, filename='trade_log.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Soundmap:
    def __init__(self):
        self.authorization_token = ""
        self.owner_id = ""
        self.API_BASE = "https://api10.soundmap.dev"
        self.API_SONG = "/trpc/song"
        self.API_SONGS2 = "/trpc/songs2"
        self.API_NOTIFS = "/trpc/notifs?batch=1&input=%7B%7D"
        self.API_UNREAD_NOTIFICATIONS_COUNT = "/trpc/unreadNotificationsCount?batch=1&input=%7B%7D"
        self.OPEN_TRADE_OFFERS = "/trpc/openTradeOffers?batch=1&input=%7B%7D"
        self.API_CREATE_TRADE_OFFER = "/trpc/createTradeOffer?batch=1"
        self.API_DELETE_TRADE_OFFER = "/trpc/deleteTradeOffer?batch=1"
        self.API_ACCEPT_TRADE_OFFER = "/trpc/acceptTradeRequest?batch=1"
        self.API_SEND_TRADE_ACCEPTANCE_EMOJI = "/trpc/sendTradeRequestAcceptanceEmoji?batch=1"
        self.API_REJECT_TRADE_OFFER = "/trpc/rejectTradeRequest?batch=1"
        self.API_SEND_TRADE_REJECTION_EMOJI = "/trpc/sendTradeRequestRejectionEmoji?batch=1"
        self.API_CLAIM_LOOTBOX = "/trpc/openLootbox?batch=1"
        self.API_CLAIM_COINS = "/trpc/claimDailyFreeCoins?batch=1"
        self.API_SET_BIO = "/trpc/setBio?batch=1"
        self.API_OPEN_TRADE_REQUESTS_OFFERS = "/trpc/openTradeRequests,openTradeOffers?batch=1&input=%7B%7D"
        self.API_ARTIST_QUESTS = "/trpc/artistQuests?batch=1&input=%7B%7D"
        self.API_COMPLETE_ARTIST_QUEST = "/trpc/completeArtistQuest?batch=1"
        self.API_ARTIST_QUEST_TRADE = "/trpc/tradeOffers?batch=1&input=%s"
        self.API_ADD_SONG_TO_FOLDER = "/trpc/addSongsToFolder?batch=1"
        self.API_REMOVE_SONG_FROM_FOLDER = "/trpc/removeSongsFromFolder?batch=1"
        self.API_SEARCH = "/trpc/tradeOffers?batch=1"
        self.REROLL_ARTIST_QUEST = "/trpc/rerollArtistQuest?batch=1"

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Version": "1.57.0",
            "Authorization": self.authorization_token,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Platform": "ios",
            "User-Agent": "Mmap/650 CFNetwork/3826.400.120 Darwin/24.3.0",
            "Timezone": "America/Chicago"
        }

        self.retry_strategy = Retry(
            total=5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )

        self.http = cloudscraper.create_scraper()
        adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)

    def get_unique_timestamp(self, hour, minute):
        today = datetime.date.today()
        custom_time = datetime.datetime.combine(today, datetime.time(int(hour), int(minute)))
        timestamp = int(time.mktime(custom_time.timetuple()))
        return timestamp
    
    def build_url_song(self, song_id):
        params = {
            "batch": 1,
            "input": json.dumps({
                "0": {"id": song_id}
            })
        }
        query_string = urlencode(params)
        return f"{self.API_BASE}{self.API_SONG}?{query_string}"
    
    def change_bio(self, bio):
        bio_payload = {
            "0": {
                "bio": f"{bio}"
            }
        }
        
        bio_url = f"{self.API_BASE}{self.API_SET_BIO}"
        try:
            response = self.http.post(f"{bio_url}", headers=self.headers, json=bio_payload)
            response.raise_for_status()
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error claiming daily free coins: {e}")
            return None

    def search_song(self, song_id):
        url = self.build_url_song(song_id)
        try:
            response = self.http.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            #print(f"Data for song_id {song_id}: {data}")  # debugging
            result = data[0]['result']['data']['song']
            owner = data[0]['result']['data']['owner']

            # idk why i think this format is ugly but ig 
            song_data = {
                "song_id": result['id'],
                "song_name": result['name'],
                "coin_value": result['coinValue'],
                "artist": result['artist'],
                "artist_id": result['artistId'],
                "image_url": result['imageUrl'],
                "preview_url": result['previewUrl'],
                "genre": result['genre'],
                "rarity": result['rarity'],
                "owner_id": result['ownerId'],
                "colors": result['colors'],
                "comment_count": result['commentCount'],
                "owner_username": owner['username'],
                "owner_image_url": owner['imageUrl'],
                "owner_songs_seen": owner['songsSeen'],
                "owner_trades_completed": owner['tradesCompleted'],
                "owner_coins": owner['coins'],
                "owner_favourite_artists": owner['favouriteArtists'],
                "owner_background_image_url": owner.get('backgroundImageUrl'),
                "owner_bio": owner.get('bio')
            }


            return {"song": song_data}

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None
        
    def fetch_songs(self, owner_id=None):
        if owner_id is None:
            owner_id = self.owner_id

        encode_this = urllib.parse.quote(f'{{"0":{{"ownerId":"{owner_id}"}}}}')
        fetch_url = f"{self.API_BASE}{self.API_SONGS2}??batch=1&input={encode_this}"
        #fetch_url = f"{self.API_BASE}{self.API_SONGS2}??batch=1&input=%7B%220%22%3A%7B%22ownerId%22%3A%22{owner_id}%22%7D%7D"
        print(fetch_url)
        retries = 3
        backoff_factor = 2

        for attempt in range(retries):
            try:
                socket.gethostbyname('api10.soundmap.dev')

                response = self.http.get(fetch_url, headers=self.headers)
                response.raise_for_status()
                songs_data = response.json()

                # debug json output
                # with open("song_data.json", 'w') as f:
                #     json.dump(songs_data, f, indent=4)

                songs_by_rarity = {
                    "common": [],
                    "uncommon": [],
                    "rare": [],
                    "epic": [],  # Added epic rarity
                    "shiny": [],
                    "other": [],
                }

                for song in songs_data['result']['data']['songs']:
                    song_data = {
                        "id": song['id'],
                        "name": song['name'],
                        "artist": song['artist'],
                        "genre": song['genre'],
                        "imageUrl": song['imageUrl'],
                        "previewUrl": song.get('previewUrl', False),
                        "rarity": song['rarity'],  # Added to ensure rarity is passed
                        "type": song.get('type', 'normal')  # Added to ensure type is passed
                    }

                    if song.get('type') == 'shiny':
                        songs_by_rarity['shiny'].append(song_data)
                    elif song['rarity'] in songs_by_rarity:
                        if song.get('type') == 'mystic':
                            songs_by_rarity['epic'].append(song_data)
                        else:
                            songs_by_rarity[song['rarity']].append(song_data)
                    else:
                        songs_by_rarity["other"].append(song_data)

                with open("data/songs_by_rarity.json", 'w') as f:
                    json.dump(songs_by_rarity, f, indent=4)

                return songs_by_rarity

            except socket.gaierror as e:
                print(f"DNS resolution error: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching songs: {e}")

            time.sleep(backoff_factor ** attempt)

        print("Failed to fetch songs after several attempts.")
        return None


    
    def create_trade_offer(self, song_ids, coins=0, note=""):
        if not isinstance(song_ids, list):
            raise ValueError("song_igs must be a list")

        offer_id = str(uuid.uuid4())

        trade_offer = {
            "0": {
                "songIds": song_ids,
                "coins": coins,
                "note": note,
                "offerId": offer_id
            }
        }

        trade_url = f"{self.API_BASE}{self.API_CREATE_TRADE_OFFER}"

        try:
            response = self.http.post(f"{trade_url}", headers=self.headers, json=trade_offer)
            response.raise_for_status()
            #print(response.json())
            if response.status_code == 200:
                return True, offer_id
            
            return False, None
            #return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating trade offer: {e}")
            logging.error(f"Error creating trade offer: {e}")
            return None, None
        
    def delete_trade_offer(self, offer_id):

        trade_offer = {
            "0":{
                "offerId": f"{offer_id}"
            }
        }

        delete_url = f"{self.API_BASE}{self.API_DELETE_TRADE_OFFER}"

        try:
            response = self.http.post(f"{delete_url}", headers=self.headers, json=trade_offer)
            response.raise_for_status()
            if response.status_code == 200:
                return True
            return False
        
            #return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error deleting trade offer: {e}")
            return None
        
    def fetch_trade_data(self):
        notifs_url = f"{self.API_BASE}{self.API_NOTIFS}"
        try:
            response = self.http.get(notifs_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            #print(f"Trade data: {data}")  # Debugging output
            # with open('trade_data.json', 'w') as f:
            #     json.dump(data, f, indent=4)

            active_trades = []
            for notif in data:
                for notif in data[0]['result']['data']['notifs']:
                    if notif['type'] == 'trade_request' and not notif['request']['accepted']:
                        active_trades.append(notif)

            return active_trades
        
        except requests.exceptions.RequestException as e:
            print("Error fetching trade data:", e)
            return None
        
    def parse_trades(self, active_trades):
        amount_of_trades = len(active_trades)
        trades = []

        for trade in active_trades:
            offered_songs = []
            requested_songs = []

            # trade data
            trade_id = trade['request']['id']
            trade_coins = trade['request']['coins']
            trade_note = trade['request']['note']

            # user data
            trade_user_id = trade['user']['id']
            trade_username = trade['user']['username']
            trade_user_coins = trade['user']['coins']
            trade_user_image = trade['user']['imageUrl']

            # requested
            for song in range(len(trade['requestedSongs'])):
                request_song_id = trade['requestedSongs'][song]['id']
                request_song_name = trade['requestedSongs'][song]['name']
                request_song_coin_value = trade['requestedSongs'][song]['coinValue']
                request_song_arist = trade['requestedSongs'][song]['artist']
                request_song_image_url = trade['requestedSongs'][song]['imageUrl']
                request_song_preview_url = trade['requestedSongs'][song].get('previewUrl')
                request_song_genre = trade['requestedSongs'][song]['genre']
                request_song_rarity = trade['requestedSongs'][song]['rarity']
                request_song_type = trade['requestedSongs'][song].get('type', "normal")


                request_song = {
                    "song_id": f"{request_song_id}",
                    "song_name": f"{request_song_name}",
                    "song_coin_value": f"{request_song_coin_value}",
                    "song_artist": f"{request_song_arist}",
                    "song_image_url": f"{request_song_image_url}",
                    "song_preview_url": f"{request_song_preview_url}",
                    "song_genre": f"{request_song_genre}",
                    "song_rarity": f"{request_song_rarity}",
                    "song_type": f"{request_song_type}",
                }

                requested_songs.append(request_song)
            
            # offered
            for song in range(len(trade['offeredSongs'])):
                offered_song_id = trade['offeredSongs'][song]['id']
                offered_song_name = trade['offeredSongs'][song]['name']
                offered_song_coin_value = trade['offeredSongs'][song]['coinValue']
                offered_song_arist = trade['offeredSongs'][song]['artist']
                offered_song_image_url = trade['offeredSongs'][song]['imageUrl']
                offered_song_preview_url = trade['offeredSongs'][song].get('previewUrl')
                offered_song_genre = trade['offeredSongs'][song]['genre']
                offered_song_rarity = trade['offeredSongs'][song]['rarity']
                offered_song_type = trade['offeredSongs'][song].get('type', "normal")


                offered_song = {
                    "song_id": f"{offered_song_id}",
                    "song_name": f"{offered_song_name}",
                    "song_coin_value": f"{offered_song_coin_value}",
                    "song_artist": f"{offered_song_arist}",
                    "song_image_url": f"{offered_song_image_url}",
                    "song_preview_url": f"{offered_song_preview_url}",
                    "song_genre": f"{offered_song_genre}",
                    "song_rarity": f"{offered_song_rarity}",
                    "song_type": f"{offered_song_type}",
                }

                offered_songs.append(offered_song)

            trade = {
                "trade_id": f"{trade_id}",
                "trade_username": f"{trade_username}",
                "trade_user_id": f"{trade_user_id}",
                "trade_user_coins": f"{trade_user_coins}",
                "trade_user_image": f"{trade_user_image}",
                "trade_coins": f"{trade_coins}",
                "trade_note": f"{trade_note}",
                "offered_songs": offered_songs,
                "requested_songs": requested_songs
            }

            return trade
        
    def notification_count(self):
        notification_url = f"{self.API_BASE}{self.API_UNREAD_NOTIFICATIONS_COUNT}"
        try:
            response = self.http.get(f"{notification_url}", headers=self.headers)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                count = data[0]['result']['data']['count']
                return count
        except requests.exceptions.RequestException as e:
            print(f"Error deleting trade offer: {e}")
            return None
        
    def accept_trade(self, trade_id, emoji=None, note=""):
        emoji_response = False
        note_response = False

        accept_offer = {
            "0": {
                "tradeRequestId": f"{trade_id}"
            }
        }
        if emoji and note == "":
            emoji_response = True
            accept_reaction = {
                "0": {
                    "emoji": f"{emoji}",
                    "tradeRequestId": f"{trade_id}"
                }
            }
        elif emoji is None and note != "":
            note_response = True
            accept_reaction = {
                "0": {
                    "tradeRequestId": f"{trade_id}",
                    "text": f"{note}"
                }
            }

        accept_url = f"{self.API_BASE}{self.API_ACCEPT_TRADE_OFFER}"
        acceptance_url = f"{self.API_BASE}{self.API_SEND_TRADE_ACCEPTANCE_EMOJI}"

        try:
            response = self.http.post(f"{accept_url}", headers=self.headers, json=accept_offer)
            response.raise_for_status()
            if response.status_code == 200:
                if emoji_response:
                    response = self.http.post(f"{acceptance_url}", headers=self.headers, json=accept_reaction)
                if note_response:
                    response = self.http.post(f"{acceptance_url}", headers=self.headers, json=accept_reaction)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error creating trade offer: {e}")
            return None
        
    def reject_trade(self, trade_id, emoji=None, note=""):
        emoji_response = False
        note_response = False

        reject_offer = {
            "0": {
                "tradeRequestId": f"{trade_id}"
            }
        }
        if emoji and note == "":
            emoji_response = True
            reject_reaction = {
                "0": {
                    "emoji": f"{emoji}",
                    "tradeRequestId": f"{trade_id}"
                }
            }
        elif emoji is None and note != "":
            note_response = True
            reject_reaction = {
                "0": {
                    "tradeRequestId": f"{trade_id}",
                    "text": f"{note}"
                }
            }

        reject_url = f"{self.API_BASE}{self.API_REJECT_TRADE_OFFER}"
        rejection_url = f"{self.API_BASE}{self.API_SEND_TRADE_REJECTION_EMOJI}"

        try:
            response = self.http.post(f"{reject_url}", headers=self.headers, json=reject_offer)
            response.raise_for_status()
            if response.status_code == 200:
                if emoji_response:
                    response = self.http.post(f"{rejection_url}", headers=self.headers, json=reject_reaction)
                if note_response:
                    response = self.http.post(f"{rejection_url}", headers=self.headers, json=reject_reaction)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error rejecting trade offer: {e}")
            return None
            
    def claim_lootbox(self, genre):
        valid_genres = ["pop", "hiphop", "kpop", "indie", "rnb", "rock", "electronic"]

        if genre not in valid_genres:
            raise ValueError(f"Invalid genre: {genre}. Valid genres are: {', '.join(valid_genres)}")

        lootbox_type = {
            "0": {
                "lootboxId": "dailyFree",
                "genre": genre
            }
        }

        claim_url = f"{self.API_BASE}{self.API_CLAIM_LOOTBOX}"

        try:
            response = self.http.post(claim_url, headers=self.headers, json=lootbox_type)
            print(response.text)
            response.raise_for_status()
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error claiming lootbox offer: {e}")
            return None

    def claim_coins(self):
        coin_data = {}
        coin_url = f"{self.API_BASE}{self.API_CLAIM_COINS}"

        try:
            response = self.http.post(coin_url, headers=self.headers, json=coin_data)
            response.raise_for_status()
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error claiming daily free coins: {e}")
            return None

    def fetch_open_trade_ids(self):
        url = f"{self.API_BASE}{self.API_OPEN_TRADE_REQUESTS_OFFERS}"
        try:
            response = self.http.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            open_trade_ids = []

            for trade in data[1]['result']['data']:
                open_trade_ids.append(trade['tradeOffer']['id'])

            return open_trade_ids
        except requests.exceptions.RequestException as e:
            print(f"Error fetching open trade IDs: {e}")
            return None

    def fetch_quests(self, artist=None):
        fetch_url = f"{self.API_BASE}{self.API_ARTIST_QUESTS}"
        try:
            response = self.http.get(fetch_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                quests = [item["result"]["data"]["quests"] for item in data if "result" in item and "data" in item["result"] and "quests" in item["result"]["data"]]
                # Flatten the list of quests
                quests = [quest for sublist in quests for quest in sublist]

                if artist:
                    # Filter quests for the specified artist
                    filtered_quests = [quest for quest in quests if quest["artist"]["name"].lower() == artist.lower()]
                    if filtered_quests:
                        return {"quests": [quest["current"] for quest in filtered_quests]}
                    else:
                        return {"message": "No quests found for the specified artist."}
                else:
                    # Return all current quests for each artist
                    all_quests = [{"artist": quest["artist"], "current_quest": quest["current"]} for quest in quests]
                    return {"all_quests": all_quests}

            else:
                return {"message": "Unexpected data format received from API."}

        except requests.exceptions.RequestException as e:
            print(f"Error fetching quests: {e}")
            return None

    def build_quest_trade_url(self, quest_requirements):
        input_data = {
            "0": {
                "questRequirements2": quest_requirements,
                "includeMine": False
            }
        }
        input_string = json.dumps(input_data)
        trade_url = f"{self.API_BASE}/trpc/tradeOffers?batch=1&input={input_string}"
        return trade_url

    def get_quest_trade_data(self, quest_requirements):
        trade_url = self.build_quest_trade_url(quest_requirements)
        try:
            response = self.http.get(trade_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trade data: {e}")
            return None

    def add_song_to_folder(self, song_id, folder_id):
        payload = {
            "0": {
                "folderId": folder_id,
                "songIds": [song_id]
            }
        }

        url = f"{self.API_BASE}{self.API_ADD_SONG_TO_FOLDER}"

        try:
            response = self.http.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error adding song to folder: {e}")
            return None

    def remove_song_from_folder(self, song_id, folder_id):
        payload = {
            "0": {
                "folderId": folder_id,
                "songIds": [song_id]
            }
        }

        url = f"{self.API_BASE}{self.API_REMOVE_SONG_FROM_FOLDER}"

        try:
            response = self.http.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error adding song to folder: {e}")
            return None

    def fetch_folders(self, owner_id=None):
        if owner_id is None:
            owner_id = self.owner_id

        fetch_url = f"{self.API_BASE}{self.API_SONGS2}??batch=1&input=%7B%220%22%3A%7B%22ownerId%22%3A%22{owner_id}%22%7D%7D"
        retries = 3
        backoff_factor = 2

        for attempt in range(retries):
            try:
                socket.gethostbyname('api10.soundmap.dev')

                response = self.http.get(fetch_url, headers=self.headers)
                response.raise_for_status()
                songs_data = response.json()

                return songs_data

            except socket.gaierror as e:
                print(f"DNS resolution error: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Error fetching songs: {e}")

            time.sleep(backoff_factor ** attempt)

        print("Failed to fetch songs after several attempts.")
        return None

    def extract_folder_ids_and_names(self, song_data):
        try:
            folders_data = song_data['result']['data']['folders']
            folders_dict = {folder['name']: folder['id'] for folder in folders_data}
            return folders_dict
        except KeyError as e:
            print(f"KeyError: {e}")
            return {}

    def search_song_details(self, song_name, artist_name, rarity_type):
        rarity_parts = sorted(rarity_type.replace(",", " ").split())
        normalized_rarity_type = " ".join(rarity_parts).lower()

        compatible_rarities = [
            "common", "uncommon", "rare", "shiny", 
            "mystic", "exclusive",
            "rare shiny", "uncommon shiny", "common shiny"
        ]

        if normalized_rarity_type not in compatible_rarities:
            return "Please check a different rarity."

        query = {
            "0": {
                "query": f"{song_name} {artist_name}",
                "includeMine": False,
                "rarities": normalized_rarity_type.split()
            }
        }
        encoded_query = urllib.parse.quote(json.dumps(query))
        url = f"{self.API_BASE}{self.API_SEARCH}&input={encoded_query}"

        try:
            response = self.http.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()

            matching_songs = []
            for trade in data[0]["result"]["data"].get("tradeOffers", []):
                for song in trade.get("songs", []):
                    if "shiny" in normalized_rarity_type:
                        type_match = song.get("type", "").lower() == "shiny"
                        rarity_match = all(r in song.get("rarity", "").lower() for r in rarity_parts if r != "shiny")
                    else:
                        type_match = True
                        rarity_match = all(r in song.get("rarity", "").lower() for r in rarity_parts)

                    is_match = (
                        song_name.lower() == song.get("name", "").lower()
                        and artist_name.lower() == song.get("artist", "").lower()
                        and rarity_match
                        and type_match
                    )

                    if is_match:
                        song_data = {
                            "song_name": song["name"],
                            "artist": song["artist"],
                            "image_url": song["imageUrl"],
                            "rarity": song["rarity"],
                            "type": song.get("type", ""),
                            "owner_id": song["ownerId"],
                            "owner_username": trade["user"]["username"],
                            "owner_trades_completed": trade["user"]["tradesCompleted"]
                        }
                        if normalized_rarity_type == "mystic":
                            song_data["sequence_label"] = song.get("sequenceLabel", "")
                        matching_songs.append(song_data)

            return matching_songs if matching_songs else "Please check a different rarity."

        except requests.exceptions.RequestException as e:
            print(f"Error in search: {e}")
            return None
        
    def reroll_artist_quest(self, artist_id, rewarded_ad=False):
        reroll_url = f"{self.API_BASE}{self.reroll_artist_quest}"
        payload = {
            "0": {
                "artistId": artist_id,
                "rewardedAd": rewarded_ad
            }
        }

        try:
            response = self.http.post(reroll_url, headers=self.headers, json=payload)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error rerolling artist quest: {e}")
            return None
