import applications.WebProject.modules.matplotlib.pyplot as plt
import pandas as pd


# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
def generate_reports():
    # Retrieve data from the database
    course_data = db().select(db.courses.name, db.courses.views)

    # Process the data
    course_df = pd.DataFrame(course_data, columns=['course', 'views'])

    # Generate reports
    enrollment_report = generate_enrollment_report(course_df)
    popularity_report = generate_popularity_report(course_df)

    return dict(enrollment_report=enrollment_report, popularity_report=popularity_report)

# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')    
def generate_enrollment_report(data):
    # Generate enrollment report using pandas and matplotlib
    plt.figure(figsize=(8, 6))
    plt.bar(data['course'], data['views'])
    plt.xlabel('Course')
    plt.ylabel('Views')
    plt.title('Course Enrollment Report')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot to a file or return the plot object
    # If saving to a file:
    # plt.savefig('enrollment_report.png')
    # If returning the plot object:
    # return plt
    
    # Display the plot
    plt.show()

# Restrict access to a page to users with the 'administrator' role
@auth.requires_membership('administrator')
def generate_popularity_report(data):
    # Generate popularity report using pandas and matplotlib
    plt.figure(figsize=(8, 6))
    plt.plot(data['course'], data['views'], marker='o')
    plt.xlabel('Course')
    plt.ylabel('Views')
    plt.title('Course Popularity Report')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot to a file or return the plot object
    # If saving to a file:
    # plt.savefig('popularity_report.png')
    # If returning the plot object:
    # return plt
    
    # Display the plot
    plt.show()