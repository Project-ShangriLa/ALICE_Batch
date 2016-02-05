import json
from pixivpy3 import *

f = open('config/conf.json', 'r')
conf = json.load(f)
f.close

user_id = conf['pixiv']['user_id']
password = conf['pixiv']['password']

api = PixivAPI()
api.login(user_id, password)
