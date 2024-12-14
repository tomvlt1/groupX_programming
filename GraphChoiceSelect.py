#The user will have selected the number of variables he wants and assigned it as independent or dependent
#The user will select the graph of interest based on the list of graphs available

#if the user selects a histogram, then he must have selected only one variable
    #Plot the histogram of the variable selected by the user
#if the user selects bar chart, he needs 2 categorical variables maximum with one numetical
    #if 1 variable was selected
        #plot the bar  chart with one variable
    #if the user selects 2 variables
        #plot a stacked bar plot with the two variables
#if the user selects two categorical variables and grouped bar chart
    #make grouped bar chart
#if the user selects a box plot then he must have selected a maxim of 2 variables
    #if the user has selected one variable that is numerical
        #make the box plot with one variable
    #if the user has selected 2 variables one that is numerical and one that is categorical
        #make the box plot with 2 variable
#if the user selects a violin plot then he must have selected a maxim of 2 variables
    #if the user has selected one variable that is numerical
        #make the violin plot with one variable
    #if the user has selected 2 variables one that is numerical and one that is categorical
        #make the violin plot with 2 variable
#if the user selects a scatter plot, 2 numerical variables should have been selected
    #plot the scatter plot with the two variables
#if the user a pie chart he must have selected a pie chart he must have selected a numerical and a categorical variable
    #plot the pie chart with the variables requested by the user
#if the user selects a scatter plot, 3 numerical variables should have been selected
    #plot the scatter plot with the three variables
# scatter, Stacked




import pandas as pd
import matplotlib.pyplot as plt
from graphics import *
import random



def GraphSelection():
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
        rect = Rectangle(Point(100, y_start + loop_counter * 70), Point(700, y_start + loop_counter * 70 + 50))
        rect.setFill("lightgrey")
        rect.draw(win)
        text = Text(rect.getCenter(), i)
        text.draw(win)
        rectangles.append((rect, i, text))
        loop_counter = loop_counter + 1


    submit_btn = Rectangle(Point(350, 500), Point(450, 550))
    submit_btn.setFill("lightgreen")
    submit_btn.draw(win)
    submit_text = Text(submit_btn.getCenter(), "Submit")
    submit_text.setTextColor("Darkgreen")
    submit_text.draw(win)


    while True:
        click = win.getMouse()
        if 350 < click.x < 450 and 500 < click.y < 550:
            break

        for rect, col, text in rectangles:
            if rect.getP1().x < click.x < rect.getP2().x and rect.getP1().y < click.y < rect.getP2().y:
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
    print("displays",numerical_display,"\n",categorical_display)

    return numerical_display, categorical_display, dataset


def VariableOptions(selected,numerical_display,categorical_display,dataset):
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

    bg_image = Image(Point(400, 300), "pic.png")
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
            rect = Rectangle(Point(300, y_base + counter_for_display * vertical_spacing), Point(500, y_base + counter_for_display * vertical_spacing + 50))

            if i in selected_options:
                rect.setFill("lightgreen")
            else:
                rect.setFill("lightgrey")
            rect.draw(win)

            text = Text(rect.getCenter(), i)
            text.setTextColor("black")
            text.draw(win)

            rectangles.append((rect, i, text))


    page_setter(counter_for_display, page_number, avalible_choices)


    submit_btn = Rectangle(Point(350, 525), Point(450, 575))
    submit_btn.setFill("green")
    submit_btn.draw(win)
    submit_text = Text(submit_btn.getCenter(), "Submit")
    submit_text.setTextColor("white")
    submit_text.draw(win)



    while True:
        click = win.getMouse()

        if 350 < click.x < 450 and 525 < click.y < 575:
            break

        if 705 < click.x < 775 and 160 < click.y < 210:
            page_number = page_number-1
            page_setter(counter_for_display, page_number, avalible_choices)

        if 705 < click.x < 775 and 400 < click.y < 450:
            page_number = page_number+1
            page_setter(counter_for_display, page_number, avalible_choices)



        for rect, option, text in rectangles:
            if rect.getP1().x < click.x < rect.getP2().x and rect.getP1().y < click.y < rect.getP2().y:
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

    print("selected numericals are: ", numerical,"carecoriacals are",categorical)

    print("These are the variables selected",numerical,"\n","categorical",categorical)

    return numerical, categorical


def display_graph(numerical,categorical,selected,dataset):
    file_name_number = random.randint(1, 250000)
    filename = f"graph_{file_name_number}.png"
    if selected[0] == "Histogram":
        plt.hist(dataset[numerical[0]],15, histtype='stepfilled', align = 'mid', color = "g")
        plt.ylabel('Observations')
        plt.xlabel(f'{numerical[0]}', color="Black")
        plt.title(f'{numerical[0]} ', color="Black")
        plt.savefig(filename)
    elif selected[0] == "Bar chart (Simple and Stacked)" and len(categorical) <= 2 and len(numerical) <= 1:
        if len(categorical) == 1 and len(numerical)  == 1:
            plt.bar(dataset[categorical[0]], dataset[numerical[0]], color="g", align='center')
            plt.ylabel(f'{numerical[0]}', color="Black")
            plt.xlabel(f'{categorical[0]}', color="Black")
            plt.title(f'{numerical[0]} ', color="Black")
            plt.savefig(filename)
        elif len(categorical) == 2 and len(numerical) == 0:
            plt.figure()
            cross_tab = pd.crosstab(dataset[numerical[0]],dataset[ numerical[1]])
            cross_tab.plot(kind='bar', stacked=True, colormap='Greens')
            plt.title(f'{numerical[0]} vs {numerical[1]}', color='w')
            plt.savefig(filename)
    elif selected[0] == "Box Plot" and len(categorical) <= 1 and len(numerical) == 1:
        if len(numerical) ==1 and len(categorical) ==0:
            plt.boxplot(dataset[numerical[0]], sym='gx', widths=0.75, notch=True)
            plt.ylabel(f'{numerical[0]}', color='Black')
            plt.title(f'{numerical[0]} ', color='Black')
            plt.savefig(filename)
        elif len(categorical) == 1 and len(categorical) == 1:
            plt.boxplot(dataset[numerical[0]], labels = dataset[categorical[0]].unique(), sym='gx', widths=0.75, notch=True)
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.title('Histogram')
            plt.savefig(filename)
    elif selected[0] == "Scatter Plot" and len(numerical) <= 3 and len(categorical) == 0:
        if len(numerical) == 2:
            plt.scatter(dataset[numerical[0]], dataset[numerical[1]], s=[100], color='m')
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.xlabel(f'{numerical[0]}', color="Black")
            plt.ylabel(f'{numerical[1]}', color="Black")
            plt.title(f'{numerical[0]} vs {numerical[1]} ', color="Black")
            plt.savefig(filename)
        elif len(numerical) == 3:
            plane = plt.figure()
            axis = plane.add_subplot(projection='3d')
            axis.scatter(dataset[numerical[0]], dataset[numerical[1]], dataset[numerical[2]])
            axis.set_xlabel(f'{numerical[0]}', color="Black")
            axis.set_ylabel(f'{numerical[1]}', color="Black")
            axis.set_zlabel(f'{numerical[2]}', color="Black")
            plt.title(f'{numerical[0]} vs. {numerical[1]} vs. {numerical[2]}', color="Black")
            plt.savefig(filename)
    elif selected[0] == "Pie Chart" and len(categorical) ==1 or len(numerical) == 1:
        if len(numerical) == 1:
            datanew = dataset.groupby(numerical[0]).size()
        elif len(categorical) == 1:
            datanew = dataset.groupby(categorical[0]).size()


        print(datanew.columns)

        plt.xlabel('Entries')
        plt.ylabel('Values')
        plt.title('Histogram')
        plt.pie(datanew[1], labels=datanew[0], autopct='%1.1f%%', counterclock=False, shadow=False)
        plt.savefig(filename)
    return filename

def displayer(filename):
    win = GraphWin("Show", 800, 600)
    win.setBackground('dark green')
    bg_image = Image(Point(400, 300), filename)
    bg_image.draw(win)
    done= Rectangle(Point(350, 545), Point(450, 595))
    done.setFill("green")
    done.draw(win)
    done_writting = Text(done.getCenter(), "Done")
    done_writting.setTextColor("white")
    done_writting.draw(win)
    while True:
        click = win.getMouse()
        if 350 < click.x < 450 and 545 < click.y < 595:
            break


def main():
    selected = GraphSelection()
    numerical_display, categorical_display, dataset=variable_split()
    numerical, categorical = VariableOptions(selected,numerical_display,categorical_display,dataset)
    filename = display_graph(numerical, categorical, selected,dataset)
    displayer(filename)



#main()






