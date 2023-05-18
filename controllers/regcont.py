
# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
def addSchedule():

	form = SQLFORM(db.courseschedule)

	if form.process().accepted:
		response.flash = 'form accepted'
	elif form.errors:
		response.flash = 'form has errors'
	else:
		response.flash = 'please fill out the form'

	return dict(form=form)


# Restrict access to a page to authenticated users
@auth.requires_login()
def schedules():

	grid = SQLFORM.grid(db.courseschedule, csv=False)

	return dict(grid=grid)

# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
def addCourse():

	form = SQLFORM(db.courses)

	if form.process().accepted:
		response.flash = 'form accepted'
	elif form.errors:
		response.flash = 'form has errors'
	else:
		response.flash = 'please fill out the form'

	return dict(form=form)



def courses():

	grid = SQLFORM.grid(db.courses)

	return dict(grid=grid)
