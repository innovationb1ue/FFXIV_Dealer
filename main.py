import requests
from settings import SERVERS, ITEMS, LOCAL_SERVER
import numpy as np
import json
import os
import time

MARKET_BOARD_LISTING_URL = 'https://universalis.app/api/{}/{}'
MARKET_SALES_URL = 'https://universalis.app/api/history/{}/{}'

ITEM_INFO_URL = 'https://cafemaker.wakingsands.com/item/{}'


class FFXIVDealer:
    def __init__(self):
        self.s = requests.Session()
        if os.path.exists('./item.json'):
            with open('./item.json', 'r') as f:
                self.item_info = json.load(f)
        else:
            self.item_info = {}

    def get_board_list_info(self, world_id: str, item_id: str) -> dict[str]:
        url = MARKET_BOARD_LISTING_URL.format(world_id, item_id)
        resp = self.s.get(url, timeout=5)
        res_json = resp.json()
        listings = res_json['listings']
        world_name = res_json['worldName']
        min_price_nq = res_json['minPriceNQ']
        max_price_nq = res_json['maxPriceNQ']
        min_price_hq = res_json['minPriceHQ']
        max_price_hq = res_json['maxPriceHQ']
        average_price_hq = res_json['averagePriceHQ']
        average_price_nq = res_json['averagePriceNQ']
        prices = [i['pricePerUnit'] for i in listings]

        if not self.item_info.get(item_id):
            resp = self.s.get(ITEM_INFO_URL.format(item_id), timeout=5)
            item_info_res_json = resp.json()
            self.item_info[item_id] = {}
            self.item_info[item_id]['item_name'] = item_info_res_json['Singular_chs']
            with open('./item.json', 'w') as f:
                json.dump(self.item_info, f)

        return {'prices': prices,
                "world_name": world_name,
                'min_price_nq': min_price_nq,
                'max_price_nq': max_price_nq,
                'min_price_hq': min_price_hq,
                'max_price_hq': max_price_hq,
                'average_price_hq': average_price_hq,
                'average_price_nq': average_price_nq,
                'item_name': self.item_info[item_id]['item_name']
                }

    def get_market_history(self, world_id: str, item_id: str):
        url = MARKET_SALES_URL.format(world_id, item_id)
        resp = self.s.get(url, timeout=5)
        res_json = resp.json()

    def query_all(self):
        for item_id in ITEMS:
            # get local server price
            local_sever_item_info = self.get_board_list_info(LOCAL_SERVER[0], item_id)
            local_price = local_sever_item_info['average_price_hq']
            local_server_name = local_sever_item_info['world_name']
            # target server prices
            average_prices_nq = []
            average_prices_hq = []
            server_names = []
            for server in SERVERS:
                item_info = self.get_board_list_info(server, item_id)
                average_prices_nq.append(item_info['average_price_nq'])
                average_prices_hq.append(item_info['average_price_hq'])
                server_names.append(item_info['world_name'])
            # analysis
            idx = np.argmin(average_prices_hq)
            gap = local_price - average_prices_hq[idx]
            if gap > 10000:
                print(f"{self.item_info[item_id]['item_name']}, Buy at {server_names[idx]}, Sell at {local_server_name}, Expect revenue: {gap}")
            time.sleep(2)


if __name__ == '__main__':
    e = FFXIVDealer()
    e.query_all()



