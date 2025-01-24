#!/bin/bash


# Ensure the script is executed with bash
if [ -z "$BASH_VERSION" ]; then
    echo "Error: This script must be run with bash. Please use 'bash build.sh'."
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "run.py" ]; then
    echo "Error: run.py not found. Please run this script from the correct directory."
    exit 1
fi

# Prompt the user to select the build type
echo "Choose the build type:"
echo "1. ALL"
echo "2. Standalone package (cx_Freeze)"
# echo "3. Flatpak"
read -p "Enter your choice (number): " choice


function build_flatpak {
    VERSION=$(jq -r '.versions[0].version' resources/version.json)
    echo "Software version: $VERSION"

    echo "Building Flatpak package... Ensure a tar.gz file is created in the dist directory, or build it using cx_Freeze first."

    # Execute the flatpak-builder command
    flatpak-builder --repo=build/flatpak-repo --force-clean build/flatpak resources/flatpak.yml --state-dir=build/flatpak-builder --default-branch=$VERSION
    echo "Flatpak package built successfully. Exporting the package to dist directory..."
    flatpak build-bundle build/flatpak-repo dist/WebDeck-linux-x86_64-v$VERSION.flatpak com.webdeck.app $VERSION
    echo "Flatpak package exported successfully."

    # Install the Flatpak package
    INSTALL=true
    if [ $INSTALL ]; then
        echo "Uninstalling the existing Flatpak package..."
        flatpak uninstall com.webdeck.app --force-remove -y 
        echo "Installing the Flatpak package..."
        flatpak install --user --reinstall --noninteractive dist/WebDeck-linux-x86_64-v$VERSION.flatpak
        echo "Flatpak package installed successfully."
    fi
}

function build_cx_freeze {
    # Execute the cx_Freeze command
    if [ -f "venv/bin/activate" ]; then
        . venv/bin/activate
    elif [ -f "venv/bin/activate.fish" ]; then
        . venv/bin/activate.fish
    else
        echo "Error: virtual environment not found. Please set up the virtual environment first."
        exit 1
    fi

    echo "Building standalone package using cx_Freeze..."
    python setup.py build
}

# Set default choice to 1 if no input is provided
choice=${choice:-1}

case $choice in
    1)
        echo "You selected ALL."
        echo "----------------------------------"
        build_cx_freeze
        # build_flatpak
        ;;
    2)
        echo "You selected cx_Freeze."
        echo "----------------------------------"
        build_cx_freeze
        ;;
    # 3)
    #     echo "You selected Flatpak."
    #     echo "----------------------------------"
    #     build_flatpak
    #     ;;
    *)
        echo "Invalid choice. Exiting."
        echo "----------------------------------"
        exit 1
        ;;
esac
