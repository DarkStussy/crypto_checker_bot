# DESCRIPTION

Telegram bot to track the prices of cryptocurrencies. Bot notifies users of spikes and drops in monitored
cryptocurrencies.
Shows the entire list of cryptocurrency pairs that are available on the Binance crypto exchange in inline mode.
LINK: https://t.me/crypto_ds_bot

# How to use

### 1. Prepare your environment:

Ensure you have Docker and Docker Compose installed.

### 2. Set up environment variables in docker-compose.yaml:

```
BOT_TOKEN=your_bot_token
ADMINS=123456789
DB_HOST=your_host
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_DATABASE=your_db_name
```

### 3. Build and start the bot:

```
docker compose up -d --build
```
