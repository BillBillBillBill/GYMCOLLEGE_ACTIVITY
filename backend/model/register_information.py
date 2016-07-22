# -*- coding: utf-8 -*-
from server import db
from datetime import datetime
from collections import OrderedDict
import time
from util.qiniu_auth import get_file_link


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    job = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    register_type = db.Column(db.String(200), nullable=False)
    openid = db.Column(db.String(200), nullable=False)

    def __init__(self, name, sex, job, phone, email, location, register_type, openid):
        self.create_time = datetime.now()
        self.name = name
        self.sex = sex
        self.job = job
        self.phone = phone
        self.email = email
        self.location = location
        self.openid = openid
        if register_type == "1":
            self.register_type = u"单人"
        elif register_type == "2":
            self.register_type = u"双人"
        else:
            self.register_type = u"亲子"

    def to_dict(self):
        ret = OrderedDict()
        ret[u'id'] = self.id
        ret[u'openid'] = self.openid
        ret[u'类型'] = self.register_type
        ret[u'姓名'] = self.name
        ret[u'性别'] = self.sex
        ret[u'职业'] = self.job
        ret[u'联系电话'] = self.phone
        ret[u'邮箱'] = self.email
        ret[u'所在地区'] = self.location
        c = self.create_time
        ret[u'报名时间'] = "%s/%s/%s %s:%s:%s" % (c.year, c.month, c.day, c.hour, c.minute, c.second)
        ret[u'照片'] = [get_file_link(photo.key) for photo in self.photos] if self.photos else []
        ret[u'视频'] = [get_file_link(video.key) for video in self.videos] if self.videos else []
        return ret

    def to_eng_dict(self):
        return {
            'id': self.id,
            'openid': self.openid,
            'register_type': self.register_type,
            'name': self.name,
            'sex': self.sex,
            'job': self.job,
            'phone': self.phone,
            'email': self.email,
            'location': self.location,
            'photos': [photo.to_dict() for photo in self.photos] if self.photos else [],
            'videos': [video.to_dict() for video in self.videos] if self.videos else []
        }


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(200), nullable=False)
    key = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    user = db.relationship('User', backref=db.backref('photos', lazy='dynamic'))

    def __init__(self, user_id, hash, key):
        self.user_id = int(user_id)
        self.hash = hash
        self.create_time = datetime.now()
        self.key = key

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user.id,
            'hash': self.hash,
            'key': self.key
        }


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(200), nullable=False)
    key = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    user = db.relationship('User', backref=db.backref('videos', lazy='dynamic'))

    def __init__(self, user_id, hash, key):
        self.user_id = int(user_id)
        self.hash = hash
        self.create_time = datetime.now()
        self.key = key

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user.id,
            'hash': self.hash,
            'key': self.key
        }
