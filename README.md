# htmlcsswithdocker
Htmlcss run with docker compose

![First Lab Image](https://github.com/khunlinnaing/htmlcsswithdocker/blob/main/first_lab.png?raw=true)
# Install Docker and Docker Compose

This guide provides instructions for installing Docker and Docker Compose on your system.

## Prerequisites

- A system running Linux, macOS, or Windows.
- Administrative privileges (sudo/root access) on the system.

## Table of Contents

1. [Install Docker](#install-docker)
2. [Install Docker Compose](#install-docker-compose)
3. [Verify Installation](#verify-installation)

## 1. Install Docker

### On Linux

1. Update your package index:
    ```bash
    sudo apt update
    ```

2. Install the required dependencies:
    ```bash
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    ```

3. Add Docker’s official GPG key:
    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

4. Set up the Docker stable repository:
    ```bash
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    ```

5. Install Docker CE (Community Edition):
    ```bash
    sudo apt update
    sudo apt install docker-ce
    ```

6. Enable Docker to start on boot:
    ```bash
    sudo systemctl enable docker
    sudo systemctl start docker
    ```

### On macOS

1. Download Docker Desktop for Mac from the [Docker website](https://www.docker.com/products/docker-desktop).
2. Open the downloaded `.dmg` file and drag Docker to your Applications folder.
3. Launch Docker from the Applications folder, and follow the on-screen instructions.

### On Windows

1. Download Docker Desktop for Windows from the [Docker website](https://www.docker.com/products/docker-desktop).
2. Run the installer and follow the on-screen instructions.
3. After installation, launch Docker from the Start menu.

## 2. Install Docker Compose

### On Linux

1. Download the latest version of Docker Compose:
    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r .tag_name)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

2. Apply executable permissions to the binary:
    ```bash
    sudo chmod +x /usr/local/bin/docker-compose
    ```

3. Verify the installation:
    ```bash
    docker-compose --version
    ```

### On macOS & Windows

Docker Compose is included with Docker Desktop, so there’s no need to install it separately. After installing Docker Desktop, you can use Docker Compose directly from the terminal.

## 3. Verify Installation

After installing Docker and Docker Compose, verify the installations:

1. Check Docker version:
    ```bash
    docker --version
    ```

2. Check Docker Compose version:
    ```bash
    docker-compose --version
    ```

Both commands should return the version numbers, confirming that Docker and Docker Compose are successfully installed.

## Additional Information

- For more information about Docker, visit the [official documentation](https://docs.docker.com/).
- For more information about Docker Compose, visit the [official documentation](https://docs.docker.com/compose/).


- **Firewall Issues**: Ensure that your firewall settings do not block Docker from communicating with the internet or local networks.
## Run docker compose
Run the following command to build and start your containers in detached mode:
    ```
    docker-compose up --build -d
    ```

