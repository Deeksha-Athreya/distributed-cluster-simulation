class NetworkPolicy:
    """
    Manages network communication policies between pods
    """
    def __init__(self):
        # Allows defining communication rules between pods and nodes
        self.allowed_communications = {}
        self.default_policy = 'deny'  # Default to deny
    
    def add_network_rule(self, source, destination, allowed=True):
        """
        Add a network communication rule
        """
        if source not in self.allowed_communications:
            self.allowed_communications[source] = {}
        
        self.allowed_communications[source][destination] = allowed
    
    def can_communicate(self, source, destination):
        """
        Check if communication is allowed between source and destination
        """
        # If no specific rule, fall back to default policy
        if source in self.allowed_communications:
            if destination in self.allowed_communications[source]:
                return self.allowed_communications[source][destination]
        
        return self.default_policy == 'allow'
    
    def simulate_pod_communication(self, source_pod, destination_pod):
        """
        Simulate communication between pods
        """
        if self.can_communicate(source_pod, destination_pod):
            return {
                'status': 'allowed',
                'message': f'Communication from {source_pod} to {destination_pod} is permitted'
            }
        else:
            return {
                'status': 'denied',
                'message': f'Communication from {source_pod} to {destination_pod} is blocked'
            }