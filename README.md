# Polymarket CLI & Telegram Bot

Docker-based setup for Polymarket CLI with a Telegram bot interface for remote command execution.

## Architecture

```
┌─────────────────┐     Docker API     ┌─────────────────────┐
│  Telegram Bot   │ ─────────────────> │  Polymarket CLI     │
│(Python/Aiogram) │      container     │  (Docker/Debian)    │
└─────────────────┘                    └─────────────────────┘
```

- **polymarket-cli**: Polymarket CLI tool running in a container
- **telegram-bot**: Python bot that forwards commands to polymarket-cli

## Requirements

- Docker
- Docker Compose
- Polymarket private key (for wallet access)

## Quick Start

```bash
# Create .env file
cp .env.example .env
# Edit .env with your keys

# Start services
make up

# Or use Makefile commands
make shell        # Interactive Polymarket shell
make markets-list # List markets
make wallet-show  # Show wallet info
make my-balance   # Check balance
```

## Configuration

Edit `.env` with:

```env
# Polymarket
POLYMARKET_PRIVATE_KEY=0xyour_private_key
POLYMARKET_SIGNATURE_TYPE=proxy  # proxy | eoa | gnosis-safe
RUST_LOG=info                    # info | debug | trace

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
AUTHORIZED_USER_IDS=123456789    # comma-separated
ALLOW_ALL_USERS=false            # set true for testing
```

## Commands

Once the bot is running, send any Polymarket CLI command:

- `clob balance --asset-type collateral`
- `markets list --limit 10`
- `wallet show`
- `help`

## Makefile Targets

| Target          | Description                              |
|-----------------|------------------------------------------|
| `build`         | Build Docker images                      |
| `up`            | Start services in background             |
| `down`          | Stop and remove containers               |
| `shell`         | Open polymarket CLI shell                |
| `wallet-create` | Generate new wallet                      |
| `wallet-show`   | Show current wallet info                 |
| `markets-list`  | List latest markets (limit 10)           |
| `my-balance`    | Check collateral balance                 |
| `bash`          | Open bash in polymarket-cli container    |
| `logs`          | Stream logs                              |
| `clean`         | Remove containers and volumes            |

## Files

- `Dockerfile` - Polymarket CLI container (Debian + install.sh)
- `Dockerfile.bot` - Telegram bot container (Python 3.11 slim)
- `docker-compose.yml` - Service definitions
- `bot/bot.py` - Telegram bot source
- `scripts/quick-start.sh` - Setup helper script
