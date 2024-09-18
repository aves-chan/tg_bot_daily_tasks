# quick start

## Before launching, you need to create `.env` file. You can create with a command or create manually
# Create manually:
### Add file `.env` the same place as docker-compose.yml
### You can change anything to any value.
```
DB_PASSWORD=<your_postgresql_password>
DB_PORT=5432
REDIS_PASSWORD=<your_redis_password>
REDIS_PORT=6379
BOT_TOKEN=<your_telegram_bot_api_token>
```
# Now use the command `docker-compose build`, then `docker-compose up`




