from graphics import *
from Globals import is_click_in_rectangle, create_label
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
        return headers[1:]  # Exclude first column if you don't need it
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
    """
    Removed 'LIKE' operator as requested. Only basic operators remain.
    """
    datatype = get_column_datatype(column_name)
    if datatype == "numerical":
        return ["=", ">", "<", ">=", "<="]
    else:
        return ["="]  # For text columns, only '='

def create_button(win, p1, p2, label, fill_color="gray", text_color="black", text_size=12):
    rect = Rectangle(p1, p2)
    rect.setFill(fill_color)
    rect.setOutline(fill_color)
    rect.draw(win)

    txt = Text(rect.getCenter(), label)
    txt.setSize(text_size)
    txt.setTextColor(text_color)
    txt.draw(win)
    return rect, txt

def create_scrollable_dropdown(win, label, options, position, width=15, visible_count=10):
    dropdown_label_color = "white"
    label_position = Point(position.getX() - (width * 7), position.getY())
    create_label(win, label, label_position, size=12)

    dropdown_bg_color = color_rgb(255, 255, 255) 
    dropdown_outline_color = "black"

    dropdown = Rectangle(
        Point(position.getX() - width*5, position.getY() - 10),
        Point(position.getX() + width*5, position.getY() + 10)
    )
    dropdown.setOutline(dropdown_outline_color)
    dropdown.setFill(dropdown_bg_color)
    dropdown.draw(win)

    selected_text = Text(dropdown.getCenter(), "Select...")
    selected_text.setSize(10)
    selected_text.setTextColor("black")
    selected_text.draw(win)

    while True:
        click = win.getMouse()
        if is_click_in_rectangle(click, dropdown):
            dropdown_options = []
            visible_options = options[:visible_count]

            for i, option in enumerate(visible_options):
                option_rect = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() + i * 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (i+1)*20)
                )
                option_rect.setFill("white")
                option_rect.setOutline("black")
                option_rect.draw(win)

                option_text = Text(option_rect.getCenter(), str(option))
                option_text.setSize(10)
                option_text.setTextColor("black")
                option_text.draw(win)

                dropdown_options.append((option_rect, option_text, option))

            up_button = down_button = up_text = down_text = None
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
                up_text.setTextColor("black")
                up_text.draw(win)

                down_button = Rectangle(
                    Point(dropdown.getP1().getX(), dropdown.getP2().getY() + visible_count * 20),
                    Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (visible_count+1)*20)
                )
                down_button.setFill("#D3D3D3")
                down_button.setOutline("black")
                down_button.draw(win)
                down_text = Text(down_button.getCenter(), "▼")
                down_text.setSize(10)
                down_text.setTextColor("black")
                down_text.draw(win)

            start_index = 0
            while True:
                option_click = win.getMouse()
                if up_button and is_click_in_rectangle(option_click, up_button) and start_index > 0:
                    start_index -= visible_count
                elif (down_button 
                      and is_click_in_rectangle(option_click, down_button) 
                      and start_index + visible_count < len(options)):
                    start_index += visible_count

                for rect, t, _ in dropdown_options:
                    rect.undraw()
                    t.undraw()
                dropdown_options.clear()

                visible_options = options[start_index:start_index+visible_count]
                for i, opt in enumerate(visible_options):
                    option_rect = Rectangle(
                        Point(dropdown.getP1().getX(), dropdown.getP2().getY() + i * 20),
                        Point(dropdown.getP2().getX(), dropdown.getP2().getY() + (i+1)*20)
                    )
                    option_rect.setFill("white")
                    option_rect.setOutline("black")
                    option_rect.draw(win)

                    option_text = Text(option_rect.getCenter(), str(opt))
                    option_text.setSize(10)
                    option_text.setTextColor("black")
                    option_text.draw(win)

                    dropdown_options.append((option_rect, option_text, opt))

                for rect, text_obj, val_opt in dropdown_options:
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
                        selected_text.setText(str(val_opt))
                        return val_opt

def filter_data_from_db(filters=None, columns=None):
    conn = None
    cursor = None
    try:
        conn = openconnection()
        cursor = conn.cursor()

        # If no columns selected, select all
        if not columns or len(columns) == 0:
            column_str = "*"
        else:
            column_str = ", ".join(f"`{col}`" for col in columns)

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

def build_filters_page(win):
    title = Text(Point(450, 40), "Add Filters (Football Theme)")
    title.setSize(16)
    title.setTextColor("white")
    title.setStyle("bold")
    title.draw(win)

    instructions = Text(Point(450, 70), "Add as many filters as you want, then click Next Step.\nThis will get you to the column selection page.")
    instructions.setSize(12)
    instructions.setTextColor("white")
    instructions.draw(win)

    available_columns = get_headers()
    applied_filters = []

    filters_display = Text(Point(450, 280), "No filters yet.")
    filters_display.setSize(12)
    filters_display.setTextColor("white")
    filters_display.draw(win)

    col_label = Text(Point(290, 120), "Column:")
    op_label  = Text(Point(290, 160), "Operator:")
    val_label = Text(Point(290, 200), "Value:")
    for lbl in (col_label, op_label, val_label):
        lbl.setSize(12)
        lbl.setTextColor("white")
        lbl.draw(win)

    col_box = Rectangle(Point(340, 105), Point(520, 135))
    op_box  = Rectangle(Point(340, 145), Point(520, 175))
    val_box = Rectangle(Point(340, 185), Point(520, 215))
    for box in (col_box, op_box, val_box):
        box.setFill("white")
        box.setOutline("white")
        box.draw(win)

    col_text = Text(Point(430, 120), "Select column")
    col_text.setSize(10)
    col_text.setTextColor("black")
    col_text.draw(win)

    op_text = Text(Point(430, 160), "Select operator")
    op_text.setSize(10)
    op_text.setTextColor("black")
    op_text.draw(win)

    val_text = Text(Point(430, 200), "Select value")
    val_text.setSize(10)
    val_text.setTextColor("black")
    val_text.draw(win)

    selected_col = None
    selected_op  = None
    selected_val = None

    add_filter_btn, add_filter_txt = create_button(
        win, Point(540, 105), Point(640, 135), "Add Filter",
        fill_color=color_rgb(28,195,170), text_color="white", text_size=12
    )
    next_step_btn, next_step_txt = create_button(
        win, Point(540, 145), Point(640, 175), "Next Step",
        fill_color=color_rgb(0,128,255), text_color="white", text_size=12
    )
    clear_filters_btn, clear_filters_txt = create_button(
        win, Point(540, 185), Point(640, 215), "Clear All",
        fill_color=color_rgb(200, 128, 0), text_color="white", text_size=12
    )

    while True:
        click = win.getMouse()
        if click is None:
            continue

        x, y = click.getX(), click.getY()

        if 340 <= x <= 520 and 105 <= y <= 135:
            selected_col = create_scrollable_dropdown(win, "", available_columns, Point(430,120))
            col_text.setText(selected_col if selected_col else "Select column")
            selected_op = None
            selected_val = None
            op_text.setText("Select operator")
            val_text.setText("Select value")

        if 340 <= x <= 520 and 145 <= y <= 175 and selected_col:
            operators = get_operators_for_column(selected_col)
            selected_op = create_scrollable_dropdown(win, "", operators, Point(430,160))
            op_text.setText(selected_op if selected_op else "Select operator")
            selected_val = None
            val_text.setText("Select value")

        if 340 <= x <= 520 and 185 <= y <= 215 and selected_col and selected_op:
            unique_vals = get_unique_values(selected_col)
            selected_val = create_scrollable_dropdown(win, "", unique_vals, Point(430,200))
            val_text.setText(str(selected_val) if selected_val else "Select value")

        # Add Filter
        if 540 <= x <= 640 and 105 <= y <= 135:
            if selected_col and selected_op and selected_val is not None:
                applied_filters.append((selected_col, selected_op, selected_val))
                filters_str = [f"{c} {o} '{v}'" for (c, o, v) in applied_filters]
                filters_display.setText(" AND\n".join(filters_str))
                selected_col = None
                selected_op = None
                selected_val = None
                col_text.setText("Select column")
                op_text.setText("Select operator")
                val_text.setText("Select value")

        # Next Step
        if 540 <= x <= 640 and 145 <= y <= 175:
            return applied_filters

        # Clear All
        if 540 <= x <= 640 and 185 <= y <= 215:
            applied_filters.clear()
            filters_display.setText("No filters yet.")
            selected_col = None
            selected_op = None
            selected_val = None
            col_text.setText("Select column")
            op_text.setText("Select operator")
            val_text.setText("Select value")

def build_columns_page(win, filters):
    for item in win.items[:]:
        item.undraw()
    win.items.clear()

    sidebar_color = color_rgb(31, 27, 58)
    sidebar = Rectangle(Point(0,0), Point(200,500))
    sidebar.setFill(sidebar_color)
    sidebar.setOutline(sidebar_color)
    sidebar.draw(win)

    title = Text(Point(450, 40), "Select Columns to Display")
    title.setSize(16)
    title.setTextColor("white")
    title.setStyle("bold")
    title.draw(win)

    instructions = Text(Point(450, 70), "Add columns, then click Submit. \nIf you select no columns, all columns will be displayed.")
    instructions.setSize(12)
    instructions.setTextColor("white")
    instructions.draw(win)

    back_btn, back_txt = create_button(
        win, Point(20,20), Point(180,60), "Back",
        fill_color=color_rgb(28,195,170), text_color="white", text_size=12
    )
    submit_btn, submit_txt = create_button(
        win, Point(20,80), Point(180,120), "Submit",
        fill_color=color_rgb(28,195,170), text_color="white", text_size=12
    )

    available_columns = get_headers()
    selected_columns = []
    columns_display = Text(Point(450, 280), "No columns selected.")
    columns_display.setSize(12)
    columns_display.setTextColor("white")
    columns_display.draw(win)

    col_label = Text(Point(290, 140), "Display Column:")
    col_label.setSize(12)
    col_label.setTextColor("white")
    col_label.draw(win)

    disp_box = Rectangle(Point(340,125), Point(520,155))
    disp_box.setFill("white")
    disp_box.setOutline("white")
    disp_box.draw(win)

    disp_text = Text(Point(430,140), "Select column")
    disp_text.setSize(10)
    disp_text.setTextColor("black")
    disp_text.draw(win)

    add_col_btn, add_col_txt = create_button(
        win, Point(540,125), Point(640,155), "Add Column",
        fill_color=color_rgb(28,195,170), text_color="white", text_size=12
    )

    selected_col = None

    while True:
        click = win.getMouse()
        if click is None:
            continue
        x, y = click.getX(), click.getY()

        if 20 <= x <= 180 and 20 <= y <= 60:
            return None  # back to filters

        if 20 <= x <= 180 and 80 <= y <= 120:
            # If no columns selected, everything is selected
            df = filter_data_from_db(filters=filters, columns=selected_columns if selected_columns else None)
            return df

        if 340 <= x <= 520 and 125 <= y <= 155:
            selected_col = create_scrollable_dropdown(win, "", available_columns, Point(430,140))
            disp_text.setText(selected_col if selected_col else "Select column")

        if 540 <= x <= 640 and 125 <= y <= 155 and selected_col:
            if selected_col not in selected_columns:
                selected_columns.append(selected_col)
                columns_display.setText(", ".join(selected_columns))
            selected_col = None
            disp_text.setText("Select column")

def build_2_page_ui():
    win = GraphWin("Football Data Filtering", 900, 500)
    bg_color = color_rgb(44, 40, 85)
    win.setBackground(bg_color)

    sidebar_color = color_rgb(31, 27, 58)
    sidebar = Rectangle(Point(0,0), Point(200,500))
    sidebar.setFill(sidebar_color)
    sidebar.setOutline(sidebar_color)
    sidebar.draw(win)

    filters = build_filters_page(win)
    if filters is None:
        win.close()
        return pd.DataFrame()

    while True:
        df = build_columns_page(win, filters)
        if df is None:
            # user clicked back => re-draw filter page
            for item in win.items[:]:
                item.undraw()
            win.items.clear()
            sidebar = Rectangle(Point(0,0), Point(200,500))
            sidebar.setFill(sidebar_color)
            sidebar.setOutline(sidebar_color)
            sidebar.draw(win)
            filters = build_filters_page(win)
        else:
            win.close()
            return df

def main():
    final_df = build_2_page_ui()
    print("\nData returned to main():")
    print(final_df)

if __name__ == "__main__":
    main()
