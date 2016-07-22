# -*- coding: utf-8 -*-
import random
import time
from hashlib import sha256
from hmac import HMAC

from flask import request

from api import api, ERROR_USER, GlobalError
from model.register_information import User, Photo, Video
from server import db
from util.jsonResponse import jsonSuccess, jsonError
from util.weixin_sign import sign1


class UserError():
    USER_NOT_EXIST = {
        'err': ERROR_USER + 1,
        'msg': 'User Not Exist'
    }
    PASSWORD_ERROR = {
        'err': ERROR_USER + 2,
        'msg': 'Password Error'
    }
    USERNAME_HAS_EXISTED = {
        'err': ERROR_USER + 3,
        'msg': 'Username has existed'
    }
    USER_DELETE_FAILED = {
        'err': ERROR_USER + 4,
        'msg': 'User Delete Failed'
    }
    USER_UPDATE_FAILED = {
        'err': ERROR_USER + 5,
        'msg': 'User Update Failed'
    }
    REGISTER_FAILED = {
        'err': ERROR_USER + 6,
        'msg': 'Register Failed'
    }
    FORM_DATA_INVALID = {
        'err': ERROR_USER + 7,
        'msg': 'Form Data Invalid'
    }
    MOBILE_NUMBER_ILLEGAL = {
        'err': ERROR_USER + 9,
        'msg': 'Mobile Number Illegal'
    }
    CHECKCODE_ERROR = {
        'err': ERROR_USER + 10,
        'msg': 'Checkcode Error'
    }


def register(name, sex, job, phone, email, location, photos, videos, register_type, openid):
    try:
        # 存入数据库
        newUser = User(name, sex, job, phone, email, location, register_type, openid)
        db.session.add(newUser)
        db.session.commit()
        for photo in photos:
            photo = Photo(newUser.id, photo['hash'], photo['key'])
            db.session.add(photo)
            db.session.commit()
        for video in videos:
            video = Video(newUser.id, video['hash'], video['key'])
            db.session.add(video)
            db.session.commit()
        return {"register_id": newUser.id}
    except Exception, e:
        db.session.rollback()
        print "注册失败" + str(e)
        return False
    finally:
        # 记得关闭！！
        db.session.close()


@api.route('/register', methods=["POST"])
def user_register():
    try:
        if not request.json:
            return jsonError(GlobalError.INVALID_ARGUMENTS), 400
        openid = request.json.get('openid', '')
        name = request.json.get('name', '')
        register_type = request.json.get('register_type', '')
        sex = request.json.get('sex', '')
        job = request.json.get('job', '')
        phone = request.json.get('phone', '')
        email = request.json.get('email', '')
        location = request.json.get('location', '')
        videos = request.json.get('videos', [])
        photos = request.json.get('photos', [])
        ret = register(name, sex, job, phone, email, location, photos, videos, register_type, openid)
        if ret:
            return jsonSuccess(ret), 201
        else:
            return jsonError(UserError.REGISTER_FAILED), 403
    except Exception, e:
        print e
        db.session.rollback()
        return jsonError(GlobalError.UNDEFINED_ERROR), 403


@api.route('/register', methods=["OPTIONS"])
def user_register_options():
    a = jsonify()
    a.headers["Access-Control-Allow-Origin"] = "*"
    a.headers["Access-Control-Allow-Headers"] = "DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type"
    a.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    a.headers["Access-Control-Max-Age"] = 1728000
    return a


@api.route('/check_subscribe', methods=["POST"])
def subscribe_or_not():
    code = request.json.get('code', '')
    openid = (sign1.getUserOpenId(code)).get("openid")
    print code
    print openid
    if not openid:
        return jsonSuccess(), 200
    else:
        return jsonSuccess(sign1.check_subscribe(code)), 200
