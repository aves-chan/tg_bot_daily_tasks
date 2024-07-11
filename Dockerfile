FROM python:3.11-rc-slim

WORKDIR /tg_bot_daily_tasks

COPY requirements.txt .

RUN python -m venv venv
ENV PATH="/tg_bot_daily_tasks/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/tg_bot_daily_tasks"

CMD ["python", "/tg_bot_daily_tasks/bot/run_bot.py"]
