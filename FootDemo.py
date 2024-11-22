import graphics

def ClearWindow(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

#we set the windows size to be x and y, we set the background to green to reflect the color of football 
# we need to draw every aspect of the football field, we will start with the center line, t
# the boundary, 
# the center circle, 
# the center spot, 
# the left goal area,
# the right goal area, 
# the left penalty spot, 
# the right penalty spot, 
# the stands, 
# the goals
def DrawFootballField():
    win = graphics.GraphWin("Football Field", 1300, 800)
    win.setBackground("dark green")

    
    center_line = graphics.Line(graphics.Point(650, 0), graphics.Point(650, 800))
    center_line.setWidth(2)
    center_line.setFill("white")
    center_line.draw(win)

    
    boundary = graphics.Rectangle(graphics.Point(100, 50), graphics.Point(1200, 750))
    boundary.setWidth(3)
    boundary.setOutline("white")
    boundary.draw(win)

    
    center_circle = graphics.Circle(graphics.Point(650, 400), 75)
    center_circle.setWidth(2)
    center_circle.setOutline("white")
    center_circle.draw(win)
    
    #center spot
    center_spot = graphics.Circle(graphics.Point(650, 400), 5)
    center_spot.setFill("white")
    center_spot.setOutline("white")
    center_spot.draw(win)

    
    left_goal_area = graphics.Rectangle(graphics.Point(100, 300), graphics.Point(200, 500))
    left_goal_area.setWidth(2)
    left_goal_area.setOutline("white")
    left_goal_area.draw(win)

    
    right_goal_area = graphics.Rectangle(graphics.Point(1100, 300), graphics.Point(1200, 500))
    right_goal_area.setWidth(2)
    right_goal_area.setOutline("white")
    right_goal_area.draw(win)

   
    left_penalty_spot = graphics.Circle(graphics.Point(175, 400), 5)
    left_penalty_spot.setFill("white")
    left_penalty_spot.setOutline("white")
    left_penalty_spot.draw(win)


    right_penalty_spot = graphics.Circle(graphics.Point(1125, 400), 5)
    right_penalty_spot.setFill("white")
    right_penalty_spot.setOutline("white")
    right_penalty_spot.draw(win)

  
    for i in range(5):
        y_offset = 50 + i * 20
        left_stand = graphics.Rectangle(graphics.Point(50, 50 + y_offset), graphics.Point(100, 750 - y_offset))
        left_stand.setFill("gray")
        left_stand.setOutline("black")
        left_stand.draw(win)


    for i in range(5):
        y_offset = 50 + i * 20
        right_stand = graphics.Rectangle(graphics.Point(1200, 50 + y_offset), graphics.Point(1250, 750 - y_offset))
        right_stand.setFill("gray")
        right_stand.setOutline("black")
        right_stand.draw(win)


    left_goal = graphics.Rectangle(graphics.Point(50, 300), graphics.Point(100, 500))
    left_goal.setFill("white")
    left_goal.setOutline("grey")
    left_goal.draw(win)

    
    right_goal = graphics.Rectangle(graphics.Point(1200, 300), graphics.Point(1250, 500))
    right_goal.setFill("white")
    right_goal.setOutline("white")
    right_goal.draw(win)

    
    win.getMouse()
    win.close()


DrawFootballField()
