
# OppenPass

The Decentralized Microservice Drone System for Digital Agriculture is a distributed, scalable platform designed to orchestrate autonomous drone operations for agricultural field missions. The system captures, processes, and analyzes aerial imagery and video data to support precision agriculture, crop monitoring, and field management operations.

### License
- MIT, BSD etc.
- e.g  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
- Add any other liceses that you want to include.
  
## References
- [K3s](https://docs.k3s.io/)


## Acknowledgements
*National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606)*


---

# Tutorials

### Prerequisites
- Ubuntu (22.01 or higher)
- Libraries using apt-get: bash, curl, python3, git, and docker.
- Hardware: at least (1) 4 1.2 Ghz CPU cores, (2) 8 GB Ram, and (3) 256 GB storage.
- Parrot Anafi Drones
- K3s (Lightweight Kubernetes)
 
 
The installation requires an Ubuntu-based edge device with the following configurations:

**User Configuration**: The system must have a user account named "icicle" with passwordless sudo privileges to root access. This user account serves as the primary operator for the OpenPASS installation and ongoing operations.

**Directory Structure**: The installation expects the `/home/icicle` directory to exist and be accessible by the current user. Any existing `icicleEdge` directory will be removed and recreated during the installation process.

**Network Access**: The device requires internet connectivity for package downloads, Git repository access, and DNS resolution configuration.


---

# How-To Guides

### Quick Guide
```bash
# Download the install.sh file first
git clone https://github.com/ICICLE-ai/OpenPass.git

# Check if pods are READ and in RUNNING state
kubecmd get pods

#Once all pods are in READY state run 
bash home/icicle/icicleEdge/ea1openpass/startWebsite.sh
```

## Overview

This installation script automates the deployment of OpenPASS and its required dependencies on edge computing devices, specifically configured for laptop-based implementations. The system establishes a complete microservice environment with containerized applications, networking configuration, and essential development tools.



## Installation Process

### System Configuration
The installation begins by configuring the Ubuntu system to optimize performance for edge computing operations. The script disables system hibernation, sleep modes, and screen locking features that could interfere with continuous microservice operations. These modifications ensure uninterrupted service availability during extended operational periods.

### Package Installation
The script installs a comprehensive set of software packages required for the OpenPASS ecosystem. Core components include Docker for containerization, Python 3 for application development, Git for version control, and various networking utilities. Additional packages support database connectivity through MariaDB libraries and multimedia processing capabilities via SDL2 libraries.

### Network Configuration
A critical component of the installation involves DNS resolution configuration. The script replaces the default systemd-resolved service with traditional resolv.conf configuration, pointing to Google's public DNS servers (8.8.4.4). This change ensures reliable network connectivity for containerized services and external API communications.

### Development Environment Setup
The installation configures Git with default user credentials and repository settings, establishing a standardized development environment. Helm package manager installation through Snap provides Kubernetes application deployment capabilities essential for microservice orchestration.

### Repository and File Structure
The script clones the OpenPASS repository from GitHub and establishes a structured directory hierarchy within the icicleEdge folder. This includes separate directories for binary executables, OpenPASS applications, and Helm configuration files. The installation creates convenient aliases for Kubernetes command-line operations.

### Network Interface Configuration
A virtual network interface (icl231) is created using Linux dummy network drivers, configured with a specific MAC address and IP address (192.168.231.231/24). This interface provides isolated networking capabilities for testing and development scenarios without requiring physical network hardware.

### Python Environment
The installation configures Python dependencies through pip3, installing specialized packages for software pilot operations, multimedia processing, and API development. These packages support the core functionality required for drone operations and data processing workflows.

### Security Configuration
SSH key management is automated through the installation script, copying necessary authentication credentials from the OpenPASS repository to the user's SSH directory. Proper file permissions are set to ensure secure access to remote repositories and services.

## Post-Installation Operations

### Microservice Initialization
The installation concludes by executing the microservice startup script, which initializes the core OpenPASS services and establishes the runtime environment. This automated startup ensures that all components are properly configured and ready for operational use.

### Verification Steps
Following successful installation, users should verify that Docker services are running, Kubernetes cluster is accessible through the kubecmd alias, and the virtual network interface is properly configured. The OpenPASS web interface should be accessible for mission planning and system monitoring.

## Repository Access

### Default Configuration
The installation uses the "stage" Git repository by default, providing read-only access to stable releases. This configuration ensures operational stability while preventing unauthorized modifications to core system components.

### Development Mode
Alternative repository access can be configured by passing parameters to the installation script, enabling development repository access with write permissions for system administrators and developers.

## Support Considerations

### System Maintenance
Regular updates should be performed through the established Git workflow, ensuring that security patches and feature enhancements are properly integrated. The modular architecture allows for selective component updates without full system reinstallation.

### Troubleshooting
Common installation issues typically relate to user permissions, network connectivity, or conflicting software packages. The script includes error checking for critical prerequisites, providing clear diagnostic messages when installation requirements are not met.

This installation framework provides a robust foundation for deploying OpenPASS on edge computing devices, supporting scalable drone operations and agricultural data processing workflows.

---

# Explanation

### Architecture:
![](docs/images/architecture.jpg)
![](/docs/images/dashboard.png)