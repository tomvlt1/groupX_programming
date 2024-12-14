import random
import time
from graphics import GraphWin, Point, Circle, Text  

def make_circle(win):
    center = Point(random.randint(10, 490), random.randint(10, 490))
    radius = random.randint(5, 50)
    circle = Circle(center, radius)
    circle.setFill("red")
    circle.draw(win)
    return circle

def display_count(count, win):
    count_label = Text(Point(250, 250), count)
    count_label.setSize(36)
    count_label.draw(win)
    return count_label

def is_click(circle, pt):
    dx = circle.getCenter().getX() - pt.getX()
    dy = circle.getCenter().getY() - pt.getY()
    distance = (dx**2 + dy**2)**0.5 
    return distance < circle.getRadius() 

def display_average_time(avg_time, win):
    time_label = Text(Point(270, 270), "Your average time per click was: " + str(round(avg_time, 2)) + " seconds")
    time_label.setSize(12)
    time_label.draw(win)
    return time_label

def main():
    getQuantity = int(input("How many circles do you want to click? "))
    win = GraphWin("Bubbles", 500, 500)
    win.setBackground("lightblue")
    
    count = 0
    count_label = display_count(count, win)
    circle = make_circle(win)
    start = time.time() 

    while count < getQuantity:
        pt = win.checkMouse()
        if pt:
            if is_click(circle, pt):
                count += 1
                count_label.setText(count)
                circle.undraw()
                circle = make_circle(win)
        time.sleep(0.1)

    end = time.time() 
    total_time = end - start
    
    if count > 0:
        average_time = total_time / count
        print("Total time: ", total_time, " Count: ", count, " Average time: ", average_time)
        display_average_time(average_time, win)
    
    win.getMouse()
    win.close()

main()
