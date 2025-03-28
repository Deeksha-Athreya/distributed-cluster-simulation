import time

class AutoScaler:
    """
    Manages automatic scaling of cluster nodes based on load
    """
    def __init__(self, cluster, min_nodes=1, max_nodes=10):
        self.cluster = cluster
        self.min_nodes = min_nodes
        self.max_nodes = max_nodes
        self.last_scaling_time = time.time()
        self.scaling_cooldown = 300  # 5 minutes between scaling operations
    
    def evaluate_cluster_load(self):
        """
        Evaluate cluster load and determine if scaling is needed
        """
        if not self.cluster.nodes:
            return {'total_nodes': 0, 'utilization': 0}
        
        total_cores = sum(node['cpu_cores'] for node in self.cluster.nodes.values())
        used_cores = total_cores - sum(node['available_cores'] for node in self.cluster.nodes.values())
        utilization = used_cores / total_cores if total_cores > 0 else 0
        
        return {
            'total_nodes': len(self.cluster.nodes),
            'utilization': utilization
        }
    
    def scale(self):
        """
        Automatically scale nodes based on cluster load
        Implements cooldown to prevent rapid scaling
        """
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_scaling_time < self.scaling_cooldown:
            return
        
        load_info = self.evaluate_cluster_load()
        
        # Scale up if utilization is high and we haven't reached max nodes
        if load_info['utilization'] > 0.75 and load_info['total_nodes'] < self.max_nodes:
            # Add a new node with standard configuration
            new_node_cores = 4  # Standard node size
            new_node_id = self.cluster.add_node(new_node_cores)
            print(f"Auto-scaled: Added new node {new_node_id} with {new_node_cores} cores")
            self.last_scaling_time = current_time
        
        # Scale down if utilization is very low and we have more than min nodes
        elif load_info['utilization'] < 0.2 and load_info['total_nodes'] > self.min_nodes:
            # Find the least utilized node to remove
            least_utilized_node = min(
                self.cluster.nodes.values(), 
                key=lambda node: node['available_cores'] / node['cpu_cores']
            )
            
            # Remove the node if it has no running pods
            if not least_utilized_node['pods']:
                del self.cluster.nodes[least_utilized_node['id']]
                print(f"Auto-scaled: Removed node {least_utilized_node['id']}")
                self.last_scaling_time = current_time