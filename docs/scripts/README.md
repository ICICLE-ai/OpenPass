# ICICLE Edge Platform Administration Tools

This directory contains essential tools for administering, deploying, and managing the ICICLE Edge Platform environment.

## Directory Structure

The `script` directory is organized into the following subdirectories:

### `/deployment`

Tools for deploying and managing microservices on the ICICLE Edge Platform. These scripts handle the deployment lifecycle, from initial setup to monitoring and management.

- **deployMicroservice.py**: The primary deployment script that coordinates the installation of microservices on the Kubernetes cluster.
  - **Usage**: `python3 deployMicroservice.py <microservice_name> <port_number> [options]`
  - **Options**:
    - `--developer`: Run in developer mode for testing
    - `--edge-name NAME`: Specify edge device name
    - `--context NAME`: Specify Kubernetes context
    - `--wait-time SECONDS`: Override default wait time
  - **Process**:
    1. Validates microservice naming according to conventions
    2. Checks if the port is already in use (indicating a redeploy)
    3. Creates temporary directories for deployment
    4. Fetches microservice code from Git repository
    5. Copies and modifies Helm templates as needed
    6. Performs Helm installation or uninstallation
    7. Runs unit tests to validate deployment
    8. Updates the service registry in the database if successful

- **copyFirstPod.sh**: Copies files to the first pod of a deployment.
  - **Usage**: `./copyFirstPod.sh <deployment_name> <source_path> <destination_path>`
  - **Example**: `./copyFirstPod.sh my-service ./config.json /app/config.json`
  
- **getFirstPod.sh**: Retrieves the name of the first pod in a deployment.
  - **Usage**: `./getFirstPod.sh <deployment_name>`
  - **Returns**: Name of the first pod as a string
- **getMsAddr.sh**: Retrieves the IP address of a microservice.
  - **Usage**: `./getMsAddr.sh <service_name>`
  - **Returns**: IP address as a string

- **gitconfig.sh**: Configures Git settings for deployments
- **redirectLocalHost.sh**: Sets up port forwarding from localhost to a Kubernetes service.
  - **Usage**: `./redirectLocalHost.sh <service_name> <local_port> <service_port>`
  - **Options**:
    - `-b, --background`: Run in background mode
    - `-t, --timeout SECONDS`: Set connection timeout
  - **Example**: `./redirectLocalHost.sh api-service 8080 80`

- **reduceGitFolder.sh**: Reduces Git repository size by cleaning unnecessary files
- **waitForFirstExec.sh**: Waits until a pod is in a state where it can execute commands.
  - **Usage**: `./waitForFirstExec.sh <pod_name> [timeout_seconds]`
  - **Default Timeout**: 180 seconds
  - **Exit Codes**:
    - 0: Pod is ready for execution
    - 1: Timeout reached
    - 2: Invalid arguments
- **waitForFirstPod.sh**: Waits until the first pod of a deployment is in a running state.
  - **Usage**: `./waitForFirstPod.sh <deployment_name> [timeout_seconds]`
  - **Default Timeout**: 120 seconds
  - **Exit Codes**:
    - 0: Pod is ready
    - 1: Timeout reached
    - 2: Invalid arguments

### `/setup`

Tools for managing edge devices and their connectivity to the platform.

- **setupOfflineMode.sh**: Configures the system for offline operation
- **ASUinstall.sh**: Installation script for ASU (Application Service Utility)
- **killASU.sh**: Terminates running ASU processes
- **restartASU.sh**: Stops and restarts the ASU
- **restartMicroservices-barebone.sh**: Restarts microservices in barebone mode
- **restartMicroservices-edge2cloud.sh**: Restarts microservices with edge-to-cloud connectivity
- **restartMicroservices-only.sh**: Only restarts the microservices without additional configurations
- **restartMicroservices.sh**: Main script for restarting all microservices
- **showServices.sh**: Displays currently running services
- **startWebsite.sh**: Starts the web server for the platform's interface

## Usage Guidelines

### Deployment Process

1. To deploy a new microservice, use the `deployment/deployMicroservice.py` script:
   ```bash
   # Deploy a new microservice on port "8800"
   python3 deployMicroservice.py -home `pwd` -devel -edge edgedevel <port_number><microservice_name> 
   ```

2. For managing existing services, use the appropriate scripts in the `setup` directory:
   ```bash
   ./setup/showServices.sh
   ./setup/restartMicroservices.sh
   ```

## Troubleshooting

If you encounter issues with any of these utilities:

1. Check that Kubernetes is accessible with `kubectl get nodes`
2. Check that Kubernetes created pods with `kubectl get pods`
3. Verify that the correct context is active with `kubectl config current-context`
4. Ensure proper permissions for script execution (`chmod +x script.sh`)
5. Check logs with `kubectl logs <pod_name>`

## Requirements

- K3s Kubernetes cluster
- Helm 3.2.0+
- Python 3.6+
- Git
- Proper network connectivity to Git repositories and container registries

## Security Considerations

- Some scripts require elevated privileges and should be used with caution
- Always verify microservice configurations before deployment to production environments
