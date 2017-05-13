#!/bin/bash

# transmission daemon
cp config/settings.exam.json config/settings.json
cp auth.exam.json auth.json

# gdrive
wget -O drive https://drive.google.com/uc?id=0B3X9GlR6Embnb095MGxEYmJhY2c
sudo install drive /usr/local/bin/drive
rm drive
drive
