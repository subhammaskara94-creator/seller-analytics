from sp_api.base import Marketplaces
from sp_api.api import Sellers

from amazon.auth import get_credentials


class AmazonClient:

    def __init__(self):
        creds = get_credentials()

        self.sellers = Sellers(
            credentials={
                "refresh_token": creds["refresh_token"],
                "lwa_app_id": creds["client_id"],
                "lwa_client_secret": creds["client_secret"],
            },
            marketplace=Marketplaces.IN,
        )

    def get_marketplaces(self):
        return self.sellers.get_marketplace_participation()