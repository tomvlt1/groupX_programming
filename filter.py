from graphics import *
from Globals import is_click_in_rectangle, create_label
from DataFunctions import openconnection
import pandas as pd


def filter_data_from_db(table_name = "DataDetails", filters=None, columns=None):
    """
    Filters data from a table in the database based on the provided filters.

    Args:
        table_name (str): The name of the table to query.
        filters (dict): A dictionary of conditions to apply as filters.
        columns (list): List of columns to select. If None, selects all columns.

    Returns:
        pd.DataFrame: A DataFrame containing the filtered data.
    """
    conn = None
    cursor = None

    try:
        conn = openconnection()
        cursor = conn.cursor()

        # Build SELECT query
        column_str = ", ".join(columns) if columns else "*"
        query = f"SELECT {column_str} FROM `{table_name}`"

        # Add WHERE clause for filters
        if filters:
            conditions = []
            for col, (op, val) in filters.items():
                conditions.append(f"`{col}` {op} {val}")
            query += " WHERE " + " AND ".join(conditions)

        # Execute query
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        return pd.DataFrame(results, columns=column_names)

    except Exception as e:
        print(f"Error occurred: {e}")
        return pd.DataFrame()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def draw_text_input(win, label_text, position, width=20):
    """Draw a text input field with a label."""
    label = Text(position, label_text)
    label.setSize(12)
    label.draw(win)

    input_box = Entry(Point(position.getX() + width * 5, position.getY()), width)
    input_box.draw(win)

    return input_box


def display_results(data):
    """Display query results in a new window."""
    result_win = GraphWin("Query Results", 800, 600)
    result_win.setBackground("white")

    if data.empty:
        no_results = Text(Point(400, 300), "No Results Found")
        no_results.setSize(14)
        no_results.setTextColor("red")
        no_results.draw(result_win)
        result_win.getMouse()
        result_win.close()
        return

    # Display results as a table
    x_start, y_start = 50, 50
    col_width = 150

    # Display headers
    for i, col in enumerate(data.columns):
        header = Text(Point(x_start + i * col_width, y_start), col)
        header.setSize(10)
        header.setStyle("bold")
        header.draw(result_win)

    # Display rows
    for row_idx, row in data.iterrows():
        for col_idx, value in enumerate(row):
            cell = Text(Point(x_start + col_idx * col_width, y_start + (row_idx + 1) * 20), str(value))
            cell.setSize(10)
            cell.draw(result_win)

    result_win.getMouse()
    result_win.close()


def create_dropdown(win, label, options, position, width=15):
    """
    Creates a dropdown menu at the specified position.
    
    Args:
        win: GraphWin object.
        label: Label for the dropdown.
        options: List of options to show in the dropdown.
        position: Point for the dropdown position.
        width: Width of the dropdown menu.
        
    Returns:
        str: The selected option from the dropdown.
    """
    # Draw label
    label_text = Text(Point(position.getX() - 80, position.getY()), label)
    label_text.setSize(12)
    label_text.draw(win)

    # Create the dropdown rectangle
    dropdown = Rectangle(
        Point(position.getX() - width * 5, position.getY() - 10),
        Point(position.getX() + width * 5, position.getY() + 10)
    )
    dropdown.setOutline("black")
    dropdown.setFill("white")
    dropdown.draw(win)

    # Show the initial value
    selected_text = Text(dropdown.getCenter(), "Select...")
    selected_text.setSize(10)
    selected_text.draw(win)

    # Wait for the dropdown to be clicked
    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click, dropdown):
            # Display dropdown options
            dropdown_options = []
            for i, option in enumerate(options):
                option_rect = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() + i * 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (i + 1) * 20)
                )
                option_rect.setFill("white")
                option_rect.setOutline("black")
                option_rect.draw(win)

                option_text = Text(option_rect.getCenter(), option)
                option_text.setSize(10)
                option_text.draw(win)

                dropdown_options.append((option_rect, option_text, option))

            # Wait for user to select an option
            while True:
                option_click = win.getMouse()
                for rect, text, option in dropdown_options:
                    if is_click_in_rectangle(option_click, rect):
                        # Clear all dropdown options
                        for r, t, _ in dropdown_options:
                            r.undraw()
                            t.undraw()

                        # Set the selected text
                        selected_text.setText(option)
                        return option

        time.sleep(0.1)
def create_dropdown(win, label, options, position, width=15):
    """
    Creates a dropdown menu at the specified position.
    
    Args:
        win: GraphWin object.
        label: Label for the dropdown.
        options: List of options to show in the dropdown.
        position: Point for the dropdown position.
        width: Width of the dropdown menu.
        
    Returns:
        str: The selected option from the dropdown.
    """
    # Draw label
    label_text = Text(Point(position.getX() - 80, position.getY()), label)
    label_text.setSize(12)
    label_text.draw(win)

    # Create the dropdown rectangle
    dropdown = Rectangle(
        Point(position.getX() - width * 5, position.getY() - 10),
        Point(position.getX() + width * 5, position.getY() + 10)
    )
    dropdown.setOutline("black")
    dropdown.setFill("white")
    dropdown.draw(win)

    # Show the initial value
    selected_text = Text(dropdown.getCenter(), "Select...")
    selected_text.setSize(10)
    selected_text.draw(win)

    # Wait for the dropdown to be clicked
    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click, dropdown):
            # Display dropdown options
            dropdown_options = []
            for i, option in enumerate(options):
                option_rect = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() + i * 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (i + 1) * 20)
                )
                option_rect.setFill("white")
                option_rect.setOutline("black")
                option_rect.draw(win)

                option_text = Text(option_rect.getCenter(), option)
                option_text.setSize(10)
                option_text.draw(win)

                dropdown_options.append((option_rect, option_text, option))

            # Wait for user to select an option
            while True:
                option_click = win.getMouse()
                for rect, text, option in dropdown_options:
                    if is_click_in_rectangle(option_click, rect):
                        # Clear all dropdown options
                        for r, t, _ in dropdown_options:
                            r.undraw()
                            t.undraw()

                        # Set the selected text
                        selected_text.setText(option)
                        return option

        time.sleep(0.1)


def build_filter_ui():
    """Build a graphical user interface for filtering data."""
    win = GraphWin("Filter Data", 800, 600)
    win.setBackground("lightgray")

    # Define available columns and filters
    available_columns = [
        "Home Team", "Away Team", "Score", "Half Time Score", "Match Excitement",
        "Home Team Goals Scored", "Away Team Goals Scored", "year"
    ]
    filterable_fields = [
        "Home Team Goals Scored", "Away Team Goals Scored", "year", "Match Excitement"
    ]

    # Draw UI elements using a modular function from Globals.py
    create_label(win, "Data Filtering Tool", Point(400, 30), size=18, style="bold")

    # Column selection
    create_label(win, "Select Column for Filters:", Point(100, 120), size=12)
    selected_column = create_dropdown(win, "Column:", available_columns, Point(300, 120))

    # Operator selection
    create_label(win, "Select Operator:", Point(100, 160), size=12)
    operators = ["=", ">", "<", ">=", "<="]
    selected_operator = create_dropdown(win, "Operator:", operators, Point(300, 160))

    # Value input
    value_input = draw_text_input(win, "Value:", Point(100, 200))

    # Submit button
    submit_button = Rectangle(Point(350, 550), Point(450, 580))
    submit_button.setFill("green")
    submit_button.draw(win)
    submit_text = Text(submit_button.getCenter(), "Submit")
    submit_text.setSize(12)
    submit_text.setTextColor("white")
    submit_text.draw(win)

    # Wait for user to submit
    while True:
        click = win.getMouse()

        # Check if submit button is clicked
        if is_click_in_rectangle(click, submit_button):
            selected_value = value_input.getText().strip()
            if selected_column and selected_operator and selected_value:
                # Execute query
                filters = {selected_column: [selected_operator, selected_value]}
                data = filter_data_from_db(filters=filters, columns=available_columns)
                display_results(data)
                break
            else:
                error_msg = Text(Point(400, 500), "Please complete all fields!")
                error_msg.setSize(12)
                error_msg.setTextColor("red")
                error_msg.draw(win)
                time.sleep(2)
                error_msg.undraw()

    win.close()


if __name__ == "__main__":
    build_filter_ui()
