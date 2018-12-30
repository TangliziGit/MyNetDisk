import os
from pymongo import MongoClient
import util

mdb=MongoClient().MyNetDisk

def get_user_by_id(user_id):
    return mdb.users.find_one({'id': user_id})

def get_user_by_username(username):
    return mdb.users.find_one({'userName': username})

def get_file_count():
    return mdb.files.count({})

def get_file_path(ids):
    dirs=[];names=[]
    for x in mdb.files.find({'id': {'$in': ids}}):
        dirs.append(x['directory'])
        names.append(x['filename'])
    return dirs, names

def get_file_information():
    file_info=[]
    for file in list(mdb.files.find({})):
        file['id']=str(int(file['id']))
        file['downloadTime']=str(int(file['downloadTime']))
        file_info.append(file)
    return file_info

def add_download_time(ids):
    mdb.files.update({'id': {'$in': ids}}, {'$inc': {'downloadTime': 1}})

def upload_file(d, name):
    mdb.files.insert({
        'id': get_file_count(),
        "directory": d,
        "filename": name,
        "updateDate": util.get_date(),
        "downloadTime": 0
    })

def remove_file(ids):
    dirs, names=get_file_path(ids)
    for d, name in zip(dirs, names):
        os.remove(os.path.join(d, name))
    mdb.files.remove({'id': {'$in': ids}})
