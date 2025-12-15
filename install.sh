#!/usr/bin/env bash
set -e

################################################################################
# OpenPASS Installation Script
################################################################################
# Installs OpenPASS and required open-source software on an edge device.
#
# By default, pulls from the stage environment (read-only access).
# Use 'devel' parameter to switch to development environment (write access).
################################################################################

################################################################################
# CONFIGURATION VARIABLES
################################################################################

# System Configuration
readonly EXPECTED_PATH="/home/icicle/icicleEdge"
readonly ICICLE_USER="icicle"
readonly ICICLE_HOME="/home/icicle"
readonly ROOT_USER="root"

# SSH Configuration
readonly CONFIG_DIR="${EXPECTED_PATH}/config"
readonly SSH_KEY_FILE="${CONFIG_DIR}/stage"

# Git Server Configuration
readonly GIT_SERVER_IP="149.165.169.119"
readonly GIT_BASE_PATH="/volume"

# Network Configuration
readonly DUMMY_INTERFACE="icl231"
readonly DUMMY_MAC="C8:D7:4A:4E:47:50"
readonly DUMMY_IP="192.168.231.231/24"
readonly HTTP_SERVER_PORT="2311"
readonly DNS_SERVER="8.8.4.4"

# Directory Configuration
readonly LOCAL_SERVICE_DIR="${ICICLE_HOME}/icicleEdge/local.softwarepilotservice"
readonly LOCAL_GIT_BASE="${ICICLE_HOME}/icicleLocalGit"
readonly LOCAL_GIT_STAGE="${LOCAL_GIT_BASE}/stage"
readonly DESKTOP_DIR="${ICICLE_HOME}/Desktop/OpenPASS"
readonly OPENPASS_DIR="${ICICLE_HOME}/icicleEdge/installation"

# Python Configuration
readonly PYTHON_BIN="/usr/bin/python3"
readonly ICICLE_ASU_BIN="/usr/bin/icicleasu"
readonly PYTHON_SITE_PACKAGES="${ICICLE_HOME}/.local/lib/python3.10/site-packages"
readonly OLYMPE_RENDERER="${PYTHON_SITE_PACKAGES}/olympe/video/renderer.py"

# Context File
readonly CONTEXT_FILE="${ICICLE_HOME}/icicleEdge/ctxt"

# Repository List
readonly REPOSITORIES=(
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

# Runtime Flags
EDGE=0
VERBOSE=0
WHOAMISERVER="stage"

################################################################################
# UTILITY FUNCTIONS
################################################################################

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

log() {
    printf '%s\n' "$*"
}

step() {
    printf '\n==> %s\n' "$*"
}

vlog() {
    (( VERBOSE )) && printf '[DEBUG] %s\n' "$*"
}

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

################################################################################
# VALIDATION FUNCTIONS
################################################################################

validate_ssh_key() {
    step "Validating SSH key"
    if [ ! -f "$SSH_KEY_FILE" ]; then
        log "Error: SSH key not found at $SSH_KEY_FILE"
        log "Please place your SSH key in the config folder"
        exit 1
    fi
    log "SSH key found"
}

validate_path() {
    step "Validating installation path"
    if [ "$(pwd)" = "$EXPECTED_PATH" ]; then
        log "Correct path. Continuing..."
    else
        log "Error: Please move/clone the repository to: ${ICICLE_HOME}/"
        exit 1
    fi
}

validate_user() {
    step "Validating current user"
    if [ "$ICICLE_USER" == "$(whoami)" ]; then
        log "Current user is $ICICLE_USER"
    else
        log "Error: Current user must be $ICICLE_USER"
        exit 1
    fi
}

validate_home_directory() {
    step "Validating home directory"
    if [ -d "$ICICLE_HOME" ]; then
        log "The directory $ICICLE_HOME exists"
    else
        log "Error: The directory $ICICLE_HOME must exist"
        exit 1
    fi
}

validate_sudo_access() {
    step "Validating sudo access"
    if [ "$ROOT_USER" == "$(sudo whoami)" ]; then
        log "Sudo access confirmed"
    else
        log "Error: Sudo must provide passwordless access to root"
        exit 1
    fi
}

validate_git_server_access() {
    step "Validating Git server access"
    if [ "$WHOAMISERVER" == "devel" ]; then
        log "Git will pull from the devel environment"
    else
        log "Git will pull from the stage environment"
    fi

    if GIT_SSH_COMMAND="ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=accept-new" \
       ssh ${WHOAMISERVER}@${GIT_SERVER_IP} whoami | grep -q "$WHOAMISERVER"; then
        log "Server user is $WHOAMISERVER"
    else
        log "Error: Server login to $WHOAMISERVER environment failed"
        exit 1
    fi
}

################################################################################
# SYSTEM CONFIGURATION FUNCTIONS
################################################################################

configure_power_management() {
    step "Configuring power management"

    sudo systemctl mask sleep.target
    sudo systemctl mask hibernate.target
    sudo systemctl mask hybrid-sleep.target
    gsettings set org.gnome.desktop.session idle-delay 0
    gsettings set org.gnome.desktop.screensaver lock-enabled false

    log "Power management configured"
}

install_system_packages() {
    step "Installing system packages"

    sudo apt-get -y install docker
    sudo apt-get -y install python3
    sudo apt-get -y install git
    sudo apt-get -y install docker wget net-tools curl
    sudo apt-get -y install python3-pip libmariadb3 libmariadb-dev
    sudo apt-get -y install libsdl2-2.0-0
    sudo apt-get -y install python3-softwarepilot

    log "System packages installed"
}

configure_dns() {
    step "Configuring DNS resolution"

    sudo systemctl disable --now systemd-resolved.service
    echo "nameserver ${DNS_SERVER}" > ./resolv.conf

    if [ -e "/etc/resolv.conf.original" ]; then
        log "Original resolv.conf already backed up"
    else
        sudo mv /etc/resolv.conf /etc/resolv.conf.original
        vlog "Original resolv.conf backed up"
    fi

    sudo mv ./resolv.conf /etc/resolv.conf
    log "DNS configured"
}

install_helm() {
    step "Installing Helm"

    sudo snap install helm --classic
    log "Helm installed"
}

configure_git() {
    step "Configuring Git"

    git config --global user.name "ICICLE Edge Admin"
    git config --global user.email "icicle.edge.admin"
    git config --global init.defaultBranch "master"

    log "Git configured"
}

setup_kubectl_alias() {
    step "Setting up kubectl alias"

    echo 'alias kubecmd="sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml"' >> ~/.bashrc
    log "kubectl alias added to .bashrc"
}

################################################################################
# NETWORK CONFIGURATION FUNCTIONS
################################################################################

setup_dummy_interface() {
    step "Setting up dummy network interface"

    cd "$EXPECTED_PATH"
    sudo modprobe dummy
    sudo ip link del "$DUMMY_INTERFACE" 2>/dev/null || true
    sudo ip link add "$DUMMY_INTERFACE" type dummy
    sudo ifconfig "$DUMMY_INTERFACE" hw ether "$DUMMY_MAC"
    sudo ip addr add "$DUMMY_IP" brd + dev "$DUMMY_INTERFACE" label "${DUMMY_INTERFACE}:0"
    sudo ip link set dev "$DUMMY_INTERFACE" up

    log "Dummy IP: ${DUMMY_IP%/*}"
    sleep 15
}

################################################################################
# SOFTWARE PILOT SERVICE FUNCTIONS
################################################################################

install_python_packages() {
    step "Installing Python packages"

    pip3 install softwarepilot
    pip3 install pysdl2
    pip3 install fastapi
    pip3 install py-lz4framed

    log "Python packages installed"
}

clone_softwarepilot_service() {
    step "Cloning Software Pilot Service"

    if [ -d "$LOCAL_SERVICE_DIR" ]; then
        rm -rf "$LOCAL_SERVICE_DIR"
        vlog "Removed existing local.softwarepilotservice"
    else
        log "Fresh install - no existing service found"
    fi

    log "Cloning from ${WHOAMISERVER}@${GIT_SERVER_IP}..."
    GIT_SSH_COMMAND="ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=accept-new" \
    git clone "${WHOAMISERVER}@${GIT_SERVER_IP}:${GIT_BASE_PATH}/${WHOAMISERVER}/softwarepilotservice.git" "$LOCAL_SERVICE_DIR"

    log "Software Pilot Service cloned"
}

configure_olympe() {
    step "Configuring Olympe"

    sed -i 's/from OpenGL import GLX/\#OpenGL import GLX/g' "$OLYMPE_RENDERER"
    vlog "Olympe renderer patched"
}

launch_local_services() {
    step "Launching local services"

    cd "$LOCAL_SERVICE_DIR"
    sudo cp "$PYTHON_BIN" "$ICICLE_ASU_BIN"
    $ICICLE_ASU_BIN onDevice/main.py >& localservice.logs & disown

    mkdir -p static
    cd static
    $ICICLE_ASU_BIN -m http.server --bind "${DUMMY_IP%/*}" "$HTTP_SERVER_PORT" >& httpservice.logs & disown

    log "Local services launched"
    sleep 15
}

save_context() {
    step "Saving context"

    echo "$WHOAMISERVER" > "$CONTEXT_FILE"
    log "Context saved: $WHOAMISERVER"
}

################################################################################
# EDGE-SPECIFIC FUNCTIONS
################################################################################

setup_edge_directories() {
    step "Setting up edge directories"

    if [ ! -d "$LOCAL_GIT_BASE" ]; then
        mkdir -p "$LOCAL_GIT_BASE"
        log "Created $LOCAL_GIT_BASE"
    else
        log "$LOCAL_GIT_BASE already exists"
    fi

    if [ ! -d "$LOCAL_GIT_STAGE" ]; then
        mkdir -p "$LOCAL_GIT_STAGE"
        log "Created $LOCAL_GIT_STAGE"
    else
        log "$LOCAL_GIT_STAGE already exists"
    fi

    log "Directory setup complete"
}

clone_repository() {
    local repo_name="$1"
    local folder_name="${repo_name}"
    local repo_url="${WHOAMISERVER}@${GIT_SERVER_IP}:${GIT_BASE_PATH}/${WHOAMISERVER}/${repo_name}.git"

    echo "----------------------------------------"
    echo "Cloning repository: $repo_name"
    echo "From: $repo_url"
    echo "To: ${LOCAL_GIT_STAGE}/${folder_name}"

    GIT_SSH_COMMAND="ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=accept-new" \
    git clone "$repo_url" "${LOCAL_GIT_STAGE}/${folder_name}"

    if [ $? -eq 0 ]; then
        log "Successfully cloned $repo_name"
    else
        log "Failed to clone $repo_name"
    fi
}

clone_all_repositories() {
    step "Cloning repositories"

    echo "=== Git Repository Cloning Tool ==="
    echo "Will clone ${#REPOSITORIES[@]} repositories"

    for repo in "${REPOSITORIES[@]}"; do
        clone_repository "$repo"
    done

    echo "=== Cloning complete ==="
    echo "Repositories cloned to: $LOCAL_GIT_STAGE"
    echo "=== Cloned Repositories ==="
    ls -la "$LOCAL_GIT_STAGE"
}

################################################################################
# POST-INSTALLATION FUNCTIONS
################################################################################

setup_desktop_shortcuts() {
    step "Setting up desktop shortcuts"

    rm -rf "$DESKTOP_DIR"
    mkdir -p "$DESKTOP_DIR"

    ln -s "${OPENPASS_DIR}/installMicroservice.sh" \
        "${DESKTOP_DIR}/restartOpenPass.sh"
    ln -s "${OPENPASS_DIR}/edge2cloudInstallation/installEdge2Cloud.sh" \
        "${DESKTOP_DIR}/restartOpenPass_in_Edge2Cloud_mode.sh"
    ln -s "${ICICLE_HOME}/icicleEdge/adminTools/edgeTools/showServices.sh" \
        "${DESKTOP_DIR}/checkOpenPass_status.sh"
    ln -s "${ICICLE_HOME}/icicleEdge/startWebsite.sh" \
        "${DESKTOP_DIR}/startWebsite.sh"
    ln -s "${OPENPASS_DIR}/ASU/restartASU.sh" \
        "${DESKTOP_DIR}/restart_Aerial_Scouting_Units.sh"

    log "Desktop shortcuts created"
}

start_openpass() {
    step "Starting OpenPASS"

    cd "$OPENPASS_DIR"
    bash "${OPENPASS_DIR}/installMicroservice.sh" -a
    log "OpenPASS started successfully"
}

################################################################################
# MAIN INSTALLATION WORKFLOW
################################################################################

preflight() {
    step "Running preflight checks"

    validate_ssh_key
    validate_path
    validate_git_server_access
    validate_sudo_access
    validate_home_directory
    validate_user

    log "Preflight checks completed"
}

standard_install() {
    step "Running standard installation"

    configure_power_management
    install_system_packages
    configure_dns
    install_helm
    configure_git
    setup_kubectl_alias
    setup_dummy_interface
    install_python_packages
    clone_softwarepilot_service
    configure_olympe
    launch_local_services
    save_context

    log "Standard installation completed"
}

edge_install() {
    step "Running edge-specific installation"

    setup_edge_directories
    clone_all_repositories

    log "Edge installation completed"
}

post_install() {
    step "Running post-installation tasks"

    setup_desktop_shortcuts
    start_openpass

    log "Post-installation completed"
}

################################################################################
# ARGUMENT PARSING
################################################################################

parse_arguments() {
    local positional=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --edge|-e)
                EDGE=1
                shift
                ;;
            --verbose|-v)
                VERBOSE=1
                shift
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            devel)
                WHOAMISERVER="devel"
                positional+=("$1")
                shift
                ;;
            --)
                shift
                break
                ;;
            -*)
                echo "Unknown flag: $1"
                usage
                exit 2
                ;;
            *)
                positional+=("$1")
                shift
                ;;
        esac
    done

    set -- "${positional[@]:-}"
}

################################################################################
# MAIN EXECUTION
################################################################################

main() {
    display_banner
    preflight
    standard_install

    if (( EDGE )); then
        edge_install
    fi

    post_install
    log $'\n\nInstallation completed successfully'
}

################################################################################
# SCRIPT ENTRY POINT
################################################################################

parse_arguments "$@"
main
