<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soundmap API Documentation</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            line-height: 1.6;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            width: 80%;
            margin: auto;
            overflow: hidden;
            padding: 20px;
            background: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #333;
        }
        code {
            background: #e8e8e8;
            padding: 2px 5px;
            border-radius: 5px;
            color: #d14;
        }
        pre {
            background: #e8e8e8;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            color: #d14;
        }
        .highlight {
            background-color: #fffae5;
            padding: 5px;
            border-left: 5px solid #ffecb3;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px 0;
        }
        a {
            color: #d14;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Soundmap API</h1>
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA..." alt="Soundmap API Logo">
        <p>This Python library allows you to interact with the Soundmap API to manage songs, trades, and quests.</p>

        <h2>Features</h2>
        <ul>
            <li>Search for songs</li>
            <li>Fetch songs from a profile</li>
            <li>Create, delete, and manage trade offers</li>
            <li>Fetch and parse trade data</li>
            <li>Get notification counts</li>
            <li>Accept and reject trade offers with optional emojis or notes</li>
            <li>Claim daily lootboxes and coins</li>
            <li>Change user bio</li>
            <li>Fetch and manage artist quests</li>
        </ul>

        <h2>Installation</h2>
        <p>Clone the repository:</p>
        <pre><code>git clone https://github.com/yourusername/soundmap-api.git</code></pre>
        <p>Navigate to the project directory:</p>
        <pre><code>cd soundmap-api</code></pre>
        <p>Install the required dependencies:</p>
        <pre><code>pip install requests urllib3</code></pre>

        <h2>Usage</h2>

        <h3>Initialization</h3>
        <p>To use the API, first create an instance of the <code>Soundmap</code> class:</p>
        <pre><code>from soundmap import Soundmap

api = Soundmap()</code></pre>

        <h3>Search for a Song</h3>
        <pre><code>song_data = api.search_song("song_id")
print(song_data)</code></pre>

        <h3>Fetch Songs from a Profile</h3>
        <pre><code>songs = api.fetch_songs("profile_owner_id")
print(songs)</code></pre>

        <h3>Create a Trade Offer</h3>
        <pre><code>song_ids = ["song_id1", "song_id2"]
result, offer_id = api.create_trade_offer(song_ids, note="Trade note here")
print(result, offer_id)</code></pre>

        <h3>Delete a Trade Offer</h3>
        <pre><code>result = api.delete_trade_offer("offer_id")
print(result)</code></pre>

        <h3>Fetch and Parse Trade Data</h3>
        <pre><code>active_trades = api.fetch_trade_data()
parsed_trades = api.parse_trades(active_trades)
print(parsed_trades)</code></pre>

        <h3>Get Notification Count</h3>
        <pre><code>count = api.notification_count()
print(count)</code></pre>

        <h3>Accept a Trade Offer</h3>
        <pre><code>result = api.accept_trade("trade_id", emoji="🤝", note="Thank you!")
print(result)</code></pre>

        <h3>Reject a Trade Offer</h3>
        <pre><code>result = api.reject_trade("trade_id", emoji="😐", note="Not interested")
print(result)</code></pre>

        <h3>Claim Daily Lootbox</h3>
        <pre><code>result = api.claim_lootbox("genre")
print(result)</code></pre>

        <h3>Claim Daily Coins</h3>
        <pre><code>result = api.claim_coins()
print(result)</code></pre>

        <h3>Change User Bio</h3>
        <pre><code>result = api.change_bio("New bio content")
print(result)</code></pre>

        <h3>Fetch Artist Quests</h3>
        <pre><code>all_quests = api.fetch_quests()
print(all_quests)

specific_artist_quest = api.fetch_quests(artist="The Weeknd")
print(specific_artist_quest)</code></pre>

        <h3>Fetch Trade Data for Quest Requirements</h3>
        <pre><code>trade_requirements = {
    "type": "trade",
    "username": "w"
}
trade_data = api.get_quest_trade_data(trade_requirements)
print(trade_data)</code></pre>

        <h2>Configuring an iOS Device for Burp Suite</h2>
        <p>To configure your iOS device to work with Burp Suite, follow these steps:</p>

        <ol>
            <li>
                <strong>Install Burp Suite:</strong>
                Download and install Burp Suite on your computer from the <a href="https://portswigger.net/burp">official website</a>.
            </li>
            <li>
                <strong>Configure Burp Suite Proxy:</strong>
                <ul>
                    <li>Open Burp Suite and go to the "Proxy" tab.</li>
                    <li>Click on "Options" and ensure the interface is set to listen on 127.0.0.1:8080 (or another desired port).</li>
                </ul>
            </li>
            <li>
                <strong>Configure iOS Device to Use Burp as a Proxy:</strong>
                <ul>
                    <li>On your iOS device, go to <code>Settings</code> > <code>Wi-Fi</code>.</li>
                    <li>Tap the <code>i</code> icon next to the connected Wi-Fi network.</li>
                    <li>Scroll down to <code>HTTP Proxy</code> and select <code>Manual</code>.</li>
                    <li>Enter your computer's IP address in the <code>Server</code> field and <code>8080</code> (or the port set in Burp) in the <code>Port</code> field.</li>
                </ul>
            </li>
            <li>
                <strong>Install Burp Suite CA Certificate on iOS:</strong>
                <ul>
                    <li>Open Safari on your iOS device and navigate to <code>http://burp</code> (or <code>http://&lt;your-computer-ip&gt;:&lt;port&gt;</code>).</li>
                    <li>Download the CA certificate and follow the prompts to install it.</li>
                    <li>Go to <code>Settings</code> > <code>General</code> > <code>Profile</code> (or <code>Profile & Device Management</code>) to install the certificate.</li>
                    <li>Enable full trust for the Burp Suite certificate under <code>Settings</code> > <code>General</code> > <code>About</code> > <code>Certificate Trust Settings</code>.</li>
                </ul>
            </li>
            <li>
                <strong>Start Intercepting Traffic:</strong>
                <ul>
                    <li>Go back to Burp Suite, ensure intercept is on in the "Proxy" > "Intercept" tab.</li>
                    <li>Browse on your iOS device, and you should see traffic being captured in Burp Suite.</li>
                </ul>
            </li>
        </ol>

        <p>For detailed instructions and troubleshooting, refer to the <a href="https://portswigger.net/burp/documentation/desktop/mobile/config-ios-device">Burp Suite documentation</a>.</p>
    </div>
</body>
</html>
