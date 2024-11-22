


#The user will have selected the number of variables he wants and assigned it as independent or dependent
#The user will select the graph of interest based on the list of graphs available

#if the user selects a histogram, then he must have selected only one variable
    #Plot the histogram of the variable selected by the user
#if the user selects bar chart, he needs 2 categorical variables maximum
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
#if the user a pir chart he must have selected a pie chart he must have selected a numerical and a categorical variable
    #plot the pie chart with the variables requested by the user
#if the user selects a scatter plot, 3 numerical variables should have been selected
    #plot the scatter plot with the three variables

import matplotlib.pyplot as plt
if graph_select = histogrm:
    plt.hist(var1,15, range = (-50,50), histtype='stepfilled', align = 'mid', color = "g")
elif graph_select = bar







