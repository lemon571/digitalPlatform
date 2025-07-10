from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    subgroups = db.relationship('Group')

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
