from SignInApp.mainApp import app, db
from SignInApp.models import Member
from flask_script import Manager, prompt_bool
import requests
from spreadsheet import sheet

manager = Manager(app)

@manager.command
def initdb():
	db.create_all()
	print('Initialized the database.')

@manager.command
def dropdb():
	if prompt_bool(
		"Are you sure you want to lose all your data?"):
		db.drop_all()
		print('Dropped the database.')

@manager.command
def get_from_sheet():
	row_index = 2
	end_index = 1000

	for index in range(row_index, end_index):
		if str(sheet.cell(index, 3).value):
			eid = str(sheet.cell(index, 3).value).lower()
			member = Member.get_by_eid(eid)
			if not member is None:
				member.firstName = str(sheet.cell(index, 1).value).title()
				member.lastName = str(sheet.cell(index, 2).value).title()
				member.email = str(sheet.cell(index, 4).value).lower()
				member.attendance = int(sheet.cell(index, 11).value)
				if sheet.cell(index, 6).value:
					member.dues = int(sheet.cell(index, 6).value)
				else:
					member.dues = 0
				member.rowOnSheet = index
				db.session.commit()
				print("I updated the information for", member.firstName, member.lastName)
			else:
				eid = str(sheet.cell(index, 3).value).lower()
				firstName = str(sheet.cell(index, 1).value).title()
				lastName = str(sheet.cell(index, 2).value).title()
				email = str(sheet.cell(index, 4).value).lower()
				attendance = int(sheet.cell(index, 11).value)
				if sheet.cell(index, 6).value:
					dues = int(sheet.cell(index, 6).value)
				else:
					dues = 0
				rowOnSheet = index
				member = Member(eid = eid, firstName = firstName, lastName = lastName, email = email, attendance = attendance, dues = dues, rowOnSheet = rowOnSheet)
				db.session.add(member)
				print("I added", firstName, lastName)
				db.session.commit()

@manager.command
def reset_attendance():
	eid = str(input("EID: "))
	member = Member.get_by_eid(eid)
	if not member is None:
		meetings_attended = int(input("How many meetings do you want to reset it to? "))
		member.attendance = meetings_attended
		member.atLatestMeeting = False
		db.session.commit()

@manager.command
def write_to_sheet():
	row_index = 2
	end_index = 1000

	column = int(input("What is the column for attendance? "))

	for member in Member.query.filter_by(atLatestMeeting = True):
		if member.rowOnSheet != 0:
			sheet.update_cell(member.rowOnSheet, column, "X")
			member.atLatestMeeting = False
			if not str(sheet.cell(member.rowOnSheet, 1).value):
				sheet.update_cell(member.rowOnSheet, 1, member.firstName)
			if not str(sheet.cell(member.rowOnSheet, 2).value):
				sheet.update_cell(member.rowOnSheet, 2, member.lastName)
			if not str(sheet.cell(member.rowOnSheet, 4).value):
				sheet.update_cell(member.rowOnSheet, 4, member.email)
			print("I updated attendance in column", column, "for", member.firstName, member.lastName)
		else:
			for index in range(row_index, end_index):
				if not str(sheet.cell(index, 1).value) and not str(sheet.cell(index, 2).value) and not str(sheet.cell(index, 3).value):
					sheet.update_cell(index, 1, member.firstName)
					sheet.update_cell(index, 2, member.lastName)
					sheet.update_cell(index, 3, member.eid)
					sheet.update_cell(index, 4, member.email)
					sheet.update_cell(index, column, "X")
					member.atLatestMeeting = False
					print("I added in the info for", member.firstName, member.lastName, "and updated attendance in column", column)
					break;

		db.session.commit()

if __name__ == '__main__':
	manager.run()