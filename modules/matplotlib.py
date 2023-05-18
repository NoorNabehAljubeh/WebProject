
from matplotlib import pyplot


def generate_bar_chart(data):
    # Generate and customize your bar chart using matplotlib.pyplot functions
    plt.bar(data['x'], data['y'])
    plt.xlabel('X-axis label')
    plt.ylabel('Y-axis label')
    plt.title('Bar Chart')
    plt.show()
