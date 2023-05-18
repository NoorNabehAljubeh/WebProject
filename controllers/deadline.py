from datetime import datetime, timedelta

@auth.requires_login()
def deadlines():
    # Fetch the list of deadlines from the database
    deadlines = db(db.deadlines).select()

    return dict(deadlines=deadlines)

def check():
    # Check deadlines and send notifications
    if 'email' in session and session.expires > datetime.now():
        email = session.email
        # Perform actions with the email or retrieve additional data from the database
        remaining_time = session.expires - datetime.now()
        return f'Welcome, {email}! Your session will expire in {remaining_time} minutes.'
    else:
        redirect(URL('login'))


# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
@auth.requires_login()
# Function to send notification
def send_notification(deadline_id):
    # Retrieve the deadline information
    deadline = db.deadline(deadline_id)
    if deadline:
        # Send notification to the user (e.g., email)
        mail.send(to=deadline.user_email,
                  subject='Deadline Reminder',
                  message=f"Reminder: {deadline.description} deadline is approaching!")


# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
@auth.requires_login()
def add_deadline():
    # Process the form submission to add a new deadline
    form = SQLFORM(db.deadlines)
    if form.process().accepted:
        response.flash = 'Deadline Added'
    elif form.errors:
        response.flash = 'Deadline has Problem'
    else:
        response.flash = 'please fill out the Deadline form'

    return dict(form=form)  

    # if request.method == 'POST':
    #     description = request.post_vars.description
    #     deadline_date = request.post_vars.deadline_date

    #     # Parse the deadline date and time
    #     deadline_datetime = datetime.strptime(deadline_date, '%Y-%m-%d %H:%M:%S')

    #     # Insert the new deadline into the database
    #     db.deadlines.insert(description=description, deadline_date=deadline_datetime)

    # # Redirect back to the index page after adding the deadline
    # redirect(URL('default', 'index'))