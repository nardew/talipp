import csv

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def thousands_separator(x):
    return f'{int(x):,}'


def draw_graph(csv_file_path):
    x_values = []
    y_values = []
    y2_values = []

    # Open the CSV file and read the values
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            # Assume the first value is x and the second value is y
            x_values.append(int(row[1].replace(",", "")))
            y_values.append(float(row[2]))
            y2_values.append(float(row[4]))

    # Plot the values
    plt.figure(figsize=[10,5]) # You can adjust the figure size as needed
    #plt.plot(x_values, y_values) # You can change the marker style
    plt.plot(x_values, y_values, color='orange')
    plt.plot(x_values, y2_values, color='royalblue')  # You can change the marker style
    plt.title('SMA(20) performance comparison', fontweight='bold', fontname='Helvetica', fontsize=16, color="black") # Add a title to the graph
    plt.xlabel('Input size', color="dimgray") # Label the x-axis
    plt.ylabel('Time [ms]', color="dimgray") # Label the y-axis
    #plt.grid(True) # Add grid lines for better readability
    plt.grid(True, which='both', axis='both', linestyle='-', color='lightgray')
    formatter = FuncFormatter(thousands_separator)
    plt.gca().xaxis.set_major_formatter(formatter)
    x_ticks = [x for x in x_values if x % 10000 == 0]
    if x_values[0] not in x_ticks:
        x_ticks.insert(0, x_values[0])
    if x_values[-1] not in x_ticks:
        x_ticks.append(x_values[-1])
    plt.xticks(ticks=x_ticks, fontname='Helvetica', color="dimgray")
    plt.yticks(color="dimgray")

    end_x = x_values[-1]
    end_y = y_values[-1]
    plt.text(end_x - 0.005 * (max(x_values) - min(x_values)),
             end_y + 1 * (max(y_values) - min(y_values)), 'talipp', fontsize=12, fontweight='bold', ha='right', color='orange', fontname='Helvetica')

    end_y2 = y2_values[-1]
    plt.text(end_x - 0.03 * (max(x_values) - min(x_values)),
             end_y2 - 0.01 * (max(y2_values) - min(y2_values)), 'non-incremental library (talib)', fontsize=12, fontweight='bold', ha='right',
             color='royalblue', fontname='Helvetica')

    #plt.show()
    plt.savefig("sma20-comparison.svg", format='svg', bbox_inches='tight')

if __name__ == "__main__":
    draw_graph('in.csv')
