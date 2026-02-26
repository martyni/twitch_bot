# twitch_bot

A Twitch chat bot built with [TwitchIO](https://github.com/PythonistaGuild/TwitchIO) that runs in the **martyn123** channel using the bot account **bot123**.

## Features

- **`!hello`** – Greets the user who sent the command
- **`!dice`** – Rolls a six-sided dice and reports the result
- **`!help`** – Lists all available commands

## Step-by-Step Setup Guide

Follow these steps to run the bot in the **martyn123** channel using the **bot123** bot account.

### Prerequisites

- Python 3.10 or newer
- Two Twitch accounts: `martyn123` (the channel) and `bot123` (the bot)

---

### Step 1 – Register a Twitch Application

1. Go to the [Twitch Developer Console](https://dev.twitch.tv/console) and log in with the **bot123** account (or any account you control).
2. Click **Register Your Application**.
3. Fill in the form:
   - **Name**: choose any name (e.g. `martyn123-bot`)
   - **OAuth Redirect URLs**: `http://localhost:4000/oauth/callback`
   - **Category**: Chat Bot
4. Click **Create**, then open the application and click **Manage**.
5. Copy the **Client ID** and generate a **Client Secret** – keep these safe.

---

### Step 2 – Find the Twitch User IDs

You need the numeric User ID for both `martyn123` (the broadcaster) and `bot123` (the bot).

Use the [Twitch CLI](https://dev.twitch.tv/docs/cli/) or run this one-liner (replace values):

```bash
curl -s -X GET \
  "https://api.twitch.tv/helix/users?login=martyn123&login=bot123" \
  -H "Client-Id: <YOUR_CLIENT_ID>" \
  -H "Authorization: Bearer <APP_ACCESS_TOKEN>"
```

Note the `id` field for each user. You can get a temporary app access token with:

```bash
curl -s -X POST "https://id.twitch.tv/oauth2/token" \
  -d "client_id=<YOUR_CLIENT_ID>&client_secret=<YOUR_CLIENT_SECRET>&grant_type=client_credentials" \
  | python -m json.tool
```

---

### Step 3 – Install Dependencies

Clone this repository (if you haven't already) and install the requirements:

```bash
git clone https://github.com/martyni/twitch_bot.git
cd twitch_bot
pip install -r requirements.txt
```

---

### Step 4 – Set Environment Variables

Export the following variables in your shell (replace the placeholder values):

```bash
export CLIENT_ID="<your_app_client_id>"
export CLIENT_SECRET="<your_app_client_secret>"
export BOT_ID="<numeric_user_id_of_bot123>"
export BROADCASTER_ID="<numeric_user_id_of_martyn123>"
```

On Windows (Command Prompt):

```cmd
set CLIENT_ID=<your_app_client_id>
set CLIENT_SECRET=<your_app_client_secret>
set BOT_ID=<numeric_user_id_of_bot123>
set BROADCASTER_ID=<numeric_user_id_of_martyn123>
```

---

### Step 5 – Authorise the Bot Account

The bot needs a User Access Token (OAuth token) scoped to the **bot123** account.

1. Start the bot for the first time:

   ```bash
   python bot.py
   ```

2. TwitchIO starts a local web server on `http://localhost:4000`. Open that URL in your browser while **logged in as bot123** on Twitch.
3. Follow the Twitch OAuth prompt and click **Authorize**.
4. You will be redirected back and the bot will receive and save its token automatically to `.tio.tokens.json`.

> **Note:** The **martyn123** broadcaster also needs to grant the bot permission to post in their chat. Share the OAuth URL with them or log into Twitch as `martyn123` and authorise via the same local server URL before closing the window.

---

### Step 6 – Run the Bot

After authorisation, start the bot normally:

```bash
python bot.py
```

You should see log output similar to:

```
2024-01-01 12:00:00 [INFO] TwitchBot: Subscribed to chat messages in channel <BROADCASTER_ID>
2024-01-01 12:00:00 [INFO] TwitchBot: Bot is ready! Logged in as bot123 (ID: <BOT_ID>)
```

The bot is now active in **martyn123**'s chat. Type `!hello` in the chat to test it.

---

### Step 7 – Keep the Bot Running (Optional)

To keep the bot running continuously, consider using a process manager such as `systemd`, `supervisor`, or `screen`/`tmux`:

```bash
# Example with screen
screen -S twitchbot
python bot.py
# Detach with Ctrl+A then D
```

---

## Environment Variables Reference

| Variable | Description |
|---|---|
| `CLIENT_ID` | App Client ID from the Twitch Developer Console |
| `CLIENT_SECRET` | App Client Secret from the Twitch Developer Console |
| `BOT_ID` | Numeric Twitch User ID of the bot account (`bot123`) |
| `BROADCASTER_ID` | Numeric Twitch User ID of the channel (`martyn123`) |

## Token Storage

On first run the bot saves OAuth tokens to `.tio.tokens.json` in the working directory. This file is loaded automatically on subsequent starts. **Keep this file private** and do not commit it to version control.

Add it to `.gitignore`:

```
.tio.tokens.json
```
