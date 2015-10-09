# -*- coding:utf-8 -*-
from flask import render_template, request, url_for, current_app, jsonify, redirect,flash, send_from_directory
from . import mainBlueprint
from .. import mail
from flask.ext.mail import Message
from threading import Thread
import os, math, json
from itertools import groupby
from operator import itemgetter
import patoolib
from datetime import datetime
import pymongo
from pymongo import MongoClient, ASCENDING, DESCENDING
from shutil import rmtree
from . import xmlImport
import yaml, bson
from bson import ObjectId
import pandas as pd
from pandas import DataFrame, Series
from openpyxl import load_workbook
from collections import defaultdict
# from bson.json_util import dumps, loads
# import simplejson

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__iter__'):
            return list(obj)
        elif isinstance(obj, pymongo.cursor.Cursor):
            return list(obj)
        elif isinstance(obj, bson.objectid.ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

# checking s is a numberic/float
def isnumeric(s):
    if all(c in "0123456789.+-" for c in s) and any(c in "0123456789" for c in s):
        return yaml.load(s)
    else:
        return s
# connect mongodb
def conn():
    client = MongoClient(current_app.config['MONGO_URL'])
    return client[current_app.config['MONGO_DB']]

# 文件上传
@mainBlueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    db = conn()
    # data = db['ManagerInfo'].find()
    if request.method == 'POST':
        for key, upload_file in request.files.items():
            if upload_file:
                c_dict = {}
                filename = upload_file.filename
                
                if list(db['ManagerInfo'].find({'_id':filename})):
                    flash('You were fail logged in')
                else:
                    parts_dir = os.path.join(current_app.config['UPLOAD'], "%s" % filename.split('.')[0])
                    if not os.path.exists(parts_dir):
                        os.mkdir(parts_dir)
                    destination_path = os.path.join(parts_dir, "%s" % (filename))
                    upload_file.save(destination_path)

                    c_dict['_id'] = filename
                    c_dict['creator'] = 'admin'
                    c_dict['ctime'] = datetime.now().strftime('%Y%m%d')
                    c_dict['status'] = '已上传'
                    c_dict['operator'] = '未导入'
                    
                    db['ManagerInfo'].save(c_dict)
                    flash('You were successfully logged in')
                
        data = db['ManagerInfo'].find().sort('_id')
        return render_template('upload.html', data=data)
    else:
        data = db['ManagerInfo'].find().sort('_id')
        return render_template('upload.html', data=data)

# file unzip and import 
@mainBlueprint.route('/unzip', methods=['GET', 'POST'])
def unzip():
    db = conn()
    filename = request.args.get('o_id')
    parts_dir = os.path.join(current_app.config['UPLOAD'], "%s" % filename.split('.')[0])
    destination_path = os.path.join(parts_dir, "%s" % (filename))
    patoolib.extract_archive(destination_path,outdir=parts_dir)
    for root, dirs, files in os.walk(os.path.join(parts_dir, "%s" % (filename.split('.')[0]))):
        for name in files:
            if name == 'ENBCFG.XML.gz':
                patoolib.extract_archive(os.path.join(root, name),outdir=root)
                # print(os.path.join(root, 'ENBCFG.XML'))
                xmlImport.xml_import(db, os.path.join(root, 'ENBCFG.XML'), filename.split('.')[0])
    db['ManagerInfo'].update({'_id':filename},{'$set':{'operator':'未分析','status':'已导入'}})
    data = db['ManagerInfo'].find().sort('_id')
    return render_template('upload.html', data=data)

# setting
@mainBlueprint.route('/setting', methods=['GET', 'POST'])
def setting():
    db = conn()
    if request.method == 'POST':
        d=request.form.to_dict()
        oper = d.get('oper')
        _id = d.get('id')
        del d['id']
        print(d)
        if oper == 'edit':
            db['Profile'].update({'_id':ObjectId(_id)},{'$set':d})
        elif oper == 'del':
            for i in _id.split(','):
                db['Profile'].remove({'_id':ObjectId(i)})
        elif oper == 'add':
            # del d['id']
            db['Profile'].save(d)
    grid_data = MongoEncoder().encode(db['Profile'].find())
    # print(grid_data)
    return render_template('Lconfig.html',grid_data=grid_data)

# file analysis
@mainBlueprint.route('/analysis', methods=['GET', 'POST'])
def analysis():
    db=conn()
    filename = request.args.get('o_id')
    iDate = request.args.get('o_id').split('.')[0]
    # iDate = '200'
    #attention:Must trans to list or something, if the setting is cursor ,the loop will just be onece
    settings = list(db['Profile'].find())
    writer = pd.ExcelWriter(current_app.config['DOWNLOAD']+iDate+'.xlsx',engine='xlsxwriter')
    # print(current_app.config['DOWNLOAD']+iDate+'.xlsx')
    a_counter = 0
    a_total = 0

    ######## base on cell
    e_count = defaultdict(int)
    n_count = defaultdict(int)
    ########

    ######## base on bts, be_count is bts equal count , bn_count is bts not count
    be_count = defaultdict(int)
    bn_count = defaultdict(int)
    ########

    for i in settings:
        #############
        data = db[i['MML_Object']].find({'iDate':iDate})
        df1 = DataFrame(columns=('_id',i['ParameterID']))
        df2 = DataFrame(columns=('_id',i['ParameterID']))
        t_be_count = defaultdict(int)
        t_bn_count = defaultdict(int)

        t_e_count = defaultdict(int)
        t_n_count = defaultdict(int)

        for row in data:
            if row[i['ParameterID']] == isnumeric(i['OptimizationRange']):
                # if n_counter.get(i['ParameterID']):
                #     # del e_counter[i['ParameterID']]
                # else:
                if t_bn_count.get(row['_id'].split(':')[0]):
                    del t_be_count[row['_id'].split(':')[0]]
                else:
                    t_be_count[row['_id'].split(':')[0]] += 1
                t_e_count[str(row[i['ParameterID']])] +=  1
                df1.loc[len(df1) + 1] = [row['_id'],row[i['ParameterID']]]
            else:
                t_bn_count[row['_id'].split(':')[0]] += 1
                t_n_count[str(row[i['ParameterID']])] += 1
                df2.loc[len(df2) + 1] = [row['_id'],row[i['ParameterID']]]
        be_count[i['ParameterID']] = t_be_count
        bn_count[i['ParameterID']] = t_bn_count
        e_count[i['ParameterID']] = t_e_count
        n_count[i['ParameterID']] = t_n_count
        ###################
        #static
        e_config = ','.join([str(key)+'('+str(value)+')' for key, value in t_e_count.items() if value])
        n_config = ','.join([str(key)+'('+str(value)+')' for key, value in t_n_count.items() if value])
        config = ','.join([x for x in [e_config,n_config] if x])
        print(config)
        counter = len(t_bn_count)
        total = len(t_bn_count)+len(t_be_count)
        print(config,':',counter,':',total)
        db['Profile'].update({'_id':i['_id']},{'$set':{'config':config,'counter':int(total)-int(counter),'total':int(total)}})


        ###################
        # detail = db[i['MML_Object']].find({'$and':[{i['ParameterID']:{'$ne':isnumeric(i['OptimizationRange'])}},{'iDate':iDate}]},{'_id':1,i['ParameterID']:1})
        # df = DataFrame(list(detail))
        # if not(df.empty):
        if not(df2[['_id',i['ParameterID']]].empty):
            # print('start:',len(df2))
            df2[['_id',i['ParameterID']]].to_excel(writer,sheet_name=i['ParameterID'])

            workbook = writer.book
            worksheet = writer.sheets[i['ParameterID']]
            # Add some cell formats.
            format1 = workbook.add_format({'num_format': '#,##0.00'})
            format2 = workbook.add_format({'num_format': '0%'})
            format3 = workbook.add_format({'num_format': 'h:mm:ss AM/PM'})
            # Set the column width and format.
            worksheet.set_column('B:B', 44)
            worksheet.set_column('C:C', 18)
            # Set the format but not the column width.
            # worksheet.set_column('C:C', None, format2)
            # worksheet.set_column('D:D', 16, format3)
        ###################

        ###################
        # statistics
        # reducer = """function(obj, prev){prev.count++;}"""
        # data = db[i['MML_Object']].group(key={i['ParameterID']:1},condition={'iDate':iDate},initial={'count':0},reduce=reducer)
        # counter = 0
        # total = 0
        # for j in data:
        #     total = total + j['count']
        #     if j[i['ParameterID']] == isnumeric(i['OptimizationRange']):
        #         counter = counter + j['count']
        # config = ','.join([str(var[i['ParameterID']])+'('+str(int(var['count']))+')' for var in data])
        # db['Profile'].update({'_id':i['_id']},{'$set':{'config':config,'counter':int(total)-int(counter),'total':int(total)}})
        # a_counter = a_counter + counter
        # a_total = a_total + total
    #######################
    # for item in e_counter:



    # for item in n_counter:



    print('e_count:',e_count)
    print('n_count:',n_count)    
    print('be_count:',be_count)    
    print('bn_count:',bn_count)    

    #######################

    df = DataFrame(list(db['Profile'].find({},{'_id':0})))
    l_filter = ['ParameterSubj','MML_Object','ParameterID','DefaultValue','RecommandedValue','OptimizationRange','config','counter','total','MML_Script']
    df[l_filter].to_excel(writer,sheet_name='statics')
    workbook = writer.book
    worksheet = writer.sheets['statics']
    worksheet.set_column('B:Z', 24)
    writer.save()

    print('step:')
    db['ManagerInfo'].update({'_id':filename},{'$set':{'operator':'已下载','status':'已分析','counter':int(a_counter),'total':int(a_total)}})
    # db['ManagerInfo'].update({'_id':filename},{'$set':{'operator':'已下载','status':'已分析','counter':int(a_counter),'total':int(a_total)}})

    data = db['ManagerInfo'].find().sort('_id')
    return render_template('upload.html', data=data)

# file downloads

@mainBlueprint.route('/download', methods=['GET', 'POST'])
def download():
    # db=conn()
    filename = request.args.get('o_id').split('.')[0]+'.xlsx'
    print('step1:',ROOT_FOLDER,':',current_app.config['DOWNLOAD'])
#     @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
    downloads = os.path.join(ROOT_FOLDER, current_app.config['DOWNLOAD'])
    print(downloads+filename)
    return send_from_directory(directory=downloads, filename=filename, as_attachment=True)


# send email
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@mainBlueprint.route('/sendmail', methods=['GET', 'POST'])
def sendmail():
    db = conn()
    # filename = os.path.join(current_app.config['DOWNLOAD'],request.form['filename'])
    filepath = os.path.join(ROOT_FOLDER, current_app.config['DOWNLOAD'])
    recipient = request.form['recipient'].split(',')
    msg = Message(request.form['subject'], sender=current_app.config['MAIL_SENDER'], recipients=recipient)
    msg.html = request.form['wysiwyg_html']
    filename = filepath + request.form['attachments'].split('.')[0]+'.xlsx'
    with current_app.open_resource(filename.strip()) as fp:
        msg.attach(request.form['subject'], "application/vnd.ms-excel", fp.read())
    print('start:')
    # never forget to get the current_app because of the blueprint
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    data = db['ManagerInfo'].find().sort('_id')
    return render_template('upload.html', data=data)


@mainBlueprint.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')



# 4G to 3G
@mainBlueprint.route('/LtoC', methods=['GET', 'POST'])
def LtoC():
    db=conn()
    data = db['Profile'].find({}).sort('ParameterSubj')
    return render_template('LtoC.html', data=data)



# df1 = pd.DataFrame()
# df2 = pd.DataFrame()

# # df is your original DataFrame
# for col in df.columns:
#     df1[col] = df[col].apply(lambda x: x.split('|')[0])
#     df2[col] = df[col].apply(lambda x: x.split('|')[1])