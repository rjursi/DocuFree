import requests

def add(hash):
    # hash = file()
    # print(hash)
    url=f'http://35.233.216.2:5000/add'
    #파일이름, 파일형식 정보 받아와야됨(name, extension)
    data = {'name' : 'test', 'sha256' : hash['sha256'], 'sha512' : hash['sha512'], 'md5' : hash['md5'], 'extension' : 'txt'}
    res = requests.post(url, json=data)
    flag = res.text
    if flag == "Insert Success":
        return 2
    elif flag == "Insert Fail":
        return 1
