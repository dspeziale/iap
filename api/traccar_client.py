import requests
import random

class TraccarClient:
    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.auth = (user, password)
        
    def get_positions(self):
        """
        Fetch latest positions for all devices.
        In a real scenario: requests.get(f"{self.base_url}/api/positions", auth=self.auth)
        """
        # Mock data for demonstration
        return [
            {
                "deviceId": 1,
                "latitude": 41.9028,
                "longitude": 12.4964, # Rome
                "speed": 0,
                "address": "Via Roma, 1"
            },
            {
                "deviceId": 2,
                "latitude": 45.4642,
                "longitude": 9.1900, # Milan
                "speed": 45,
                "address": "Autostrada A1"
            }
        ]
