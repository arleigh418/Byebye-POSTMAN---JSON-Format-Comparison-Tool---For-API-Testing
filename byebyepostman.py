import requests
import json
import time
from datetime import datetime
import sys
import pandas as pd

class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    
    def flush(self):
        pass

# sys.stdout = Logger("D:\Test_Item.txt") 

def cmp_update(src_data,dst_data,jsona_title,jsonb_title):
    if isinstance(src_data, dict) == True:
        try:
            for key in dst_data:
                if key not in src_data:
                    print(jsona_title," don't have this key:",key)
            for key in src_data:
                if key in dst_data:
                    thiskey = key
                    cmp_update(src_data[key], dst_data[key],jsona_title,jsonb_title)       
                else:
                    print(jsonb_title," don't have this key:",key)
        except:
            print('Unknown Compare Error')
    elif isinstance(src_data, list)== True:
        if len(src_data) != len(dst_data):
            print("list len: '{}' != '{}'".format(len(src_data), len(dst_data)))
        for src_list, dst_list in zip(src_data, dst_data):
            cmp_update(src_list, dst_list,jsona_title,jsonb_title)
    else:   
        if str(src_data) != str(dst_data):
            print('Not Equal Position')
            print(jsona_title,' --> ',src_data)
            print(jsonb_title,' --> ',dst_data)
            print('\n')

method = input('請輸入模式，輸入0為兩網址比對，輸入1為Excel File多網址比對:')

if method =='0':
    url1 = input('請輸入網址1:')
    url2 = input('請輸入網址2:')

    try:
        json1_name = '網址1'
        json2_name = '網址2'
        print(json1_name,' Output')
        x = requests.get(url1)
        print(x.json())
        print(json2_name,' Output')
        y = requests.get(url2)     
        print(y.json())
        print('\n')
        print('Compare Output')
        
        cmp_update(x.json(),y.json(),json1_name,json2_name)
    except:
        print('\n')
        print('Error Output')
        print('Error in api , must be check this api')

elif method == '1':
    file_path = input('請輸入檔案路徑(.xlsx):')
    jsonA_title = input('請輸入欲比對的JSON1 Excel Title:')
    jsonB_title= input('請輸入欲比對的JSON2 Excel Title:')
    sys.stdout = Logger("Test Result.txt") 
    Count =1
    print('\n')
    try:
        url = pd.read_excel(file_path,encoding = 'utf-8')
        jsona_url = url[jsonA_title].tolist()
        jsonb_url = url[jsonB_title].tolist()
    except:
        print('\nInpur Error,please check')
        exit()

    for lenth in range(len(jsona_url)):
        print('<','-'*40,Count,'-'*40,'>')
        Count+=1    
        try:
            print(jsonA_title,jsona_url[lenth])
            print(jsonB_title,jsonb_url[lenth])
            print('\n')
            print(jsonA_title,' Output')
            x = requests.get(jsona_url[lenth])
            print(x.json())
            print(jsonB_title,' Output')
            y = requests.get(jsonb_url[lenth])     
            print(y.json())
            print('\n')
            print('Compare Output')
            cmp_update(x.json(),y.json(),jsonA_title,jsonB_title)
        except:
            print('\n')
            print('Error Output')
            print('Error in api , must be check this api')

else:
    print('Error in method choose')
  
  
    
