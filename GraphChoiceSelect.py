import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from graphics import *
from Globals import messages,create_button,is_click_in_rectangle



def GraphSelection():
    from Dashboard import create_dashboard
    win = GraphWin("Select a Graph", 800, 600)
    title = Text(Point(400, 40), "Which graph do you want?")
    title.setSize(20)
    title.setTextColor("white")
    title.draw(win)
    win.setBackground('dark green')


    rectangles = []
    selected = []
    y_start = 100
    graph_possibilities = ["Bar chart (Simple and Stacked)","Box Plot", "Scatter Plot", "Pie Chart", "Histogram"]
    loop_counter = 0
    for i in graph_possibilities:
        rect, text = create_button(win, Point(100, y_start + loop_counter * 70), Point(700, y_start + loop_counter * 70 + 50), i, "lightgrey", "Darkgreen")    
        rectangles.append((rect, i, text))
        loop_counter = loop_counter + 1

    submit_btn, txt_submit = create_button(win, Point(200, 500), Point(300, 550), "Submit", "lightgreen", "Darkgreen",size=12)    
    back_button, vim = create_button(win, Point(350, 500), Point(500, 550), "Go to Dashboard", "lightgreen", "Darkgreen",size=12)   
  


    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click, submit_btn):
            if len (selected)<1:
                 messages("Select option")     
                 win.close()
                 main()     
            break
        if is_click_in_rectangle(click, back_button):
            win.close()
            create_dashboard()
        for rect, col, text in rectangles:
            if is_click_in_rectangle(click, rect):
                if selected == (rect, col):
                    rect.setFill("lightgrey")
                    selected = None
                else:
                    if selected:
                        selected[0].setFill("lightgrey")
                    rect.setFill("lightgreen")
                    selected = (rect, col)
                break
    win.close()
   
    finalselect = [selected[1]]
    return finalselect

def variable_split():
   
    dataset = pd.read_csv("temp_data.csv")
    numerical_display = []
    categorical_display = []
    for i in dataset.columns:
        if isinstance(dataset[i][1],float) or isinstance(dataset[i][1],int):
            numerical_display.append(i)
        else:
            categorical_display.append(i)

    return numerical_display, categorical_display, dataset


def VariableOptions(selected,numerical_display,categorical_display,dataset):
    from Dashboard import create_dashboard
     
    win = GraphWin("Variable Options", 800, 600)

    win.setBackground('dark green')

    square_around_opperarrow = Rectangle(Point(705,160),Point(775,210))
    square_around_opperarrow.draw(win)

    up_arrow = Polygon(Point(740, 170), Point(710, 200), Point(770, 200))
    up_arrow.setFill("white")
    up_arrow.draw(win)

    square_around_lowerarrow = Rectangle(Point(705,400),Point(775,450))
    square_around_lowerarrow.draw(win)

    down_arrow = Polygon(Point(740, 440), Point(710, 410), Point(770, 410))
    down_arrow.setFill("white")
    down_arrow.draw(win)

    bg_image = Image(Point(400, 300), "images/pic.png")
    bg_image.draw(win)

    title = Text(Point(400, 30), f"Select a Variable for {selected}")
    title.setSize(16)
    title.setTextColor("white")
    title.draw(win)

    avalible_choices = []
    if selected[0] == 'Histogram':
        avalible_choices.extend(numerical_display)
    if selected[0] == "Bar chart (Simple and Stacked)":
        avalible_choices.extend(numerical_display)
        avalible_choices.extend(categorical_display)        
    if selected[0] == "Box Plot":
        avalible_choices.extend(numerical_display)
        avalible_choices.extend(categorical_display)
    if selected[0] == "Scatter Plot":
        avalible_choices.extend(numerical_display)
    if selected[0] == "Pie Chart":
        avalible_choices.extend(numerical_display)
        avalible_choices.extend(categorical_display)



    y_base = 100
    vertical_spacing = 70
    rectangles = []
    selected_options = []

    page_number = 0

    counter_for_display=-1



    def page_setter(counter_for_display,page_number,avalible_choices):
        rectangles.clear()
        for i in avalible_choices[page_number*6:page_number*6+6]:
            counter_for_display=counter_for_display+1 
            if i in selected_options:
                rect, text = create_button(win, Point(300, y_base + counter_for_display * vertical_spacing), Point(500, y_base + counter_for_display * vertical_spacing + 50), i, "lightgreen", "black",size=12)                 
            else:
                rect, text = create_button(win, Point(300, y_base + counter_for_display * vertical_spacing), Point(500, y_base + counter_for_display * vertical_spacing + 50),i, "lightgrey", "black",size=12)                 
           
            rectangles.append((rect, i, text))
    page_setter(counter_for_display, page_number, avalible_choices)

    submit_btn, txt_submit = create_button(win, Point(300, 525), Point(400, 575), "Submit", "green", "white",size=12)    
    back_button, vim = create_button(win, Point(450, 525), Point(600, 575), "Go to Dashboard", "green", "white",size=12)       
  


    while True:
        click = win.getMouse()

        if  is_click_in_rectangle(click, submit_btn):
            break
        elif is_click_in_rectangle(click, back_button):
            create_dashboard()

        if 705 < click.x < 775 and 160 < click.y < 210:
            page_number = page_number-1
            page_setter(counter_for_display, page_number, avalible_choices)

        if 705 < click.x < 775 and 400 < click.y < 450:
            page_number = page_number+1
            page_setter(counter_for_display, page_number, avalible_choices)



        for rect, option, text in rectangles:
            if is_click_in_rectangle(click,rect):
                if option in selected_options:
                    selected_options.remove(option)
                    rect.setFill("lightgrey")
                elif len(selected_options) <3:
                    selected_options.append(option)
                    rect.setFill("lightgreen")
                break

    win.close()

    numerical = []
    categorical = []

    for i in selected_options:
        if isinstance(dataset[i][1],float) or isinstance(dataset[i][1],int):
            numerical.append(i)
        else:
            categorical.append(i)



    return numerical, categorical


def display_graph(numerical,categorical,selected,dataset):
    filename ="graph_1.png"
    vcontrol=0
        
    plt.rcParams['figure.dpi'] = 96
    plt.rcParams['savefig.dpi'] = 96 
    
    plt.close()  
   
    if selected[0] == "Histogram" and len(numerical) >0:
        vcontrol=1   
       
        plt.figure(dpi=96)      
        plt.hist(dataset[numerical[0]],bins=15, histtype='stepfilled', align = 'mid', color = "g") 
        plt.ylabel('Observations')
        plt.xlabel(f'{numerical[0]}', color="Black")
        plt.title(f'{numerical[0]} ', color="Black")          
               
        
    elif selected[0] == "Bar chart (Simple and Stacked)" and len(categorical) <= 2 and len(numerical) <= 1:
        
        if len(categorical) == 1 and len(numerical)  == 1:
            vcontrol=1
            plt.figure(dpi=96) 
            plt.bar(dataset[categorical[0]], dataset[numerical[0]], color="g", align='center')
            plt.ylabel(f'{numerical[0]}', color="Black")
            plt.xlabel(f'{categorical[0]}', color="Black")
            plt.title(f'{numerical[0]} ', color="Black")
           
        elif len(categorical) == 2 and len(numerical) == 0:
            vcontrol=1
            plt.figure(dpi=96)  
            cross_tab = pd.crosstab(dataset[categorical[0]],dataset[categorical[1]])
            cross_tab.plot(kind='bar', stacked=True, colormap='Greens')
            plt.title(f'{categorical[0]} vs {categorical[1]}', color='w')            
            
    elif selected[0] == "Box Plot" and len(categorical) <= 1 and len(numerical) == 1:
        if len(numerical) ==1 and len(categorical) ==0:
            vcontrol=1
            plt.figure(dpi=96)   
            plt.boxplot(dataset[numerical[0]], sym='gx', widths=0.75, notch=True)
            plt.ylabel(f'{numerical[0]}', color='Black')
            plt.title(f'{numerical[0]} ', color='Black')
           
        elif len(categorical) == 1 and len(categorical) == 1:
            vcontrol=1
            plt.figure(dpi=96)  
            plt.boxplot(dataset[numerical[0]], labels = dataset[categorical[0]].unique(), sym='gx', widths=0.75, notch=True)
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.title('Histogram')
           
    elif selected[0] == "Scatter Plot" and len(numerical) <= 3 and len(categorical) == 0:
        if len(numerical) == 2:
            vcontrol=1
            plt.figure(dpi=96) 
            plt.scatter(dataset[numerical[0]], dataset[numerical[1]], s=[100], color='m')
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.xlabel(f'{numerical[0]}', color="Black")
            plt.ylabel(f'{numerical[1]}', color="Black")
            plt.title(f'{numerical[0]} vs {numerical[1]} ', color="Black")
            
        elif len(numerical) == 3:
            vcontrol=1
            plane = plt.figure(dpi=96) 
            axis = plane.add_subplot(projection='3d')
            axis.scatter(dataset[numerical[0]], dataset[numerical[1]], dataset[numerical[2]])
            axis.set_xlabel(f'{numerical[0]}', color="Black")
            axis.set_ylabel(f'{numerical[1]}', color="Black")
            axis.set_zlabel(f'{numerical[2]}', color="Black")
            plt.title(f'{numerical[0]} vs. {numerical[1]} vs. {numerical[2]}', color="Black")
          
    elif (selected[0] == "Pie Chart" and len(categorical) ==1) or (selected[0] == "Pie Chart" and  len(numerical) == 1):
        if len(numerical) == 1:
            vcontrol = 1
            datanew = dataset.groupby(numerical[0]).size()
        elif len(categorical) == 1:
            vcontrol = 1
            datanew = dataset.groupby(categorical[0]).size()
        plt.figure(dpi=96) 
        plt.xlabel('Entries')
        plt.ylabel('Values')
        plt.title('Pie Chart')
        plt.pie(datanew.values, labels=datanew.index, autopct='%1.1f%%', counterclock=False, shadow=False)
        
           
    return filename,vcontrol,plt

def displayer(filename):
    win = GraphWin("Show", 800, 600)
    win.setBackground('dark green')
    bg_image = Image(Point(400, 300), filename)       
    
    bg_image.draw(win)
    done, done_writting  = create_button(win, Point(350, 545), Point(450, 595), "Done", "green", "white",size=10)    
    
    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click,done):
            win.close()
            main()
           


def main():
    
    selected = GraphSelection()
    numerical_display, categorical_display, dataset=variable_split()
    numerical, categorical = VariableOptions(selected,numerical_display,categorical_display,dataset)
   
    filename,vcontrol,plt = display_graph(numerical, categorical, selected,dataset)
    if vcontrol==0:
        messages ("It is not possible to graph with these options")
        main()        
    else:  
        plt.savefig(filename,dpi=96) 
        displayer(filename)

#main()






