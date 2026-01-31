#!/bin/bash
# Tips-Endstone Build Script (Unix/Linux/macOS)
# Uses uv for dependency management

set -e

echo "🔧 Tips-Endstone Build Script"
echo "=============================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "📦 uv version: $(uv --version)"

# Sync dependencies
echo ""
echo "📥 Installing dependencies..."
uv sync

# Build wheel
echo ""
echo "🔨 Building wheel..."
uv build --wheel

echo ""
echo "✅ Build complete!"
echo "📁 Output: dist/"
ls -la dist/*.whl 2>/dev/null || echo "No wheel files found"
