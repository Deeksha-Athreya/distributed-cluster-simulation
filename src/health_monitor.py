import time

class HealthMonitor:
    """
    Monitors health of nodes and pods in the cluster
    """
    def __init__(self, cluster, heartbeat_timeout=60):
        self.cluster = cluster
        self.heartbeat_timeout = heartbeat_timeout
    
    def check_node_health(self):
        """
        Check health of all nodes based on their last heartbeat
        """
        current_time = time.time()
        failed_nodes = []
        
        for node_id, node in list(self.cluster.nodes.items()):
            # Check if node has missed heartbeats
            if current_time - node.get('last_heartbeat', 0) > self.heartbeat_timeout:
                # Mark node as failed
                node['status'] = 'failed'
                failed_nodes.append(node_id)
                
                # Attempt to reschedule pods from failed node
                self._reschedule_pods_from_failed_node(node)
        
        return failed_nodes
    
    def _reschedule_pods_from_failed_node(self, failed_node):
        """
        Reschedule pods from a failed node to healthy nodes
        """
        for pod_id in failed_node.get('pods', []):
            try:
                # Find a new node for the pod
                available_nodes = [
                    node for node in self.cluster.nodes.values() 
                    if node['status'] == 'healthy' and 
                    node['available_cores'] >= pod_id['cpu_requirement']
                ]
                
                if available_nodes:
                    # Select the first available node (can be improved with scheduling algorithm)
                    new_node = available_nodes[0]
                    
                    # Add pod to new node
                    new_node['pods'].append(pod_id)
                    new_node['available_cores'] -= pod_id['cpu_requirement']
            except Exception as e:
                print(f"Could not reschedule pod {pod_id}: {e}")
    
    def record_node_heartbeat(self, node_id):
        """
        Record a heartbeat for a specific node
        """
        if node_id in self.cluster.nodes:
            self.cluster.nodes[node_id]['last_heartbeat'] = time.time()
            self.cluster.nodes[node_id]['status'] = 'healthy'
            return True
        return False