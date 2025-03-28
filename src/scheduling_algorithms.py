class PodScheduler:
    """
    Implements multiple scheduling algorithms for pod placement
    """
    @staticmethod
    def first_fit(nodes, cpu_requirement):
        """
        First-Fit scheduling algorithm
        Selects the first node that can accommodate the pod
        """
        for node in nodes:
            if node['available_cores'] >= cpu_requirement:
                return node
        return None

    @staticmethod
    def best_fit(nodes, cpu_requirement):
        """
        Best-Fit scheduling algorithm
        Selects the node with the least remaining cores after placement
        """
        best_node = None
        min_remaining = float('inf')
        
        for node in nodes:
            if node['available_cores'] >= cpu_requirement:
                remaining = node['available_cores'] - cpu_requirement
                if remaining < min_remaining:
                    min_remaining = remaining
                    best_node = node
        
        return best_node

    @staticmethod
    def worst_fit(nodes, cpu_requirement):
        """
        Worst-Fit scheduling algorithm
        Selects the node with the most remaining cores after placement
        """
        worst_node = None
        max_remaining = -1
        
        for node in nodes:
            if node['available_cores'] >= cpu_requirement:
                remaining = node['available_cores'] - cpu_requirement
                if remaining > max_remaining:
                    max_remaining = remaining
                    worst_node = node
        
        return worst_node