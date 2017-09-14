from datetime import datetime
from SignInApp import db
from flask_sqlalchemy import SQLAlchemy
import json
import requests

num_gms_semester = 13
num_gms_free = 2
year_dues = 70
semester_dues = 45

class Member(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	eid = db.Column(db.String(8), unique = True)
	firstName = db.Column(db.String(80))
	lastName = db.Column(db.String(80))
	email = db.Column(db.String(80))
	attendance = db.Column(db.Integer)
	dues = db.Column(db.Integer)
	atLatestMeeting = db.Column(db.Boolean)
	rowOnSheet = db.Column(db.Integer)

	@staticmethod
	def get_by_eid(eid):
		return Member.query.filter_by(eid=eid).first()

	@staticmethod
	def check_attendance(dues, attendance):
		if dues == 70:
			return True
		elif dues == 45:
			return attendance <= num_gms_semester
		elif dues == 0:
			return attendance <= num_gms_free
		return False



