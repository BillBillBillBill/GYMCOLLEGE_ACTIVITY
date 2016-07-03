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

def register(photos, videos):
    try:
        enc_password = get_enc_password(password)
        # 存入数据库
        newUser = User()
        db.session.add(newUser)
        db.session.flush()
        for photo in photos:
            photo = Photo(newUser.id, photo.hash, photo.key)
            db.session.add(photo)
            db.session.commit()
        for video in videos:
            video = Video(newUser.id, video.hash, video.key)
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
        videos = request.json.get('videos', [])
        photos = request.json.get('photos', [])
        ret = register(photos, videos)
        if ret:
            return jsonSuccess(ret), 201
        else:
            return jsonError(UserError.REGISTER_FAILED), 403
    except Exception, e:
        print e
        db.session.rollback()
        return jsonError(GlobalError.UNDEFINED_ERROR), 403
