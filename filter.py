from graphics import *
from Globals import is_click_in_rectangle, create_label, create_button
from DataFunctions import openconnection
import pandas as pd

def get_headers():
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM `DataDetail`")
        headers = [row[0] for row in cursor.fetchall()]
        # Exclude the first column if you don’t need it:
        return headers[1:]
    except Exception as e:
        print(f"Error fetching headers: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_column_datatype(column_name):
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()
        query = f"SELECT `{column_name}` FROM `DataDetail` WHERE `{column_name}` IS NOT NULL LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            if isinstance(result[0], (int, float)):
                return "numerical"
            else:
                return "text"
    except Exception as e:
        print(f"Error determining datatype for column {column_name}: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return "text"

def get_unique_values(column_name):
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()
        query = f"SELECT DISTINCT `{column_name}` FROM `DataDetail`"
        cursor.execute(query)
        results = cursor.fetchall()
        return [row[0] for row in results if row[0] is not None]
    except Exception as e:
        print(f"Error fetching unique values: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_operators_for_column(column_name):
    datatype = get_column_datatype(column_name)
    if datatype == "numerical":
        return ["=", ">", "<", ">=", "<="]
    elif datatype == "text":
        return ["=", "LIKE"]
    else:
        return ["="]

def create_scrollable_dropdown(win, label, options, position, width=15, visible_count=10):
    label_position = Point(position.getX() - (width * 8), position.getY())
    create_label(win, label, label_position, size=12)

    dropdown = Rectangle(
        Point(position.getX() - width * 5, position.getY() - 10),
        Point(position.getX() + width * 5, position.getY() + 10)
    )
    dropdown.setOutline("black")
    dropdown.setFill("white")
    dropdown.draw(win)

    selected_text = Text(dropdown.getCenter(), "Select...")
    selected_text.setSize(10)
    selected_text.draw(win)

    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click, dropdown):
            dropdown_options = []
            visible_options = options[:visible_count]

            # Draw visible options
            for i, option in enumerate(visible_options):
                option_rect = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() + i * 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (i + 1) * 20)
                )
                option_rect.setFill("white")
                option_rect.setOutline("black")
                option_rect.draw(win)

                option_text = Text(option_rect.getCenter(), str(option))
                option_text.setSize(10)
                option_text.draw(win)

                dropdown_options.append((option_rect, option_text, option))

            # Draw navigation buttons if needed
            up_button, down_button = None, None
            if len(options) > visible_count:
                up_button = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() - 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY())
                )
                up_button.setFill("#D3D3D3")
                up_button.setOutline("black")
                up_button.draw(win)
                up_text = Text(up_button.getCenter(), "▲")
                up_text.setSize(10)
                up_text.draw(win)

                down_button = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() + visible_count * 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (visible_count + 1) * 20)
                )
                down_button.setFill("#D3D3D3")
                down_button.setOutline("black")
                down_button.draw(win)
                down_text = Text(down_button.getCenter(), "▼")
                down_text.setSize(10)
                down_text.draw(win)

            start_index = 0
            while True:
                option_click = win.getMouse()

                # Handle up/down clicks
                if up_button and is_click_in_rectangle(option_click, up_button) and start_index > 0:
                    start_index -= visible_count
                elif (down_button 
                      and is_click_in_rectangle(option_click, down_button) 
                      and start_index + visible_count < len(options)):
                    start_index += visible_count

                # Clear old items
                for rect, text, _ in dropdown_options:
                    rect.undraw()
                    text.undraw()
                dropdown_options.clear()

                visible_options = options[start_index:start_index + visible_count]
                for i, option in enumerate(visible_options):
                    option_rect = Rectangle(
                        Point(dropdown.getP1().getX(), dropdown.getP2().getY() + i * 20),
                        Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (i + 1) * 20)
                    )
                    option_rect.setFill("white")
                    option_rect.setOutline("black")
                    option_rect.draw(win)
                    option_text = Text(option_rect.getCenter(), str(option))
                    option_text.setSize(10)
                    option_text.draw(win)
                    dropdown_options.append((option_rect, option_text, option))

                # Check if user clicked an option
                for rect, text, opt in dropdown_options:
                    if is_click_in_rectangle(option_click, rect):
                        for r, t, _ in dropdown_options:
                            r.undraw()
                            t.undraw()
                        if up_button:
                            up_button.undraw()
                            up_text.undraw()
                        if down_button:
                            down_button.undraw()
                            down_text.undraw()
                        selected_text.setText(str(opt))
                        return opt

def filter_data_from_db(filters=None, columns=None):
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()

        if columns:
            column_str = ", ".join(f"`{col}`" for col in columns)
        else:
            column_str = "*"

        query = f"SELECT {column_str} FROM `DataDetail`"

        if filters:
            conditions = []
            for (col, op, val) in filters:
                conditions.append(f"`{col}` {op} '{val}'")
            query += " WHERE " + " AND ".join(conditions)

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

def build_filter_ui():
    win = GraphWin("Filter Data", 1100, 800)
    win.setBackground("#FFFFFF")

    # Left sidebar
    sidebar = Rectangle(Point(0, 0), Point(200, 800))
    sidebar.setFill("#2E8B57")
    sidebar.draw(win)

    # Left-side buttons: Back and Submit Data
    back_button, back_txt = create_button(win, Point(20, 20), Point(180, 60), "Back", "#1E2A39", "white")
    submit_button, submit_txt = create_button(win, Point(20, 80), Point(180, 120), "Submit Data", "#1E2A39", "white")

    create_label(win, "Data Filtering Tool", Point(600, 50), size=20, style="bold")

    available_columns = get_headers()

    # Lists to keep track of columns to display and filters
    selected_display_columns = []
    applied_filters = []

    # Text objects to show user selections
    displayed_columns_text = Text(Point(600, 120), "No columns selected.")
    displayed_filters_text = Text(Point(600, 160), "No filters applied.")
    displayed_columns_text.setSize(12)
    displayed_filters_text.setSize(12)
    displayed_columns_text.draw(win)
    displayed_filters_text.draw(win)

    # Filter inputs (main area)
    col_label = Text(Point(600, 250), "Filter Column:")
    op_label  = Text(Point(600, 300), "Operator:")
    val_label = Text(Point(600, 350), "Value:")
    for lbl in (col_label, op_label, val_label):
        lbl.setSize(12)
        lbl.draw(win)

    col_box  = Rectangle(Point(650, 235), Point(950, 265))
    op_box   = Rectangle(Point(650, 285), Point(950, 315))
    val_box  = Rectangle(Point(650, 335), Point(950, 365))
    for box in (col_box, op_box, val_box):
        box.setOutline("black")
        box.setFill("white")
        box.draw(win)

    col_text = Text(Point(800, 250), "Select column")
    op_text  = Text(Point(800, 300), "Select operator")
    val_text = Text(Point(800, 350), "Select value")
    for t in (col_text, op_text, val_text):
        t.setSize(10)
        t.draw(win)

    # Add Filter button (placed near the filter boxes)
    add_filter_button, add_filter_txt = create_button(
        win, Point(980, 290), Point(1080, 330), "Add Filter", "#1E2A39", "white"
    )

    selected_filter_col = None
    selected_operator   = None
    selected_value      = None

    # Column to Display (main area)
    disp_col_label = Text(Point(600, 450), "Display Column:")
    disp_col_label.setSize(12)
    disp_col_label.draw(win)

    disp_col_box = Rectangle(Point(650, 435), Point(950, 465))
    disp_col_box.setOutline("black")
    disp_col_box.setFill("white")
    disp_col_box.draw(win)

    disp_col_text = Text(Point(800, 450), "Select column")
    disp_col_text.setSize(10)
    disp_col_text.draw(win)

    # Add Column button (placed near the column box)
    add_col_button, add_col_txt = create_button(
        win, Point(980, 435), Point(1080, 475), "Add Column", "#1E2A39", "white"
    )

    selected_display_col = None

    result_df = pd.DataFrame()

    while True:
        click = win.getMouse()

        if is_click_in_rectangle(click, back_button):
            print("Back clicked.")
            # If you want to return an empty df or something:
            win.close()
            return pd.DataFrame()

        if is_click_in_rectangle(click, submit_button):
            # Generate final data with chosen columns & filters
            result_df = filter_data_from_db(filters=applied_filters, columns=selected_display_columns)
            print("Final Data:")
            print(result_df)
            win.close()
            return result_df

        # If user clicks the filter column box
        if is_click_in_rectangle(click, col_box):
            selected_filter_col = create_scrollable_dropdown(win, "Filter Column", available_columns, Point(800, 250))
            col_text.setText(selected_filter_col if selected_filter_col else "Select column")
            selected_operator = None
            selected_value = None
            op_text.setText("Select operator")
            val_text.setText("Select value")

        # If user clicks operator box
        if is_click_in_rectangle(click, op_box) and selected_filter_col:
            operators = get_operators_for_column(selected_filter_col)
            selected_operator = create_scrollable_dropdown(win, "Operator", operators, Point(800, 300))
            op_text.setText(selected_operator if selected_operator else "Select operator")
            selected_value = None
            val_text.setText("Select value")

        # If user clicks value box
        if is_click_in_rectangle(click, val_box) and selected_filter_col and selected_operator:
            unique_values = get_unique_values(selected_filter_col)
            selected_value = create_scrollable_dropdown(win, "Value", unique_values, Point(800, 350))
            val_text.setText(str(selected_value) if selected_value else "Select value")

        # Add Filter clicked
        if is_click_in_rectangle(click, add_filter_button):
            if selected_filter_col and selected_operator and (selected_value is not None):
                applied_filters.append((selected_filter_col, selected_operator, selected_value))
                filters_str = [f"{col} {op} '{val}'" for (col, op, val) in applied_filters]
                displayed_filters_text.setText(" AND\n".join(filters_str))
                # Reset
                selected_filter_col = None
                selected_operator   = None
                selected_value      = None
                col_text.setText("Select column")
                op_text.setText("Select operator")
                val_text.setText("Select value")

        # If user clicks the display column box
        if is_click_in_rectangle(click, disp_col_box):
            selected_display_col = create_scrollable_dropdown(win, "Display Column", available_columns, Point(800, 450))
            disp_col_text.setText(selected_display_col if selected_display_col else "Select column")

        # Add Column clicked
        if is_click_in_rectangle(click, add_col_button) and selected_display_col:
            if selected_display_col not in selected_display_columns:
                selected_display_columns.append(selected_display_col)
                displayed_columns_text.setText(", ".join(selected_display_columns))
            selected_display_col = None
            disp_col_text.setText("Select column")

def main():
    df = build_filter_ui()

    print("\nData returned to main():")
    print(df)
    return df

if __name__ == "__main__":
    main()
