from gluon.migrator import update_table

def upgrade(migrate):
    if migrate:
        # Add the course_code field to the auth_user table
        update_table(migrate, 'auth_user',
                     fields=[Field('course_code', 'string', length=50, default='')])
