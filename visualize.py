
def display_year_selection(win, years):
    # Label for selecting year
    year_label = create_label(win, "Select Year:", Point(620, 100), 16, "#1E2A39", "bold")
    year_buttons = []

    # Add buttons for each year
    for idx, year in enumerate(years):
        btn, txt13 = create_button(win, Point(550, 130 + (idx * 40)), Point(750, 170 + (idx * 40)), str(year), "#4682B4", "white")
        year_buttons.append((year, btn, txt13))
    
    # Create the "X" to close the selection
    close_button = Rectangle(Point(720, 90), Point(740, 110))  # Position of the "X"
    close_button.setFill("#4682B4")
    close_button.setOutline("#4682B4")
    close_button.draw(win)

    # Create the "X" text inside the button
    close_text = Text(Point(730, 100), "X")
    close_text.setSize(16)
    close_text.setTextColor("white")
    close_text.draw(win)

    # Wait for the user to click
    while True:
        click = win.getMouse()

        # Check if the "X" was clicked
        if is_click_in_rectangle(click, close_button):
            # Undraw the buttons, label, and "X" when closing
            for _, b, c in year_buttons:
                b.undraw()
                c.undraw()
            year_label.undraw()
            close_button.undraw()
            close_text.undraw()
            return None  # Return None if the selection is closed
        
        # Check if a year button was clicked
        for year, btn, vtxt in year_buttons:
            if is_click_in_rectangle(click, btn):
                # Undraw all buttons and the label when a year is selected
                for _, b, c in year_buttons:
                    b.undraw()
                    c.undraw()
                year_label.undraw()
                close_button.undraw()
                close_text.undraw()
                return year  # Return the selected year

def display_team_selection(win, teams):
    # Label for selecting a team
    team_label = create_label(win, "Select Team:", Point(620, 100), 16, "#1E2A39", "bold")

    # Number of columns and rows
    columns = 3  # 3 columns
    rows_per_column = 10  # 10 rows per column

    # List to store buttons and icons
    team_buttons = []
    icon_objects = []  # List to store icon objects

    # Create a button for each team and display its icon if available
    for idx, (team_name, icon_filename) in enumerate(teams):
        # Calculate the row and column for the current team
        row = idx % rows_per_column  # Row within the column
        col = idx // rows_per_column  # Column index (0, 1, 2)

        # Calculate the position for the button
        x_offset = 550 + col * 250  # X-axis offset for columns
        y_offset = 130 + row * 50  # Y-axis offset for rows

        # Create the button for the team
        btn, txt1 = create_button(
            win,
            Point(x_offset, y_offset),
            Point(x_offset + 250, y_offset + 50),
            team_name,
            "#4682B4",
            "white",
            size=12
        )
        team_buttons.append((team_name, btn, txt1))  # Add the button to the list

        # Draw the icon if the filename is provided
        if icon_filename:
            # Assume the icon exists if a filename is provided
            icon_path = f"images/{icon_filename}"  # Construct the path for the icon
            icon = Image(Point(x_offset + 30, y_offset + 25), icon_path)  # Position the icon
            icon.draw(win)
            icon_objects.append(icon)

    # Create the "X" to close the team selection
    close_button = Rectangle(Point(720, 90), Point(740, 110))  # Position of the "X"
    close_button.setFill("#4682B4")
    close_button.setOutline("#4682B4")
    close_button.draw(win)

    # Create the "X" text inside the button
    close_text = Text(Point(730, 100), "X")
    close_text.setSize(16)
    close_text.setTextColor("white")
    close_text.draw(win)

    # Wait for the user to click on a team or close the selection
    while True:
        click_point = win.getMouse()

        # Check if the "X" was clicked
        if is_click_in_rectangle(click_point, close_button):
            # Undraw all buttons, icons, and the label when closing
            for _, b, c in team_buttons:
                b.undraw()
                c.undraw()
            for icon in icon_objects:
                icon.undraw()
            team_label.undraw()
            close_button.undraw()
            close_text.undraw()
            return None  # Return None if the selection is closed

        # Check if a team button was clicked
        for team_name, btn, txt1 in team_buttons:
            if is_click_in_rectangle(click_point, btn):
                # Undraw all buttons, icons, and the label when a team is selected
                for _, b, c in team_buttons:
                    b.undraw()
                    c.undraw()
                for icon in icon_objects:
                    icon.undraw()
                team_label.undraw()
                close_button.undraw()
                close_text.undraw()
                return team_name  # Return the selected team