import requests
from settings import SERVERS, ITEMS
import numpy as np

MARKET_BOARD_LISTING_URL = 'https://universalis.app/api/{}/{}'


class FFXIVDealer:
    def __init__(self):
        self.s = requests.Session()

    def get_item(self, world_id: str, item_id: str) -> dict[str]:
        url = MARKET_BOARD_LISTING_URL.format(world_id, item_id)
        resp = self.s.get(url, timeout=5)
        res_json = resp.json()
        listings = res_json['listings']
        world_name = res_json['worldName']
        min_price_nq = res_json['minPriceNQ']
        max_price_nq = res_json['maxPriceNQ']
        min_price_hq = res_json['minPriceHQ']
        max_price_hq = res_json['maxPriceHQ']
        prices = [i['pricePerUnit'] for i in listings]
        return {'prices': prices, "world_name": world_name,
                'min_price_nq': min_price_nq,
                'max_price_nq': max_price_nq,
                'min_price_hq': min_price_hq,
                'max_price_hq': max_price_hq
                }

    def query_all(self):
        for item_id in ITEMS:
            min_prices_hq = []
            max_prices_hq = []
            server_names = []
            for server in SERVERS:
                item_info = self.get_item(server, item_id)
                min_prices_hq.append(item_info['min_price_hq'])
                max_prices_hq.append(item_info['max_price_hq'])
                server_names.append(item_info['world_name'])
            idx = np.argmax(max_prices_hq)
            idx1 = np.argmin(min_prices_hq)
            gap = max_prices_hq[idx] - min_prices_hq[idx1]
            if gap > 20000:
                print(f"Buy at {server_names[idx1]}, Sell at {server_names[idx]}, Expect revenue: {gap}")


if __name__ == '__main__':
    e = FFXIVDealer()
    e.query_all()



