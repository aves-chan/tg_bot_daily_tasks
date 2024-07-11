FROM python:3.11-rc-slim

WORKDIR /tg_bot_daily_tasks

COPY requirements.txt .

RUN python -m venv venv

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/tg_bot_daily_tasks:${PYTHONPATH}

CMD ["python", "/tg_bot_daily_tasks/bot/run_bot.py"]
