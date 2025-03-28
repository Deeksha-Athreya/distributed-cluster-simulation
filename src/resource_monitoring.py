import time

class ResourceMonitor:
    """
    Monitors and tracks resource usage for pods in the cluster
    """
    def __init__(self):
        self.pod_usage_history = {}
    
    def record_pod_usage(self, pod_id, cpu_usage, memory_usage=None):
        """
        Record resource usage for a specific pod
        """
        if pod_id not in self.pod_usage_history:
            self.pod_usage_history[pod_id] = []
        
        usage_record = {
            'timestamp': time.time(),
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage
        }
        
        self.pod_usage_history[pod_id].append(usage_record)
        
        # Keep only last 10 usage records
        if len(self.pod_usage_history[pod_id]) > 10:
            self.pod_usage_history[pod_id] = self.pod_usage_history[pod_id][-10:]
    
    def get_pod_usage_summary(self, pod_id):
        """
        Get usage summary for a specific pod
        """
        if pod_id not in self.pod_usage_history:
            return None
        
        history = self.pod_usage_history[pod_id]
        
        if not history:
            return None
        
        return {
            'average_cpu_usage': sum(record['cpu_usage'] for record in history) / len(history),
            'peak_cpu_usage': max(record['cpu_usage'] for record in history),
            'usage_records': history
        }
    
    def identify_resource_intensive_pods(self, threshold=0.8):
        """
        Identify pods with high resource utilization
        """
        high_usage_pods = []
        
        for pod_id, history in self.pod_usage_history.items():
            if history:
                avg_usage = sum(record['cpu_usage'] for record in history) / len(history)
                if avg_usage > threshold:
                    high_usage_pods.append({
                        'pod_id': pod_id,
                        'average_usage': avg_usage
                    })
        
        return sorted(high_usage_pods, key=lambda x: x['average_usage'], reverse=True)