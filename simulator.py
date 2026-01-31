import time
import random

class PaymentSimulator:
    def __init__(self):
        self.primary_gateway = "Stripe"
        self.secondary_gateway = "Adyen"
        self.active_route = "Stripe"
        self.status = "HEALTHY" 
    
    def get_metrics(self):
        base_success = 0.98
        latency = 200
        
        if self.status == "DEGRADED" and self.active_route == "Stripe":
            base_success = 0.65 
            latency = 1500      
            error_code = "504_GATEWAY_TIMEOUT"
        else:
            error_code = "200_OK"

        current_sr = base_success + random.uniform(-0.02, 0.02)
        current_latency = latency + random.randint(-50, 50)
        
        return {
            "timestamp": time.strftime("%H:%M:%S"),
            "active_gateway": self.active_route,
            "success_rate": round(current_sr, 2),
            "avg_latency_ms": current_latency,
            "dominant_error": error_code
        }


    def set_status(self, status):
        self.status = status

env = PaymentSimulator()