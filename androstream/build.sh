#!/bin/bash
# AndroStream Build Script for Linux/Mac/WSL

set -e

echo "╔═══════════════════════════════════════════════╗"
echo "║       AndroStream APK Build Script            ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer not found!"
    echo "Installing buildozer..."
    pip3 install --user buildozer cython
fi

# Check Java version
echo "Checking Java version..."
if ! command -v java &> /dev/null; then
    echo "❌ Java not found!"
    echo "Please install: sudo apt install openjdk-17-jdk"
    exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | cut -d'.' -f1)
echo "✓ Java version: $JAVA_VERSION"

if [ "$JAVA_VERSION" -lt 11 ]; then
    echo "⚠️  Warning: Java 11+ recommended, you have $JAVA_VERSION"
fi

echo ""
echo "Select build type:"
echo "1) Debug (for testing)"
echo "2) Release (for distribution)"
echo "3) Clean build"
echo "4) Deploy to device"
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Building DEBUG APK..."
        buildozer android debug
        echo ""
        echo "✓ Build complete!"
        echo "APK location: bin/AndroStream-*-debug.apk"
        ;;
    2)
        echo ""
        echo "Building RELEASE APK..."
        echo "⚠️  You'll need to sign the APK for distribution"
        buildozer android release
        echo ""
        echo "✓ Build complete!"
        echo "APK location: bin/AndroStream-*-release-unsigned.apk"
        ;;
    3)
        echo ""
        echo "Cleaning build..."
        buildozer android clean
        echo "✓ Clean complete!"
        echo ""
        read -p "Rebuild now? (y/n): " rebuild
        if [ "$rebuild" = "y" ]; then
            buildozer android debug
        fi
        ;;
    4)
        echo ""
        echo "Deploying to device..."
        echo "Make sure USB debugging is enabled!"
        buildozer android deploy run
        echo ""
        echo "✓ Deploy complete!"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║              Build Process Done               ║"
echo "╚═══════════════════════════════════════════════╝"
