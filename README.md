# Book Seller Telegram Bot

A small Telegram bot written in Python that sells a single digital book in PDF format.
The idea is simple: a user opens the bot, sees a short description, goes to an external payment page, and then receives the book file.

---

## Overview

The bot is aimed at authors or small projects that want a minimal, no-frills way to sell a single digital product through Telegram.
Payment itself happens on an external page; the bot only handles the flow around it and keeps track of buyers

---

## Features

- `/start` - greeting, short book description and an inline **"Buy book 💳"** button with an external payment link.
- `/i_paid` - the user tells the bot they completed the payment; the user is then marked as "paid" in the database.
- `/get_book` - if the user is marked as paid, the bot send the PDF book.
- `/buyers` - show a list of all buyers (available only for admins).
- `/broadcast` - send a simple broadcast message to all users (admins only).

---

## Tech Stack

- Python 3.x
- [aiogram](https://docs.aiogram.dev)
- [python-dotenv](https://pypi.org/project/python-dotenv)
- SQLite - lightweight built-in database for users and purchases
- Standard library: `asyncio`, `logging`, `pathlib`, `database`, etc.

---

## Project Structure

A simplified view of the project layout:

```text
app/
    main.py            # bot entrypoint (used with: python -m app.main)
    handlers.py        # command/message handlers
    keyboards.py       # inline keyboards
    config.py          # configuration, paths, .env loading
    services/
        payments.py    # payment / purchase storage logic
        crm.py         # simple CRM: user tracking, first
   
data/
    book.pdf           # the book file
    images/            # optional images for intro / cover

requirements.txt
README.md
```

---

## Installation

1. Clone the repository and go to the project directory:
    ```bash
   git clone https://github.com/<username>/<repo-name>.git
   cd <repo-name> 
    ```
2. (Optional) Create and activate virtual environment:
    ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
   pip install -r requirements.txt
    ```

---

## Configuration
Copy `.env.example` to .env and fill in your values:
```bash
cp .env.example .env
```
Then edit .env and set:
```dotenv
BOT_TOKEN=...
PAY_URL=...
```
If you want to show an intro image on `/start`, you can also add files like:
```text
data/images/01_intro.jpg
data/images/02_author.jpg
```
Images are loaded from the `data/images` folder and sorted by file name.

---

## Running the bot
```bash
  python -m app.main
```
The bot will start in polling mode.
Open Telegram, find your bot and send `/start` to begin.

---

## Fake payment flow
In this version, there is no real payment provider integration. The flow is intentionally simple:
1. The user taps the "Buy book 💳" button and goes to an external payment page (PAY_URL).
2. After payment, the user returns to the bot and sends `/i_paid`.
3. The bot marked as paid in the SQLite database.
4. The next `/get_book` call sends the PDF book.

This setup is enough for a prototype or for internal use, and it keeps the bot logic independent of any specific payment service.

---

## Notes for recruiters / engineers

I treat this project as a small but complete example of Telegram bot:
- Structure - code is split into modules (`handlers`, `keyboards`, `services`, `config`) instead of one big script.
- Configuration - the bot token and payment URL are loaded from `.env`; secrets are not hard-coded and should not be committed to the repository.
- Database layer - SQLite is used for storing users and purchases; there is a separate CRM module that keeps track of `first_seen/last_seen` timestamps.
- Logging - key actions (commands, book delivery, broadcast failures) are logged using the standard logging module.

In a real production setup this bot could be extended with a proper payment provider integration, more detailed CRM, and additional admin tooling. For now, it shows how I structure and ship a small, self-contained Python project.