#!/usr/bin/env bash
set -e

################################################################################
# OpenPASS Microservice Installation Script
################################################################################
# Install OpenPASS microservices individually or all together
################################################################################

################################################################################
# CONFIGURATION VARIABLES
################################################################################

# System Paths
readonly ICICLE_HOME="/home/icicle"
readonly ICICLE_EDGE="${ICICLE_HOME}/icicleEdge"
readonly DEPLOY_SCRIPT="${ICICLE_EDGE}/bin/deployMicroservice.py"
readonly DEPLOY_EDGE_SCRIPT="${ICICLE_EDGE}/bin/deployEdgeMicroservice.py"
readonly KUBECTL_CONFIG="/etc/rancher/k3s/k3s.yaml"

# K3s Configuration
readonly FLANNEL_IFACE="icl43"
readonly NODE_TYPE="edgedevel"

# Microservice Definitions
declare -A MICROSERVICES=(
    ["website"]="30080website"
    ["openpass"]="54292openpass"
    ["asu"]="43210asu"
    ["boundarymap"]="8383boundarymap"
    ["yolomissions"]="2222yolomissions"
    ["aimissions"]="1212aimissions"
)

declare -A MICROSERVICE_TYPES=(
    ["website"]="standard"
    ["openpass"]="standard"
    ["asu"]="standard"
    ["boundarymap"]="standard"
    ["yolomissions"]="standard"
    ["aimissions"]="standard"
)

declare -A MICROSERVICE_DESCRIPTIONS=(
    ["website"]="Web Interface (Port 30080)"
    ["openpass"]="OpenPASS Core Service (Port 54292)"
    ["asu"]="Aerial Scouting Unit Service (Port 43210)"
    ["boundarymap"]="Boundary Map Utilities (Port 8383)"
    ["yolomissions"]="YOLO Mission Service (Port 2222)"
    ["aimissions"]="AI Mission Service (Port 1212)"
)

# Deployment Configuration
readonly DEPLOYMENT_DELAY=15
readonly K3S_RESTART_DELAY=5

# Runtime Flags
INSTALL_ALL=0
INSTALL_K3S=1
MICROSERVICE_TO_INSTALL=""

################################################################################
# UTILITY FUNCTIONS
################################################################################

usage() {
    cat <<'HELP'
Usage: ./installMicroservice.sh [options]

Description:
  Install OpenPASS microservices individually or all together.
  By default, K3s will be reinstalled. Use --no-k3s to skip K3s installation.

Options:
  -a, --all                Install all microservices
  -m, --microservice NAME  Install specific microservice
  --no-k3s                 Skip K3s installation (only install microservices)
  -l, --list              List all available microservices
  -h, --help              Show this help

Available Microservices:
  website       - Web Interface (Port 30080)
  openpass      - OpenPASS Core Service (Port 54292)
  asu           - Aerial Scouting Unit Service (Port 43210)
  boundarymap   - Boundary Map Utilities (Port 8383)
  yolomissions  - YOLO Mission Service (Port 2222)
  aimissions    - AI Mission Service (Port 1212)

Examples:
  ./installMicroservice.sh -a                    # Install all microservices
  ./installMicroservice.sh -m website            # Install only website
  ./installMicroservice.sh -m openpass           # Install only OpenPASS
  ./installMicroservice.sh -m asu --no-k3s       # Install ASU without K3s
  ./installMicroservice.sh -l                    # List all microservices

HELP
}

list_microservices() {
    echo "=============================================================="
    echo "Available Microservices"
    echo "=============================================================="
    for key in "${!MICROSERVICES[@]}"; do
        printf "  %-15s - %s\n" "$key" "${MICROSERVICE_DESCRIPTIONS[$key]}"
    done | sort
    echo "=============================================================="
}

log() {
    printf '%s\n' "$*"
}

step() {
    printf '\n==> %s\n' "$*"
}

error() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

validate_microservice() {
    local name="$1"
    if [[ ! -v MICROSERVICES[$name] ]]; then
        error "Unknown microservice: '$name'. Use -l to list available microservices."
    fi
}

################################################################################
# K3S FUNCTIONS
################################################################################

uninstall_k3s() {
    step "Uninstalling existing K3s installation"

    if command -v k3s-killall.sh &> /dev/null; then
        sudo bash /usr/local/bin/k3s-killall.sh
    fi

    if command -v k3s-uninstall.sh &> /dev/null; then
        sudo bash /usr/local/bin/k3s-uninstall.sh
    fi

    sudo rm -f /var/lib/rancher/k3s/server/token

    log "Removing Kubernetes directories..."
    sudo rm -rf /etc/ceph \
           /etc/cni \
           /etc/kubernetes \
           /etc/rancher \
           /opt/cni \
           /opt/rke \
           /run/secrets/kubernetes.io \
           /run/calico \
           /run/flannel \
           /var/lib/calico \
           /var/lib/etcd \
           /var/lib/cni \
           /var/lib/kubelet \
           /var/lib/rancher \
           /var/log/containers \
           /var/log/kube-audit \
           /var/log/pods \
           /var/run/calico

    log "K3s uninstalled successfully"
}

setup_offline_mode() {
    step "Configuring offline mode"

    bash "${ICICLE_EDGE}/adminTools/edgeTools/setupOfflineMode.sh" reset
    sleep 1
    bash "${ICICLE_EDGE}/adminTools/edgeTools/setupOfflineMode.sh" init

    log "Offline mode configured"
}

install_k3s() {
    step "Installing K3s"

    sudo curl -sfL https://get.k3s.io | \
        INSTALL_K3S_EXEC="server --flannel-iface=${FLANNEL_IFACE}" /bin/sh -

    sleep "$K3S_RESTART_DELAY"
    log "K3s installed successfully"
}

configure_k3s_node() {
    step "Configuring K3s node"

    local node_name
    node_name=$(sudo k3s kubectl --kubeconfig "$KUBECTL_CONFIG" get nodes | tail -n 1 | awk '{print $1}')

    local edge_id="${node_name}-${NODE_TYPE}"

    sudo k3s kubectl --kubeconfig "$KUBECTL_CONFIG" label node "$node_name" icicletype="$NODE_TYPE"
    echo "$edge_id" > ~/.ssh/icicletype

    log "Node configured: $edge_id"
}

################################################################################
# MICROSERVICE DEPLOYMENT FUNCTIONS
################################################################################

deploy_microservice() {
    local service_key="$1"
    local service_name="${MICROSERVICES[$service_key]}"
    local service_type="${MICROSERVICE_TYPES[$service_key]}"
    local description="${MICROSERVICE_DESCRIPTIONS[$service_key]}"

    step "Deploying ${description}"

    cd "$ICICLE_EDGE"

    if [[ "$service_type" == "edge" ]]; then
        "$DEPLOY_EDGE_SCRIPT" -home "$(pwd)" -devel -edge "$NODE_TYPE" "$service_name"
    else
        "$DEPLOY_SCRIPT" -home "$(pwd)" -devel -edge "$NODE_TYPE" "$service_name"
    fi

    log "Deployed ${service_key}! Waiting ${DEPLOYMENT_DELAY} seconds..."
    sleep "$DEPLOYMENT_DELAY"
}

deploy_all_microservices() {
    step "Deploying all microservices"

    local ordered_services=("website" "openpass" "asu" "boundarymap" "yolomissions" "aimissions")

    for service in "${ordered_services[@]}"; do
        deploy_microservice "$service"
    done

    log "All microservices deployed successfully"
}

################################################################################
# MAIN INSTALLATION WORKFLOW
################################################################################

run_k3s_installation() {
    step "Starting K3s installation"

    uninstall_k3s
    sleep 3
    setup_offline_mode
    install_k3s
    configure_k3s_node

    log "K3s installation completed"
}

run_microservice_installation() {
    if [[ "$INSTALL_ALL" -eq 1 ]]; then
        deploy_all_microservices
    elif [[ -n "$MICROSERVICE_TO_INSTALL" ]]; then
        deploy_microservice "$MICROSERVICE_TO_INSTALL"
    else
        error "No microservice specified. Use -a for all or -m <name> for specific service."
    fi
}

################################################################################
# ARGUMENT PARSING
################################################################################

parse_arguments() {
    if [[ $# -eq 0 ]]; then
        echo "=============================================================="
        echo "OpenPASS Microservice Installation Script"
        echo "=============================================================="
        echo ""
        echo "No options provided. Please specify installation options."
        echo ""
        usage
        exit 0
    fi

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -a|--all)
                INSTALL_ALL=1
                shift
                ;;
            -m|--microservice)
                if [[ -z "$2" ]] || [[ "$2" == -* ]]; then
                    error "Option -m requires a microservice name"
                fi
                MICROSERVICE_TO_INSTALL="$2"
                validate_microservice "$MICROSERVICE_TO_INSTALL"
                shift 2
                ;;
            --no-k3s)
                INSTALL_K3S=0
                shift
                ;;
            -l|--list)
                list_microservices
                exit 0
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            --)
                shift
                break
                ;;
            -*)
                error "Unknown option: $1. Use -h for help."
                ;;
            *)
                error "Unexpected argument: $1. Use -h for help."
                ;;
        esac
    done

    # Validation
    if [[ "$INSTALL_ALL" -eq 1 ]] && [[ -n "$MICROSERVICE_TO_INSTALL" ]]; then
        error "Cannot use -a and -m together. Choose one."
    fi

    if [[ "$INSTALL_ALL" -eq 0 ]] && [[ -z "$MICROSERVICE_TO_INSTALL" ]]; then
        error "Must specify either -a (all) or -m <name> (specific microservice)"
    fi
}

################################################################################
# MAIN EXECUTION
################################################################################

main() {
    log "=============================================================="
    log "OpenPASS Microservice Installation"
    log "=============================================================="

    if [[ "$INSTALL_K3S" -eq 1 ]]; then
        run_k3s_installation
    else
        log "Skipping K3s installation (--no-k3s flag set)"
    fi

    run_microservice_installation

    log ""
    log "=============================================================="
    log "Installation completed successfully!"
    log "=============================================================="
}

################################################################################
# SCRIPT ENTRY POINT
################################################################################

parse_arguments "$@"
main
