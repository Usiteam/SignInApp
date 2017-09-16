from __future__ import print_function
import sys, os, operator
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from SignInApp.models import Member
from SignInApp import db, app
import requests
import time
import json
import smtplib
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import func 
import ntpath

basedir = os.path.abspath(os.path.dirname(__file__))
date = time.strftime("%m/%d/%Y")

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST' and request.form['enter-eid'] == 'Check In':
		eid = str(request.form['eid'])
		member = Member.get_by_eid(eid.lower())

		if member is None:
			return render_template('dashboard.html', missingInformation = False, notInSystem = True, allowedIn = False, notAllowedIn = False, eid = eid)
		elif member is not None and member.check_attendance(member.dues, member.attendance + 1):
			member.attendance += 1
			member.atLatestMeeting = True
			db.session.commit()

			if not member.email or not member.firstName or not member.lastName:
				needEmail = not member.email
				needFirstName = not member.firstName
				needLastName = not member.lastName
				return render_template('dashboard.html', eid = eid, needEmail = needEmail, needFirstName = needFirstName, needLastName = needLastName, missingInformation = True, notInSystem = False, allowedIn = False, notAllowedIn = False)

			return render_template('dashboard.html', missingInformation = False, notInSystem = False, allowedIn = True, notAllowedIn = False, attendance = member.attendance, dues = member.dues, firstName = member.firstName, lastName = member.lastName, date = date)
		elif member is not None and not member.check_attendance(member.dues, member.attendance + 1):
			return render_template('dashboard.html', missingInformation = False, notInSystem = False, allowedIn = False, notAllowedIn = True, attendance = member.attendance, dues = member.dues, firstName = member.firstName, lastName = member.lastName, date = date)
	return render_template('index.html')

@app.route('/new-member', methods=['POST'])
def new_user():
	if request.method == 'POST':
		eid = str(request.form['eid']).lower()
		firstName = str(request.form['first-name'])
		lastName = str(request.form['last-name'])
		email = str(request.form['email'])
		member = Member(eid = eid, firstName = firstName, lastName = lastName, email = email, attendance=1, dues=0, atLatestMeeting = True, rowOnSheet = 0)
		db.session.add(member)
		db.session.commit()
		return render_template('dashboard.html', notInSystem = False, allowedIn = True, notAllowedIn = False, missingInformation = False, attendance = member.attendance, dues = member.dues, firstName = member.firstName, lastName = member.lastName, date = date)

@app.route('/more-info', methods=['POST'])
def add_info():
	if request.method == 'POST':
		eid = str(request.form['eid'])
		member = Member.get_by_eid(eid.lower())

		if not member.email:
			member.email = str(request.form['email']).lower()
		if not member.firstName:
			member.firstName = str(request.form['first-name']).title()
		if not member.lastName:
			member.lastName = str(request.form['last-name']).title()

		db.session.commit()

		return render_template('dashboard.html', notInSystem = False, allowedIn = True, notAllowedIn = False, missingInformation = False, attendance = member.attendance, dues = member.dues, firstName = member.firstName, lastName = member.lastName, date = date)