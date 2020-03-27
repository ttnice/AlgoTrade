import datetime
import oandapyV20
from oandapyV20.endpoints import trades, pricing, instruments, orders, forexlabs, accounts
from math import e
import time

class Primary:
    def __init__(self):
        self.accountID = '101-004-11969890-001'
        self.access_token = '1f4b0414fa0f618fced5a83e01db7ffc-316d266c3a8cdd3ef9e29273bbbd8bef'
        self.client = oandapyV20.API(access_token=self.access_token, environment="practice")

        self.instrument = None
        self.count = None
        self.granularity = None

        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.last_close = None
        self.last_volume = None
        self.get_prices()

    def sigmoid(self, n, rang):
        return 1/(1+e**(-rang*n + rang))

    def liste_to_evol(self, high, low, close, volume):
        self.highs.append(self.sigmoid(high/close, 1e4))
        self.lows.append(self.sigmoid(low/close, 1e4))
        self.closes.append(self.sigmoid(close/self.last_close, 1e4))
        self.volumes.append(self.sigmoid(volume/self.last_volume, 1))
        if len(self.closes) > 60:
            self.highs = self.highs[-60:]
            self.lows = self.lows[-60:]
            self.closes = self.closes[-60:]
            self.volumes = self.volumes[-60:]
            self.times = self.times[-60:]
        self.last_close = close
        self.last_volume = volume

    def get_prices(self, instrument='EUR_USD', count=65, granularity='M1'):
        self.instrument = instrument
        self.count = count
        self.granularity = granularity

        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []
        self.times = []
        return self.get_candle(instrument=instrument, count=count, granularity=granularity)

    def get_candle(self, instrument='EUR_USD', count=2, granularity='M1'):
        r = instruments.InstrumentsCandles(instrument=instrument, params=
        {
            'count': count,
            'granularity': granularity
        })
        candleprice = self.client.request(r)
        completed = False
        for count in candleprice["candles"]:
            if count['complete']:
                volume = float(count['volume'])
                high = float(count['mid']['h'])
                low = float(count['mid']['l'])
                close = float(count['mid']['c'])
                date = count['time']
                times = self.reverse_format_func(date)
                if len(self.times) == 0:
                    completed = True
                    self.times = [times]
                    self.last_close = close
                    self.last_volume = volume
                elif times != self.times[-1]:
                    completed = True
                    self.times.append(times)
                    self.liste_to_evol(high=high, low=low, close=close, volume=volume)
        return completed

    def reverse_format_func(self, date):
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:10])
        hour = int(date[11:13])
        minute = int(date[14:16])
        second = int(date[17:19])
        times = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        return times

    def spread(self, instruments='EUR_USD'):
        params = {
            "instrument": instruments,
            "period": 50
        }
        s = forexlabs.Spreads(params=params)
        r = self.client.request(s)
        spread = float(r['avg'][0][1])
        return spread

    def get_data(self):
        data = []
        for h, l, c, v in zip(self.highs, self.lows, self.closes, self.volumes):
            data.append(h)
            data.append(l)
            data.append(c)
            data.append(v)
        return data


if __name__ == '__main__':
    my_primary = Primary()
    print(my_primary.spread())

