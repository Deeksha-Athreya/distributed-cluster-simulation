# Distributed Systems Cluster Simulation Framework

## Project Overview
A lightweight, simulation-based distributed system mimicking core Kubernetes cluster management functionalities.

## Features
- Node Management
- Pod Scheduling (First-Fit, Best-Fit, Worst-Fit)
- Health Monitoring
- Auto-Scaling
- Resource Usage Tracking
- Network Policy Simulation

## Prerequisites
- Python 3.9+
- Docker
- Docker Compose

## Setup and Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Local Development
```bash
# Run API Server
python -m src.api_server

# In another terminal, use CLI
python -m src.cli_client add-node --cpu-cores 4
python -m src.cli_client list-nodes
python -m src.cli_client launch-pod --cpu-requirement 2
```

### Using Docker
```bash
# Build and start services
docker-compose up --build

# Use CLI client (in another terminal)
docker-compose run cli-client add-node --cpu-cores 4
docker-compose run cli-client list-nodes
docker-compose run cli-client launch-pod --cpu-requirement 2
```

## CLI Commands
- `add-node`: Add a new node to the cluster
- `list-nodes`: List all nodes and their status
- `launch-pod`: Launch a pod with specific CPU requirements

## Scheduling Algorithms
- First-Fit
- Best-Fit
- Worst-Fit

## Monitoring
- Periodic health checks
- Resource usage tracking
- Auto-scaling based on cluster load

## License
MIT License