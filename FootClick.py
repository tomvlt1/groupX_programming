import random
import time
import math
from graphics import GraphWin, Point, Circle, Polygon, Text, Line

def draw_football_net(win):
    """Draw a football net background with grid lines."""
    win.setBackground("green")  
    grid_spacing = 50  
    line_width = 3     
    width = win.getWidth()
    height = win.getHeight()

    for x in range(0, width, grid_spacing):
        line = Line(Point(x, 0), Point(x, height))
        line.setFill("white")
        line.setWidth(line_width)
        line.draw(win)

    for y in range(0, height, grid_spacing):
        line = Line(Point(0, y), Point(width, y))
        line.setFill("white")
        line.setWidth(line_width)
        line.draw(win)

def make_football(win):
    """Create a football with white and black patches."""
    center = Point(random.randint(50, 450), random.randint(50, 450))
    radius = random.randint(20, 40) 
    football = Circle(center, radius)
    football.setFill("white")
    football.setOutline("black")
    football.draw(win)

    patches = []
    for angle in range(0, 360, 72):  
        x = center.getX() + radius * 0.6 * math.cos(math.radians(angle))
        y = center.getY() + radius * 0.6 * math.sin(math.radians(angle))
        patch_center = Point(x, y)
        patch = create_pentagon(patch_center, radius * 0.3)  
        patch.setFill("black")
        patch.setOutline("white")
        patch.draw(win)
        patches.append(patch)

    return football, patches

def create_pentagon(center, radius):
    """Create a pentagon centered at `center` with `radius`."""
    points = []
    for angle in range(0, 360, 72):  
        x = center.getX() + radius * math.cos(math.radians(angle))
        y = center.getY() + radius * math.sin(math.radians(angle))
        points.append(Point(x, y))
    return Polygon(points)

def display_count(count, win):
    count_label = Text(Point(250, 20), f"Score: {count}")
    count_label.setSize(20)
    count_label.setStyle("bold")
    count_label.setTextColor("darkgreen")
    count_label.draw(win)
    return count_label

def is_click(football, pt):
    """Check if the click is within the football radius."""
    dx = football.getCenter().getX() - pt.getX()
    dy = football.getCenter().getY() - pt.getY()
    distance = math.sqrt(dx**2 + dy**2)
    return distance < football.getRadius()

def display_average_time(avg_time, win):
    time_label = Text(Point(250, 450), f"Reaction time: {round(avg_time, 2)} seconds \n Click to exit.")
    time_label.setSize(30)
    time_label.setStyle("italic")
    time_label.setTextColor("blue")
    time_label.draw(win)

def run_footclick():
    win = GraphWin("Football Click Game ⚽", 500, 500)
    draw_football_net(win)  

    count = 0
    count_label = display_count(count, win)
    football, patches = make_football(win)
    start = time.time()

    while count < 5:
        pt = win.checkMouse()
        if pt:
            if is_click(football, pt):
                count += 1
                count_label.setText(f"Score: {count}")
                football.undraw()
                for patch in patches:
                    patch.undraw()
                football, patches = make_football(win)
        time.sleep(0.1)

    end = time.time()
    total_time = end - start

    if count > 0:
        average_time = total_time / count
        print(f"Total time: {total_time:.2f}s, Count: {count}, Average time: {average_time:.2f}s")
        display_average_time(average_time, win)

    win.getMouse()  
    win.close()

if __name__ == "__main__":
    run_footclick()
