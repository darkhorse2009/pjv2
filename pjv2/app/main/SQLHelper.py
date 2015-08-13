# -*- coding:utf-8 -*-
import xlrd
import collections
import json
from .. import mysql
import pymysql
# from . import myfunc
import csv
#获得数据库连接
def connect():
    return mysql.connect


###
#配置数据操作
###
#1,导入配置数据
def import_xls_to_db(filename, tablename, *args, **kwargs):
    workbook = xlrd.open_workbook(filename)
    sh = workbook.sheet_by_index(0)
    rows = sh.nrows
    conn = connect()
    with conn.cursor() as cur:
        keys_value = [str(x) + ' varchar(128)' for x in sh.row_values(0)]
        create_table(conn, tablename, ','.join(keys_value))
        for row in range(1, rows):
            rows_data = []
            for i in sh.row_values(row):
                rows_data.append(str(i))
            insert_data(conn, tablename, ','.join(sh.row_values(0)), '","'.join(rows_data), args[0])
        conn.commit()


#2,生成参数表
def create_table(conn, sheet_name, row_value, *args, **kwargs):
    # conn = connect()
    cur = conn.cursor()
    sql = 'create table %s (id int not null auto_increment, status varchar(128), %s, primary key(id))' \
          % (sheet_name, row_value)
    cur.execute(sql)


#3,插入参数表数据
def insert_data(conn, sheet_name, keys, fields, *args, **kwargs):
    # conn = connect()
    cur = conn.cursor()
    sql = 'insert into %s (status, %s) values ("useable", "%s")' % (sheet_name, keys, fields)
    # print(sql)
    cur.execute(sql)


#4,获得配置文件记录
def get_profile(sidx, sord, offset, rows, *args):
    conn = connect()
    with conn.cursor() as cur:
        sql = 'select id, categories, tablename, parachnname, paraname, defaultvalue from profile order by %s %s limit %s, %s' % (sidx, sord, offset, rows)
        # print(sql)
        # sql = """select id, tablename, paraname, defaultvalue from profile"""
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
    return data


#5,获取配置文件总记录总数, 表名profile
def get_profile_count(*args):
    conn = connect()
    with conn.cursor() as cur:
        sql = 'select count(*) from profile'
        cur.execute(sql)
        records = cur.fetchone()[0]
        conn.commit()
    return records

#6,获得条件查询记录
def get_query_profile(_filter, sidx, sord, offset, rows, *args):
    conn = connect()
    with conn.cursor() as cur:
        sql = 'select id, categories, tablename, parachnname, paraname, defaultvalue from profile %s order by %s %s limit %s, %s' % (_filter, sidx, sord, offset, rows)
        # print(sql)
        # sql = """select id, tablename, paraname, defaultvalue from profile"""
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
    return data

#7,获取条件查询记录总数
def get_query_profile_count(_filter, sidx, sord, *args):
    conn = connect()
    with conn.cursor() as cur:
        sql = 'select count(*) from profile %s order by %s %s' % (_filter, sidx, sord)
        cur.execute(sql)
        records = cur.fetchone()[0]
        conn.commit()
    return records


#8,增加
def add_profile(keys, values, *args):
    conn = connect()
    with conn.cursor() as cur:
        sql = 'insert into profile (%s) values (%s)' %(keys, values)
        cur.execute(sql)
        conn.commit()

#9,删除
def del_profile(del_id, *args):
    conn = connect()
    with conn.cursor() as cur:
        sql = 'delete from profile where id=%s' % del_id
        cur.execute(sql)
        conn.commit()

#9,编辑
def edit_profile(items, id, *args):
    conn = connect()
    with conn.cursor() as cur:
        sql = 'update profile set %s where id=%s' % (items, id)
        cur.execute(sql)
        conn.commit()


####
##核查
###

#1,获取需要查询的字段，profile
# def get_chk_profile():
#     conn = connect()
#     with conn.cursor() as cur:
#         sql = 'select * from profile'
#         cur.execute(sql)
#         data = cur.fetchall()
#         conn.commit()
#     return data
#
# def get_chk_query(tablename, paraname, _filter, *args):
#     print(args[1])
#     conn = connect()
#     with conn.cursor() as cur:
#         if args[0]:
#             if args[0] == ',':
#                 sql = 'select %s from %s where %s not in (%s)' % (','.join(args[1]), tablename, paraname, '"'+'","'.join(_filter)+'"')
#             elif args[0] == '~':
#                 sql = 'select %s from %s where %s > %s or %s < %s' % (','.join(args[1]), tablename, paraname, _filter[1], paraname, _filter[0])
#         else:
#             sql = 'select %s from %s where %s != %s' % (','.join(args[1]), tablename, paraname, _filter)
#         print(sql)
#         cur.execute(sql)
#         data = cur.fetchall()
#         conn.commit()
#     return data
#
# def get_chk_query_count(tablename, paraname, _filter, *args):
#     conn = connect()
#     with conn.cursor() as cur:
#         if args:
#             if args[0] == ',':
#                 sql = 'select count(*) from %s where %s not in (%s)' % (tablename, paraname, '"'+'","'.join(_filter)+'"')
#             elif args[0] == '~':
#                 sql = 'select count(*) from %s where %s > %s or %s < %s' % (tablename, paraname, _filter[1], paraname, _filter[0])
#         else:
#             sql = 'select count(*) from %s where %s != %s' % (tablename, paraname, _filter)
#         print(sql)
#         cur.execute(sql)
#         data = cur.fetchone()
#         conn.commit()
#     return data


################
###参数核查2####
##############

#1,获得profile表的核查字段
def getchkprofile():
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cur:
        sql = 'select * from profile limit 20'
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
    yield data

#2,获得核查的数据
def getchkquery(tablename, paraname, _filter, *args):
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cur:
        # print(args)
        # if args[0]:
        if args[0] == ',':
            sql = 'select %s from %s where %s not in (%s) and availabe = "working"' % (','.join(args[1:]), tablename, paraname, '"'+'","'.join(_filter)+'"')
        elif args[0] == '~':
            sql = 'select %s from %s where (%s > %s or %s < %s) and availabe = "working"' % (','.join(args[1:]), tablename, paraname, _filter[1], paraname, _filter[0])
        else:
            sql = 'select %s from %s where %s != %s and availabe = "working"' % (','.join(args), tablename, paraname, _filter)
        # print('getchkquery:',sql)
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
    yield data

#3,获得核查的统计
def getchkcount(tablename, paraname, _filter, *args):
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cur:
        if args:
            if args[0] == ',':
                sql = 'select count(*) from %s where %s not in (%s) and availabe = "working"' % (tablename, paraname, '"'+'","'.join(_filter)+'"')
            elif args[0] == '~':
                sql = 'select count(*) from %s where (%s > %s or %s < %s) and availabe = "working"' % (tablename, paraname, _filter[1], paraname, _filter[0])
        else:
            sql = 'select count(*) from %s where %s != %s and availabe = "working"' % (tablename, paraname, _filter)
        # print(sql)
        cur.execute(sql)
        data = cur.fetchone()
        # print(data)
        conn.commit()
    yield data





#####参数核查2--End######


#####LTE参数查询#########
#获得某参数的所有记录
def getqryrec(tablename, paraname, filter=''):
    print(filter)
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cur:
        if filter:
            sql = 'select %s,%s,%s from %s %s' %('ENBFunctionFDD','EUtranCellFDD',paraname, tablename,filter)
        else:
            sql = 'select %s,%s,%s from %s' %('ENBFunctionFDD','EUtranCellFDD',paraname, tablename)
        print('step3:',sql)
        cur.execute(sql)
        data = cur.fetchall()
        conn.commit()
    yield data


#4,获得条件查询记录
# def get_query_profile(_filter, sidx, sord, offset, rows, *args):
#     conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
#     with conn.cursor() as cur:
#         sql = 'select id, categories, tablename, parachnname, paraname, defaultvalue from profile %s order by %s %s limit %s, %s' % (_filter, sidx, sord, offset, rows)
#         # print(sql)
#         # sql = """select id, tablename, paraname, defaultvalue from profile"""
#         cur.execute(sql)
#         data = cur.fetchall()
#         conn.commit()
#     return data


######LTE参数查询--End#####



####导入掌上优的测试csv数据
# path=''
def getCSV(path):
    # records = []
    with open(path, 'rU') as data:
        reader = csv.reader(data)
        for row in reader:
            yield tuple(row)
def insertCSV(path):
    conn = connect()
    with conn.cursor() as cur:
        sql = "insert into data08 (" \
              "start,userNM,buildingNM,province,city,area,netNM,company,center,taskID,IMEI,IMSI,phone,rbnet,lon,lat,province1,city1," \
              "district,street,address,city2,btsNum,btsNM,cellNum,freNum,MCC,MNC,CI,PCI,TAC,RSRP,RSRQ,RSSI,RSSNR,CQI,city3,BSC,btsNM1," \
              "btsNum1,cellNum1,SID,NID,CID,G3RX,G3EcIo,G3SNR,G2RX,G2EcIo,GSMCELLID,GSMLAC,GSMRX,remark" \
              ") values(" \
              "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
              ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
              ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
              ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
              ",'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        # tmp = sql % data
        # print(sql)
        # data = []
        for row in getCSV(path):
            try:
                sqlcode = sql % row
                # print(sqlcode)
                cur.execute(sqlcode)
            except:
                pass
                print(row)
    conn.commit()


#插入楼宇的信息
def insertCSVbuilding(path):
    conn = connect()
    with conn.cursor() as cur:
        sql = "insert into building (city, buildingNM, company, center, lon, lat, remark) values('%s','%s','%s','%s','%s','%s','%s')"
        # print(sql)
        for row in getCSV(path):
            try:
            #     print(row)
                sqlcode = sql % row
                print(sqlcode)
                cur.execute(sqlcode)
            except:
                print(row)
    conn.commit()

#获得楼宇的经纬信息
def getPoints():
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    # conn = connect()
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        sql = 'select * from building'
        cur.execute(sql)
        buildinginfo = cur.fetchall()
        yield buildinginfo

#获得以point为中心点，小于一定距离的记录
def getCMPpointRS(point,searchdate=['2014-06-01','CURDATE()'],distance='50'):
    # print('@@@@@@@@')
    print('####',distance)
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        # print(point)

        lon2 = float(point[0])
        lat2 = float(point[1])
        startdate = searchdate[0]
        if searchdate[1] == 'CURDATE()':
            finitdate = searchdate[1]
        else:
            finitdate = "'" + searchdate[1] + "'"
        #distance = 6378137.0 * 2 * atan2(sqrt((sin((lat2 - lat1)/2))**2 + cos(lat1) * cos(lat2) * (sin((lon2 - lon1)/2))**2), sqrt(1-(sin((lat2 - lat1)/2))**2 + cos(lat1) * cos(lat2) * (sin((lon2 - lon1)/2))**2))
        #单位是分米
        #获得总的采样点记录数
        sql1 = "select count(*) from data08 where " \
              "6378137.0*2 * " \
              "atan2(" \
              "sqrt(pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2)), " \
              "sqrt(1-pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2))) <= %s and not(RSRP = '-') and str_to_date(start,'%s') between '%s' and %s" \
              %(lat2,lat2,lon2,lat2,lat2,lon2,distance,'%Y-%m-%d',startdate,finitdate)
        print(sql1)

        cur.execute(sql1)
        rs1 = cur.fetchall()
        # rs = cur.fetchall()
        yield rs1
        #获得RSRP小于115的记录数
        sql2 = "select count(*) from data08 where " \
              "6378137.0*2 * " \
              "atan2(" \
              "sqrt(pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2)), " \
              "sqrt(1-pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2))) <= %s and not(RSRP = '-') and  RSRP < -115 and str_to_date(start,'%s') between '%s' and %s" \
              %(lat2,lat2,lon2,lat2,lat2,lon2,distance,'%Y-%m-%d',startdate,finitdate)
        print(sql2)
        cur.execute(sql2)
        rs2 = cur.fetchall()
        yield rs2
        #获得RSRP小于-95,大于-115的记录数
        sql3 = "select count(*) from data08 where " \
              "6378137.0*2 * " \
              "atan2(" \
              "sqrt(pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2)), " \
              "sqrt(1-pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2))) <= %s and not(RSRP = '-') and  RSRP>=-115 and RSRP < -95 and str_to_date(start,'%s') between '%s' and %s" \
              %(lat2,lat2,lon2,lat2,lat2,lon2,distance,'%Y-%m-%d',startdate,finitdate)
        print(sql3)
        cur.execute(sql3)
        rs3 = cur.fetchall()
        yield rs3
        #获得RSRP大于-95的记录数
        sql4 = "select count(*) from data08 where " \
              "6378137.0*2 * " \
              "atan2(" \
              "sqrt(pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2)), " \
              "sqrt(1-pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2))) <= %s and not(RSRP = '-') and  RSRP >= -95 and str_to_date(start,'%s') between '%s' and %s" \
              %(lat2,lat2,lon2,lat2,lat2,lon2,distance,'%Y-%m-%d',startdate,finitdate)
        print(sql4)
        cur.execute(sql4)
        rs4 = cur.fetchall()
        yield rs4


#获得以point为中心点，小于一定距离的详细记录
def getCMPpointDRS(point,searchdate=['2014-06-01','CURDATE()'],distance='200'):
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        # print(point)

        lon2 = float(point[0])
        lat2 = float(point[1])
        startdate = searchdate[0]
        if searchdate[1] == 'CURDATE()':
            finitdate = searchdate[1]
        else:
            finitdate = "'" + searchdate[1] + "'"
        #distance = 6378137.0 * 2 * atan2(sqrt((sin((lat2 - lat1)/2))**2 + cos(lat1) * cos(lat2) * (sin((lon2 - lon1)/2))**2), sqrt(1-(sin((lat2 - lat1)/2))**2 + cos(lat1) * cos(lat2) * (sin((lon2 - lon1)/2))**2))
        #单位是分米
        #获得总的采样点记录数
        sql1 = "select RSRP,lon,lat from data08 where " \
              "6378137.0*2 * " \
              "atan2(" \
              "sqrt(pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2)), " \
              "sqrt(1-pow((sin((radians(%s) - radians(lat))/2)),2) + cos(radians(lat)) * cos(radians(%s)) * pow((sin((radians(%s) - radians(lon))/2)),2))) <= %s and RSRP != '-' and str_to_date(start,'%s') between '%s' and %s" \
              %(lat2,lat2,lon2,lat2,lat2,lon2,distance,'%Y-%m-%d',startdate,finitdate)
        # print(sql1)
        cur.execute(sql1)
        rs = cur.fetchall()
        return rs

#将掌上优统计结果插入数据库
#sql = "create table buildingres (id int not null auto_increment, %s)" \
#                        % ('city varchar(32),buildingNM varchar(128), company varchar(32), center varchar(32),lon varchar(32),lat varchar(32),'
#                           'remark varchar(32), samples varchar(32), rsrp115 varchar(32),rsrp115and95 varchar(32),rsrp95 varchar(32),distance varchar(32), primary key(id)')
def insertHand(data,distance='200'):
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        for rs in data:
            sql = 'insert into buildingrs300 (city ,buildingNM, company, center,lon,lat,remark, samples, rsrp115,rsrp115and95,rsrp95,distance) values("%s","%s")' % ('","'.join([str(x) for x in rs]),distance)
            print(sql)
            cur.execute(sql)
        conn.commit()


#查询buildingres表的掌上优统计记录
def getBDRes(distance='100'):
    # print(distance)
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8')
    with conn.cursor() as cur:
        # sql = 'select buildingNM,company,center,lon,lat,samples,rsrp115,rsrp115and95,rsrp95 from buildingres'
        sql = 'select buildingNM,company,center,lon,lat,samples from buildingrs300 where distance=%s' % distance
        # print(sql)
        cur.execute(sql)
        data = cur.fetchall()
    conn.commit()
    return data



def getCompanyCat(distance='200'):
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        sql = 'select company, count(*) as counter from buildingrs300 where distance="%s" group by company' % distance
        cur.execute(sql)
        data1 = cur.fetchall()
        yield data1

        sql = 'select company, count(*) as counter from buildingrs300 where samples!=0 and distance="%s" group by company' %distance
        cur.execute(sql)
        data2 = cur.fetchall()
        yield data2


def getCenterCat(distance='200'):
    conn = pymysql.connect(host='localhost',port=3306,user='root',password='fangww',db='data_dev',charset='utf8')
    with conn.cursor() as cur:
        #获得以center分类的统计数
        sql = 'select company, center, count(*) as counter from buildingrs300 where distance="%s" group by center' % distance
        cur.execute(sql)
        data1 = cur.fetchall()
        # print(data1,':',data1)
        yield data1

        sql = 'select company, center, count(*) as counter from buildingrs300 where samples!=0 and distance="%s" group by center' %distance
        cur.execute(sql)
        data2 = cur.fetchall()
        yield  data2

# def getDetail(point):
#
#