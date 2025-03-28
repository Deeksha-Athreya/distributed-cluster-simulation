import click
import requests

BASE_URL = 'http://localhost:5000'

@click.group()
def cli():
    """Distributed Cluster Simulation CLI"""
    pass

@cli.command()
@click.option('--cpu-cores', type=int, required=True, help='Number of CPU cores for the node')
def add_node(cpu_cores):
    """Add a new node to the cluster"""
    response = requests.post(f'{BASE_URL}/nodes', json={'cpu_cores': cpu_cores})
    click.echo(response.json())

@cli.command()
def list_nodes():
    """List all nodes in the cluster"""
    response = requests.get(f'{BASE_URL}/nodes')
    nodes = response.json()
    
    click.echo("Cluster Nodes:")
    for node in nodes:
        click.echo(f"Node ID: {node['id']}")
        click.echo(f"  Total CPU Cores: {node['cpu_cores']}")
        click.echo(f"  Available Cores: {node['available_cores']}")
        click.echo(f"  Status: {node['status']}")
        click.echo(f"  Pods: {node['pods']}")
        click.echo("---")

@cli.command()
@click.option('--cpu-requirement', type=int, required=True, help='CPU cores required for the pod')
@click.option('--scheduling-algorithm', type=click.Choice(['first_fit', 'best_fit', 'worst_fit']), default='first_fit', help='Scheduling algorithm to use')
def launch_pod(cpu_requirement, scheduling_algorithm):
    """Launch a new pod in the cluster"""
    response = requests.post(f'{BASE_URL}/pods', json={
        'cpu_requirement': cpu_requirement,
        'scheduling_algorithm': scheduling_algorithm
    })
    click.echo(response.json())

if __name__ == '__main__':
    cli()