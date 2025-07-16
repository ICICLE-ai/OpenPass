
KEY_SRC="/home/icicle/icicleEdge/Harmona/creds"
KEY_DEST="/home/icicle/.ssh/"
KEY_FILE="stage"

mkdir -p "$KEY_DEST"
cp "$KEY_SRC/$KEY_FILE" "$KEY_DEST/"
chmod 600 "$KEY_DEST/$KEY_FILE"

CONFIG="$KEY_DEST/config"
if [ ! -f "$CONFIG" ]; then
  echo -e "Host *\n    IdentityFile $KEY_DEST/$KEY_FILE" > "$CONFIG"
fi
