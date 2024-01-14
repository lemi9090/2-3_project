import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder



SERVER = "http://127.0.0.1:8000"
target = 'D:\\virous_sample\\MobSF_virous_sample\\repack.apk'
APIKey = 'd1129369caedf6877bb7f158a30af9301cbd0e8d27778ecea78916336c5c4f63'

def upload():
    print('start_file_analysing')
    multipart_data = MultipartEncoder(fields= {'file' : (target, open(target, 'rb'), 'application/octet-stream')})
    headers = { 'Content-Type' : multipart_data.content_type,'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/upload' , data=multipart_data, headers=headers)
    print(r.text) # 내가 보기위해 사용
    return r.text # 출력값 다른 곳에서 활용
    #requests 인자 : url, data, json, headers, cookies는 dict 형태로, 
    # files : 'file' : (target, open(target, 'rb') 처럼
    # url 을 제외하고는 나머지는 필수가 아니다. 

def scan(data):
    print("스캐닝!!! 주우우웅!")
    post_dict = json.loads(data)
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/scan', data=post_dict, headers=headers)
    print(r.text)

def pdf(data):
    data = {"hash" : json.loads(data)['hash']}
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/download_pdf', data=data, headers=headers, stream=True)
    with open('D:\\virous_sample\\MobSF_virous_sample\\report_file.pdf', 'wb') as word :
        for chunk in r.iter_content(chunk_size = 8192):
            if chunk:
                word.write(chunk)
        return 'D:\\virous_sample\\MobSF_virous_sample\\report_file.pdf'       

def json_pdf(data):
    data = {'hash' : json.loads(data)['hash']}
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/report_json', data=data, headers=headers)
    print(r.text)


def delete_scan(data):
    post_dict = {'hash' : json.loads(data)['hash']}
    headers = {'Authorization' : APIKey}
    r = requests.post(SERVER + '/api/v1/delete_scan', data=post_dict, headers=headers)
    print(r.text)

RESP = upload()
scan(RESP)
pdf(RESP)
json_pdf(RESP)
delete_scan(RESP)