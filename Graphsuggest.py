from graphics import GraphWin,Point, Text
from graphics import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas as pd
from load_data import data

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
    x_start = 120  # Position them 100px from the left side of the window

    # Create a list of rectangles and placeholder texts for all variables
    for i in range(visible_count):
        rect = Rectangle(Point(x_start, y_start + i * 70), Point(x_start + 550, y_start + i * 70 + 50))  # Wider for centering
        rect.setFill("lightgrey")
        rectangles.append(rect)

        text = Text(rect.getCenter(), "")  # Placeholder text
        text.setSize(12)  # Adjust font size as needed
        texts.append(text)

    def draw_visible():
        """Draw exactly 6 variables based on the scroll offset."""
        # Undraw all current items
        for rect in rectangles:
            rect.undraw()
        for text in texts:
            text.undraw()

        # Determine which variables to display
        start = scroll_offset * visible_count
        end = start + visible_count

        for i in range(start, min(end, len(data.columns))):
            index = i - start
            rect = rectangles[index]
            text = texts[index]

            # Update rectangle color based on selection
            rect.setFill("lightgreen" if data.columns[i] in selected else "lightgrey")

            # Update text to match variable name
            text.setText(data.columns[i])

            # Draw the updated rectangle and text
            rect.draw(win)
            text.draw(win)

    draw_visible()

    # Submit button positioned at the bottom center
    submit_btn = Rectangle(Point(300, 520), Point(500, 570))  # Adjusted for bottom
    submit_btn.setFill("green")
    submit_btn.draw(win)
    submit_text = Text(submit_btn.getCenter(), "Submit")
    submit_text.setTextColor("white")
    submit_text.draw(win)

    while True:
        click = win.getMouse()

        if 300 < click.x < 500 and 520 < click.y < 570:  # Submit button clicked
            break

        # Check for clicks on the up arrow (right side)
        if 710 < click.x < 770 and 160 < click.y < 200:  # Up arrow clicked
            if scroll_offset > 0:
                scroll_offset -= 1
                draw_visible()

        # Check for clicks on the down arrow (right side)
        if 710 < click.x < 770 and 410 < click.y < 440:  # Down arrow clicked
            if (scroll_offset + 1) * visible_count < len(data.columns):
                scroll_offset += 1
                draw_visible()

        # Check for clicks on visible rectangles
        start = scroll_offset * visible_count
        end = start + visible_count

        for i in range(start, min(end, len(data.columns))):
            index = i - start
            rect = rectangles[index]
            text = texts[index]

            if rect.getP1().x < click.x < rect.getP2().x and rect.getP1().y < click.y < rect.getP2().y:
                col_name = data.columns[i]
                if col_name in selected:
                    selected.remove(col_name)
                    rect.setFill("lightgrey")
                elif len(selected) < 3:
                    selected.append(col_name)
                    rect.setFill("lightgreen")
                break

    win.close()
    return selected


def GraphOptions(selected):
    win = GraphWin("Graph Options", 800, 600)

    bg_image = Image(Point(400, 300), "pic.gif")
    bg_image.draw(win)

    title = Text(Point(400, 30), f"Select a Graph for {', '.join(selected)}")
    title.setSize(16)
    title.setTextColor("white")
    title.draw(win)

    options = []
    if len(selected) == 1:
        if IsNumerical(selected[0]):
            options = ["Histogram", "Boxplot"]
        elif IsCategorical(selected[0]):
            options = ["Bar Chart", "Pie Chart"]
    elif len(selected) == 2:
        if IsNumerical(selected[0]) and IsNumerical(selected[1]):
            options = ["Scatter Plot", "Line Chart"]
        elif IsCategorical(selected[0]) and IsCategorical(selected[1]):
            options = ["Stacked Bar Chart"]
        elif (IsNumerical(selected[0]) and IsCategorical(selected[1])) or \
                (IsCategorical(selected[0]) and IsNumerical(selected[1])):
            options = ["Heatmap"]
    elif len(selected) == 3:
        if all(IsNumerical(col) for col in selected):
            options = ["3D Scatterplot"]
        elif len([col for col in selected if IsNumerical(col)]) == 2 and \
                len([col for col in selected if IsCategorical(col)]) == 1:
            # Rearranging the selected variables so the categorical one is always on the y-axis
            numerical_vars = [col for col in selected if IsNumerical(col)]
            categorical_var = [col for col in selected if IsCategorical(col)][0]

            # In a heatmap, we expect categorical on the y-axis and numericals on x and values
            options = ["Heatmap With Two Numericals"]

            # Re-order selected to ensure categorical is on the y-axis
            selected = [numerical_vars[0], numerical_vars[1], categorical_var]

    y_base = 200
    vertical_spacing = 100
    buttons = []
    for i, option in enumerate(options):
        rect = Rectangle(Point(300, y_base + i * vertical_spacing), Point(500, y_base + 50 + i * vertical_spacing))
        rect.setFill("lightgreen")
        rect.draw(win)

        text = Text(rect.getCenter(), option)
        text.setTextColor("black")
        text.draw(win)

        buttons.append((rect, option))

    back_arrow = Line(Point(50, 50), Point(100, 50))
    back_arrow.setArrow('first')
    back_arrow.setWidth(3)
    back_arrow.setFill("white")
    back_arrow.draw(win)

    selected_option = None
    while True:
        click = win.getMouse()

        for rect, option in buttons:
            if rect.getP1().x < click.x < rect.getP2().x and rect.getP1().y < click.y < rect.getP2().y:
                selected_option = option
                break

        if 50 < click.x < 100 and 40 < click.y < 60:
            win.close()
            return None  # Indicate that the user wants to go back

        if selected_option:
            break

    win.close()
    return selected_option, selected  # Return the modified selected variables


def DisplayGraph(filename, title_text):
    win = GraphWin("Graph Viewer", 800, 600)


    title = Text(Point(400, 30), title_text)
    title.setSize(16)
    title.setTextColor("white")
    title.draw(win)


    graph_image = Image(Point(400, 300), filename)
    graph_image.draw(win)


    back_arrow = Line(Point(50, 50), Point(100, 50))  # Starting at (50, 50) to (100, 50)
    back_arrow.setArrow('first')  # Arrow facing left
    back_arrow.setWidth(3)
    back_arrow.setFill("white")
    back_arrow.draw(win)



    while True:
        click = win.getMouse()
        if 700 < click.x < 800 and 550 < click.y < 600:  # Close button region
            break
        if 50 < click.x < 100 and 40 < click.y < 60:  # Back arrow region
            win.close()
            return True  # Indicating that the user wants to go back
    win.close()
    return False


def main():
    while True:
        selected_variables = VariableSelection()

        if selected_variables:
            while True:  # Add an inner loop for navigation between variable and graph selection
                selected_graph, selected_variables = GraphOptions(selected_variables)

                if selected_graph is None:  # Back arrow clicked
                    break  # Go back to the variable selection screen

                # Generate and display the selected graph
                if selected_graph == "Histogram":
                    Histogram(selected_variables[0], "graph.png")
                    title_text = f"Histogram of {selected_variables[0]}"
                elif selected_graph == "Boxplot":
                    Boxplot(selected_variables[0], "graph.png")
                    title_text = f"Box Plot of {selected_variables[0]}"
                elif selected_graph == "Bar Chart":
                    Barchart(selected_variables[0], "graph.png")
                    title_text = f"Bar Chart of {selected_variables[0]}"
                elif selected_graph == "Pie Chart":
                    Piechart(selected_variables[0], "graph.png")
                    title_text = f"Pie Chart of {selected_variables[0]}"
                elif selected_graph == "Scatter Plot":
                    ScatterPlot(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Scatter Plot: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Line Chart":
                    LineChart(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Line Chart: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Stacked Bar Chart":
                    StackedBarChart(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Stacked Bar Chart: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Heatmap":
                    Heatmap(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Heatmap: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "3D Scatterplot":
                    ThreeDScatterplot(selected_variables[0], selected_variables[1],selected_variables[2],"graph.png",data=data)
                    title_text = f"3D Scatter Plot for {selected_variables[0]} vs {selected_variables[1]} vs {selected_variables[2]} "
                elif selected_graph == "Heatmap With Two Numericals":
                    HeatmapWithTwoNumericals(selected_variables[0], selected_variables[1], selected_variables[2], "graph.png", data=data, agg_func='mean')
                    title_text = f"Heatmap: {selected_variables[0]} vs {selected_variables[1]} vs {selected_variables[2]}"

                else:
                    print("Graph type not implemented!")

                if DisplayGraph("graph.png", title_text):
                    continue  # User clicked back in the graph viewer, return to graph options
                else:
                    break
main()
