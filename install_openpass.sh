#!/usr/bin/env bash
set -Eeuo pipefail

################################################################################################
# This script installs OpenPASS and required open-source software on an edge device (laptop).  
# 
# It installs from the stage git repository by default. The packages pulled will be read only.
# If the first parameter is set.  We will shift to the devel repo, allowing write access.
################################################################################################

######################################################################
#                                                                    #
#    ######   #####   ######  ##   ##  #####    ####    ####  ####   #
#   ##    ## ##   ##  ##      ###  ##  ##  ##  ##  ##  ##     ##     #
#   ##    ## ##   ##  ##      #### ##  ##  ##  ##  ##  ##     ##     #
#   ##    ## #######  ######  ## ####  #####   ######   ####   ###   #
#   ##    ## ##       ##      ##  ###  ##      ##  ##      ##    ##  #
#   ##    ## ##       ##      ##   ##  ##      ##  ##      ##    ##  #
#    ######  ##       ######  ##   ##  ##      ##  ##   ####  ####   #
#                                                                    #
######################################################################
# ----------------------------
# Config / Flags
# ----------------------------
EDGE=0      # set to 1 when --edge is passed
VERBOSE=0
WHOAMISERVER="stage"

usage() {
  cat <<'HELP'
Usage: ./install_openpass.sh [options]

Options:
  --edge        Include edge-only steps in addition to the standard install
  -e            (short alias for --edge)
  -v, --verbose Verbose output
  -h, --help    Show this help
  --            End of options
HELP
}

# ----------------------------
# Logging helpers
# ----------------------------
log() { printf '%s\n' "$*"; }
step() { printf '\n==> %s\n' "$*"; }
vlog() { (( VERBOSE )) && printf '[DEBUG] %s\n' "$*"; }

# ----------------------------
# Parse args (supports long flags)
# ----------------------------
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --edge|-e) EDGE=1; shift ;;
    --verbose|-v) VERBOSE=1; shift ;;
    --help|-h) usage; exit 0 ;;
    devel) WHOAMISERVER="devel"; POSITIONAL+=("$1"); shift ;;
    --) shift; break ;;        # everything after -- is positional
    -*)
      echo "Unknown flag: $1"
      usage; exit 2
      ;;
    *)
      POSITIONAL+=("$1"); shift ;;
  esac
done
# restore remaining args if you need them later
set -- "${POSITIONAL[@]:-}"

# ----------------------------
# Banner Display
# ----------------------------
display_banner() {
  clear
  echo "=============================================================="
  cat <<'BANNER'
  ___                   ____
 / _ \ _ __   ___ _ __ |  _ \ __ _ ___ ___
| | | | '_ \ / _ \ '_ \| |_) / _` / __/ __|
| |_| | |_) |  __/ | | |  __/ (_| \__ \__ \
 \___/| .__/ \___|_| |_|_|   \__,_|___/___/
      |_|
BANNER
  echo "=============================================================="
}

# ----------------------------
# Tasks
# ----------------------------
preflight() {
  step "Preflight checks"

  KEY_SRC="/home/icicle/icicleEdge/OpenPass/creds"
  KEY_DEST="/home/icicle/.ssh"
  KEY_FILE="stage"

  mkdir -p "$KEY_DEST"
  cp "$KEY_SRC/$KEY_FILE" "$KEY_DEST"
  chown icicle:icicle "$KEY_DEST/$KEY_FILE"
  chmod 600 "$KEY_DEST/$KEY_FILE"
  CONFIG="$KEY_DEST/config"

  SSH_CONFIG_BLOCK="Host 149.165.169.119
  HostName 149.165.169.119
  User stage
  StrictHostKeyChecking no
  IdentityFile $KEY_DEST/$KEY_FILE"

  if [ ! -f "$CONFIG" ]; then
      echo "$SSH_CONFIG_BLOCK" > "$CONFIG"
  elif ! grep -q "Host 149.165.169.119" "$CONFIG"; then
      echo "" >> "$CONFIG"
      echo "$SSH_CONFIG_BLOCK" >> "$CONFIG"
  fi

  # Check correct path
  EXPECTED_PATH="/home/icicle/icicleEdge"
  if [ "$(pwd)" = "$EXPECTED_PATH" ]; then
      echo "✅ Correct path. Continuing..."
  else
      echo "❌ Please move/clone the repository to: /home/icicle/"
      exit 1
  fi

  # Check Git server access
  if [ "$WHOAMISERVER" == "devel" ]; then
      echo "Git will pull from the devel env"
  else
      echo "Git will pull from the stage env"
  fi

  SERVER="149.165.169.119"
  if [ "$WHOAMISERVER" == "`ssh $WHOAMISERVER@$SERVER whoami`" ]; then
      echo "Server user is $WHOAMISERVER"
  else
      echo "Error: server login to server env failed "
      exit 1
  fi

  # Check that user has root access via passwordless sudo
  WHOAMIROOT="root"
  if [ "$WHOAMIROOT" == "`sudo whoami`" ]; then
      echo "Server user is $WHOAMIROOT"
  else
      echo "Error: sudo must provide passwordless access to root on the device "
      exit 1
  fi

  # Check that current user is icicle
  if [ -d "/home/icicle" ]; then
      echo "the directory /home/icicle exists"
  else
      echo "Error: the directory /home/icicle must exist. Is the user 'icicle' on this device"
      exit 1
  fi

  WHOAMI="icicle"
  if [ "$WHOAMI" == "`whoami`" ]; then
      echo "Current user is $WHOAMI"
  else
      echo "Error: the current user should be icicle "
      exit 1
  fi
}

standard_install() {

  # If icicleEdge already exists, remove it
  if [ -d "/home/icicle/icicleEdge" ]; then
      rm -rf /home/icicle/icicleEdge
  else
      echo "This appears to be a fresh install"
  fi

  # Configure Ubuntu to avoid Hibernate and screenlock
  # These features can interfere with the operation of K3S
  sudo systemctl mask sleep.target
  sudo systemctl mask hibernate.target
  sudo systemctl mask hybrid-sleep.target
  gsettings set org.gnome.desktop.session idle-delay 0
  gsettings set org.gnome.desktop.screensaver lock-enabled false

  # Install required packages
  sudo apt-get -y install docker
  sudo apt-get -y install python3
  sudo apt-get -y install git
  sudo apt-get -y install docker wget net-tools curl
  sudo apt-get -y install python3-pip libmariadb3 libmariadb-dev
  sudo apt-get -y install libsdl2-2.0-0

  # Enable (old school) resolv.conf for DNS resolution
  sudo systemctl disable --now systemd-resolved.service
  echo nameserver 8.8.4.4 > ./resolv.conf
  if [ -e "/etc/resolv.conf.original" ]; then
      echo "The original resolv.conf has already been saved"
  else
      sudo mv /etc/resolv.conf /etc/resolv.conf.original
  fi
  sudo mv ./resolv.conf /etc/resolv.conf

  # Install helm and snap and set up Git
  sudo snap install helm --classic
  git config --global user.name "ICICLE Edge Admin"
  git config --global user.email "icicle.edge.admin"
  git config --global init.defaultBranch "master"

  echo 'alias kubecmd="sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml"' >> ~/.bashrc

  # Setup ASU
  cd /home/icicle/icicleEdge
  sudo modprobe dummy
  sudo ip link del icl231 2>/dev/null || true
  sudo ip link add icl231 type dummy
  sudo ifconfig icl231 hw ether C8:D7:4A:4E:47:50
  sudo ip addr add 192.168.231.231/24 brd + dev icl231 label icl231:0
  sudo ip link set dev icl231 up
  echo Dummy IP: 192.168.231.231
  sleep 15

  if [ -d "/home/icicle/icicleEdge/local.softwarepilotservice" ]; then
      rm -rf local.softwarepilotservice
  else
      echo "This appears to be a fresh install, so local.softwarepilot was not found"
  fi

  # Install Python packages and clone repository
  pip3 install softwarepilot
  pip3 install pysdl2
  pip3 install fastapi
  pip3 install py-lz4framed
  sudo apt-get -y install python3-softwarepilot
  git clone $WHOAMISERVER@149.165.169.119:/volume/$WHOAMISERVER/softwarepilotservice.git local.softwarepilotservice
  sed -i 's/from OpenGL import GLX/\#OpenGL import GLX/g' /home/icicle/.local/lib/python3.10/site-packages/olympe/video/renderer.py
  cd local.softwarepilotservice
  sudo cp /usr/bin/python3 /usr/bin/icicleasu
  icicleasu onDevice/main.py >& localservice.logs & disown
  mkdir static
  cd static
  icicleasu -m http.server --bind 192.168.231.231 2311 >& httpservice.logs & disown
  echo Local Service Launched
  sleep 15

  # Set context file -- stage or devel
  echo $WHOAMISERVER > /home/icicle/icicleEdge/ctxt

}

edge_install() {
  BASE_DIR="/home/icicle/icicleLocalGit"
  DEV_DIR="$BASE_DIR/stage"

  # Check if BASE_DIR exists, if not, create it
  if [ ! -d "$BASE_DIR" ]; then
      echo "Creating $BASE_DIR ..."
      mkdir -p "$BASE_DIR"
  else
      echo "$BASE_DIR already exists."
  fi

  # Check if DEV_DIR exists, if not, create it
  if [ ! -d "$DEV_DIR" ]; then
      echo "Creating $DEV_DIR ..."
      mkdir -p "$DEV_DIR"
  else
      echo "$DEV_DIR already exists."
  fi

  echo "✅ Directory setup complete."

  GIT_SERVER="stage@149.165.169.119"
  BASE_PATH="/volume/stage"

  REPO_NAMES=(
      "1212aimissions"
      "2222yolomissions"
      "30080website"
      "43210asu"
      "54292openpass"
      "6532wildwing"
      "8383boundarymap"
      "aimissions"
      "boundarymapcode"
      "icicleDABWeb"
      "openpasswebsite"
      "softwarepilotservice"
      "yolomissionsrc"
  )

  DEST_DIR=$DEV_DIR

  # Function to clone a repository
  clone_repo() {
      local repo_name="stage"
      local folder_name="${repo_name}"
      local repo_url="${GIT_SERVER}:${BASE_PATH}/${repo_name}.git"
      
      echo "----------------------------------------"
      echo "Cloning repository: $repo_name"
      echo "From: $repo_url"
      echo "To: $DEST_DIR/$folder_name"
      
      git clone "$repo_url" "$DEST_DIR/$folder_name"
      
      if [ $? -eq 0 ]; then
          echo "✅ Successfully cloned $repo_name"
      else
          echo "❌ Failed to clone $repo_name"
      fi
  }

  # Main execution
  echo "=== Git Repository Cloning Tool ==="
  echo "Will clone ${#REPO_NAMES[@]} repositories"

  for repo in "${REPO_NAMES[@]}"; do
      clone_repo "$repo"
  done

  echo "=== Cloning complete ==="
  echo "Repositories were cloned to: $DEST_DIR"

  echo "=== Cloned Repositories ==="
  ls -la "$DEST_DIR"
}

post_install() {
    # Add desktop resources
  rm -rf /home/icicle/Desktop/OpenPASS
  mkdir /home/icicle/Desktop/OpenPASS
  ln -s /home/icicle/icicleEdge/ea1openpass/restartMicroservices.sh  /home/icicle/Desktop/OpenPASS/restartOpenPass.sh
  ln -s /home/icicle/icicleEdge/ea1openpass/restartMicroservices-edge2cloud.sh  /home/icicle/Desktop/OpenPASS/restartOpenPass_in_Edge2Cloud_mode.sh
  ln -s /home/icicle/icicleEdge/ea1openpass/restartMicroservices-barebones.sh  /home/icicle/Desktop/OpenPASS/restartOpenPass_in_barebones_mode.sh
  ln -s /home/icicle/icicleEdge/ea1openpass/restartMicroservices-only.sh  /home/icicle/Desktop/OpenPASS/lightweight_restart_keepK3s_running.sh
  ln -s /home/icicle/icicleEdge/ea1openpass/showServices.sh  /home/icicle/Desktop/OpenPASS/checkOpenPass_status.sh
  ln -s /home/icicle/icicleEdge/ea1openpass/startWebsite.sh  /home/icicle/Desktop/OpenPASS/startWebsite.sh
  ln -s /home/icicle/icicleEdge/ea1openpass/restartASU.sh  /home/icicle/Desktop/OpenPASS/restart_Aerial_Scouting_Units.sh

  # Start the application
  cd /home/icicle/icicleEdge/ea1openpass
  bash /home/icicle/icicleEdge/ea1openpass/startMicroservice.sh
  log "OpenPASS installation completed successfully"
}

# ----------------------------
# Orchestration
# ----------------------------
main() {
  display_banner
  preflight
  standard_install
  if (( EDGE )); then
    edge_install
  fi
  post_install
  log $'\n✅ Done.'
}

main "$@"
