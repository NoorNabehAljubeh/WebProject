# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from gluon.tools import Auth
from datetime import datetime, timedelta


import time
# Initialize the Auth object
auth = Auth(db)



TIMEOUT = 1 * 60  # Timeout time in seconds
PATH_ON_TIMEOUT = '/%s/default/logout' % request.application

def check_session_timeout():
    if session.lastrequest and session.lastrequest < time.time() - TIMEOUT and request.env.path_info != PATH_ON_TIMEOUT:
        # Perform logout or any other desired action on timeout
        redirect(PATH_ON_TIMEOUT)

    session.lastrequest = time.time()





@auth.requires_login()
def index():
    check_session_timeout()
    courses = db.executesql("SELECT * FROM courses", as_dict=True)
    return dict(courses=courses)

def logout():
    # Code to perform logout (clear session variables, redirect to login page, etc.)
    session.clear()
    redirect(URL('default', 'user/login'))



# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
@auth.requires_login()    
def list_students():

    students = db.executesql("SELECT * FROM auth_user", as_dict=True)

    return dict(students=students)

# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
@auth.requires_login()
def addStudentForm():

    return locals()

def addroom():


    form = SQLFORM(db.rooms)

    if form.process().accepted:
        response.flash = 'Room added'
    elif form.errors:
        response.flash = 'Room has Problem'
    else:
        response.flash = 'please fill out the Room form'

    return dict(form=form)    

def add_user():

    name = request.vars['name']
    email = request.vars['email']

    return locals()

# Restrict access to a page to authenticated users
@auth.requires_login()
def showcourses():
    grid = SQLFORM.grid(db.courses,csv=False,deletable=False,editable=False)
    return dict(grid=grid)



# def testviews():
   

#     return locals()


# def city():

#     grid = SQLFORM.grid(db.city)

#     return locals()
    


auth.define_tables(username=False)

# Function to create a session with expiration time
def create_session(user_id, is_admin=False):
    # Set session variables
    session.user_id = user_id
    session.is_admin = is_admin
    session.session_expires = datetime.now() + timedelta(minutes=1)  # Set expiration time to 30 minutes

    # Redirect to the appropriate page
    if is_admin:
        redirect(URL('admin', 'dashboard'))
    else:
        redirect(URL('default', 'index'))

# Controller action for user login
def login():
    form = auth.login()
    if form.process().accepted:
        # Login successful
        user = db.auth_user(form.vars.id)  # Assuming you have an "auth_user" table in your database
        if user and user.is_admin:  # Assuming you have an "is_admin" field in your "auth_user" table
            create_session(user.id, is_admin=True)
        else:
            create_session(user.id)
        redirect(URL('default', 'index'))
    return dict(form=form)

# Controller action for checking session expiration
def check_session():
    if 'session_expires' in session and datetime.now() > session.session_expires:
        # Session has expired, clear session variables and redirect to login page
        session.clear()
        redirect(URL('default', 'login'))

# Decorator for requiring authentication and session expiration check
def requires_login(f):
    def decorated(*args, **kwargs):
        if not session.user_id:
            redirect(URL('default', 'login'))
        check_session()
        return f(*args, **kwargs)
    return decorated

# Example usage of the requires_login decorator
@requires_login
def some_protected_page():
    # Code for the protected page
    return dict()

# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
def addSchedule():

    form = SQLFORM(db.courseSchedules)
    if form.process().accepted:
       response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form)

# Restrict access to a page to authenticated users
@auth.requires_login()
def courses():

    grid = SQLFORM.grid(db.courses)

    return dict(grid=grid)

def deadlines():

    grid = SQLFORM.grid(db.deadlines)

    return dict(grid=grid)    

# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
@auth.requires_login()
def addcourse():


    form = SQLFORM(db.courses)
    if form.process().accepted:
       response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form)

# Define the auth tables
auth.define_tables(username=True, signature=False)

# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
@auth.requires_login()
def addStudent():
    if request.vars['firstName'] and request.vars['password']:
        first_name = request.vars['firstName']
        last_name = request.vars['lastName']
        email = request.vars['email']
        password = request.vars['password']

        # Save the student details including the password
        student_id = db.auth_user.insert(first_name=first_name, last_name=last_name, email=email, password=password)

        # # Log in the student automatically
        # auth.login_user(student_id)

        # Redirect to the desired page after successful registration and login
        redirect(URL('index'))
    else:
        redirect(URL('addStudentForm'))

    return locals()

# Restrict access to a page to authenticated users
@auth.requires_login()
def details():

    if request.vars['id']:
        id = request.vars['id']
        students = db.executesql("SELECT * FROM auth_user WHERE id=" + id, as_dict=True)

    return dict(student=students[0], students=students)


# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
@auth.requires_login()
def delete():

    if request.vars['id']:
        id = request.vars['id']

        db.executesql("DELETE FROM auth_user WHERE id=" + id)
    
    redirect(URL('list_students'))


def register():
    # Customize the registration form
    db.auth_user.email.widget = SQLFORM.widgets.email.widget
    db.auth_user.password.widget = SQLFORM.widgets.password.widget

    # Create the registration form using the "auth_user" table
    form = SQLFORM(db.auth_user)

    if form.validate():
        # Save the form data to the "auth_user" table
        student_id = db.auth_user.insert(**db.auth_user._filter_fields(form.vars))

        # Perform any additional operations or redirection as needed

    return dict(form=form)

def coursesSchedules():
    grid = SQLFORM.grid(
        db.courses.scheduleId == db.courseschedule.id,
        fields=[
            db.courses.name, db.courses.code, db.courses.instructor,
            db.courses.prerequisites, db.courses.capacity, db.courseschedule.days,
            db.courseschedule.startTime, db.courseschedule.endTime, db.courseschedule.RoomNo
        ],
        csv=False, editable=False, deletable=False, details=False, create=False,
        selectable=lambda ids: redirect(URL('default', 'StudentSchedule', vars=dict(id=ids)))
    )
    return dict(grid=grid)


def StudentSchedule():
    grid = SQLFORM.grid(
        (db.courses.code.belongs(db.studentsreg.courseId)) &
        (db.students.id.belongs(db.studentsreg.studentId)),
        fields=[
            db.students.id, db.courses.code, db.courses.name,
            db.courses.instructor, db.courses.prerequisites, db.courses.capacity,
            db.courseschedule.days, db.courseschedule.startTime,
            db.courseschedule.endTime, db.courseschedule.RoomNo
        ],
        csv=False, editable=False, deletable=False, details=False, create=False
    )
    return dict(grid=grid)



def delete():

    if request.vars['id']:
        id = request.vars['id']

        db.executesql("DELETE FROM studentsreg WHERE id=" + id)
    
    redirect(URL('StudentSchedule'))

#     def create_admin_account():
#     # Check if the admin account already exists
#     if not db(db.auth_user.email == 'admin@example.com').count():
#         # Create the admin user account
#         user_id = db.auth_user.insert(
#             first_name='Admin',
#             last_name='User',
#             email='admin@example.com',
#             password=auth.hash('adminpassword')  # Replace 'adminpassword' with the desired password
#         )
        
#         # Assign the admin group membership to the user
#         group_id = auth.id_group('admin')
#         db.auth_membership.insert(user_id=user_id, group_id=group_id)
        
#         # Display a success message
#         message = 'Admin account created successfully.'
#     else:
#         # Display an error message if the admin account already exists
#         message = 'Admin account already exists.'
    
#     return dict(message=message)





# def admin_page():
#     admin_url = URL('admin', 'default', 'index')
#     return dict(admin_url=admin_url)






# def addCourse():

#     if request.get_vars:
#         code = request.vars['code']
#         name = request.vars['name']
#         description = request.vars['description']
#     else:
#         redirect(URL('addCourseForm'))


#     return locals()

# def addCourseForm():

#     return locals()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)



# Call check_session_timeout() before any controller action that requires session authentication
check_session_timeout()