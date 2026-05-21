#!/usr/bin/env python3
"""Telegram bot for executing Polymarket CLI commands."""

import asyncio
import os
import re
from typing import Final

import docker
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

# Configuration
BOT_TOKEN: Final = os.environ.get("TELEGRAM_BOT_TOKEN")
AUTHORIZED_USERS: Final = [
    int(uid) for uid in os.environ.get("AUTHORIZED_USER_IDS", "").split(",") if uid.strip()
]

# Debug flag - allow everyone (for testing)
ALLOW_ALL_USERS: Final = os.environ.get("ALLOW_ALL_USERS", "false").lower() == "true"

# Docker client
docker_client = docker.APIClient(base_url="unix:///var/run/docker.sock")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def is_authorized(user_id: int) -> bool:
    """Checks if the user is authorized."""
    if ALLOW_ALL_USERS:
        return True
    return user_id in AUTHORIZED_USERS


def clean_command_output(output: str) -> str:
    """Cleans output from extra ANSI codes and formatting."""
    # Remove ANSI codes (colors, bold text, etc.)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned = ansi_escape.sub('', output)
    # Limit message length (Telegram limit ~4096 characters)
    max_length = 4000
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "\n\n[output truncated]"
    return cleaned.strip()


def run_polymarket_command(command: list[str]) -> str:
    """Executes polymarket command in Docker container."""
    try:
        # Run the command in polymarket-cli container
        container = "polymarket-cli"
        full_command = ["polymarket"] + command

        # Execute command via Docker API
        result = docker_client.exec_create(
            container,
            cmd=full_command,
            stdout=True,
            stderr=True,
            tty=False
        )

        output = docker_client.exec_start(
            result["Id"],
            stream=False
        ).decode("utf-8")

        return output

    except Exception as e:
        return f"❌ Error executing command: {e}"


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Command /start."""
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    if not is_authorized(user_id):
        await message.answer(
            "❌ Your ID is not authorized to use this bot.\n"
            f"Your ID: {user_id}"
        )
        return

    await message.answer(
        f"👋 Hello, {user_name}!\n"
        "I am a bot for working with Polymarket CLI.\n\n"
        "Quick commands:\n"
        "`/balance` - Show collateral balance\n"
        "`/wallet` - Show wallet info\n"
        "`/markets` - List latest markets\n"
        "`/orders` - List your orders\n"
        "`/positions` - List your positions\n\n"
        "Or send any polymarket command directly:\n"
        "`clob balance --asset-type collateral`\n"
        "`markets list --limit 10`\n"
        "`help`",
        parse_mode="Markdown"
    )


@dp.message(Command("exec", "run"))
async def cmd_exec(message: Message, command: CommandObject) -> None:
    """Command /exec <command> — executes a polymarket command."""
    user_id = message.from_user.id

    if not is_authorized(user_id):
        await message.answer("❌ You are not authorized to use this bot.")
        return

    if not command.args:
        await message.answer(
            "⚠️ A command to execute is required.\n"
            "Example: `/exec clob balance --asset-type collateral`",
            parse_mode="Markdown"
        )
        return

    # Prepare command
    cmd_parts = command.args.strip().split()

    if not cmd_parts:
        await message.answer("❌ Empty command.")
        return

    # Show "typing..." to user
    await message.answer("⏳ Executing command...")

    # Execute command
    result = run_polymarket_command(cmd_parts)
    cleaned = clean_command_output(result)

    # Send result
    # If too long - send as file
    if len(cleaned) > 4000:
        with open("/tmp/polymarket_result.txt", "w") as f:
            f.write(result)
        await message.answer_document(
            types.input_file.FSInputFile("/tmp/polymarket_result.txt"),
            caption="Command output (file)"
        )
        os.remove("/tmp/polymarket_result.txt")
    else:
        await message.answer(f"```\n{cleaned}\n```", parse_mode="Markdown")


@dp.message(Command("balance"))
async def cmd_balance(message: Message) -> None:
    """Command /balance - Show collateral balance."""
    user_id = message.from_user.id

    if not is_authorized(user_id):
        await message.answer("❌ You are not authorized to use this bot.")
        return

    await message.answer("⏳ Checking balance...")
    result = run_polymarket_command(["clob", "balance", "--asset-type", "collateral"])
    cleaned = clean_command_output(result)

    if len(cleaned) > 4000:
        with open("/tmp/polymarket_result.txt", "w") as f:
            f.write(result)
        await message.answer_document(
            types.input_file.FSInputFile("/tmp/polymarket_result.txt"),
            caption="Command output (file)"
        )
        os.remove("/tmp/polymarket_result.txt")
    else:
        await message.answer(f"```\n{cleaned}\n```", parse_mode="Markdown")


@dp.message(Command("wallet"))
async def cmd_wallet(message: Message) -> None:
    """Command /wallet - Show wallet info."""
    user_id = message.from_user.id

    if not is_authorized(user_id):
        await message.answer("❌ You are not authorized to use this bot.")
        return

    await message.answer("⏳ Loading wallet info...")
    result = run_polymarket_command(["wallet", "show"])
    cleaned = clean_command_output(result)

    if len(cleaned) > 4000:
        with open("/tmp/polymarket_result.txt", "w") as f:
            f.write(result)
        await message.answer_document(
            types.input_file.FSInputFile("/tmp/polymarket_result.txt"),
            caption="Command output (file)"
        )
        os.remove("/tmp/polymarket_result.txt")
    else:
        await message.answer(f"```\n{cleaned}\n```", parse_mode="Markdown")


@dp.message(Command("markets"))
async def cmd_markets(message: Message) -> None:
    """Command /markets - List latest markets."""
    user_id = message.from_user.id

    if not is_authorized(user_id):
        await message.answer("❌ You are not authorized to use this bot.")
        return

    await message.answer("⏳ Listing markets...")
    result = run_polymarket_command(["markets", "list", "--limit", "10"])
    cleaned = clean_command_output(result)

    if len(cleaned) > 4000:
        with open("/tmp/polymarket_result.txt", "w") as f:
            f.write(result)
        await message.answer_document(
            types.input_file.FSInputFile("/tmp/polymarket_result.txt"),
            caption="Command output (file)"
        )
        os.remove("/tmp/polymarket_result.txt")
    else:
        await message.answer(f"```\n{cleaned}\n```", parse_mode="Markdown")


@dp.message(Command("orders"))
async def cmd_orders(message: Message) -> None:
    """Command /orders - List your orders."""
    user_id = message.from_user.id

    if not is_authorized(user_id):
        await message.answer("❌ You are not authorized to use this bot.")
        return

    await message.answer("⏳ Loading orders...")
    result = run_polymarket_command(["orders", "list"])
    cleaned = clean_command_output(result)

    if len(cleaned) > 4000:
        with open("/tmp/polymarket_result.txt", "w") as f:
            f.write(result)
        await message.answer_document(
            types.input_file.FSInputFile("/tmp/polymarket_result.txt"),
            caption="Command output (file)"
        )
        os.remove("/tmp/polymarket_result.txt")
    else:
        await message.answer(f"```\n{cleaned}\n```", parse_mode="Markdown")


@dp.message(Command("positions"))
async def cmd_positions(message: Message) -> None:
    """Command /positions - List your positions."""
    user_id = message.from_user.id

    if not is_authorized(user_id):
        await message.answer("❌ You are not authorized to use this bot.")
        return

    await message.answer("⏳ Loading positions...")
    result = run_polymarket_command(["positions", "list"])
    cleaned = clean_command_output(result)

    if len(cleaned) > 4000:
        with open("/tmp/polymarket_result.txt", "w") as f:
            f.write(result)
        await message.answer_document(
            types.input_file.FSInputFile("/tmp/polymarket_result.txt"),
            caption="Command output (file)"
        )
        os.remove("/tmp/polymarket_result.txt")
    else:
        await message.answer(f"```\n{cleaned}\n```", parse_mode="Markdown")


@dp.message()
async def handle_message(message: Message) -> None:
    """Handle plain messages as commands."""
    user_id = message.from_user.id

    if not is_authorized(user_id):
        await message.answer("❌ You are not authorized to use this bot.")
        return

    # Simply pass the message as a command
    cmd_text = message.text.strip()
    if not cmd_text:
        return

    await message.answer("⏳ Executing command...")

    cmd_parts = cmd_text.split()
    result = run_polymarket_command(cmd_parts)
    cleaned = clean_command_output(result)

    if len(cleaned) > 4000:
        with open("/tmp/polymarket_result.txt", "w") as f:
            f.write(result)
        await message.answer_document(
            types.input_file.FSInputFile("/tmp/polymarket_result.txt"),
            caption="Command output (file)"
        )
        os.remove("/tmp/polymarket_result.txt")
    else:
        await message.answer(f"```\n{cleaned}\n```", parse_mode="Markdown")


async def main() -> None:
    """Start the bot."""
    # Check configuration
    if not BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not set")
        return

    if not ALLOW_ALL_USERS and not AUTHORIZED_USERS:
        print("❌ Error: AUTHORIZED_USER_IDS not set")
        return

    # Test Docker connection
    try:
        docker_client.ping()
        print("✅ Docker connection OK")
    except Exception as e:
        print(f"❌ Docker connection error: {e}")
        return

    print("✅ Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
