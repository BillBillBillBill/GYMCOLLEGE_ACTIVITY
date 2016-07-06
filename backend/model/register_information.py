# -*- coding: utf-8 -*-
from server import db
from datetime import datetime
from collections import OrderedDict
import time


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    job = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    declaration = db.Column(db.String(300), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, sex, job, phone, email, location, declaration):
        self.create_time = datetime.now()
        self.name = name
        self.sex = sex
        self.job = job
        self.phone = phone
        self.email = email
        self.location = location
        self.declaration = declaration

    def to_dict(self):
        ret = OrderedDict()
        ret[u'id'] = self.id
        ret[u'姓名'] = self.name
        ret[u'性别'] = self.sex
        ret[u'职业'] = self.job
        ret[u'联系电话'] = self.phone
        ret[u'邮箱'] = self.email
        ret[u'所在地区'] = self.location
        ret[u'参赛宣言'] = self.declaration
        ret[u'报名时间'] = int(time.mktime(self.create_time.timetuple()))
        ret[u'照片'] = [photo.to_dict() for photo in self.photos] if self.photos else []
        ret[u'视频'] = [video.to_dict() for video in self.videos] if self.videos else []
        return ret

    def to_eng_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sex': self.sex,
            'job': self.job,
            'phone': self.phone,
            'email': self.email,
            'location': self.location,
            'declaration': self.declaration,
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
        self.key = key

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user.id,
            'hash': self.hash,
            'key': self.key
        }
