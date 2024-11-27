


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





import matplotlib.pyplot as plt


all_variables[]
def variable_split(all_variables):
    numerical_display = []
    categorical_display = []
    for i in all_variables:
        if type(i) = "int" or "float":
            numerical_display.append(i)
        else:
            categorical_display.append(i)
    return numerical_display, categorical_display

def variables_avalible(categorical_display,numerical_display):
    avalible_choices = []
    if graph_select = histogram:
        avalible_choices.extend(numerical_display)
    if graph_select = bar:
        avalible_choices.extend(numerical_display)
        avalible_choices.extend(categorical_display)
    if graph_select = box:
        avalible_choices.extend(numerical_display)
        avalible_choices.extend(categorical_display)
    if graph_select = scatter:
        avalible_choices.extend(numerical_display)
    if graph_select = pie:
        avalible_choices.extend(numerical_display)
        avalible_choices.extend(categorical_display)
    if graph_select = heat_map:
        avalible_choices.extend(numerical_display)
        avalible_choices.extend(categorical_display)



numerical = []
categorical = []


def display_graph(numerical,categorical):
    if graph_select = histogrm:
        plt.hist(numerical[0],15, range = (-50,50), histtype='stepfilled', align = 'mid', color = "g")
        plt.xlabel('Entries')
        plt.ylabel('Values')
        plt.title('Histogram')
        plt.show()
    elif graph_select = bar and len(categotical)<=2 and len(numerical) = 1:
        if len(categorical) =1 and len(numerical)==1:
            plt.bar(cetegorical[0], numerical[0], color="g", align='center')
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.title('Histogram')
            plt.show()
        if len(categorical) =1 and len(numerical)==0:
            plt.bar(cetegorical[0], color="g", align='center')
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.title('Histogram')
            plt.show()
        if len(categorical) =2 and len(numerical)==0:
            plt.figure()
            cross_tab = pd.crosstab(numerical[0], numerical[1])
            cross_tab.plot(kind='bar', stacked=True, colormap='Greens')  # Darker green shades are used here
            plt.title(f'Stacked Bar Chart: {x} vs {y}', color='white')
            plt.savefig(filename)
            plt.close()
    elif graph_select = box and len(categotical)<=1 and len(numerical) = 1:
        if len(numerical)=1 and len(categotical)=0:
            plt.boxplot(numerical[0], sym='gx', widths=0.75, notch=True, color)
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.title('Histogram')
            plt.show()
        elif len(categorical) = 1:
            plt.boxplot(numerical[0], label=categorical[0], sym='gx', widths=0.75, notch=True
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.title('Histogram')
            plt.show()
    elif graph_select = scatter and len(categotical) <=3 and len(categorical) =0:
        if len(numerical) = 2:
            plt.scatter(categorical[0], categorical[1], s=[100], marker='^', color='m')
            plt.xlabel('Entries')
            plt.ylabel('Values')
            plt.title('Histogram')
            plt.show()
        elif len(numerical) = 3:
            plane = plt.figure()
            axis = plane.add_subplot(projection='3d')
            axis.scatter(x, y, z)
            axis.set_xlabel('Entries')
            axis.set_ylabel('Values')
            axis.set_zlabel('Values')
            plt.title('Histogram')
            plt.show()
    elif graph_select = pie and len(categorical)=1 and len(numerical) = 1:
        plt.xlabel('Entries')
        plt.ylabel('Values')
        plt.title('Histogram')
        plt.show()
        green_shades = plt.get_cmap('Greens')(np.linspace(0.3, 1, len(sizes)))
        plt.pie(numerical[1], colors=green_shades, labels=categorical[0], explode=explode, autopct='%1.1f%%', counterclock=False, shadow=False)


















