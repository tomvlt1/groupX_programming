from graphics import GraphWin, Rectangle, Point, Text, Image, Line
from graphics import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


try:
    data = pd.read_csv('laliga.csv')  # Replace with the actual path to your dataset
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: Dataset file not found. Please check the file path.")
    exit()

data = data.dropna()

def IsNumerical(column):
    return data[column].dtype in ['int64', 'float64']


def IsCategorical(column):
    return data[column].dtype == 'object' or pd.api.types.is_categorical_dtype(data[column])



def Histogram(column, filename):
    plt.figure()
    plt.hist(data[column], bins=10, color='#006400', alpha=0.7, edgecolor='black')  # Dark Green
    plt.title(f'Histogram of {column}', color='white')
    plt.xlabel(column, color='white')
    plt.ylabel('Frequency', color='white')
    plt.savefig(filename)
    plt.close()


def Boxplot(column, filename):
    plt.figure()
    data.boxplot(column=column, patch_artist=True, sym="ro", boxprops=dict(facecolor='#006400', color='black'))  # Dark Green
    plt.title(f'Box Plot of {column}', color='white')
    plt.savefig(filename)
    plt.close()


def Barchart(column, filename):
    plt.figure()
    counts = data[column].value_counts()
    plt.bar(counts.index, counts.values, color='#006400', alpha=0.7, edgecolor='black')  # Dark Green
    plt.title(f'Bar Chart of {column}', color='white')
    plt.xlabel('Categories', color='white')
    plt.ylabel('Counts', color='white')
    plt.savefig(filename)
    plt.close()


def Piechart(column, filename):
    plt.figure()
    counts = data[column].value_counts()
    num_colors = len(counts)
    dark_green_shades = plt.cm.Greens(np.linspace(0.5, 1, len(counts)))  # Darker shades of green
    explode = [0.2 if count == max(counts.values) else 0 for count in counts.values]
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90,
            explode=explode, colors=dark_green_shades, counterclock=False, shadow=True)
    plt.title(f'Pie Chart of {column}', color='white')
    plt.savefig(filename)
    plt.close()


def ScatterPlot(x, y, filename):
    plt.figure()
    plt.scatter(data[x], data[y], color='#006400', alpha=0.7, edgecolor='black')  # Dark Green
    plt.title(f'Scatter Plot: {x} vs {y}', color='white')
    plt.xlabel(x, color='white')
    plt.ylabel(y, color='white')
    plt.savefig(filename)
    plt.close()


def LineChart(x, y, filename):
    plt.figure()
    plt.plot(data[x], data[y], color='#006400', alpha=0.7)  # Dark Green
    plt.title(f'Line Chart: {x} vs {y}', color='white')
    plt.xlabel(x, color='white')
    plt.ylabel(y, color='white')
    plt.savefig(filename)
    plt.close()


def StackedBarChart(x, y, filename):
    plt.figure()
    cross_tab = pd.crosstab(data[x], data[y])
    cross_tab.plot(kind='bar', stacked=True, colormap='Greens')  # Darker green shades are used here
    plt.title(f'Stacked Bar Chart: {x} vs {y}', color='white')
    plt.savefig(filename)
    plt.close()


def Heatmap(x, y, filename):
    pivot_table = data.pivot_table(index=x, columns=y, aggfunc='size', fill_value=0)
    plt.figure()
    plt.imshow(pivot_table, cmap='Greens', interpolation='nearest')  # Darker green shades for the heatmap
    plt.colorbar(label='Counts')
    plt.title(f'Heatmap: {x} vs {y}', color='white')
    plt.savefig(filename)
    plt.close()




def HeatmapWithTwoNumericals(cat_var, numvar1, numvar2, filename, data, agg_func='mean'):
    try:
        if not pd.api.types.is_numeric_dtype(data[numvar2]):
            print(f"Column '{numvar2}' is not numeric. Attempting to convert...")
            data[numvar2] = pd.to_numeric(data[numvar2], errors='coerce')

        if data[numvar2].isna().all():
            raise ValueError(f"Column '{numvar2}' cannot be converted to numeric or contains only invalid values.")

        pivot_table = data.pivot_table(index=cat_var, columns=numvar1, values=numvar2, aggfunc=agg_func, fill_value=0)

        plt.imshow(pivot_table, cmap='coolwarm', aspect='auto', interpolation='nearest')
        plt.colorbar(label=f'{numvar2} ({agg_func})')
        plt.title(f'Heatmap of {numvar2} by {cat_var} and {numvar1} ({agg_func})', color='black')

        plt.xticks(ticks=np.arange(len(pivot_table.columns)), labels=pivot_table.columns, rotation=45, ha='right')
        plt.yticks(ticks=np.arange(len(pivot_table.index)), labels=pivot_table.index)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        print(f"Heatmap saved to {filename}")

    except Exception as e:
        print(f"Error: {e}")





def ThreeDScatterplot(numvar1, numvar2, numvar3, filename, data):
    try:
        # Extract data
        x = data[numvar1]
        y = data[numvar2]
        z = data[numvar3]

        # Create subplots for projections
        fig, axs = plt.subplots(1, 3, figsize=(8, 3), dpi=100)

        # XY Projection
        sc1 = axs[0].scatter(x, y, c=z, cmap='viridis')
        axs[0].set_xlabel(numvar1)
        axs[0].set_ylabel(numvar2)
        axs[0].set_title(f'{numvar1} vs {numvar2}')
        axs[0].grid(True)

        # XZ Projection
        sc2 = axs[1].scatter(x, z, c=y, cmap='plasma')
        axs[1].set_xlabel(numvar1)
        axs[1].set_ylabel(numvar3)
        axs[1].set_title(f'{numvar1} vs {numvar3}')
        axs[1].grid(True)

        # YZ Projection
        sc3 = axs[2].scatter(y, z, c=x, cmap='coolwarm')
        axs[2].set_xlabel(numvar2)
        axs[2].set_ylabel(numvar3)
        axs[2].set_title(f'{numvar2} vs {numvar3}')
        axs[2].grid(True)


        cbar = fig.colorbar(sc1, ax=axs, orientation='horizontal', fraction=0.05, pad=0.1)
        cbar.set_label('Color scale')
        plt.tight_layout(pad=5.0)

        plt.tight_layout()
        plt.savefig(filename)
        plt.close()  # Close to prevent display in some environments
    except Exception as e:
        print(f"Error: {e}")


def VariableSelection():
    win = GraphWin("Variable Selector", 800, 600)
    title = Text(Point(400, 40), "Select Variables (Up to 3)")
    title.setSize(20)
    title.setTextColor("white")
    title.draw(win)

    # Create up and down arrow shapes on the right side of the page
    up_arrow = Polygon(Point(740, 170), Point(710, 200), Point(770, 200))  # Smaller triangle pointing up
    up_arrow.setFill("green")
    up_arrow.draw(win)

    down_arrow = Polygon(Point(740, 440), Point(710, 410), Point(770, 410))  # Smaller triangle pointing down
    down_arrow.setFill("green")
    down_arrow.draw(win)

    # Variables and scrolling logic
    rectangles = []
    texts = []
    selected = []
    y_start = 100
    visible_count = 6  # Number of items visible at a time
    scroll_offset = 0  # Track the scroll position

    # Shift the x-position of the rectangles and text to the left for centering
 
VariableSelection()