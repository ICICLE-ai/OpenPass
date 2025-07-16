KEY_SRC="/home/icicle/icicleEdge/OpenPass/creds"
KEY_DEST="/home/icicle/.ssh"
KEY_FILE="stage"

mkdir -p "$KEY_DEST"
cp "$KEY_SRC/$KEY_FILE" "$KEY_DEST/"
sudo chmod 600 "$KEY_DEST/$KEY_FILE"
CONFIG="$KEY_DEST/config"

if [ ! -f "$CONFIG" ]; then
  sudo echo -e "IdentityFile $KEY_DEST/$KEY_FILE" > "$CONFIG"
elif ! grep -q "IdentityFile $KEY_DEST/$KEY_FILE" "$CONFIG"; then
  sudo echo -e "\nIdentityFile $KEY_DEST/$KEY_FILE" >> "$CONFIG"
fi