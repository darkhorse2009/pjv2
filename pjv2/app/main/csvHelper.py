# -*- coding:utf-8 -*-
import csv
from collections import Counter, namedtuple
import time
# from . import SQLHelper

# FUNDING = '../upload/csv/data0607.csv'
# def read_funding_data(path):
#     with open(path, 'rU') as data:
#         reader = csv.DictReader(data)
#         for row in reader:
#             yield row
#
# class FundingReader(object):
#     def __init__(self, path):
#         self.path       = path
#         self._length    = None
#         self._counter   = None
#
#     def __iter__(self):
#         self._length    = 0
#         self._counter   = Counter()
#         with open(self.path, 'rU') as data:
#             reader = csv.DictReader(data)
#             for row in reader:
#                 self._length += 1
#                 self._counter[row['company']] += 1
#                 yield row
#     def __len__(self):
#         if self._length is None:
#             for row in self: continue
#         return self._length
#     @property
#     def counter(self):
#         if self._counter is None:
#             for row in self: continue
#         return self._counter
#     @property
#     def companies(self):
#         return self.counter.keys()
#
#     def reset(self):
#         self._length = None
#         self._counter = None

path = '../upload/csv/signalDetail1437352059239.csv'
def benchmark_namedtuples(path):
    # Record = namedtuple('Record', ('permalink','company','numEmps','category','city','state','fundedDate','raisedAmt','raisedCurrency','round'))
    Record = namedtuple('Record', ('start','userNM','buildingNM','province','city','area','netNM','company','center','taskID','IMEI','IMSI','phone','rbnet','lon','lat'
        ,'province1','city1','district','street','address','city2','btsNum','btsNM','cellNum','freNum','MCC','MNC','CI','PCI','TAC','RSRP','RSRQ'
        ,'RSSI','RSSNR','CQI','city3','BSC','btsNM1','btsNum1','cellNum1','SID','NID','CID','G3RX','G3EcIo','G3SNR','G2RX','G2EcIo','GSMCELLID'
        ,'GSMLAC','GSMRX'))
    print(Record)
    # keys = ['start','userNM','buildingNM','province','city','area','netNM','company','center','taskID','IMEI','IMSI','phone','rbnet','lon','lat'
    #     ,'province1','city1','district','street','address','city2','btsNum','btsNM','cellNum','freNum','MCC','MNC','CI','PCI','TAC','RSRP','RSRQ'
    #     ,'RSSI','RSSNR','CQI','city3','BSC','btsNM1','btsNum1','cellNum1','SID','NID','CID','3GRX','3GEcIo','3GSNR','2GRX','2GEcIo','GSMCELLID'
    #     ,'GSMLAC','GSMRX']
    records = []
    with open(path, 'rU') as data:
        reader = csv.reader(data)
        sqlCreate = "create table signalData07 (id int not null auto_increment, %s)" \
                        % ('start date,userNM varchar(32),buildingNM varchar(128),province varchar(16),city varchar(32),'
                           'area varchar(32),netNM varchar(32),company varchar(32), center varchar(32),taskID varchar(32),'
                           'IMEI varchar(32),IMSI varchar(32),phone varchar(32),rbnet varchar(32),lon varchar(32),lat varchar(32),'
                           'province1 varchar(32),city1 varchar(32),district varchar(32),street varchar(32),address varchar(32),'
                           'city2 varchar(32),btsNum varchar(32),btsNM varchar(32),cellNum varchar(32),freNum varchar(32),'
                           'MCC varchar(32),MNC varchar(32),CI varchar(32),PCI varchar(32),TAC varchar(32),RSRP varchar(32),'
                           'RSRQ varchar(32),RSSI varchar(32),RSSNR varchar(32),CQI float,city3 varchar(32),BSC varchar(32),'
                           'btsNM1 varchar(32),btsNum1 varchar(32),cellNum1 varchar(32),SID varchar(32),NID varchar(32),'
                           'CID varchar(32),G3RX varchar(32),G3EcIo varchar(32),G3SNR varchar(32),G2RX varchar(32),G2EcIo varchar(32),'
                           'GSMCELLID varchar(32),GSMLAC varchar(32),GSMRX varchar(32),remark varchar(32), primary key(id)')
        print(sqlCreate)
        # for row in reader:
        #     yield tuple(row)
            # print(row.company)

            # tmp = "insert into tablename('start','userNM','buildingNM','province','city','area','netNM','company','center','taskID','IMEI','IMSI','phone','rbnet','lon','lat'" \
            #       ",'province1','city1','district','street','address','city2','btsNum','btsNM','cellNum','freNum','MCC','MNC','CI','PCI','TAC','RSRP','RSRQ'" \
            #       ",'RSSI','RSSNR','CQI','city3','BSC','btsNM1','btsNum1','cellNum1','SID','NID','CID','G3RX','G3EcIo','G3SNR','G2RX','G2EcIo','GSMCELLID'" \
            #       ",'GSMLAC','GSMRX') values('%s','%s')" \
            #       %(row.start,row.userNM,row.buildingNM,row.province,row.city,row.area,row.netNM,row.company,row.center,row.taskID,row.IMEI,row.IMSI,row.phone
            #         ,row.rbnet,row.lon,row.lat,row.province1,row.city1,row.district,row.street,row.address,row.city2,row.btsNum,row.btsNM,row.cellNum,row.freNum
            #         ,row.MCC,row.MNC,row.CI,row.PCI,row.TAC,row.RSRP,row.RSRQ,row.RSSI,row.RSSNR,row.CQI,row.city3,row.BSC,row.btsNM1,row.btsNum1,row.cellNum1
            #         ,row.SID,row.NID,row.CID,row.G3RX,row.G3EcIo,row.G3SNR,row.G2RX,row.G2EcIo,row.GSMCELLID,row.GSMLAC,row.GSMRX)
            # tmp = "insert into " \
            #       "signalData" \
            #       "(" \
            #       "start,userNM,buildingNM,province,city,area,netNM,company,center,taskID,IMEI,IMSI,phone,rbnet,lon,lat,province1,city1," \
            #       "district,street,address,city2,btsNum,btsNM,cellNum,freNum,MCC,MNC,CI,PCI,TAC,RSRP,RSRQ,RSSI,RSSNR,CQI,city3,BSC,btsNM1," \
            #       "btsNum1,cellNum1,SID,NID,CID,G3RX,G3EcIo,G3SNR,G2RX,G2EcIo,GSMCELLID,GSMLAC,GSMRX" \
            #       ") values(" \
            #       "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
            #       ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
            #       ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
            #       ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
            #       ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
            #       %(row.start,row.userNM,row.buildingNM,row.province,row.city,row.area,row.netNM,row.company,row.center,row.taskID,row.IMEI,row.IMSI,row.phone
            #         ,row.rbnet,row.lon,row.lat,row.province1,row.city1,row.district,row.street,row.address,row.city2,row.btsNum,row.btsNM,row.cellNum,row.freNum
            #         ,row.MCC,row.MNC,row.CI,row.PCI,row.TAC,row.RSRP,row.RSRQ,row.RSSI,row.RSSNR,row.CQI,row.city3,row.BSC,row.btsNM1,row.btsNum1,row.cellNum1
            #         ,row.SID,row.NID,row.CID,row.G3RX,row.G3EcIo,row.G3SNR,row.G2RX,row.G2EcIo,row.GSMCELLID,row.GSMLAC,row.GSMRX)

            # records.append(tuple(row))
            # print(row[0])
    # print(records)

sql = "create table buildingres (id int not null auto_increment, %s)" \
                        % ('city varchar(32),buildingNM varchar(128), company varchar(32), center varchar(32),lon varchar(32),lat varchar(32),'
                           'remark varchar(32), samples varchar(32), rsrp115 varchar(32),rsrp115and95 varchar(32),rsrp95 varchar(32), primary key(id)')




if __name__ == "__main__":
    # reader = FundingReader(FUNDING)
    # print(len(reader),':',reader.companies)
    start   = time.time()
    print(start)
    sqlCreate = "create table signalData07 (id int not null auto_increment, %s)" \
                        % ('start date,userNM varchar(32),buildingNM varchar(128),province varchar(16),city varchar(32),'
                           'area varchar(32),netNM varchar(32),company varchar(32), center varchar(32),taskID varchar(32),'
                           'IMEI varchar(32),IMSI varchar(32),phone varchar(32),rbnet varchar(32),lon varchar(32),lat varchar(32),'
                           'province1 varchar(32),city1 varchar(32),district varchar(32),street varchar(32),address varchar(32),'
                           'city2 varchar(32),btsNum varchar(32),btsNM varchar(32),cellNum varchar(32),freNum varchar(32),'
                           'MCC varchar(32),MNC varchar(32),CI varchar(32),PCI varchar(32),TAC varchar(32),RSRP varchar(32),'
                           'RSRQ varchar(32),RSSI varchar(32),RSSNR varchar(32),CQI float,city3 varchar(32),BSC varchar(32),'
                           'btsNM1 varchar(32),btsNum1 varchar(32),cellNum1 varchar(32),SID varchar(32),NID varchar(32),'
                           'CID varchar(32),G3RX varchar(32),G3EcIo varchar(32),G3SNR varchar(32),G2RX varchar(32),G2EcIo varchar(32),'
                           'GSMCELLID varchar(32),GSMLAC varchar(32),GSMRX varchar(32),remark varchar(32), primary key(id)')
    print(sqlCreate)
    sql = "insert into signalData (" \
          "start,userNM,buildingNM,province,city,area,netNM,company,center,taskID,IMEI,IMSI,phone,rbnet,lon,lat,province1,city1," \
          "district,street,address,city2,btsNum,btsNM,cellNum,freNum,MCC,MNC,CI,PCI,TAC,RSRP,RSRQ,RSSI,RSSNR,CQI,city3,BSC,btsNM1," \
          "btsNum1,cellNum1,SID,NID,CID,G3RX,G3EcIo,G3SNR,G2RX,G2EcIo,GSMCELLID,GSMLAC,GSMRX,remark" \
          ") values(" \
          "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
          ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
          ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
          ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
          ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"


    # benchmark_namedtuples(path)
    # for row in data:
    #     for i in row:
    #         print(i)
    finit   = time.time()
    print(finit)
    delta   = finit - start
    print("NamedTuple Benchmark took %0.3f seconds" % delta)
    # for i in benchmark_namedtuples(path):
    #     print(i)







