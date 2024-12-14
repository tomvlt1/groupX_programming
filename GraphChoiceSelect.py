#The user will have selected the number of variables he wants and assigned it as independent or dependent
#The user will select the graph of interest based on the list of graphs available





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
    graph_possibilities = ["Bar chart","Box Plot", "Scatter Plot", "Pie Chart", "Histogram"]
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
        if 350 < click.x < 450 and 500 < click.y < 550 and len(selected)>=2:
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


def VariableOptions(selected,numerical_display,categorical_display,dataset,):
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
        options_limit = 1
        avalible_choices.extend(numerical_display)
    if selected[0] == "Bar chart":
        avalible_choices.extend(numerical_display)
        avalible_choices.extend(categorical_display)
        options_limit = 2
    if selected[0] == "Box Plot":
        avalible_choices.extend(numerical_display)
        options_limit = 1
    if selected[0] == "Scatter Plot":
        avalible_choices.extend(numerical_display)
        options_limit = 3
    if selected[0] == "Pie Chart":
        avalible_choices.extend(categorical_display)
        options_limit = 1



    y_base = 100
    vertical_spacing = 70
    rectangles = []
    selected_options = []

    page_number = 0

    counter_for_display=-1



    def page_setter(counter_for_display,page_number,avalible_choices):
        rectangles.clear()
        for i in avalible_choices[page_number*6:page_number*6+6]:
            counter_for_display = counter_for_display+1
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
    submit_btn.setFill("LightGreen")
    submit_btn.draw(win)
    submit_text = Text(submit_btn.getCenter(), "Submit")
    submit_text.setTextColor("darkgreen")
    submit_text.draw(win)



    while True:
        click = win.getMouse()

        if 350 < click.x < 450 and 525 < click.y < 575:
            if selected[0] == "Scatter Plot" and len(selected_options) == 1:
                print(selected_options)

                warning = Rectangle(Point(150, 225), Point(650, 275))
                warning.setFill("White")
                warning.draw(win)
                warningmessage = Text(warning.getCenter(), "Select mode than one variable")
                warningmessage.setTextColor("Black")
                warningmessage.draw(win)
                win.getMouse()
                warningmessage.undraw()
                warning.undraw()
            elif selected[0] == "Bar chart" and len(selected_options) != 2:
                    warning = Rectangle(Point(150, 225), Point(650, 275))
                    warning.setFill("White")
                    warning.draw(win)
                    warningmessage = Text(warning.getCenter(), "you must select more variables")
                    warningmessage.setTextColor("Black")
                    warningmessage.draw(win)
                    win.getMouse()
                    warningmessage.undraw()
                    warning.undraw()

            elif selected[0] == "Bar chart":

                numericalLap1 = []
                categoricalLap1 = []

                for i in selected_options:
                    if isinstance(dataset[i][2], float) or isinstance(dataset[i][2], int):
                            numericalLap1.append(i)
                    else:
                            categoricalLap1.append(i)

                if len(numericalLap1) != 1:
                    print(categoricalLap1)
                    print(numericalLap1)
                    warning = Rectangle(Point(150, 225), Point(650, 275))
                    warning.setFill("White")
                    warning.draw(win)
                    warningmessage = Text(warning.getCenter(), "You must select one numerical variable")
                    warningmessage.setTextColor("Black")
                    warningmessage.draw(win)
                    win.getMouse()
                    warningmessage.undraw()
                    warning.undraw()
                elif len(categoricalLap1) != 1:
                    print(categoricalLap1)
                    print(numericalLap1)
                    warning = Rectangle(Point(150, 225), Point(650, 275))
                    warning.setFill("White")
                    warning.draw(win)
                    warningmessage = Text(warning.getCenter(), "You must select one categorical variable")
                    warningmessage.setTextColor("Black")
                    warningmessage.draw(win)
                    win.getMouse()
                    warningmessage.undraw()
                    warning.undraw()

                else:
                    break
            else:
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
                elif len(selected_options) < options_limit:
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
    file_name_number = random.randint(1, 250000)
    filename = f"graph_{file_name_number}.png"
    if selected[0] == "Histogram":
        plt.hist(dataset[numerical[0]],15, histtype='stepfilled', align = 'mid', color = "g")
        plt.ylabel('Observations')
        plt.xlabel(f'{numerical[0]}', color="Black")
        plt.title(f'{numerical[0]} ', color="Black")
        plt.savefig(filename)
    elif selected[0] == "Bar chart":
        if len(categorical) == 1 and len(numerical)  == 1:
            plt.bar(dataset[categorical[0]], dataset[numerical[0]], color="g", align='center')
            plt.ylabel(f'{numerical[0]}', color="Black")
            plt.xlabel(f'{categorical[0]}', color="Black")
            plt.title(f'{categorical[0]} vs. {numerical[0]}', color="Black")
            plt.savefig(filename)
    elif selected[0] == "Box Plot" and len(numerical) == 1:
        if len(numerical) ==1 and len(categorical) ==0:
            plt.boxplot(dataset[numerical[0]], sym='gx', widths=0.75, notch=True)
            plt.ylabel(f'{numerical[0]}', color='Black')
            plt.title(f'{numerical[0]} ', color='Black')
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
    elif selected[0] == "Pie Chart" and len(categorical) ==1:
        if len(categorical) == 1:
            reference = categorical[0]
            datanew = dataset.groupby(reference).size().reset_index(name='Count')
        plt.xlabel('Entries')
        plt.ylabel('Values')
        plt.title('Histogram')
        plt.pie(datanew['Count'], labels = datanew[reference] , autopct='%1.1f%%', counterclock=False, shadow=False)
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






