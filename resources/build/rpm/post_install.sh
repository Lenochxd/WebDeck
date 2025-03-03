#!/bin/bash

# Get the latest version
latest_version=$(ls /usr/lib | grep webdeck- | sort -V | tail -n 1)

# Create the desktop icon
cat <<EOF > /usr/share/applications/webdeck.desktop
[Desktop Entry]
Name=WebDeck
Icon=/usr/lib/$latest_version/icon.png
Exec=/usr/bin/webdeck
Terminal=false
Type=Application
Categories=Utility;
EOF

update-desktop-database /usr/share/applications
gtk-update-icon-cache /usr/share/icons/hicolor
