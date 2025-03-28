
import uuid
import time
import threading
from flask import Flask, request, jsonify

from .scheduling_algorithms import PodScheduler
from .auto_scaling import AutoScaler
from .resource_monitoring import ResourceMonitor
from .network_policy import NetworkPolicy
from .health_monitor import HealthMonitor

class DistributedClusterSimulation:
    """
    Main class for managing the distributed cluster simulation
    """
    def __init__(self):
        # Stores nodes in the cluster
        self.nodes = {}
        
        # Initialize components
        self.pod_scheduler = PodScheduler()
        self.auto_scaler = AutoScaler(self)
        self.resource_monitor = ResourceMonitor()
        self.network_policy = NetworkPolicy()
        self.health_monitor = HealthMonitor(self)
        
        # Start background maintenance thread
        self._start_maintenance_thread()
    
    def add_node(self, cpu_cores):
        """
        Add a new node to the cluster
        """
        node_id = str(uuid.uuid4())
        node = {
            'id': node_id,
            'cpu_cores': cpu_cores,
            'available_cores': cpu_cores,
            'pods': [],
            'last_heartbeat': time.time(),
            'status': 'healthy'
        }
        self.nodes[node_id] = node
        return node_id
    
    def launch_pod(self, cpu_requirement, scheduling_algorithm='first_fit'):
        """
        Launch a pod with specific CPU requirements
        """
        # Convert nodes to list for scheduling algorithms
        nodes = list(self.nodes.values())
        
        # Select scheduling algorithm
        if scheduling_algorithm == 'first_fit':
            selected_node = self.pod_scheduler.first_fit(nodes, cpu_requirement)
        elif scheduling_algorithm == 'best_fit':
            selected_node = self.pod_scheduler.best_fit(nodes, cpu_requirement)
        elif scheduling_algorithm == 'worst_fit':
            selected_node = self.pod_scheduler.worst_fit(nodes, cpu_requirement)
        else:
            raise ValueError("Invalid scheduling algorithm")
        
        # Validate node selection
        if not selected_node:
            raise Exception("No suitable node found for pod")
        
        # Create pod
        pod_id = str(uuid.uuid4())
        pod = {
            'id': pod_id,
            'cpu_requirement': cpu_requirement,
            'node_id': selected_node['id']
        }
        
        # Update node resources
        selected_node['pods'].append(pod)
        selected_node['available_cores'] -= cpu_requirement
        
        # Record initial resource usage
        self.resource_monitor.record_pod_usage(pod_id, cpu_requirement)
        
        return pod_id
    
    def _start_maintenance_thread(self):
        """
        Start background thread for cluster maintenance
        """
        def maintenance_task():
            while True:
                # Perform auto-scaling
                self.auto_scaler.scale()
                
                # Check node health
                failed_nodes = self.health_monitor.check_node_health()
                
                # Identify resource-intensive pods
                high_usage_pods = self.resource_monitor.identify_resource_intensive_pods()
                
                # Sleep for a while before next maintenance cycle
                time.sleep(60)
        
        maintenance_thread = threading.Thread(target=maintenance_task, daemon=True)
        maintenance_thread.start()
    
    def list_nodes(self):
        """
        List all nodes in the cluster
        """
        return [
            {
                'id': node['id'], 
                'cpu_cores': node['cpu_cores'], 
                'available_cores': node['available_cores'], 
                'status': node['status'],
                'pods': [pod['id'] for pod in node['pods']]
            } 
            for node in self.nodes.values()
        ]

# Flask API Setup
app = Flask(__name__)
cluster = DistributedClusterSimulation()

@app.route('/nodes', methods=['POST'])
def add_node():
    """
    Endpoint to add a new node to the cluster
    """
    data = request.json
    node_id = cluster.add_node(data['cpu_cores'])
    return jsonify({'node_id': node_id, 'status': 'Node added successfully'})

@app.route('/nodes', methods=['GET'])
def list_nodes():
    """
    Endpoint to list all nodes
    """
    return jsonify(cluster.list_nodes())

@app.route('/pods', methods=['POST'])
def launch_pod():
    """
    Endpoint to launch a new pod
    """
    data = request.json
    try:
        pod_id = cluster.launch_pod(
            data['cpu_requirement'], 
            data.get('scheduling_algorithm', 'first_fit')
        )
        return jsonify({'pod_id': pod_id, 'status': 'Pod launched successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/heartbeat/<node_id>', methods=['POST'])
def node_heartbeat(node_id):
    """
    Endpoint for node heartbeat
    """
    if cluster.health_monitor.record_node_heartbeat(node_id):
        return jsonify({'status': 'Heartbeat received'})
    return jsonify({'error': 'Node not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)