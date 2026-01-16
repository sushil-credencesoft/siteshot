#!/usr/bin/env bash
set -e

INSTALL_DIR="$HOME/.siteshot"
BIN_URL="https://raw.githubusercontent.com/sushil-credencesoft/siteshot/main/dist/siteshot-linux"
BIN_PATH="$INSTALL_DIR/siteshot"

echo "Installing SiteShot CLI..."

mkdir -p "$INSTALL_DIR"
curl -fsSL "$BIN_URL" -o "$BIN_PATH"
chmod +x "$BIN_PATH"

SHELL_RC="$HOME/.bashrc"
if [[ "$SHELL" == *zsh* ]]; then
  SHELL_RC="$HOME/.zshrc"
fi

if ! grep -q ".siteshot" "$SHELL_RC"; then
  echo 'export PATH="$HOME/.siteshot:$PATH"' >> "$SHELL_RC"
fi

echo "SiteShot installed successfully."
echo "Restart terminal and run: siteshot --help"
