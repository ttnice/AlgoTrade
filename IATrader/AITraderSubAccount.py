
import oandapyV20
from oandapyV20.endpoints import trades, pricing, instruments, orders, forexlabs, accounts


class SubAccount:
    learning_doc = 'train/learning.txt'
    def __init__(self, name, number):
        self.name = name
        self.accountID = f'101-004-11969890-00{number}'
        self.access_token = '1f4b0414fa0f618fced5a83e01db7ffc-316d266c3a8cdd3ef9e29273bbbd8bef'
        self.client = oandapyV20.API(access_token=self.access_token, environment="practice")
        self.open_id = []
        file = open(f'{self.name}.txt', 'a+')
        file.close()

    def open_trade(self, take_profit, stop_loss, actual_price, action, data_input=None, instrument='EUR_USD'):
        label = [0, 0, 0, take_profit, stop_loss]
        if action == 'BUY':
            units = 1
            label[1] = 1
        if action == 'SELL':
            units = -1
            label[2] = 1
        data = {
            "order": {
                "price": str(actual_price),
                "takeProfitOnFill": {
                    "price": str(round(actual_price*take_profit + actual_price, 5))
                },
                "stopLossOnFill": {
                    "price": str(round(actual_price*stop_loss + actual_price, 5))
                },
                "instrument": str(instrument),
                "units": str(round(units)),
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        r = orders.OrderCreate(self.accountID, data=data)
        rv = self.client.request(r)
        self.create_id(data_input, label, actual_price, action)

    def existing_id(self):
        r = trades.TradesList(self.accountID)
        rv = self.client.request(r)
        existing_id = []
        for trade in rv['trades']:
            existing_id.append(int(trade['id']))
        return existing_id

    def checker(self, actual_price):
        info_line = 4
        existing_id = self.existing_id()
        to_remove = []
        file_remove = []
        for id in self.open_id:
            if not id in existing_id:
                to_remove.append(id)
                self.open_id.remove(id)
        if len(to_remove) > 0:
            with open(f'train/{self.name}.txt') as file:
                lines = file.readlines()
                file.close()
            with open(f'train/{self.name}.txt', 'w') as file:
                for i in range(0, len(lines), info_line):
                    id = int(lines[i])
                    if id in to_remove:
                        file_remove.append(lines[i:i + info_line])
                    else:
                        file.writelines(lines[i:i + info_line])
                file.close()
            with open(self.learning_doc, 'a+') as file:
                for liste in file_remove:
                    action, price = liste[1].split('-')
                    price = float(price)
                    if action == 'BUY' and actual_price-price > 0:
                        file.writelines(liste[2:])
                    if action == 'SELL' and price-actual_price > 0:
                        file.writelines(liste[2:])
                        self.open_id = []
                file.close()

    def create_id(self, data, label, price, action):
        existing_id = self.existing_id()
        if not self.open_id == self.existing_id:
            for id in existing_id:
                if id not in self.open_id:
                    self.open_id.append(id)
                    r = trades.TradesList(self.accountID)
                    rv = self.client.request(r)
                    for trade in rv['trades']:
                        if int(trade['id']) == id:
                            file = open(f'train/{self.name}.txt', 'a+')
                            liste = []
                            liste.append(str(id)+'\n')
                            liste.append(action+'-'+str(price)+'\n')
                            liste.append(str(data)+'\n')
                            liste.append(str(label)+'\n')
                            file.writelines(liste)
                            file.close()
                            break

    def balance(self):
        r = accounts.AccountSummary(self.accountID)
        self.client.request(r)
        balance = float(r.response['account']['balance'])
        balance_available = balance - float(r.response['account']['positionValue'])
        return balance_available, balance

    def balance_per_cent(self):
        balance_available, balance = self.balance()
        return float(balance_available / balance)



