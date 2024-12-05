from graphics import *
from FootGameHome import FootGameHomeMain
from GetRandomStats import GetRandomFacts
import time


def create_window():
    """Create the main application window."""
    win = GraphWin("Football Dashboard UI", 900, 500)
    win.setBackground(color_rgb(44, 40, 85))
    return win


def create_sidebar(win):
    """Create the sidebar with navigation buttons."""
    sidebar = Rectangle(Point(0, 0), Point(200, 500))
    sidebar.setFill(color_rgb(31, 27, 58))
    sidebar.draw(win)

    new_button = Rectangle(Point(20, 20), Point(180, 60))
    new_button.setFill(color_rgb(28, 195, 170))
    new_button.draw(win)
    new_button_text = Text(new_button.getCenter(), "New Match")
    new_button_text.setTextColor("white")
    new_button_text.setSize(12)
    new_button_text.draw(win)

    button_titles = ["Dashboard", "Matches", "Players", "Teams"]
    y_offset = 90

    for btn in button_titles:
        button = Rectangle(Point(20, y_offset), Point(180, y_offset + 40))
        button.setFill(color_rgb(44, 40, 85))
        button.draw(win)
        button_text = Text(button.getCenter(), btn)
        button_text.setTextColor("white")
        button_text.setSize(12)
        button_text.draw(win)
        y_offset += 50


def RefreshButton(x, y, win):
    """Create a refresh button."""
    button = Rectangle(Point(x - 25, y - 25), Point(x + 25, y + 25))
    button.setFill(color_rgb(255, 255, 255))  # Set button color
    button.draw(win)

    refresh_icon = Image(Point(x, y), "images/refresh1.png")  # PNG icon for refresh
    refresh_icon.draw(win)
    return button


def PreviewButton(x, y, win):
    """Create a preview button."""
    button = Rectangle(Point(x - 100, y - 40), Point(x + 100, y + 40))
    button.setFill(color_rgb(0, 128, 255))  # Set button color (blue for preview)
    button.draw(win)

    preview_text = Text(Point(x, y - 10), "Preview Match")
    preview_text.setSize(14)
    preview_text.setTextColor("white")
    preview_text.draw(win)

    lock_text = Text(Point(x, y + 20), "Everything will be locked!")
    lock_text.setSize(10)
    lock_text.setTextColor("white")
    lock_text.draw(win)

    return button, preview_text, lock_text


def WarningMessage(x, y, win):
    """Create a warning message inside the match box."""
    warning = Text(Point(x, y), "This will lock the dashboard until the game ends (30 - 60 seconds).")
    warning.setSize(14)
    warning.setTextColor("red")
    warning.setStyle("bold")
    warning.draw(win)
    return warning


def create_overview_section(win):
    """Create the initial overview section."""
    overview_boxes = []
    overview_y_start = 20
    x_offset = 220

    # Draw the boxes for the overview section
    for _ in range(3):
        overview_box = Rectangle(Point(x_offset, overview_y_start), Point(x_offset + 180, overview_y_start + 100))
        overview_box.setFill("white")
        overview_box.draw(win)
        overview_boxes.append(overview_box)
        x_offset += 200

    facts = GetRandomFacts(3)  # Get initial facts
    update_overview_section(win, overview_boxes, facts)

    return overview_boxes


def update_overview_section(win, overview_boxes, facts):
    """Update the overview section with new facts."""
    for i, fact in enumerate(facts):
        # Clear the previous overview section
        overview_boxes[i].setFill("white")  # Keep the box visible but clear text

        # Remove previous text inside the box
        for item in win.items[:]:
            if isinstance(item, Text):
                if overview_boxes[i].getP1().x <= item.getAnchor().x <= overview_boxes[i].getP2().x and \
                        overview_boxes[i].getP1().y <= item.getAnchor().y <= overview_boxes[i].getP2().y:
                    item.undraw()

        # Extract the description, match info, and value
        try:
            description, match_info, value = fact.split("\n")
        except ValueError:
            description, match_info, value = "N/A", "N/A", "N/A"

        # Always prepend "Match with most -" for consistency
        title_line1 = "Match with most -"
        title_line2 = description

        # Draw the updated fact in the box
        title_text1 = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 20), title_line1)
        title_text2 = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 35), title_line2)
        match_text = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 55), match_info)
        value_text = Text(Point(overview_boxes[i].getP1().x + 90, overview_boxes[i].getP1().y + 75), value)

        for text in [title_text1, title_text2, match_text, value_text]:
            text.setTextColor(color_rgb(44, 40, 85))
            text.setSize(10)
            text.draw(win)

def create_mini_game_area(win):
    """Create the mini-game area."""
    mini_game_left = 220
    mini_game_top = 140
    mini_game_right = 880
    mini_game_bottom = 480

    mini_game_area = Rectangle(Point(mini_game_left, mini_game_top), Point(mini_game_right, mini_game_bottom))
    mini_game_area.setFill(color_rgb(224, 224, 224))
    mini_game_area.draw(win)

    return mini_game_area, mini_game_left, mini_game_top, mini_game_right, mini_game_bottom


def create_dashboard():
    """Create the main dashboard."""
    win = create_window()
    create_sidebar(win)
    overview_boxes = create_overview_section(win)
    refresh_button = RefreshButton(850, 60, win)  # Refresh button

    mini_game_area, left, top, right, bottom = create_mini_game_area(win)
    preview_button, preview_text, lock_message = PreviewButton((left + right) // 2, (top + bottom) // 2, win)
    warning = WarningMessage((left + right) // 2, (top + bottom) // 2 + 60, win)

    mini_game_active = False  # Track if the mini-game is active

    while True:
        click = win.checkMouse()  # Non-blocking mouse click check

        if click:
            print(f"Mouse clicked at: {click.getX()}, {click.getY()}")  # Debugging

            # Check if preview button is clicked
            if not mini_game_active and preview_button.getP1().x <= click.getX() <= preview_button.getP2().x and \
                    preview_button.getP1().y <= click.getY() <= preview_button.getP2().y:
                print("Preview button clicked.")
                mini_game_active = True

                # Hide the preview button and warning
                preview_button.undraw()
                preview_text.undraw()
                lock_message.undraw()
                warning.undraw()

                # Start the mini-game
                FootGameHomeMain(win)

                # Re-display the preview button and warning after the game ends
                preview_button.draw(win)
                preview_text.draw(win)
                lock_message.draw(win)
                warning.draw(win)
                mini_game_active = False

            # Check if refresh button is clicked
            if (850 - 25) <= click.getX() <= (850 + 25) and (60 - 25) <= click.getY() <= (60 + 25):
                print("Refresh button clicked.")
                facts = GetRandomFacts(3)
                update_overview_section(win, overview_boxes, facts)

        time.sleep(0.05)  # Small delay to reduce CPU usage

    win.close()


if __name__ == "__main__":
    create_dashboard()
