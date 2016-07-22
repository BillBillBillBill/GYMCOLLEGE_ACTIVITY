# -*- coding: utf-8 -*-
import time
import random
import string
import hashlib
import json
import requests
from server import redisClient


class Sign:
    def __init__(self, appId, appSecret, url):
        self.appId = appId
        self.appSecret = appSecret

        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': self.getJsApiTicket(),
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

    def getJsApiTicket(self):
        data = json.loads(open('jsapi_ticket.json').read())
        jsapi_ticket = data['jsapi_ticket']
        if data['expire_time'] < time.time():
            url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?type=jsapi&access_token=%s" % (self.getAccessToken())
            response = requests.get(url)
            jsapi_ticket = json.loads(response.text)['ticket']
            data['jsapi_ticket'] = jsapi_ticket
            data['expire_time'] = int(time.time()) + 7000
            fopen = open('jsapi_ticket.json', 'w')
            fopen.write(json.dumps(data))
            fopen.close()
        return jsapi_ticket

    def getAccessToken(self):
        data = json.loads(open('access_token.json').read())
        access_token = data['access_token']
        if data['expire_time'] < time.time():
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (self.appId, self.appSecret)
            response = requests.get(url)
            access_token = json.loads(response.text)['access_token']
            data['access_token'] = access_token
            data['expire_time'] = int(time.time()) + 7000
            fopen = open('access_token.json', 'w')
            fopen.write(json.dumps(data))
            fopen.close()
        return access_token

    def check_subscribe(self, oid):
        try:
            url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" % (self.getAccessToken(), oid)
            response = requests.get(url)
            ret = json.loads(response.text)
            return {"subscribe": ret.get(u"subscribe"), "openid": ret.get(u"openid")}
        except Exception, e:
            print "wrong:", e
            return {}

    def getUserOpenId(self, code):
        try:
            try_get_code_from_redis = redisClient.get(code)
            if not try_get_code_from_redis:
                url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx318977fdaad976c1&secret=cd70f0c648cc13c82aeba641e9a751fa&code=%s&grant_type=authorization_code" % code
                response = requests.get(url)
                ret = json.loads(response.text)
                print ret
                redisClient.set(code, ret.get(u"openid"))
                return {"openid": ret.get(u"openid")}
            else:
                return {"openid": try_get_code_from_redis}
        except Exception, e:
            print "wrong:", e
            return {}


appId = 'wx318977fdaad976c1'
appSecret = 'cd70f0c648cc13c82aeba641e9a751fa'
sign1 = Sign(appId, appSecret, 'http://marserv.cn/register/')
#sign2 = Sign(appId, appSecret, 'http://marserv.cn/admin/login')
#sign3 = Sign(appId, appSecret, 'http://marserv.cn/register/')

#print sign2.getAccessToken()
#print sign1
#print sign1.getUserOpenId("011psWFd1L2E5o0foEHd18dUFd1psWF6")
#print sign1.check_subscribe("oAFIAj-7ru1SSh_TSih0Zv88kEOM")
#sign2.check_subscribe("oAFIAj-7ru1SSh_TSih0Zv88kEOM")
#sign2.getUserOpenId("011cmsqM1smJe01szGrM1D9oqM1cmsqy")
