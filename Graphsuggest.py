#In this part of our code, we establish the following:
#the user will have the choice to select the variables he desires to visualise (3 maximum)
#Then, depending on his/her selection, the possible graphs will be depicted on the user interface
#From the possible graphs, the user will choose the one they prefer


from graphics import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
from Globals import *


try:
    data = pd.read_csv('temp_data.csv')  
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: Dataset file not found. Please check the file path.")
    exit()



def IsNumerical(column):
    return data[column].dtype in ['int64', 'float64']


def IsCategorical(column):
    return isinstance(data[column].dtype, pd.CategoricalDtype) or data[column].dtype == 'object'




def Histogram(column, filename):
    plt.figure()
    plt.hist(data[column], bins=10, color='#006400', alpha=0.7, edgecolor='black')  # Dark Green
    plt.xlabel(f'{column}', color='black')  # X-axis label color to black
    plt.ylabel('Frequency', color='black')  # Y-axis label color to black
    
    
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def Boxplot(column, filename):
    plt.figure()
    data.boxplot(column=column, patch_artist=True, sym="ro", boxprops=dict(facecolor='#006400', color='black'))  # Dark Green
    plt.ylabel('Values', color='black')  # Y-axis label color to black
    
    #plt.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def Barchart(column, filename):
    plt.figure()
    counts = data[column].value_counts()
    plt.bar(counts.index, counts.values, color='#006400', alpha=0.7, edgecolor='black')  # Dark Green
    plt.xlabel('Categories', color='black')  # X-axis label color to black
    plt.ylabel('Counts', color='black')  # Y-axis label color to black
   
    #plt.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def Piechart(column, filename):
    plt.figure()
    counts = data[column].value_counts()
    num_colors = len(counts)
    dark_green_shades = plt.cm.Greens(np.linspace(0.5, 1, len(counts)))  # Darker shades of green
    explode = [0.2 if count == max(counts.values) else 0 for count in counts.values]
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90,
            explode=explode, colors=dark_green_shades, counterclock=False, shadow=True)
   
    #plt.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def Scatterplot(x, y, filename):
    plt.figure()
    plt.scatter(data[x], data[y], color='#006400', alpha=0.7, edgecolor='black')  # Dark Green
    plt.xlabel(f'{x}', color='black')  # X-axis label color to black
    plt.ylabel(f'{y}', color='black')  # Y-axis label color to black
    
    #plt.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def Linechart(x, y, filename):
    plt.figure()
    plt.plot(data[x], data[y], color='#006400', alpha=0.7)  # Dark Green
    plt.xlabel(f'{x}', color='black')  # X-axis label color to black
    plt.ylabel(f'{y}', color='black')  # Y-axis label color to black
    
    #plt.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def StackedBarchart(x, y, filename):
    plt.figure()
    cross_tab = pd.crosstab(data[x], data[y])

    # Create the stacked bar chart with custom colormap
    colors = plt.cm.Greens(np.linspace(0.3, 1, len(cross_tab.columns)))  # Adjust the color range (0.3 to 1)
    ax = cross_tab.plot(kind='bar', stacked=True, color=colors)  # Use custom colors

    # Set the x and y axis labels
    plt.xlabel(f'{x}', color='black')  # X-axis label color to black
    plt.ylabel(f'{y}', color='black')  # Y-axis label color to black

    # Adjust the position of the legend to be outside the plot area
    plt.legend(title=y, bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)

    # Save the figure
    #plt.tight_layout()  # To ensure the legend fits without overlapping
   
    #plt.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()



def Heatmap(x, y, filename):
    pivot_table = data.pivot_table(index=x, columns=y, aggfunc='size', fill_value=0)
    plt.figure()
    cmap = plt.cm.Greens(np.linspace(0.3, 1, 256))  # Darker greens range
    plt.imshow(pivot_table, cmap=ListedColormap(cmap), interpolation='nearest')
    plt.colorbar(label='Counts')  # Color bar label color to black
    plt.xlabel(f'{x}', color='black')  # X-axis label color to black
    plt.ylabel(f'{y}', color='black')  # Y-axis label color to black
    plt.title(f'Heatmap of {x} vs {y}', color='black')  # Set title color to black
    plt.tight_layout()
    
    #plt.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def HeatmapWithTwoNumericals(categorical, numerical_x, numerical_color, data, agg_func='mean', filename="graph.png"):
    data[numerical_color] = pd.to_numeric(data[numerical_color], errors='coerce')
    data = data.dropna(subset=[numerical_color])
    heatmap_data = data.pivot_table(index=categorical,
                                    columns=numerical_x,
                                    values=numerical_color,
                                    aggfunc=agg_func)


    plt.figure()
    cmap = plt.cm.Greens(np.linspace(0.3, 1, 256))  # Darker range for better visibility in green
    sns.heatmap(heatmap_data,
                cmap=ListedColormap(cmap),  # Apply custom green colormap
                annot=False,  # Do not annotate cells with values
                fmt='.2f',  # Format of annotations if annot is True
                cbar_kws={'label': numerical_color},  # Color bar label color to black
                linewidths=0.5)  # Optional: make gridlines thinner

    plt.xlabel(f'{numerical_x}', color='black')  # X-axis label color to black
    plt.ylabel(f'{categorical}', color='black')  # Y-axis label color to black

    plt.tight_layout()  # To ensure the layout is properly adjusted
      
    #plt.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def ThreeDScatterplot(numvar1, numvar2, numvar3, filename, data):
    plane = plt.figure()
    axis = plane.add_subplot(projection='3d')
    axis.scatter(data[numvar1], data[numvar2], data[numvar3],c="green")
    axis.set_xlabel(f'{numvar1}', color="black")  # Set axis label color to black
    axis.set_ylabel(f'{numvar2}', color="black")  # Set axis label color to black
    axis.set_zlabel(f'{numvar3}', color="black")  # Set axis label color to black
       
    #plane.show(block=True)
    plt.savefig(filename)
     # Get the current figure and resize it to show it large first
    fig = plt.gcf()  
    fig.set_size_inches(12, 8)       
    plt.show()
    #plt.close()

def VariableSelection():
    from Dashboard import create_dashboard
    
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()
    win = GraphWin("Variable Selector", 800, 600)
    setCurrentWindow(win)
    win.setBackground("Darkgreen")
    title = create_label(win, "Select Variables (Up to 3)", Point(400, 50), 20, colorcream, "bold")
  

    up_arrow = Polygon(Point(740, 170), Point(710, 200), Point(770, 200))  # Smaller triangle pointing up
    up_arrow.setFill("white")
    up_arrow.draw(win)

    down_arrow = Polygon(Point(740, 440), Point(710, 410), Point(770, 410))  # Smaller triangle pointing down
    down_arrow.setFill("white")
    down_arrow.draw(win)
    
    back_arrow = Line(Point(50, 57), Point(100, 57))
    back_arrow.setArrow('first')
    back_arrow.setWidth(3)
    back_arrow.setFill("white")
    back_arrow.draw(win)

    rectangles = []
    texts = []
    selected = []
    y_start = 100
    visible_count = 6  # Number of items visible at a time
    scroll_offset = 0  # Track the scroll position

    x_start = 120  # Position them 100px from the left side of the window

    # Create a list of rectangles and placeholder texts for all variables
    for i in range(visible_count):
        rect, text =create_button(win,Point(x_start, y_start + i * 70), Point(x_start + 550, y_start + i * 70 + 50), "", "lightgrey","black",vout="lightgrey",size=12)
       
        rectangles.append(rect)
        texts.append(text)

    def draw_visible():
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
    submit_btn, submit_text =create_button(win,Point(200, 520), Point(300, 570), "Submit", "lightgreen","darkgreen",vout="lightgreen",size=12)
    back_button, vim = create_button(win, Point(350, 520), Point(550, 570), "Go to Dashboard", "lightgreen", "Darkgreen",size=12)   
  
      
    while True:
        click = win.getMouse()

        if is_click_in_rectangle(click, submit_btn): # Submit button clicked
            break
        elif is_click_in_rectangle(click, back_button):
            win.close()
            create_dashboard()

        # Check for clicks on the up arrow (right side)
        elif 710 < click.x < 770 and 160 < click.y < 200:  # Up arrow clicked

            if scroll_offset > 0:
                scroll_offset -= 1
                draw_visible()

        # Check for clicks on the down arrow (right side)
        elif  710 < click.x < 770 and 410 < click.y < 440:  # Down arrow clicked

            if (scroll_offset + 1) * visible_count < len(data.columns):
                scroll_offset += 1
                draw_visible()
                
        if 50 < click.x < 100 and 55 < click.y < 58:  # Back arrow region  # If the back button is clicked            
            main()

        # Check for clicks on visible rectangles
        start = scroll_offset * visible_count
        end = start + visible_count

        for i in range(start, min(end, len(data.columns))):
            index = i - start
            rect = rectangles[index]
            text = texts[index]

            if is_click_in_rectangle(click,  rect ):
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
    from Dashboard import create_dashboard
      
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()
    win = GraphWin("Graph Options", 800, 600)
    setCurrentWindow(win)
    win.setBackground("darkgreen")
    
    bg_image = Image(Point(400, 300), "images/pic.gif")
    bg_image.draw(win)

    title = create_label(win, f"Select a Graph for {', '.join(selected)}",Point(400, 50), 18, colorcream, "bold")
  

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
            numerical_vars = [col for col in selected if IsNumerical(col)]
            categorical_var = [col for col in selected if IsCategorical(col)][0]
            options = ["Heatmap With Two Numericals"]
            selected = [numerical_vars[0], numerical_vars[1], categorical_var]

    y_base = 200
    vertical_spacing = 100
    buttons = []
    for i, option in enumerate(options):
        rect,text=create_button(win,Point(300, y_base + i * vertical_spacing), Point(500, y_base + 50 + i * vertical_spacing), option, "lightgreen","black","lightgreen",size=12)        
        buttons.append((rect, option))

    back_arrow = Line(Point(50, 57), Point(100, 57))
    back_arrow.setArrow('first')
    back_arrow.setWidth(3)
    back_arrow.setFill("white")
    back_arrow.draw(win)
    
    back_button, vim = create_button(win, Point(350, 520), Point(550, 570), "Go to Dashboard","lightgreen", "Darkgreen",size=12)   
  

    selected_option = None
    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click, back_button):
            win.close()
            create_dashboard()

        for rect, option in buttons:
            if is_click_in_rectangle(click, rect):
                selected_option = option
                break
            

        if 50 < click.x < 100 and 55 < click.y < 58:  # Back arrow region  # If the back button is clicked            
            main()

        if selected_option:
            break
    win.close()
    return selected_option, selected  # Return the selected graph and variables



def DisplayGraph(filename, title_text):
   
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()
    win = GraphWin("Graph Viewer", 800, 600)
    setCurrentWindow(win)
    win.setBackground("darkgreen")
    
    title = create_label(win, title_text,Point(400, 30), 18, colorcream, "bold")
  

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
            main()
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
                    Scatterplot(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Scatter Plot: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Line Chart":
                    Linechart(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Line Chart: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Stacked Bar Chart":
                    StackedBarchart(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Stacked Bar Chart: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "Heatmap":
                    Heatmap(selected_variables[0], selected_variables[1], "graph.png")
                    title_text = f"Heatmap: {selected_variables[0]} vs {selected_variables[1]}"
                elif selected_graph == "3D Scatterplot":
                    ThreeDScatterplot(selected_variables[0], selected_variables[1], selected_variables[2], "graph.png", data)
                    title_text = f"3D Scatter Plot for {selected_variables[0]} vs {selected_variables[1]} vs {selected_variables[2]} "
                elif selected_graph == "Heatmap With Two Numericals":
                    HeatmapWithTwoNumericals(
                        selected_variables[2],  # Categorical variable for Y-axis
                        selected_variables[0],  # Numerical variable for X-axis
                        selected_variables[1],  # Numerical variable for color
                        data=data,
                        filename="graph.png"# Data to plot
                    )
                    title_text = f"Heatmap: {selected_variables[2]} vs {selected_variables[0]} vs {selected_variables[1]}"

                else:
                    print("Graph type not implemented!")

                if DisplayGraph("graph.png", title_text):
                    continue  # User clicked back in the graph viewer, return to graph options
                else:
                    break


if __name__ == "__main__":
    main()