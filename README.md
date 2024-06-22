# quick start

## create 'config.py' and 'database.db' files

# 'config.py' 
```
BOT_TOKEN = "your token"
DB_PATH = "path db"
```
# 'database.db' 
```
CREATE TABLE "Users" (
	"id"	INTEGER,
	"telegram_id"	INTEGER,
	"username"	TEXT,
	"firstname"	TEXT,
	"lastname"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE "Tasks" (
	"telegram_id"	INTEGER,
	"completion"	TEXT DEFAULT 'False',
	"title"	TEXT,
	"description"	TEXT,
	"date"	TEXT,
	"time"	TEXT,
	"remind"	TEXT DEFAULT 'False'
);
```

