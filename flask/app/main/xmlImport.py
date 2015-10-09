from lxml import etree
import pandas as pd
from pandas import DataFrame, Series
from pymongo import MongoClient
import json
import yaml


# checking s is a numberic/float

# def isnumeric(s):
#     '''returns True if string s is numeric'''
#     return all(c in "0123456789.+-" for c in s) and any(c in "0123456789" for c in s)

def isnumeric(s):
    if all(c in "0123456789.+-" for c in s) and any(c in "0123456789" for c in s):
        return yaml.load(s)
    else:
        return s


# isFunction = hasattr(obj,'__call__'), if isFunction is function type , It is True
# data_items[0].xpath('.//attributes/*|.//comment()')
# 

def xml_import(db, filepath, i_date):
    # setting mongo client
    print(filepath,':',i_date)
    db = db#MongoClient(host='127.0.0.1', port=27017)['data_test']

    # filepath = 'ENBCFG.XML'
    tree = etree.iterparse(filepath)

    # remove namespace
    for _, el in tree:
        el.tag = el.tag.split('}', 1)[1]
    root = tree.root
    print('step1:')
    # _id = _id = eNodeBId + attributes.tag + i
    eNodeBId = root.xpath('//eNodeBFunction/attributes')[0].find('eNodeBId').text
    name = root.xpath('//eNodeBFunction/attributes')[0].find('eNodeBFunctionName').text
    data_classes = root.xpath('//class')
    for data_class in data_classes:
        attrs_set = []
        data_items = data_class.xpath('./*')
        for i in range(len(data_items)):
            data_tag = data_items[i].tag
            attr_dict = {}

            # pre save previous element's tag 
            pre = ''
            data_attrs = data_items[i].xpath('attributes/*|.//comment()')
            for data_attr in data_attrs:
                if data_attr.text:
                    # checked data_attr is comment type
                    if hasattr(data_attr.tag, '__call__'):
                        if ':' in data_attr.text:
                            for j in data_attr.text.strip().split(';'):
                                attr_dict[j.split(':')[0]+'@'+pre] = isnumeric(j.split(':')[1])
                        else:
                            attr_dict[pre] = isnumeric(data_attr.text)
                    else:
                        attr_dict[data_attr.tag] = isnumeric(data_attr.text)
                        pre = data_attr.tag

            if len(attr_dict)>=1:
                attr_dict['_id'] = eNodeBId + ':' + name + ':' + data_tag + ':' + str(i) + ':' + i_date
                print(attr_dict['_id'])
                attr_dict['iDate'] = i_date
                db[data_tag].save(attr_dict)


def importProfile(filepath):
    db = MongoClient(host='127.0.0.1', port=27017)['demodb']
    xlsfile = pd.ExcelFile(path)
    df = xlsfile.parse(xlsfile.sheet_names[0])
    rs = json.loads(df.T.to_json()).values()
    db['Setting'].insert(rs)