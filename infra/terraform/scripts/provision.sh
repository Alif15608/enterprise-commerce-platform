#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${1:-/opt/enterprise-commerce-platform}"

echo "== Updating package index =="
apt-get update -y

echo "== Installing prerequisites =="
apt-get install -y ca-certificates curl gnupg ufw git

echo "== Installing Docker Engine (official method) =="
if ! command -v docker &> /dev/null; then
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
else
    echo "Docker already installed, skipping."
fi

echo "== Enabling Docker to start on boot =="
systemctl enable docker
systemctl start docker

echo "== Configuring firewall (ufw) =="
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "== Creating application directory =="
mkdir -p "$APP_DIR"

echo "== Provisioning complete =="
docker --version
docker compose version
ufw status