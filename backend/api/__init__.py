# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import jsonify
from util.jsonResponse import jsonSuccess, jsonError
from util.qiniu_auth import q, bucket, get_file
api = Blueprint('api', __name__)


# Define error code
ERROR_GLOBAL        = 0000
ERROR_USER          = 1000
ERROR_WISH          = 2000
ERROR_ONE_PICTURE   = 3000
ERROR_LIKE          = 4000
ERROR_COMMENT       = 5000


class GlobalError():
    INVALID_ARGUMENTS = {
        'err': ERROR_GLOBAL + 1,
        'msg': 'Invalid Arguments'
    }
    TOKEN_VALIFY_FAILED = {
        'err': ERROR_GLOBAL + 2,
        'msg': 'Token Valify Failed'
    }
    UNDEFINED_ERROR = {
        'err': ERROR_GLOBAL + 3,
        'msg': ''
    }
    PERMISSION_DENIED = {
        'err': ERROR_GLOBAL + 4,
        'msg': 'Permission Denied'
    }
    INVALID_FILE = {
        'err': ERROR_GLOBAL + 5,
        'msg': 'Invalid File'
    }
    OPERATION_BLOCKED_BY_ADMIN = {
        'err': ERROR_GLOBAL + 6,
        'msg': 'Operation Blocked By Admin'
    }


# @api.route('/', methods=["GET"])
# def index():
#     from flask import render_template
#     return render_template('testapi.html')


@api.route('/apply_upload_token', methods=["GET", "POST", "OPTIONS"])
def apply_upload_token():
    token = q.upload_token("gymcollege")
    a = jsonify(uptoken=token)
    a.headers["Access-Control-Allow-Origin"] = "*"
    a.headers["Access-Control-Allow-Headers"] = "DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type"
    a.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    a.headers["Access-Control-Max-Age"] = 1728000
    return a


@api.route('/get_file', methods=["GET"])
def get_file_handler():
    get_file("o_1amogcpj71ilp3m9uk81d291rr19.jpg")
    return jsonSuccess()

# api's
import image
import user
