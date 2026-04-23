import requests
import os
import json

class CanvaAPIClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.canva.com/v1"
        self.access_token = None

    def authenticate(self, code, redirect_uri):
        """Exchange authorization code for access token."""
        url = f"{self.base_url}/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            return self.access_token
        else:
            raise Exception(f"Authentication failed: {response.text}")

    def list_designs(self):
        """List user designs."""
        if not self.access_token:
            raise Exception("Not authenticated")
        
        url = f"{self.base_url}/designs"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()

    def create_design_from_template(self, template_id, title):
        """Create a new design based on a brand template."""
        if not self.access_token:
            raise Exception("Not authenticated")
        
        url = f"{self.base_url}/designs"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "brand_template_id": template_id,
            "title": title
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

if __name__ == "__main__":
    # Example usage (requires environment variables)
    client_id = os.getenv("CANVA_CLIENT_ID")
    client_secret = os.getenv("CANVA_CLIENT_SECRET")
    if client_id and client_secret:
        client = CanvaAPIClient(client_id, client_secret)
        print("Canva API Client initialized.")
    else:
        print("Please set CANVA_CLIENT_ID and CANVA_CLIENT_SECRET environment variables.")
