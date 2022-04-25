import datetime

import requests
from user_settings import TARGET_SERVERS, TARGET_ITEMS, LOCAL_SERVER
import numpy as np
import json
import os
import time
from apis import *

import pandas as pd

VALUABLE_THRESHOLD = 10000

DF_COLUMNS = ['ItemName', 'LocalPrice', 'TargetPrice', "ExpectRevenue", 'BuyAt', 'SellAt', "LastUpdate"]


class FFXIVDealer:
    def __init__(self):
        self.s = requests.Session()
        if os.path.exists('./item.json'):
            with open('./item.json', 'r') as f:
                self.item_info = json.load(f)
        else:
            self.item_info = {}

    def get_board_list_info(self, world_id: str, item_id: str) -> dict[str]:
        # load board prices
        url = MARKET_BOARD_LISTING_URL.format(world_id, item_id)
        resp = self.s.get(url, timeout=5)
        res_json = resp.json()
        # save fields
        listings = res_json['listings']
        world_name = res_json['worldName']
        min_price_nq = res_json['minPriceNQ']
        max_price_nq = res_json['maxPriceNQ']
        min_price_hq = res_json['minPriceHQ']
        max_price_hq = res_json['maxPriceHQ']
        average_price_hq = res_json['averagePriceHQ']
        average_price_nq = res_json['averagePriceNQ']
        prices = [i['pricePerUnit'] for i in listings]
        regular_sale_velocity = res_json['regularSaleVelocity']

        # get chinese name for item
        if not self.item_info.get(item_id):
            resp = self.s.get(ITEM_INFO_URL.format(item_id), timeout=5)
            item_info_res_json = resp.json()
            self.item_info[item_id] = {}
            self.item_info[item_id]['item_name'] = item_info_res_json['Singular_chs']
            # update cache json
            with open('./item.json', 'w') as f:
                json.dump(self.item_info, f)
        item_name = self.item_info[item_id]['item_name']

        return {'prices': prices,
                "world_name": world_name,
                'min_price_nq': min_price_nq,
                'max_price_nq': max_price_nq,
                'min_price_hq': min_price_hq,
                'max_price_hq': max_price_hq,
                'average_price_hq': average_price_hq,
                'average_price_nq': average_price_nq,
                'item_name': item_name,
                'regular_sale_velocity': regular_sale_velocity
                }

    def get_market_history(self, world_id: str, item_id: str) -> dict:
        """
        the universalis api return json like below
        {
          "itemID": 34691,
          "worldID": 1171,
          "lastUploadTime": 1649426190119,
          "entries": [
            {
              "hq": true,
              "pricePerUnit": 73700,
              "quantity": 1,
              "timestamp": 1649426055
            }, ...
            ],
          "regularSaleVelocity": 4.571429,
          "nqSaleVelocity": 0,
          "hqSaleVelocity": 4.571429,
          "worldName": "神拳痕"
        }
        """
        url = MARKET_SALES_URL.format(world_id, item_id)
        resp = self.s.get(url, timeout=5)
        res_json = resp.json()
        last_upload_time = datetime.datetime.fromtimestamp(res_json['lastUploadTime']/1000)
        sale_velocity = res_json.get("regularSaleVelocity")
        histories = res_json.get("entries")
        return {"last_upload_time": last_upload_time, "histories": histories, "sale_velocity": sale_velocity}

    def query_all(self):
        """
        Main function
        Query prices at target buying servers and compare to the prices at local server
        Report if the goods are valuable
        :return:
        :rtype:
        """
        # get all available items
        # item_list = self.s.get(MARKET_ALL_ITEMS_ID_URL, timeout=5).json()[::-1]
        # get fixed items only
        item_list = TARGET_ITEMS
        df = pd.DataFrame(columns=DF_COLUMNS)
        # loop for target selling items
        for item_id in item_list:
            # get local server price
            local_sever_item_info = self.get_board_list_info(LOCAL_SERVER[0], item_id)
            local_server_histories = self.get_market_history(LOCAL_SERVER[0], item_id)
            local_price_hq = local_sever_item_info['min_price_hq']
            local_price_nq = local_sever_item_info['min_price_nq']
            local_server_name = local_sever_item_info['world_name']
            local_sale_velocity = local_server_histories['sale_velocity']
            # target server prices
            items = []
            lowest_price_nq = []
            lowest_price_hq = []
            server_names = []
            # TARGET_SERVERS is a 2d array
            for server_list in TARGET_SERVERS:
                for server in server_list:
                    item_info = self.get_board_list_info(server, item_id)
                    item_history = self.get_market_history(server, item_id)
                    item_last_update = item_history.get("last_upload_time").strftime('%Y-%m-%d %H:%m:%S')
                    item_info['item_last_update'] = item_last_update
                    items.append(item_info)
                    lowest_price_hq.append(item_info['min_price_hq'])
                    lowest_price_nq.append(item_info['min_price_nq'])
                    server_names.append(item_info['world_name'])
            # analysis & report
            idx_hq = np.argmin(lowest_price_hq)
            idx_nq = np.argmin(lowest_price_nq)
            target_price_hq = items[idx_hq]['min_price_hq']
            target_price_nq = items[idx_nq]['min_price_nq']
            gap_hq = local_price_hq - target_price_hq
            gap_nq = local_price_nq - target_price_nq
            if gap_hq > VALUABLE_THRESHOLD:
                print(f"{self.item_info[item_id]['item_name']}★, Buy at {server_names[idx_hq]},"
                      f" Sell at {local_server_name},"
                      f" Expect revenue: {gap_hq}, Sale velocity: {local_sale_velocity}, "
                      f"last update: {items[idx_hq]['item_last_update']}")
                # DF_COLUMNS = ['ItemName', 'LocalPrice', 'TargetPrice', 'BuyAt', 'SellAt', "LastUpdate"]
                item_df = pd.DataFrame([[f"{self.item_info[item_id]['item_name']}★",
                                         local_price_hq, target_price_hq, gap_hq,
                                        server_names[idx_hq], local_server_name,
                                        items[idx_hq]['item_last_update']]], columns=DF_COLUMNS)
                df = pd.concat([df, item_df])
            if gap_nq > VALUABLE_THRESHOLD:
                print(f"{self.item_info[item_id]['item_name']}, Buy at {server_names[idx_nq]}, Sell at {local_server_name},"
                      f" Expect revenue: {gap_nq}, Sale velocity: {local_sale_velocity}, "
                      f"last update: {items[idx_nq]['item_last_update']}")
                item_df = pd.DataFrame([[f"{self.item_info[item_id]['item_name']}★",
                                         local_price_nq, target_price_nq, gap_nq,
                                        server_names[idx_nq], local_server_name,
                                        items[idx_hq]['item_last_update']]], columns=DF_COLUMNS)
                df = pd.concat([df, item_df])
            else:
                print(f"{self.item_info[item_id]['item_name']}, not valuable")
        # save result to excel
        cur_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if not os.path.exists('./excel_results/'):
            os.mkdir('./excel_results/')
        df.to_excel(f"./excel_results/{cur_time}.xlsx", index=False)


if __name__ == '__main__':
    e = FFXIVDealer()
    e.query_all()



