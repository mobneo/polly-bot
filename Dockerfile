# Dockerfile - uses the official install.sh file
FROM debian:bookworm-slim

# Setting up dependencies for install.sh
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    tar \
    gzip \
    sudo \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Run the official installation script
RUN curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh

# Create a directory for the configuration
RUN mkdir -p /root/.config/polymarket

# Polymarket CLI is installed in /usr/local/bin
ENV PATH="/usr/local/bin:${PATH}"

# The container should keep running until it is stopped
CMD ["tail", "-f", "/dev/null"]
