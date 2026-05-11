
# OpenPass

The Decentralized Microservice Drone System for Digital Agriculture is a distributed, scalable platform designed to orchestrate autonomous drone operations for agricultural field missions. The system captures, processes, and analyzes aerial imagery and video data to support precision agriculture, crop monitoring, and field management operations.

### Tags
- Software
- Digital-Agriculture
- Animal-Ecology

### License
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  
## References
- [K3s](https://docs.k3s.io/)


## Acknowledgements
*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*


---

# Tutorials

### Prerequisites
- Ubuntu 22.04 or higher
- User account named `icicle` with passwordless sudo access to root
- Libraries: `bash`, `curl`, `python3`, `git`, `docker` (installed automatically by the script)
- Hardware: minimum 4 CPU cores at 1.2 GHz, 8 GB RAM, 256 GB storage
- Parrot Anafi Drones
- SSH private key with access to the OpenPASS Git server

The following must be in place **before** running the installer:

**User**: Must be logged in as `icicle`. Confirm with `whoami`.

**Path**: The repository must be cloned to exactly `/home/icicle/icicleEdge`. The installer validates this path at startup and exits if it does not match.

**SSH Key**: Place your SSH private key at `config/stage` inside the cloned repo. This authenticates against the OpenPASS Git server to pull microservice source code during deployment.

**Passwordless Sudo**: The `icicle` user must be able to run `sudo` without a password prompt. Verify with `sudo whoami` — it must return `root` instantly.


---

# How-To Guides

### Online Mode (Standard Install)

Use this when the device has internet access and can reach the OpenPASS Git server. Microservice source code is pulled from the remote server at deploy time.

```bash
# Clone the repository to the required path
cd /home/icicle
git clone https://github.com/ICICLE-ai/OpenPass.git icicleEdge

# Place your SSH key
cp /path/to/your/ssh_key /home/icicle/icicleEdge/config/stage
chmod 600 /home/icicle/icicleEdge/config/stage

# Run the installer
cd /home/icicle/icicleEdge
bash install.sh

# Stream the install log in a separate terminal to follow progress
tail -f install.log
```

Once the installer finishes:

```bash
# Confirm all pods are Running and Ready (allow up to 3 minutes)
kubecmd get pods

# Start the Aerial Scouting Units
cd /home/icicle/icicleEdge/installation/ASU
bash restartASU.sh

# Launch the web dashboard
bash /home/icicle/icicleEdge/startWebsite.sh
```


### Offline / Edge Mode

Use this when the device operates without internet after deployment. All microservice repositories are cloned locally during install and served from the device. Each pod receives a volume mount exposing the local repo mirror at `/mounted-repo` inside the container.

```bash
# Clone the repository to the required path
cd /home/icicle
git clone https://github.com/ICICLE-ai/OpenPass.git icicleEdge

# Place your SSH key (still required for initial clone during install)
cp /path/to/your/ssh_key /home/icicle/icicleEdge/config/stage
chmod 600 /home/icicle/icicleEdge/config/stage

# Run the installer with --edge flag
# This clones all microservice repos to /home/icicle/icicleLocalGit/stage/
# and configures offline networking and volume mounts
cd /home/icicle/icicleEdge
bash install.sh --edge

# Stream the install log in a separate terminal to follow progress
tail -f install.log
```

Once the installer finishes:

```bash
# Confirm all pods are Running and Ready (allow up to 3 minutes)
kubecmd get pods

# Start the Aerial Scouting Units
cd /home/icicle/icicleEdge/installation/ASU
bash restartASU.sh

# Launch the web dashboard
bash /home/icicle/icicleEdge/startWebsite.sh
```


### install.sh Flags

| Flag | Description |
|------|-------------|
| *(none)* | Standard online install — pulls source from remote Git server |
| `--edge` or `-e` | Offline/edge install — clones all repos locally, mounts them into pods |
| `--verbose` or `-v` | Print detailed debug output during installation |
| `devel` | Use the development Git environment (write access) instead of stage (read-only) |
| `--help` or `-h` | Show usage information and exit |

Examples:

```bash
bash install.sh                  # online, stage environment
bash install.sh --edge           # offline, stage environment
bash install.sh --edge -v        # offline, verbose output
bash install.sh devel            # online, devel environment
bash install.sh --edge devel     # offline, devel environment
```


### Restarting Microservices

If the application is already installed and you need to redeploy:

```bash
cd /home/icicle/icicleEdge/installation

# Online — pulls latest source from the remote Git server
bash installMicroservice.sh -a

# Offline/Edge — uses locally cloned repos and mounts volume into pods
bash installMicroservice.sh -a -e

# Reinstall a single microservice (e.g. openpass)
bash installMicroservice.sh -m openpass

# Reinstall without reinstalling K3s (faster if K3s is already healthy)
bash installMicroservice.sh -a --no-k3s

# List all available microservices and their ports
bash installMicroservice.sh -l
```

After redeployment, check pod status and restart the web interface:

```bash
kubecmd get pods

cd /home/icicle/icicleEdge/installation/ASU
bash restartASU.sh

bash /home/icicle/icicleEdge/startWebsite.sh
```

> ⚠️ **Note:** You may briefly see this error during startup — it is expected and resolves automatically as the container initialises: `Internal error occurred: unable to upgrade connection: container not found ("apache")`

> ⚠️ **Note:** `/home/icicle/icicleEdge` is the live operational directory. The original cloned repo is only used for the initial install.


After running `startWebsite.sh` you can see this dashboard:
![](/docs/images/dashboard.png)

Note: OpenPass offers several missions that can be used for data collection. These include missions utilizing GPS as well as movement-based (X,Y,Z axis) missions. OpenPass also provides an Orthomosaic Mission, which generates an orthomosaic of one acre of land. Each mission has its own description displayed on its respective button. Once you click on the mission button you can also have a look at the detailed description of the mission.

We are currently working on and testing missions that support YOLO libraries, enabling real-time object detection during mission execution on OpenPass.


## Overview

This installation script automates the deployment of OpenPASS and its required dependencies on edge computing devices, specifically configured for laptop-based implementations. The system establishes a complete microservice environment with containerized applications, networking configuration, and essential development tools.


## Installation Process

### System Configuration
The installation begins by configuring Ubuntu to optimize performance for edge computing. The script disables system hibernation, sleep modes, and screen locking to ensure uninterrupted microservice availability during extended operations.

### Package Installation
The script installs all required packages via `apt-get`: Docker for containerization, Python 3 for application runtime, Git for version control, Helm for Kubernetes deployments, and networking utilities. MariaDB and SDL2 libraries are included for database connectivity and multimedia processing.

### Network Configuration
Two virtual network interfaces are created using Linux dummy network drivers:

- **`icl231`** — IP `192.168.231.231/24`. Hosts the local Software Pilot HTTP service on port `2311`.
- **`icl43`** — IP `192.168.43.231/24`. Used by K3s as the Flannel CNI interface, routing all inter-pod traffic within the node. This ensures pods continue communicating even when external internet is unavailable.

DNS resolution is reconfigured by replacing `systemd-resolved` with a static `resolv.conf` pointing to `8.8.4.4`, ensuring reliable name resolution for containerised services.

### Development Environment Setup
Git is configured with default credentials and branch settings. Helm is installed via Snap and used to deploy each of the six microservices as independent Kubernetes releases on the K3s cluster.

### SSH Key and Repository Access
The SSH key at `config/stage` authenticates against the OpenPASS Git server. The active environment (`stage` or `devel`) is saved to `/home/icicle/icicleEdge/ctxt` and used by all subsequent deploy operations.

- **Online mode**: each microservice's source is cloned from the remote server at deploy time via `deployMicroservice.py`.
- **Offline/edge mode**: all repositories are cloned once into `/home/icicle/icicleLocalGit/stage/` during install. The deploy script `deployEdgeMicroservice.py` copies from this local mirror instead of the remote server.

### Local Volume Mount (Offline / Edge Mode Only)
When deploying with `--edge`, each Kubernetes pod receives a `hostPath` volume mount that exposes the local repo mirror at `/mounted-repo` inside the container. This is applied automatically by `deployEdgeMicroservice.py`, which appends the volume configuration to each Helm release's `values.yaml` before install. The host path `/home/icicle/icicleLocalGit/stage` is created automatically if it does not exist.

### Python Environment
Python dependencies are installed via pip3: `softwarepilot`, `pysdl2`, `fastapi`, and `py-lz4framed`. These support drone communication, video processing, and the REST API layer used by the microservices.

### Security Configuration
The SSH key at `config/stage` is used for Git server authentication. File permissions are set to `600` to ensure the key is accepted by SSH. All `sudo` operations require the `icicle` user to have passwordless access configured before installation begins.


## Post-Installation Operations

### Microservice Initialization
The installer deploys six core OpenPASS microservices via Helm on the K3s cluster:

| Microservice | Port |
|---|---|
| `website` | 30080 |
| `openpass` | 54292 |
| `asu` | 43210 |
| `boundarymap` | 8383 |
| `yolomissions` | 2222 |
| `aimissions` | 1212 |

In edge mode, this automatically uses the offline deploy path with the local volume mount.

### Verification Steps
After installation, confirm the system is healthy:

```bash
# All pods should show READY 1/1 and STATUS Running
kubecmd get pods

# Local HTTP service should respond
curl http://192.168.231.231:2311

# Both dummy interfaces should be UP
ip link show icl231
ip link show icl43

# In edge mode, confirm repos were cloned
ls /home/icicle/icicleLocalGit/stage/
```


## Repository Access

### Default Configuration (Stage)
The installation uses the `stage` Git environment by default, providing read-only access to stable releases. The active context is saved to `/home/icicle/icicleEdge/ctxt` and referenced by all deploy scripts.

### Development Mode (Devel)
Pass `devel` as an argument to switch to the development environment, which provides write access for administrators:

```bash
bash install.sh devel            # online, devel environment
bash install.sh --edge devel     # offline/edge, devel environment
```


## Troubleshooting

### Pod stuck in `ContainerCreating` or `Pending`
The startup probe copies files and runs `setup.sh` inside the container, which can take up to 3 minutes. If the pod stays stuck, inspect it:

```bash
kubecmd describe pod <pod-name>
kubecmd logs <pod-name>
```

### `validate_path` error on install
The repo must be cloned to exactly `/home/icicle/icicleEdge`. Re-clone with the correct target:

```bash
cd /home/icicle
git clone https://github.com/ICICLE-ai/OpenPass.git icicleEdge
```

### SSH key error on install
Confirm the key exists and has correct permissions:

```bash
ls -l /home/icicle/icicleEdge/config/stage
chmod 600 /home/icicle/icicleEdge/config/stage
```

### Sudo prompts for password
The `icicle` user must have passwordless sudo. Add to `/etc/sudoers` via `visudo`:

```
icicle ALL=(ALL) NOPASSWD: ALL
```

### Offline mode — pods cannot find repos
Ensure `--edge` was passed during `install.sh`. Verify the local repos exist and are populated:

```bash
ls /home/icicle/icicleLocalGit/stage/
```

If the directory is empty or missing, the edge repos were not cloned. Re-run the installer with `--edge` or manually clone the repos using the SSH key at `config/stage`.

### System Maintenance
Updates should be applied through the Git workflow — pull the latest changes into `/home/icicle/icicleEdge` and redeploy affected microservices with `installMicroservice.sh`. The modular architecture allows individual microservices to be updated without a full reinstall.

This installation framework provides a robust foundation for deploying OpenPASS on edge computing devices, supporting scalable drone operations and agricultural data processing workflows.

---
