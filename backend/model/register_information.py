# -*- coding: utf-8 -*-
from server import db
from datetime import datetime

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
