# Telegram Bot Configuration Guide

## Obtaining a Bot Token

1. Open **BotFather** in Telegram (@BotFather)
2. Send the `/newbot` command
3. Follow the instructions to create a bot
4. Get the token (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

## Obtaining Your User ID

Send the `/getmyid` command to the bot or use any bot for getting your ID.

## Configuring the .env file

Copy `.env.example` to `.env` and fill it with real data:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
AUTHORIZED_USER_IDS=987654321
ALLOW_ALL_USERS=false
