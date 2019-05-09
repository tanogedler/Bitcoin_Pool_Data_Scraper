import os
import csv
import time
from datetime import datetime
import json
import requests
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
#import ftplib

class Pool(object):
    def __init__(self,
                    name=None,
                    apiurl=None,
                    apiparams=dict(),
                    csvfile_hashrate=None,
                    csvfile_profit=None,

                ):
        self.name = name
        self.apiurl = apiurl
        self.apiparams = apiparams
        self.csvfile_hashrate = csvfile_hashrate
        self.csvfile_profit = csvfile_profit
        self.response = ""
        self.algorithms = {}
        self.timeouts = 0
        self.failures = 0

    def __repr__(self):
        return "Pool(" + \
                "\'name\'=\'{}\', ".format(self.name) + \
                "\'apiurl\'=\'{}\', ".format(self.apiurl) + \
                "\'apiparams\'=\'{}\', ".format(self.apiparams) + \
                "\'algorithms\'=\'{}\', ".format(self.algorithms) + \
                "\'timeouts\'=\'{}\', ".format(self.timeouts) + \
                "\'failures\'=\'{}\'".format(self.failures) + \
                ")"

    def __str__(self):
        return self.__dict__

    def poll_api(self):
        sleeptime=5
        self.timeouts = 0
        r = None
        while self.timeouts < 3:
            try:
                if self.apiparams:
                    r = requests.get(url=self.apiurl, params=self.apiparams)
                else:
                    r = requests.get(url=self.apiurl)
                r.raise_for_status()
            except requests.exceptions.Timeout:
                self.timeouts += 1
                time.sleep(sleeptime)
                sleeptime += 3
                continue
            except requests.exceptions.HTTPError as err:
                self.timeouts = 404
            except requests.exceptions.RequestException as e:
                self.timeouts = 666
            break
        if self.timeouts >= 3 or r is None or r.text is None or "{" not in r.text:
            self.failures += 1
            print("Failure of some kind updating API data for {}".format(self.name))
            return False
        data = json.loads(r.text)
        if data is None or data is False:
            self.failures += 1
            print("Failure of some kind updating API data for {}".format(self.name))
            return False
        self.response = data
        print("Successfully grabbed API data for {}".format(self.name))
        return True

    def update_algorithms(self, valid_algos):
        self.algorithms = {}
        if not self.poll_api():
            return
        else:
            for key in self.response:
                if key in valid_algos:
                    self.algorithms[valid_algos[key]]=dict(
                            hashrate_=self.response[key]['hashrate'],
                            profit=self.response[key]['estimate_current'],
                            #actual24h=self.response[key]['actual_last24h'],
                            workers=self.response[key]['workers']
                            #hash_rate_=self.response[key]['hash_rate']
                        )
            print("Processed algorithm data for {}".format(self.name))
            

    def get_algorithms(self):
        return self.algorithms

    def get_name(self):
        return self.name

    def get_csvfile_hashrate(self):
        return self.csvfile_hashrate

    def get_csvfile_profit(self):
        return self.csvfile_profit

    def get_csv_string_noAlgMap(self, new_timestamp):
        new_row = [new_timestamp]
        if 'hash_rate' in self.response:
            new_row.append(str(self.response['hash_rate']))
        else:
            new_row.append('')        
        return new_row
       

    def get_csv_string_hashrate(self, new_timestamp, algo_map):
        new_row = [new_timestamp]        
        if self.algorithms:
            for i in range(len(algo_map)):
                if algo_map[i] in self.algorithms:
                    new_row.append(int(self.algorithms[algo_map[i]]['hashrate_']))
                else:
                    new_row.append('')
        return new_row

    def get_csv_string_profit(self, new_timestamp, algo_map):
        new_row = [new_timestamp]        
        if self.algorithms:
            for i in range(len(algo_map)):
                if algo_map[i] in self.algorithms:
                    new_row.append(str(self.algorithms[algo_map[i]]['profit']))
                else:
                    new_row.append('')
        return new_row

    def get_csv_string_workers(self, new_timestamp, algo_map):
        new_row = [new_timestamp]        
        if self.algorithms:
            for i in range(len(algo_map)):
                if algo_map[i] in self.algorithms:
                    new_row.append(str(self.algorithms[algo_map[i]]['workers']))
                else:
                    new_row.append('')
        return new_row

    def append_row_to_csv_hashrate(self, new_row):
        with open(self.csvfile_hashrate, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(new_row)
        print("Appended data for {p} to {f}".format(p=self.name, f=self.csvfile_hashrate))

    def append_row_to_csv_profit(self, new_row):
        with open(self.csvfile_profit, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(new_row)
        print("Appended data for {p} to {f}".format(p=self.name, f=self.csvfile_profit))


def main():
    script_home = os.path.split(os.path.abspath(__file__))[0]

    valid_algos = {
        "bitcore": "bitcore",
        "blake": "blakecoin",
        "blake2s": "blake2s",
        "blakecoin": "blakecoin",
        "blakevanilla": "blakevanilla",
        "c11": "c11",
        "cryptonight": "cryptonight",
        "daggerhashimoto": "ethash",
        "darkcoinmod": "x11",
        "decred": "decred",
        "equihash": "equihash",
        "eth": "ethash",
        "ethash": "ethash",
        "groestl": "groestl",
        "groestlcoin": "groestl",
        "hmq1725": "hmq1725",
        "hsr": "hsr",
        "jha": "jha",
        "keccak": "keccak",
        "lbry": "lbry",
        "lyra2re2": "lyra2v2",
        "lyra2rev2": "lyra2v2",
        "lyra2v2": "lyra2v2",
        "lyra2z": "lyra2z",
        "maxcoin": "keccak",
        "myrgr": "myriadgroestl",
        "myr-gr": "myriadgroestl",
        "myriadcoingroestl": "myriadgroestl",
        "myriadgroestl": "myriadgroestl",
        "neoscrypt": "neoscrypt",
        "nist5": "nist5",
        "pascal": "pascal",
        "phi": "phi",
        "poly": "polytimos",
        "polytimos": "polytimos",
        "quark": "quark",
        "quarkcoin": "quark",
        "qubit": "qubit",
        "qubitcoin": "qubit",
        "scrypt": "scrypt",
        "sha256": "sha256",
        "sib": "sib",
        "sibcoinmod": "sib",
        "sigt": "skunk",
        "skein": "skein",
        "skeincoin": "skein",
        "skunk": "skunk",
        "timetravel": "timetravel",
        "tribus": "tribus",
        "vanilla": "blakevanilla",
        "whirlpoolx": "whirlpoolx",
        "veltor": "veltor",
        "x11": "x11",
        "x11gost": "sib",
        "x11evo": "x11evo",
        "x17": "x17",
        "xevan": "xevan",
        "xmr": "cryptonight",
        "yescrypt": "yescrypt",
        "zec": "equihash",
        "zuikkis": "scrypt"
    }


    algo_map = ["bitcore", "blake2s", "blakecoin", "c11", "cryptonight", \
                "decred", "equihash", "ethash", "groestl", "hmq1725", \
                "hsr", "keccak", "lbry", "lyra2v2", "lyra2z", "m7m", \
                "myr-gr", "neoscrypt", "nist5", "pascal", "phi", \
                "polytimos", "quark", "qubit", "scrypt", "sha256", \
                "sia", "sib", "skein", "skunk", "timetravel", "tribus", \
                "whirlpoolx", "x11", "x11evo", "x11gost", "x13", "x14", \
                "x15", "x17", "xevan", "yescrypt", "yescryptR16"]


    pools = []

    # siamining
    pools.append(Pool(
            name='siamining',
            apiurl='https://siamining.com/api/v1/pool',
            csvfile_hashrate=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'siamining_hashrate.csv')
            #csvfile_profit=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'siamining_profit.csv'),
        )
    )

    # ahashpool
    pools.append(Pool(
            name='ahashpool',
            apiurl='https://www.ahashpool.com/api/status/',
            csvfile_hashrate=os.path.join(os.path.split(os.path.abspath(__file__))[0],  'csvdata', 'ahashpool_hashrate.csv'),
            csvfile_profit=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'ahashpool_profit.csv')

        )
    )

    # blazepool
    pools.append(Pool(
            name='blazepool',
            apiurl='http://api.blazepool.com/status',
            csvfile_hashrate=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'blazepool_hashrate.csv'),
            csvfile_profit=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'blazepool_profit.csv')
        )
    )

    # zpool
    pools.append(Pool(
             name='zpool',
             apiurl='http://www.zpool.ca/api/status/',
             csvfile_hashrate=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'zpool_hashrate.csv'),
             csvfile_profit=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'zpool_profit.csv')
         )
     )

    # bitminter
    pools.append(Pool(
        name='bitminter',
        apiurl='https://bitminter.com/api/pool/stats',
        csvfile_hashrate=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'bitminter_hashrate.csv'),
        #csvfile_profit=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'bitminter_profit.csv')
        )
    )
    # hashrefinery
    pools.append(Pool(
             name='hashrefinery',
             apiurl='http://pool.hashrefinery.com/api/status',
             csvfile_hashrate=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'hashrefinery_hashrate.csv'),
             csvfile_profit=os.path.join(os.path.split(os.path.abspath(__file__))[0], 'csvdata', 'hashrefinery_profit.csv')
         )
    )

    while (1) :
        new_datetime = datetime.now()
        current_timestamp = new_datetime.strftime('%x %X')
        new_timestamp = datetime.strptime(current_timestamp, '%x %X')


        for pool in pools:
            pool.update_algorithms(valid_algos)
            if len(pool.get_algorithms()) == 0:
                pool.append_row_to_csv_hashrate(pool.get_csv_string_noAlgMap(new_timestamp))

            else:
                pool.append_row_to_csv_hashrate(pool.get_csv_string_hashrate(new_timestamp, algo_map))
                pool.append_row_to_csv_profit(pool.get_csv_string_profit(new_timestamp, algo_map))

        time.sleep(10)

if __name__ == '__main__':
    main()







