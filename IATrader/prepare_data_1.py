from zipfile import ZipFile
import csv
import pandas as pd
import numpy as np
import timeit
import pickle

def unzip():
    data = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909']
    for date in data:
        with ZipFile(f'price/zip/HISTDATA_COM_MT_EURUSD_M120{date}.zip', 'r') as zipObj:
           # Extract all the contents of zip file in different directory
           listOfFileNames = zipObj.namelist()
           for fileName in listOfFileNames:
               if fileName.endswith('.csv'):
                   zipObj.extract(fileName, 'price/unzip/csv')
               elif fileName.endswith('.txt'):
                   zipObj.extract(fileName, 'price/unzip/txt')
               else:
                   zipObj.extract(fileName, 'price/unzip/autre')

def group_csv():
    data = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '1901', '1902', '1903', '1904', '1905', '1906', '1907', '1908', '1909']
    list = []
    index = 0
    for date in data:
        with open(f'price/unzip/csv/DAT_MT_EURUSD_M1_20{date}.csv', 'rt')as f:
            for row in csv.reader(f):
                list.append(row[:-1]+[index])
                index += 1

    with open('price/data.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Index'])

        for candle in list:
            writer.writerow(candle)

def csv_to_pd():
    liste = []
    last_close = None
    with open('price/data.csv', 'rt') as f:
        for i, row in enumerate(csv.reader(f)):
            if i > 0:
                row[3] = float(row[3])
                row[4] = float(row[4])
                row[5] = float(row[5])
                if last_close == None:
                    last_close = row[5]
                row.append(row[3]/row[5])
                row.append(row[4]/row[5])
                row.append(row[5]/last_close)
                last_close = row[5]

                liste.append(row)

    liste = np.array(liste)
    df = pd.DataFrame(liste, columns=['Date','Time','Open','High','Low','Close','Index', 'Ehigh', 'Elow', 'Eclose'])

    df.to_csv('price/finaldata.csv', sep='\t')

    # pickle_out = open("price/data.pickle", "wb")
    # pickle.dump(df, pickle_out)
    # pickle_out.close()

    # df.to_pickle('price/data.pkl')
    print(df.head())


def get_pd():
    df = pd.read_csv('price/finaldata.csv', sep='\t', dtype={'Date': str,'Time': str,'Open': float,'High': float,'Low': float,'Close': float,'Index': float, 'Ehigh': float, 'Elow': float, 'Eclose': float})

    # pickle_in = open("price/data.pickle", "rb")
    # df = pickle.load(pickle_in)

    # df = pd.read_pickle('price/data.pkl')
    print(len(df))
    print(type(df.loc[5_000, 'Index']))
    print(df.loc[range(5_000, 5_010), ['Index', 'Close']].values)


if __name__ == '__main__':
    get_pd()
