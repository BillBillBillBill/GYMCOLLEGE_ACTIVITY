# -*- coding: utf-8 -*-
from server import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.create_time = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
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
