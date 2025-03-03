#!/bin/bash

rm -f /usr/share/applications/webdeck.desktop

update-desktop-database /usr/share/applications
gtk-update-icon-cache /usr/share/icons/hicolor
