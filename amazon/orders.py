from datetime import datetime, timedelta, timezone

from sp_api.base import Marketplaces
from sp_api.api import Orders

from amazon.auth import get_credentials


class OrdersClient:

    def __init__(self):
        creds = get_credentials()

        self.client = Orders(
            credentials={
                "refresh_token": creds["refresh_token"],
                "lwa_app_id": creds["client_id"],
                "lwa_client_secret": creds["client_secret"],
            },
            marketplace=Marketplaces.IN,
        )

    def get_recent_orders(self, days=30):
        created_after = (
            datetime.now(timezone.utc) - timedelta(days=days)
        ).strftime("%Y-%m-%dT%H:%M:%SZ")

        print(created_after)

        return self.client.get_orders(
            CreatedAfter=created_after
        )

    def get_order_items(self, amazon_order_id):
        return self.client.get_order_items(amazon_order_id)