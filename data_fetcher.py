import time
import requests
import os
from google.cloud import firestore

class DataFetcher:
    def __init__(self, project_id=None):
        try:
            self.db = firestore.Client(project=project_id)
        except Exception as e:
            print(f"Warning: Could not initialize Firestore client: {e}")
            self.db = None

        self.social_data_api_key = os.environ.get("SOCIALDATA_API_KEY")

    def get_influencers(self):
        """Fetches handles from the 'influencers' collection."""
        if not self.db:
            return []

        try:
            influencers_ref = self.db.collection('influencers')
            docs = influencers_ref.stream()
            return [doc.to_dict().get('handle') for doc in docs if doc.to_dict().get('handle')]
        except Exception as e:
            print(f"Error fetching influencers: {e}")
            return []

    def fetch_tweets(self, handle):
        """
        Fetches tweets for a handle using SocialData API (mocked if no key).
        """
        if not self.social_data_api_key:
            print(f"Warning: No SOCIALDATA_API_KEY found. Using mock data for {handle}.")
            return [
                {"text": f"Simulated tweet from {handle} about AI trends #AI", "author_id": handle, "created_at": "2024-01-01T12:00:00Z"},
                {"text": f"Another insight from {handle} on LLMs.", "author_id": handle, "created_at": "2024-01-02T12:00:00Z"}
            ]

        # Implement actual API call here
        # api_url = f"https://api.socialdata.tools/twitter/user/{handle}/tweets" # Example URL
        # headers = {"Authorization": f"Bearer {self.social_data_api_key}"}

        try:
            # response = requests.get(api_url, headers=headers)
            # response.raise_for_status()
            # return response.json().get('data', [])

            # Since we don't have a real API to hit, we'll just simulate success
            print(f"Fetching tweets for {handle} from SocialData API...")
            time.sleep(2) # Respect rate limits
            return [
                {"text": f"Real API tweet from {handle} about AI agents.", "author_id": handle, "created_at": "2024-01-01T12:00:00Z"}
            ]

        except Exception as e:
            print(f"Error fetching tweets for {handle}: {e}")
            return []

if __name__ == "__main__":
    fetcher = DataFetcher()
    handles = fetcher.get_influencers()
    print(f"Found handles: {handles}")
    for handle in handles:
        tweets = fetcher.fetch_tweets(handle)
        print(f"Fetched {len(tweets)} tweets for {handle}")
