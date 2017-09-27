from SignInApp.mainApp import app, db
from SignInApp.models import Member
from flask_script import Manager, prompt_bool
import requests
from spreadsheet import sheet
from dues import transactions, member_info

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
def if_none_attendance():
	for member in Member.query.all():
		if member.attendance is None:
			print("EID: ", member.eid)
			attendance = int(input("How many meetings have they attended? "))
			member.attendance = attendance
			db.session.commit()

@manager.command
def get_from_sheet():
	row_index = 2
	end_index = 725

	for index in range(row_index, end_index):
		if str(sheet.cell(index, 3).value):
			eid = str(sheet.cell(index, 3).value).lower()
			member = Member.get_by_eid(eid)
			if not member is None:
				# member.firstName = str(sheet.cell(index, 1).value).title()
				# member.lastName = str(sheet.cell(index, 2).value).title()
				# member.email = str(sheet.cell(index, 4).value).lower()
				# member.attendance = int(sheet.cell(index, 11).value)
				# if sheet.cell(index, 8).value:
					# member.dues = int(sheet.cell(index, 8).value)
				# else:
					# member.dues = 0
				if sheet.cell(index, 8).value:
					member.attendance = int(sheet.cell(index, 8).value)
				else:
					member.attendance = 0
				# if sheet.cell(index, 5).value:
					# member.year = str(sheet.cell(index, 5).value)
				# else:
					# member.year = ""
				# if sheet.cell(index, 7).value:
					# member.comments = str(sheet.cell(index, 7).value)
				# else:
					# member.comments = ""
				# member.rowOnSheet = index
				db.session.commit()
				print("I updated the information for", member.firstName, member.lastName)
			else:
				eid = str(sheet.cell(index, 3).value).lower()
				firstName = str(sheet.cell(index, 1).value).title()
				lastName = str(sheet.cell(index, 2).value).title()
				email = str(sheet.cell(index, 4).value).lower()
				dues = 0
				# # attendance = int(sheet.cell(index, 11).value)
				# if sheet.cell(index, 8).value:
				# 	dues = int(sheet.cell(index, 8).value)
				# else:
				# 	dues = 0
				if sheet.cell(index, 8).value:
					attendance = int(sheet.cell(index, 8).value)
				else:
					attendance = 0
				# if sheet.cell(index, 5).value:
				# 	year = str(sheet.cell(index, 5).value)
				# else:
				# 	year = ""
				# if sheet.cell(index, 7).value:
				# 	comments = str(sheet.cell(index, 7).value)
				# else:
				# 	comments = ""
				rowOnSheet = index
				member = Member(eid = eid, firstName = firstName, lastName = lastName, email = email, dues = dues, attendance = attendance, rowOnSheet = rowOnSheet)
				db.session.add(member)
				print("I added", firstName, lastName)
				db.session.commit()
				# print("He/she is not in the database.")
		else:
			print("There is no one on row", index)

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
def add_dues():
	addDues = True

	while addDues:
		eid = str(input("EID: "))
		member = Member.get_by_eid(eid)
		if not member is None:
			dues = int(input("How much dues do you want to reset it to? "))
			member.dues = dues
			db.session.commit()

		answer = input("Do you want to continue (y/n)? ")
		if answer == 'y':
			addDues = True
		else:
			addDues = False

@manager.command
def get_info_reports():
	row_index = 2
	end_index = 300

	for index in range(row_index, end_index):
		if str(member_info.cell(index, 3).value):
			eid = str(member_info.cell(index, 3).value).lower()
			member = Member.get_by_eid(eid)
			if not member is None:
				member.firstName = str(member_info.cell(index, 1).value).title()
				member.lastName = str(member_info.cell(index, 2).value).title()
				member.email = str(member_info.cell(index, 4).value).lower()
				# member.attendance = int(sheet.cell(index, 11).value)
				# if sheet.cell(index, 8).value:
				# 	member.dues = int(sheet.cell(index, 8).value)
				# else:
				# 	member.dues = 0
				# if sheet.cell(index, 9).value:
				# 	member.attendance = int(sheet.cell(index, 9).value)
				# else:
				# 	member.attendance = 0
				# if sheet.cell(index, 5).value:
				# 	member.year = str(sheet.cell(index, 5).value)
				# else:
				# 	member.year = ""
				if member_info.cell(index, 6).value:
					member.comments = str(member_info.cell(index, 6).value)
				else:
					member.comments = ""
				# gotDues = False
				# for second_index in range(row_index, end_index):
				# 	if str(transactions.cell(second_index, 4).value).lower() == (member.firstName + ' ' + member.lastName).lower():
				# 		member.dues = int(transactions.cell(second_index, 2).value)
				# 		gotDues = True
				# if gotDues == False:
				# 	member.dues = 0
				# member.rowOnSheet = index
				db.session.commit()
				print("I updated the information for", member.firstName, member.lastName)
			else:
				# print("I have started here.")
				eid = str(member_info.cell(index, 3).value).lower()
				firstName = str(member_info.cell(index, 1).value).title()
				lastName = str(member_info.cell(index, 2).value).title()
				email = str(member_info.cell(index, 4).value).lower()
				dues = 0
				# attendance = int(sheet.cell(index, 11).value)
				# if sheet.cell(index, 8).value:
				# 	dues = int(sheet.cell(index, 8).value)
				# else:
				# 	dues = 0
				# if sheet.attendance(index, 9).value:
				# 	attendance = int(sheet.cell(index, 9).value)
				# else:
				# 	attendance = 0
				# if sheet.cell(index, 5).value:
				# 	year = str(sheet.cell(index, 5).value)
				# else:
				# 	year = ""
				if member_info.cell(index, 6).value:
					comments = str(member_info.cell(index, 6).value)
				else:
					comments = ""
				# gotDues = False
				# print("I have reached here.")
				# for second_index in range(row_index, end_index):
				# 	if str(transactions.cell(second_index, 4).value).lower() == (firstName + ' ' + lastName).lower():
				# 		dues = int(transactions.cell(second_index, 2).value)
				# 		gotDues = True
				# if gotDues == False:
				# 	dues = 0
				# rowOnSheet = index
				member = Member(eid = eid, firstName = firstName, lastName = lastName, email = email, dues = dues, comments = comments)
				db.session.add(member)
				print("I added", firstName, lastName)
				db.session.commit()
		else:
			print("There is no one on row", index)

@manager.command
def get_dues():
	trans_start_index = 2
	trans_end_index = 200

	transactions_unmatched = []

	for trans_index in range(trans_start_index, trans_end_index):
		fullName = str(transactions.cell(trans_index, 4).value).lower()
		foundMatch = False

		for member in Member.query.all():
			fullNameRecord = (member.firstName + " " + member.lastName).lower()
			if fullNameRecord == fullName:
				foundMatch = True
				if member.dues == 0:
					dues = transactions.cell(trans_index, 2).value
					member.dues = int(dues.split("$")[1].split(".")[0])
					db.session.commit()
					print("I have added", dues, "to", fullName)

		if not foundMatch:
			transactions_unmatched.append(fullName)


	print("I have not found matches for the following names: ")
	for name in transactions_unmatched:
		print(name)

@manager.command
def get_info():
	eid = str(input("EID: "))
	member = Member.get_by_eid(eid)
	if not member is None:
		print("Name: " + str(member.firstName) + " " + str(member.lastName))
		print("EID: " + str(member.eid))
		print("Email: " + str(member.email))
		print("Meetings Attended: " + str(member.attendance))
		print("Dues: $" + str(member.dues))

@manager.command
def write_to_sheet():
	row_index = 2
	end_index = 1000

	new_row_start = int(input("What row do you want to start at? "))

	column = int(input("What is the column for attendance? "))

	for member in Member.query.filter_by(atLatestMeeting = True):
		if member.rowOnSheet is not None and member.rowOnSheet != 0:
			print("Row: ", member.rowOnSheet)
			sheet.update_cell(member.rowOnSheet, column, "X")
			member.atLatestMeeting = False
			# if not str(sheet.cell(member.rowOnSheet, 1).value):
			# 	sheet.update_cell(member.rowOnSheet, 1, member.firstName)
			# if not str(sheet.cell(member.rowOnSheet, 2).value):
			# 	sheet.update_cell(member.rowOnSheet, 2, member.lastName)
			# if not str(sheet.cell(member.rowOnSheet, 4).value):
			# 	sheet.update_cell(member.rowOnSheet, 4, member.email)
			print("I updated attendance in column", column, "for", member.firstName, member.lastName)
		else:
			for index in range(new_row_start, end_index):
				if not str(sheet.cell(index, 1).value) and not str(sheet.cell(index, 2).value) and not str(sheet.cell(index, 3).value):
					print("Row: ", index)
					sheet.update_cell(index, 1, member.firstName)
					sheet.update_cell(index, 2, member.lastName)
					sheet.update_cell(index, 3, member.eid)
					sheet.update_cell(index, 4, member.email)
					sheet.update_cell(index, column, "X")
					member.rowOnSheet = index
					member.atLatestMeeting = False
					db.session.commit()
					print("I added in the info for", member.firstName, member.lastName, "and updated attendance in column", column)
					break;
		

if __name__ == '__main__':
	manager.run()