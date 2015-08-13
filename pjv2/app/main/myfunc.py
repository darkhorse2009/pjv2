# -*- coding:utf-8 -*-
import math
import json
from . import SQLHelper
from .. import mysql
import csv
from collections import Counter, namedtuple
from math import sin, cos, sqrt, atan2, radians
from itertools import groupby
from operator import itemgetter



EARTH_RADIUS_METER = 6378137.0
# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


#获得数据库连接
def conn():
    return mysql.connect

#返回json格式数据
def return_json_data(data, total, page, records, *args, **kwargs):
    data_list = []
    for row in data:
        d = dict()
        d['id'] = str(row[0])
        d['categories'] = str(row[1])
        d['tablename'] = str(row[2])
        d['parachnname'] = str(row[3])
        d['paraname'] = str(row[4])
        d['defaultvalue'] = str(row[5])
        d['nav'] = "<a href='/upload?id="+str(row[0])+"'>统计</a>"
        data_list.append(d)
    grid_data = dict()
    grid_data['total'] = total  # 总页数
    grid_data['page'] = page    # 当前页
    grid_data['records'] = records  # 总记录数
    grid_data['rows'] = data_list
    print(grid_data)
    return grid_data

#返回根据条件查询json格式数据
#
#rows为每页的记录数
#

def get_filter(field, op, string):
    if op == 'eq':
        return "%s = '%s'" % (field,string)
    if op == 'ne':
        return "%s != '%s'" % (field,string)
    if op == 'lt':
        return "%s <'%s'" % (field,string)
    if op == 'gt':
        return "%s >'%s'" % (field,string)
    if op == 'le':
        return "%s <= '%s'" % (field,string)
    if op == 'ge':
        return "%s >= '%s'" % (field,string)


# 返回查询的json数据
def get_query_grid_data(rows=10, page=1, sidx='id', sord='', search='false', filters=None, searchField=None, searchOper=None, searchString=None):
    _filter=''      # #筛选的结果字符串
    _filter_ls = []     # 记录多条筛选条件,如果是单条件侧不起作用
    offset = (int(page)-1)*int(rows)      # 获取分页偏移
    if search == 'true':    # 是否有查询条件，注意multipleSearch为True时取filters，否则取searchField,searchOper,searchString
        d = json.loads(filters)     # 将json查询条件转化为字典

        _rules_len = len(d["rules"])    # 获取需要筛选的条件数
        # _filter=''      # #筛选的结果字符串
        # _filter_ls = []     # 记录多条筛选条件,如果是单条件侧不起作用
        searchgroupOp = ' ' + d["groupOp"] + ' '
        if _rules_len > 0:  # 多条件
            for i in range(_rules_len):
                _filter_ls.append(get_filter(d["rules"][i]["field"], d["rules"][i]["op"], d["rules"][i]["data"]))
                _filter=searchgroupOp.join(_filter_ls)
        else:       # 单条件查询
            searchField = d["rules"][0]["field"]
            searchOper = d["rules"][0]["op"]
            searchString = d["rules"][0]["data"]
            _filter = get_filter(searchField, searchOper, searchString)
        _filter = 'where ' + _filter
    else:
        print('请输出查询条件')
    # sql_data = 'select id, tablename, paraname, defaultvalue from profile %s order by %s %s limit %s, %s' % (_filter, sidx, sord, offset, rows)
    # print(sql_data)
    # sql_records = 'select count(*) from profile %s order by %s %s' % (_filter, sidx, sord)
    # print(sql_records)
    data = SQLHelper.get_query_profile(_filter, sidx, sord, offset, rows)
    records = SQLHelper.get_profile_count(_filter, sidx, sord)
    total = math.ceil(int(records)/int(rows))
    print(data)
    grid_data = return_json_data(data, total, page, records)
    return grid_data

# 返回所有json格式数据
def get_grid_data(rows=10, page=1, sidx='id', sord='', search='false', filters=None, searchField=None, searchOper=None, searchString=None):
    offset = (int(page)-1)*int(rows)      # 获取分页偏移
    # sql_data = 'select id, categories, tablename, parachnname, paraname, defaultvalue from profile order by %s %s limit %s, %s' % (sidx, sord, offset, rows)
    # sql_records = 'select count(*) from profile'
    data = SQLHelper.get_profile(sidx, sord, offset, rows)
    # print('grid:',data)
    records = SQLHelper.get_profile_count()
    total = math.ceil(int(records)/int(rows))
    grid_data = return_json_data(data, total, page, records)
    return grid_data

# jgrid_edit
def jqgrid_edit(request_form):
    oper = request_form['oper']
    for case in switch(oper):
        if case('add'):
            keys = []
            values = []
            for i in request_form.items():
                if i[0] not in ['oper', 'id']:
                    keys.append(i[0])
                    values.append(i[1])
            SQLHelper.add_profile(','.join(keys), '"' + '","'.join(values) + '"')
            break
        if case('del'):
            del_id = request_form['id']
            SQLHelper.del_profile(del_id)
            break
        if case('edit'):
            update_id = request_form['id']
            items = []
            for i in request_form.items():
                if i[0] not in ['oper', 'id']:
                    items.append(i[0]+'="'+i[1]+'"')
            SQLHelper.edit_profile(', '.join(items), update_id)
            break
        if case():  # default, could also just omit condition or 'if True'
            print("something else!")
            # No need to break here, it'll stop anyway
###############
#核查

#1,按字段核查:tablename=row[3], paraname=row[5], defaultvalue=row[6]，按类别返回统计
def ltechkcat():
    result = []
    chkfileds = SQLHelper.getchkprofile()
    for rs in chkfileds:
        for row in rs:
            _result=[]
            categories = row['categories']
            tablename = row['tablename']
            paraname = row['paraname']
            defaultvalue = row['defaultvalue']
            _result = [categories,tablename,paraname,defaultvalue]
            ##获得['定时器', 'UeTimer', 'T304', '6.0', 0]格式的数据
            if ',' in defaultvalue:
                _filter = defaultvalue.split(',')
                _counter = SQLHelper.getchkcount(tablename, paraname, _filter, ',')

            elif '~' in defaultvalue:
                _filter = defaultvalue.split('~')
                _counter = SQLHelper.getchkcount(tablename, paraname, _filter, '~')
            else:
                _filter = defaultvalue
                _counter = SQLHelper.getchkcount(tablename, paraname, _filter)
            for item in _counter:
                _result.append(item['count(*)'])
            result.append(_result)
    #按categories进行统计
    categoriesCat = dict()
    for key, items in groupby(result, itemgetter(0)):
        _tmp = []
        sumitem = 0
        for subitem in items:
            sumitem += subitem[4]
            _tmp.append(subitem)
        if sumitem:
            categoriesCat[key]=sumitem
    #按paraname进行统计
    paranameCat = []
    _paranameCat_key=[]
    _paranameCat_value=[]
    for key, items in groupby(result, itemgetter(0)):
        _tmp = []
        _i = 0
        for subitem in items:
            # sumitem += subitem[4]
            if subitem[4]:
                _tmp.append([subitem[2],subitem[4]])
                _i=1
        if _i:
            _paranameCat_key.append(key)
            _paranameCat_value.append(_tmp)
    paranameCat = [_paranameCat_key,_paranameCat_value]
    return [list(x) for x in categoriesCat.items()],paranameCat

#获得问题记录
def ltechkrec(pname=''):
    result = []
    chkfileds = SQLHelper.getchkprofile()
    result = dict()
    thField = []
    for rs in chkfileds:
        for row in rs:
            # thField.append([row['paraname'],row['parachnname']])
            # _result=[]
            categories = row['categories']
            tablename = row['tablename']
            paraname = row['paraname']
            defaultvalue = row['defaultvalue']
            _result = [categories,tablename,paraname,defaultvalue]
            # print(_result)
            ##获得['定时器', 'UeTimer', 'T304', '6.0', 0]格式的数据
            if pname:
                if pname == row['paraname']:
                    if tablename in ['ECellEquipmentFunction','Paging','UeEUtranMeasurement','UeRATMeasurement','PhyChannel','UeTimer']:
                        # pass    #基站级
                        continue
                    # elif tablename in ['']:
                    #     pass    #小区级
                    else:
                        if ',' in defaultvalue:
                            _filter = defaultvalue.split(',')
                            _record = SQLHelper.getchkquery(tablename, paraname, _filter, ',','ENBFunctionFDD','EUtranCellFDD',paraname)

                        elif '~' in defaultvalue:
                            _filter = defaultvalue.split('~')
                            _record = SQLHelper.getchkquery(tablename, paraname, _filter, '~','ENBFunctionFDD','EUtranCellFDD',paraname)
                        else:
                            _filter = defaultvalue
                            _record = SQLHelper.getchkquery(tablename, paraname, _filter,'ENBFunctionFDD','EUtranCellFDD',paraname)
                else:
                    continue
            else:
                if tablename in ['ECellEquipmentFunction','Paging','UeEUtranMeasurement','UeRATMeasurement','PhyChannel','UeTimer']:
                    pass    #基站级
                # elif tablename in ['']:
                #     pass    #小区级
                else:
                    if ',' in defaultvalue:
                        _filter = defaultvalue.split(',')
                        _record = SQLHelper.getchkquery(tablename, paraname, _filter, ',','ENBFunctionFDD','EUtranCellFDD',paraname)

                    elif '~' in defaultvalue:
                        _filter = defaultvalue.split('~')
                        _record = SQLHelper.getchkquery(tablename, paraname, _filter, '~','ENBFunctionFDD','EUtranCellFDD',paraname)
                    else:
                        _filter = defaultvalue
                        _record = SQLHelper.getchkquery(tablename, paraname, _filter,'ENBFunctionFDD','EUtranCellFDD',paraname)
            for item in _record:
                for i in item:
                    thField.append(row['paraname'])
                    if result.get(i['ENBFunctionFDD']+'_'+i['EUtranCellFDD']):
                        result[i['ENBFunctionFDD']+'_'+i['EUtranCellFDD']][paraname]=i[paraname]
                    else:
                        result[i['ENBFunctionFDD']+'_'+i['EUtranCellFDD']]={}
                        result[i['ENBFunctionFDD']+'_'+i['EUtranCellFDD']][paraname]=i[paraname]
    return [set(thField),result]

###END 参数核查


###参数查询


def lteqryrec(filter=''):
    #获得需要查询的参数
    print('####',filter)
    chkfileds = SQLHelper.getchkprofile()
    result = dict()
    thField = []
    for rs in chkfileds:
        for row in rs:
            categories = row['categories']
            tablename = row['tablename']
            paraname = row['paraname']
            defaultvalue = row['defaultvalue']
            if tablename in ['ECellEquipmentFunction','Paging','UeEUtranMeasurement','UeRATMeasurement','PhyChannel','UeTimer']:
                pass    #基站级
            # elif tablename in ['']:
            #     pass    #小区级
            else:
                if filter:
                    print('step2:',filter)
                    _record = SQLHelper.getqryrec(tablename, paraname, filter)
                else:
                    # print('step1:')
                    _record = SQLHelper.getqryrec(tablename, paraname)

            for item in _record:
                for i in item:
                    thField.append(paraname)
                    if result.get(i['ENBFunctionFDD']+'_'+i['EUtranCellFDD']):
                        result[i['ENBFunctionFDD']+'_'+i['EUtranCellFDD']][paraname]=i[paraname]
                    else:
                        result[i['ENBFunctionFDD']+'_'+i['EUtranCellFDD']]={}
                        result[i['ENBFunctionFDD']+'_'+i['EUtranCellFDD']][paraname]=i[paraname]
    print('result:',result)
    return [set(thField),result]


# 返回查询的json数据
def get_qry_qry_grid_data(rows=10, page=1, sidx='id', sord='', search='false', filters=None, searchField=None, searchOper=None, searchString=None):
    print('step0:',filters)
    _filter=''      # #筛选的结果字符串
    _filter_ls = []     # 记录多条筛选条件,如果是单条件侧不起作用
    offset = (int(page)-1)*int(rows)      # 获取分页偏移
    if search == 'true':    # 是否有查询条件，注意multipleSearch为True时取filters，否则取searchField,searchOper,searchString
        d = json.loads(filters)     # 将json查询条件转化为字典

        _rules_len = len(d["rules"])    # 获取需要筛选的条件数
        # _filter=''      # #筛选的结果字符串
        # _filter_ls = []     # 记录多条筛选条件,如果是单条件侧不起作用
        searchgroupOp = ' ' + d["groupOp"] + ' '
        if _rules_len > 0:  # 多条件
            for i in range(_rules_len):
                _filter_ls.append(get_filter(d["rules"][i]["field"], d["rules"][i]["op"], d["rules"][i]["data"]))
                _filter=searchgroupOp.join(_filter_ls)
        else:       # 单条件查询
            searchField = d["rules"][0]["field"]
            searchOper = d["rules"][0]["op"]
            searchString = d["rules"][0]["data"]
            _filter = get_filter(searchField, searchOper, searchString)
        _filter = 'where ' + _filter
    else:
        print('请输出查询条件')


    grid_data = dict()
    _data=[]
    print('step1:',_filter)
    _thead,tdata=lteqryrec(filter=_filter)
    print('step2:')
    thead=list(_thead)
    for key,value in tdata.items():
        print(key)
        _tmp=dict()
        _tmp['id']=key
        _data.append(dict(_tmp, **value))
    data = _data[int(offset):int(rows)+int(offset)]
    records = len(data)
    total = math.ceil(int(records)/int(rows))
    grid_data['total'] = total
    grid_data['page'] = page
    grid_data['records'] = records
    grid_data['rows'] = data
    # grid_data = return_json_data(data, total, page, records)
    return grid_data

# 返回所有json格式数据
def get_qry_grid_data(rows=10, page=1, sidx='id', sord='', search='false', filters=None, searchField=None, searchOper=None, searchString=None):
    offset = (int(page)-1)*int(rows)      # 获取分页偏移
    print('step1:',offset)
    # sql_data = 'select id, categories, tablename, parachnname, paraname, defaultvalue from profile order by %s %s limit %s, %s' % (sidx, sord, offset, rows)
    # sql_records = 'select count(*) from profile'
    grid_data = dict()
    _data=[]
    _thead,tdata=lteqryrec()
    thead=list(_thead)
    # print('setp2:',tdata)
    for key,value in tdata.items():
        # print(key)
        _tmp=dict()
        _tmp['id']=key
        _data.append(dict(_tmp, **value))
    # print('step3:',rows,':',type(rows))
    # print('setp3:',_data)
    data = _data[int(offset):int(rows)+int(offset)]
    print('step2:',data)
    # data = SQLHelper.get_profile(sidx, sord, offset, rows)
    # print('qry:',data)
    records = len(_data)
    print('records:',records)
    total = math.ceil(int(records)/int(rows))
    grid_data['total'] = total
    grid_data['page'] = page
    grid_data['records'] = records
    grid_data['rows'] = data
    # grid_data = return_json_data(data, total, page, records)
    print('get_qry_grid_data:',grid_data)
    return grid_data

###END 参数查询

###万栋楼宇处理
#获得csv数据
# path=''
def getCSV(path):
    records = []
    with open(path, 'rU') as data:
        reader = csv.reader(data)
        for row in reader:
            yield row
    # SQLHelper.insertCSV(get(path))

#根据两点（经纬度坐标）计算在地球上的距离
def spherical_distance(frompoint,topoint):
    """caculate the spherical distance of two points """
    lon1 = radians(frompoint[0])
    lat1 = radians(frompoint[1])
    lon2 = radians(topoint[0])
    lat2 = radians(topoint[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = EARTH_RADIUS_METER * c
    return distance

#获得小于特定距离的记录
def getOPrecord(distance='50'):
    result_ls = []      #总列表
    _result_ls = []     #采样点不为0列表
    f=open('output.txt','a')
    for record in SQLHelper.getPoints():
        for row in record:
            lon = row['lon']
            lat = row['lat']
            point = [lon,lat]
            city = row['city']
            buildingNM = row['buildingNM']
            company = row['company']
            center = row['center']
            lon = row['lon']
            lat = row['lat']
            remark = row['remark']
            # distance = distance
            #获得根据经纬比对的记录
            rs = SQLHelper.getCMPpointRS(point,distance=distance)
            result = [city,buildingNM,company,center,lon,lat,remark]
            for row in rs:
                result.append(list(row[0].values())[0])
            f.writelines(str(result)+'\n')
            if result[7]:       #如果该列为0,则表示没有测试
                _result_ls.append(result)
            result_ls.append(result)
    SQLHelper.insertHand(result_ls,distance=distance)
    f.close()
    return result_ls    #,companyCat,centerCat

#返回格式数据
def return_format(data):
    re = []
    for row in data.items():
        re.append(list(row))
    return re


#百度地图处理
marker_num = 2
markers = [
  {'uid':'113.121993,23.012411', 'lng':113.121993, 'lat':23.012411,'value':2.5},
  {'uid':'m2', 'lng':113.136726, 'lat':23.016669,'value':3.5},
  {'uid':'m3', 'lng':113.124078, 'lat':23.020194,'value':4.5},
]

def db_get_markers(point=[113.146763,23.054755],distance='300'):
    global marker_num, markers
    # print(distance)
    RDS = SQLHelper.getCMPpointDRS(point,distance=distance)
    # for rs in RDS:
    #     print(rs)
    return RDS

def db_add_markers(lng, lat):
    global marker_num, markers
    marker_num += 1
    markers.append({'uid':"m"+str(marker_num), 'lng':lng, 'lat':lat})