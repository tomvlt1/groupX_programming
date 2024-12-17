#In this part of our code, we establish the following:
#the user will have the choice to select the variables he desires to visualise (3 maximum)
#Then, depending on his/her selection, the possible graphs will be depicted on the user interface
#From the possible graphs, the user will choose the one they prefer


from graphics import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
from Globals import *

(colorblueBac, colorvlueButtons, colorvlueButtons1, colorgreen, colorcream)=color()
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
   
    
    plt.figure(dpi=96) 
    plt.hist(data[column], bins=10, color='#006400', alpha=0.7, edgecolor='black')  
    plt.xlabel(f'{column}', color='black')  
    plt.ylabel('Frequency', color='black')  
    
    
    plt.savefig(filename,dpi=96) 
    

def Boxplot(column, filename):
    plt.figure(dpi=96) 
    data.boxplot(column=column, patch_artist=True, sym="ro", boxprops=dict(facecolor='#006400', color='black'))  
    plt.ylabel('Values', color='black')  
    
    plt.savefig(filename,dpi=96) 
    

def Barchart(column, filename):
    plt.figure(dpi=96) 
    counts = data[column].value_counts()
    plt.bar(counts.index, counts.values, color='#006400', alpha=0.7, edgecolor='black')  
    plt.xlabel('Categories', color='black')  
    plt.ylabel('Counts', color='black')  
   
    plt.savefig(filename,dpi=96) 
    

def Piechart(column, filename):
    plt.figure(dpi=96) 
    counts = data[column].value_counts()
    num_colors = len(counts)
    dark_green_shades = plt.cm.Greens(np.linspace(0.5, 1, len(counts)))  
    explode = [0.2 if count == max(counts.values) else 0 for count in counts.values]
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%', startangle=90,
            explode=explode, colors=dark_green_shades, counterclock=False, shadow=True)
   
    
    plt.savefig(filename,dpi=96) 
    

def Scatterplot(x, y, filename):
    plt.figure(dpi=96) 
    plt.scatter(data[x], data[y], color='#006400', alpha=0.7, edgecolor='black')  
    plt.xlabel(f'{x}', color='black')  
    plt.ylabel(f'{y}', color='black')  
    
   
    plt.savefig(filename,dpi=96) 
   


def Linechart(x, y, filename):
    plt.figure(dpi=96) 
    plt.plot(data[x], data[y], color='#006400', alpha=0.7)  
    plt.xlabel(f'{x}', color='black') 
    plt.ylabel(f'{y}', color='black') 
    

    plt.savefig(filename,dpi=96) 
   

def StackedBarchart(x, y, filename):
    plt.figure(dpi=96) 
    cross_tab = pd.crosstab(data[x], data[y])   
    colors = plt.cm.Greens(np.linspace(0.3, 1, len(cross_tab.columns)))  
    ax = cross_tab.plot(kind='bar', stacked=True, color=colors)      
    plt.xlabel(f'{x}', color='black')  
    plt.ylabel(f'{y}', color='black') 
    plt.legend(title=y, bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
    plt.savefig(filename,dpi=96) 
  




def Heatmap(x, y, filename):
    pivot_table = data.pivot_table(index=x, columns=y, aggfunc='size', fill_value=0)
    plt.figure(dpi=96) 
    cmap = plt.cm.Greens(np.linspace(0.3, 1, 256))  
    plt.imshow(pivot_table, cmap=ListedColormap(cmap), interpolation='nearest')
    plt.colorbar(label='Counts')  
    plt.xlabel(f'{x}', color='black')  
    plt.ylabel(f'{y}', color='black')  
    plt.title(f'Heatmap of {x} vs {y}', color='black')  
    plt.tight_layout()
    plt.savefig(filename,dpi=96) 
   

def HeatmapWithTwoNumericals(categorical, numerical_x, numerical_color, data, agg_func='mean', filename="graph.png"):
    data[numerical_color] = pd.to_numeric(data[numerical_color], errors='coerce')
    data = data.dropna(subset=[numerical_color])
    heatmap_data = data.pivot_table(index=categorical,
                                    columns=numerical_x,
                                    values=numerical_color,
                                    aggfunc=agg_func)


    plt.figure(dpi=96) 
    cmap = plt.cm.Greens(np.linspace(0.3, 1, 256))  
                cmap=ListedColormap(cmap), 
                annot=False,  
                fmt='.2f', 
                cbar_kws={'label': numerical_color}, 
                linewidths=0.5)  

    plt.xlabel(f'{numerical_x}', color='black')  
    plt.ylabel(f'{categorical}', color='black')  
    plt.tight_layout()  
    plt.savefig(filename,dpi=96) 
   

def ThreeDScatterplot(numvar1, numvar2, numvar3, filename, data):
    plane = plt.figure(dpi=96) 
    axis = plane.add_subplot(projection='3d')
    axis.scatter(data[numvar1], data[numvar2], data[numvar3],c="green")
    axis.set_xlabel(f'{numvar1}', color="black")  
    axis.set_ylabel(f'{numvar2}', color="black")  
    axis.set_zlabel(f'{numvar3}', color="black")  
    plt.savefig(filename,dpi=96) 


def VariableSelection():
    from Dashboard import create_dashboard
    
    oldwin = getCurrentWindow()
    if oldwin:
        oldwin.close()
    win = GraphWin("Variable Selector", 800, 600)
    setCurrentWindow(win)
    win.setBackground("Darkgreen")
    title = create_label(win, "Select Variables (Up to 3)", Point(400, 50), 20, colorcream, "bold")
  

    up_arrow = Polygon(Point(740, 170), Point(710, 200), Point(770, 200))  
    up_arrow.setFill("white")
    up_arrow.draw(win)

    down_arrow = Polygon(Point(740, 440), Point(710, 410), Point(770, 410))  
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
    visible_count = 6  
    scroll_offset = 0  

    x_start = 120  


    for i in range(visible_count):
        rect, text =create_button(win,Point(x_start, y_start + i * 70), Point(x_start + 550, y_start + i * 70 + 50), "", "lightgrey","black",vout="lightgrey",size=12)
       
        rectangles.append(rect)
        texts.append(text)

    def draw_visible():
        for rect in rectangles:
            rect.undraw()
        for text in texts:
            text.undraw()

        
        start = scroll_offset * visible_count
        end = start + visible_count

        for i in range(start, min(end, len(data.columns))):
            index = i - start
            rect = rectangles[index]
            text = texts[index]

            
            rect.setFill("lightgreen" if data.columns[i] in selected else "lightgrey")

           
            text.setText(data.columns[i])

            
            rect.draw(win)
            text.draw(win)

    draw_visible()

    
    submit_btn, submit_text =create_button(win,Point(200, 520), Point(300, 570), "Submit", "lightgreen","darkgreen",vout="lightgreen",size=12)
    back_button, vim = create_button(win, Point(350, 520), Point(550, 570), "Go to Dashboard", "lightgreen", "Darkgreen",size=12)   
  
      
    while True:
        click = win.getMouse()

        if is_click_in_rectangle(click, submit_btn): 
            break
        elif is_click_in_rectangle(click, back_button):
            win.close()           
            create_dashboard()

        elif 710 < click.x < 770 and 160 < click.y < 200: 

            if scroll_offset > 0:
                scroll_offset -= 1
                draw_visible()

        elif  710 < click.x < 770 and 410 < click.y < 440: 

            if (scroll_offset + 1) * visible_count < len(data.columns):
                scroll_offset += 1
                draw_visible()
                
        if 50 < click.x < 100 and 55 < click.y < 58:       
            main()

       
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
            

        if 50 < click.x < 100 and 55 < click.y < 58:       
            main()

        if selected_option:
            break
    win.close()
    return selected_option, selected 



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

    back_arrow = Line(Point(50, 50), Point(100, 50))  
    back_arrow.setArrow('first')  
    back_arrow.setWidth(3)
    back_arrow.setFill("white")
    back_arrow.draw(win)

    while True:
        click = win.getMouse()
        if 700 < click.x < 800 and 550 < click.y < 600:  
            break
        if 50 < click.x < 100 and 40 < click.y < 60:  
            main()
            return True  
    win.close()
    return False


def main():
    while True:
        selected_variables = VariableSelection()

        if selected_variables:
            while True:  
                selected_graph, selected_variables = GraphOptions(selected_variables)

                if selected_graph is None:  
                    break 

               
                plt.rcParams['figure.dpi'] = 96
                plt.rcParams['savefig.dpi'] = 96      
                plt.close()  
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
                        selected_variables[2],  
                        selected_variables[0],  
                        selected_variables[1],  
                        data=data,
                        filename="graph.png"
                    )
                    title_text = f"Heatmap: {selected_variables[2]} vs {selected_variables[0]} vs {selected_variables[1]}"

                else:
                    print("Graph type not implemented!")

                if DisplayGraph("graph.png", title_text):
                    continue  
                else:
                    break


if __name__ == "__main__":
    main()
