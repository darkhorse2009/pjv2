# -*- coding:utf-8 -*-
from flask import render_template, request, url_for, current_app, jsonify, redirect,flash
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from . import mainBlueprint
from . import myfunc, SQLHelper
from .. import mysql
import os, math, json
from itertools import groupby
from operator import itemgetter


DISTANCE='300'

# 文件上传
@mainBlueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for key, upload_file in request.files.items():
                if upload_file:
                    filename = upload_file.filename
                    parts_dir = os.path.join(current_app.config['UPLOAD_PATH_LTE'], "%s" % filename)
                    if not os.path.exists(parts_dir):
                        os.mkdir(parts_dir)
                    destination_path = os.path.join(parts_dir, "%s" % (filename))
                    upload_file.save(destination_path)
        return render_template('upload.html')
    else:
        return render_template('upload.html')


#参数配置

#1,导入配置数据
@mainBlueprint.route('/initprofile', methods=['GET', 'POST'])
def initprofile():
    filename = 'zx/profile/zx20150617.xlsx'
    path = os.path.join(current_app.config['UPLOAD_PATH_LTE'], "%s" % (filename))
    SQLHelper.import_xls_to_db(path, 'profile', '20150709')
    return '<h1>Success</h1>'

#2,显示配置数据
@mainBlueprint.route('/setlte', methods=['GET', 'POST'])
def setlte():
    return render_template('setlte.html')

#3,返回jqgrid的json数据
@mainBlueprint.route('/json_data', methods=['GET', 'POST'])
def json_data():
    page = request.args.get('page', 1)  # 获得当前页码
    sidx = request.args.get('sidx', 'id')   # 获得主键
    sord = request.args.get('sord', 'asc')  # 排列方式
    rows = request.args.get('rows', 10)     # 显示行数
    search = request.args.get('_search', '')    # 是否有查询
    filters = request.args.get('filters', '')   # 查询条件
    searchField = request.args.get('searchField', None)
    searchOper = request.args.get('searchOper', None)
    searchString = request.args.get('searchString', None)
    if sidx=='':
        sidx='id'
    if search=='true':
        grid_data = myfunc.get_query_grid_data(rows, page, sidx, sord, search, filters, searchField, searchOper, searchString)
    else:
        grid_data = myfunc.get_grid_data(rows, page, sidx, sord, search, filters, searchField, searchOper, searchString)
    return jsonify(grid_data)

@mainBlueprint.route('/json_edit', methods=['GET', 'POST'])
def json_edit():
    myfunc.jqgrid_edit(request.form)
    return '<h1>Success</h1>'


####LTE参数核查
@mainBlueprint.route('/ltechk', methods=['GET', 'POST'])
def ltechk():
    category=request.args.get('category')
    categoriesCat, paranameCat = myfunc.ltechkcat()
    # categoriesCat =[['容量类', 7468], ['功控类', 0], ['基本类', 1915], ['接入类', 7492], ['切换类', 778964], ['小区重选类', 9433], ['定时器', 0], ['寻呼类', 0]]
    tbdata = myfunc.ltechkrec(category)
    return render_template('checklte.html', categoriesCat=categoriesCat, paranameCat=paranameCat,tbdata=tbdata,category=category)

###LTE参数查询####
################
################

@mainBlueprint.route('/lteqry', methods=['GET', 'POST'])
def lteqry():
    print('SUCCESS!')
    # key,value=myfunc.lteqryrec()
    # for item1,item2 in value.items():
    #     print(item1,'###:@@@',item2)
    # for item in key:
    #     print(item)
    # grid_data=dict()
    # _data=[]
    _thead,tdata=myfunc.lteqryrec()
    thead=list(_thead)
    thead.insert(0,'id')
    # for key,value in tdata.items():
    #     print(key)
    #     _tmp=dict()
    #     _tmp['id']=key
    #     _data.append(dict(_tmp, **value))
    # data = _data[0:10]
    # # data = SQLHelper.get_profile(sidx, sord, offset, rows)
    # # print('qry:',data)
    # records = len(data)
    # total = math.ceil(int(records)/int(3))
    # grid_data['total'] = total
    # grid_data['page'] = 2
    # grid_data['records'] = records
    # grid_data['rows'] = data
    # print('grid_data:',grid_data)
    # print('thead:',thead)
        # print(value)
    #     _tmp = [key]
    #     for item in thead:
    #         _tmp.append(value.get(item,''))
    #     data.append(_tmp)
    # print(thead)
    # print(data[0:10+2])
    # print('END@@@@@@')
    return render_template('querylte.html',thead=thead)


###获得json格式数据
@mainBlueprint.route('/qry_json_data', methods=['GET', 'POST'])
def qry_json_data():
    page = request.args.get('page', 1)  # 获得当前页码
    sidx = request.args.get('sidx', 'id')   # 获得主键
    sord = request.args.get('sord', 'asc')  # 排列方式
    rows = request.args.get('rows', 10)     # 显示行数
    search = request.args.get('_search', '')    # 是否有查询
    filters = request.args.get('filters', '')   # 查询条件
    searchField = request.args.get('searchField', None)
    searchOper = request.args.get('searchOper', None)
    searchString = request.args.get('searchString', None)
    if sidx=='':
        sidx='id'
    if search=='true':
        print('qry_json_data2')
        grid_data = myfunc.get_qry_qry_grid_data(rows, page, sidx, sord, search, filters, searchField, searchOper, searchString)
    else:
        print('qry_json_data1')
        grid_data = myfunc.get_qry_grid_data(rows, page, sidx, sord, search, filters, searchField, searchOper, searchString)
    return jsonify(grid_data)


###END参数查询###


###导入掌上优测试数据
@mainBlueprint.route('/importCSV', methods=['GET', 'POST'])
def importCSV():
    filename = 'sd08.csv'
    path = os.path.join(current_app.config['UPLOAD_PATH_CSV'], "%s" %(filename))
    # data = myfunc.getCSV(path)
    # for i in data:
    #     print(i)
    SQLHelper.insertCSV(path)


###导入掌上优测试列表
@mainBlueprint.route('/importCSVbuilding', methods=['GET', 'POST'])
def importCSVbuilding():
    filename = 'data0728-v1.csv'
    path = os.path.join(current_app.config['UPLOAD_PATH_CSV'], "%s" %(filename))
    # data = myfunc.getCSV(path)
    # for i in data:
    #     print(i)
    SQLHelper.insertCSVbuilding(path)


###导入掌上优分析结果
@mainBlueprint.route('/importrs', methods=['GET', 'POST'])
def importrs():
    #distance='300'
    myfunc.getOPrecord(DISTANCE)

@mainBlueprint.route('/handOP', methods=['GET', 'POST'])
def handOP():
    # result_ls,_companyCat,centerCat = myfunc.getOPrecord()
    result_ls = myfunc.getOPrecord()
    # print(result)
    # companyCat = myfunc.return_format(_companyCat)
    companyCat=[['南海', 152,16*100/152],['顺德', 203,55*100/203],['三水', 19,1*100/19],['高明', 13,4*100/13],['禅城', 169,39*100/169]]
    dData =[['app.com','$45','3,330','Feb 12','Expiring'],['app.com','$45','3,330','Feb 12','Expiring']]
    sData = [[['桂城',32,10],['松岗',24,14],['狮山',25,11],['桂城',32,10],['松岗',24,14],['狮山',25,11]],
             [['大良',32,10],['容桂',24,14],['乐从',25,11]],
             [['禅城',32,10],['南庄',24,14]],
             [['三水',32,10],['三水1',24,14]],
             [['高明',32,10],['高明2',24,14]],]
    print(companyCat)
    return render_template('handOP.html', companyCat=companyCat,result_ls=result_ls,dData=dData,sData=sData)


@mainBlueprint.route('/handMap', methods=['GET', 'POST'])
def handMap():
    # print(DISTANCE)
    # result_ls,_companyCat,centerCat = myfunc.getOPrecord()
    #distance = '300'
    result_ls = SQLHelper.getBDRes(DISTANCE)

    # companyCat = myfunc.return_format(_companyCat)

    #获得按company的完成情况
    _rs1,_rs2 = SQLHelper.getCompanyCat(DISTANCE)
    rs1=dict()
    rs2=dict()
    for item in _rs1:
        rs1[item['company']]=item['counter']
    for item in _rs2:
        rs2[item['company']]=item['counter']
    companyCat = []
    for item in rs1:
        companyCat.append([item,rs1[item],format(rs2[item]*100/rs1[item],'.2f')])

    #获得company和center分类的统计情况
    _rs3, _rs4 = SQLHelper.getCenterCat(DISTANCE)

    rs4 = dict()
    for key, items in groupby(sorted(_rs4,key=itemgetter(0)), itemgetter(0)):
        _tmp = dict()
        for subitem in items:
            _tmp[subitem[1]]=subitem[2]
        rs4[key] = _tmp

    rs3 = []
    for key, items in groupby(sorted(_rs3,key=itemgetter(0)), itemgetter(0)):
        _tmp = []
        for subitem in items:
            _tmp.append([subitem[1],subitem[2],rs4[key].get(subitem[1],0)])
        rs3.append(_tmp)
    sData=rs3
    points=[113.146763,23.054755]
    tn=['三水','南海','禅城','顺德','高明']


    # print(result_ls)
    return render_template('handMap.html', companyCat=companyCat,sData=sData,points=points,tn=tn,result_ls=result_ls,distance=DISTANCE)


@mainBlueprint.route('/getmarkers', methods=['POST'])
def getmarkers():
    # print('@@@@@@@:',request.form['lon'])
    # print(DISTANCE)
    res = myfunc.db_get_markers(distance=DISTANCE)
    return json.dumps(res)


@mainBlueprint.route('/getmarkers1', methods=['POST','GET'])
def getmarkers1():
    points=request.form['points'].split(',')
    # print(DISTANCE)
    res = myfunc.db_get_markers(points,distance=DISTANCE)
    return json.dumps(res)

@mainBlueprint.route('/addmarkers', methods=['POST'])
def addmarkers():
    # print('@@@@@@@:',request.form['lng'])
    class MarkPos(Form):
        lng = StringField('lng', validators=[DataRequired()])
        lat = StringField('lat', validators=[DataRequired()])
    form = MarkPos()
    lng = float(form.lng.data)
    lat = float(form.lat.data)
    myfunc.db_add_markers(lng, lat)
    return json.dumps('ok')


@mainBlueprint.route('/chg')
def chg():
    print(request.args.get('distance','200'))
    global DISTANCE
    # print(DISTANCE)
    DISTANCE=request.args.get('distance','200')
    # print(DISTANCE)
    # url_for('handMap')
    return redirect(url_for('mainBlueprint.handMap'))


# @mainBlueprint.route('/getdetail', methods=['POST'])
# def getdetail():
#     points = request.form['points'].split(',')
#     res = myfunc.db_get_detail(points)
#     return json.dumps(res)


@mainBlueprint.route('/test',)
def test():
    # print(request.args.get('category','200'))
    category=request.args.get('category')
    print('@@@:',category)
    return redirect(url_for('mainBlueprint.ltechk',category=category))


