from sp_api.base import Marketplaces
from sp_api.api import Finances

from amazon.auth import get_credentials


class FinancesClient:

    def __init__(self):
        creds = get_credentials()

        self.client = Finances(
            credentials={
                "refresh_token": creds["refresh_token"],
                "lwa_app_id": creds["client_id"],
                "lwa_client_secret": creds["client_secret"],
            },
            marketplace=Marketplaces.IN,
        )

    def get_order_financial_events(self, amazon_order_id):
        return self.client.get_financial_events_for_order(
            amazon_order_id
        )