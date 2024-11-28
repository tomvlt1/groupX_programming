from graphics import *
from applyfilters import (add_exact_match_clause,add_starts_with_clause,add_between_clause,add_ends_with_clause)

class FilterGUI:
    def __init__(self):
        self.win = GraphWin("Filtro de Datos", 600, 400)
        self.win.setBackground("lightgray")
        self.filters = {}
        self.variables = [
            "home_team_name",
            "away_team_name",
            "full_time_score",
            "half_time_score",
            "match_excitement",
            "home_team_rating",
            "away_team_rating",
            "home_team_possession",
            "away_team_possession",
            # Agrega más variables según sea necesario
        ]
        self.current_filter = None
        self.main_menu()

    def main_menu(self):
        self.win.clear()
        title = Text(Point(300, 50), "Choose a filter to filter")
        title.setSize(20)
        title.draw(self.win)

        # Crear botones para cada variable
        y_start = 100
        y_step = 40
        for idx, var in enumerate(self.variables):
            button = Rectangle(Point(150, y_start + idx * y_step - 15), Point(450, y_start + idx * y_step + 15))
            button.setFill("white")
            button.draw(self.win)
            label = Text(button.getCenter(), var.replace("_", " ").capitalize())
            label.draw(self.win)
            # Asociar el click con la variable
        self.win.update()
        self.wait_for_variable_selection()

    def wait_for_variable_selection(self):
        while True:
            click = self.win.getMouse()
            x, y = click.getX(), click.getY()
            for idx, var in enumerate(self.variables):
                y_start = 100
                y_step = 40
                button = Rectangle(Point(150, y_start + idx * y_step - 15), Point(450, y_start + idx * y_step + 15))
                if button.getP1().getX() <= x <= button.getP2().getX() and button.getP1().getY() <= y <= button.getP2().getY():
                    self.current_filter = var
                    self.filter_window(var)
                    return

    def filter_window(self, variable):
        self.win.clear()
        title = Text(Point(300, 30), f"Filtrar por: {variable.replace('_', ' ').capitalize()}")
        title.setSize(16)
        title.draw(self.win)

        # Dependiendo del tipo de variable, mostrar opciones
        # Para simplificar, asumiremos que las variables de tipo string y numéricas
        if "name" in variable or "score" in variable:
            self.string_filter_input(variable)
        else:
            self.numeric_filter_input(variable)

    def string_filter_input(self, variable):
        options = ["Exact match", "starts with", "ends with"]
        y_start = 100
        y_step = 40
        for idx, option in enumerate(options):
            button = Rectangle(Point(150, y_start + idx * y_step - 15), Point(450, y_start + idx * y_step + 15))
            button.setFill("white")
            button.draw(self.win)
            label = Text(button.getCenter(), option)
            label.draw(self.win)
        # Botón de aceptar
        accept_button = Rectangle(Point(250, y_start + len(options)*y_step + 20), Point(350, y_start + len(options)*y_step + 50))
        accept_button.setFill("lightblue")
        accept_button.draw(self.win)
        accept_label = Text(accept_button.getCenter(), "Aceptar")
        accept_label.draw(self.win)

        self.win.update()
        # Esperar selección de opción
        while True:
            click = self.win.getMouse()
            x, y = click.getX(), click.getY()
            for idx, option in enumerate(options):
                btn = Rectangle(Point(150, y_start + idx * y_step - 15), Point(450, y_start + idx * y_step + 15))
                if btn.getP1().getX() <= x <= btn.getP2().getX() and btn.getP1().getY() <= y <= btn.getP2().getY():
                    selected_option = option
                    self.get_string_value(variable, selected_option)
                    return
            # Aceptar sin seleccionar opción (puede manejarse mejor)
    
    def get_string_value(self, variable, option):
        # Crear una entrada de texto para el valor
        prompt = Text(Point(300, 150), f"Ingrese el valor para '{option}':")
        prompt.draw(self.win)
        input_box = Rectangle(Point(200, 180), Point(400, 210))
        input_box.setFill("white")
        input_box.draw(self.win)
        input_text = Text(input_box.getCenter(), "")
        input_text.draw(self.win)

        # Instrucciones para ingresar texto
        instructions = Text(Point(300, 240), "Escribe el valor y haz clic fuera de la caja.")
        instructions.setSize(10)
        instructions.draw(self.win)

        value = ""

        while True:
            click = self.win.getMouse()
            x, y = click.getX(), click.getY()
            # Detectar clic dentro de la caja de texto
            if 200 <= x <= 400 and 180 <= y <= 210:
                # Simular ingreso de texto
                value = self.get_text_input()
                input_text.setText(value)
            else:
                break  # Asumir que el usuario terminó de ingresar
        # Guardar el filtro
        if option == "Match Exacto":
            self.filters[variable] = {"exact": value}
        elif option == "Empieza con":
            self.filters[variable] = {"starts_with": value}
        elif option == "Termina con":
            self.filters[variable] = {"ends_with": value}
        self.ask_continue()

    def numeric_filter_input(self, variable):
        # Opciones: exact value, range (min - max)
        options = ["Valor Exacto", "Rango (Min - Max)"]
        y_start = 100
        y_step = 40
        for idx, option in enumerate(options):
            button = Rectangle(Point(150, y_start + idx * y_step - 15), Point(450, y_start + idx * y_step + 15))
            button.setFill("white")
            button.draw(self.win)
            label = Text(button.getCenter(), option)
            label.draw(self.win)
        # Botón de aceptar
        accept_button = Rectangle(Point(250, y_start + len(options)*y_step + 20), Point(350, y_start + len(options)*y_step + 50))
        accept_button.setFill("lightblue")
        accept_button.draw(self.win)
        accept_label = Text(accept_button.getCenter(), "Aceptar")
        accept_label.draw(self.win)

        self.win.update()
        # Esperar selección de opción
        while True:
            click = self.win.getMouse()
            x, y = click.getX(), click.getY()
            for idx, option in enumerate(options):
                btn = Rectangle(Point(150, y_start + idx * y_step - 15), Point(450, y_start + idx * y_step + 15))
                if btn.getP1().getX() <= x <= btn.getP2().getX() and btn.getP1().getY() <= y <= btn.getP2().getY():
                    selected_option = option
                    self.get_numeric_value(variable, selected_option)
                    return
            # Aceptar sin seleccionar opción (puede manejarse mejor)

    def get_numeric_value(self, variable, option):
        if option == "Valor Exacto":
            prompt = Text(Point(300, 150), f"Ingrese el valor exacto para '{variable}':")
            prompt.draw(self.win)
            input_box = Rectangle(Point(200, 180), Point(400, 210))
            input_box.setFill("white")
            input_box.draw(self.win)
            input_text = Text(input_box.getCenter(), "")
            input_text.draw(self.win)

            # Instrucciones para ingresar texto
            instructions = Text(Point(300, 240), "Escribe el valor y haz clic fuera de la caja.")
            instructions.setSize(10)
            instructions.draw(self.win)

            value = ""

            while True:
                click = self.win.getMouse()
                x, y = click.getX(), click.getY()
                # Detectar clic dentro de la caja de texto
                if 200 <= x <= 400 and 180 <= y <= 210:
                    # Simular ingreso de texto
                    value = self.get_text_input()
                    input_text.setText(value)
                else:
                    break  # Asumir que el usuario terminó de ingresar
            # Guardar el filtro
            self.filters[variable] = {"exact": value}
        elif option == "Rango (Min - Max)":
            # Ingresar valor mínimo
            prompt_min = Text(Point(300, 130), f"Ingrese el valor MÍNIMO para '{variable}':")
            prompt_min.draw(self.win)
            input_box_min = Rectangle(Point(200, 160), Point(400, 190))
            input_box_min.setFill("white")
            input_box_min.draw(self.win)
            input_text_min = Text(input_box_min.getCenter(), "")
            input_text_min.draw(self.win)

            instructions_min = Text(Point(300, 220), "Escribe el valor y haz clic fuera de la caja.")
            instructions_min.setSize(10)
            instructions_min.draw(self.win)

            min_val = ""
            while True:
                click = self.win.getMouse()
                x, y = click.getX(), click.getY()
                if 200 <= x <= 400 and 160 <= y <= 190:
                    min_val = self.get_text_input()
                    input_text_min.setText(min_val)
                else:
                    break

            # Ingresar valor máximo
            prompt_max = Text(Point(300, 250), f"Ingrese el valor MÁXIMO para '{variable}':")
            prompt_max.draw(self.win)
            input_box_max = Rectangle(Point(200, 280), Point(400, 310))
            input_box_max.setFill("white")
            input_box_max.draw(self.win)
            input_text_max = Text(input_box_max.getCenter(), "")
            input_text_max.draw(self.win)

            instructions_max = Text(Point(300, 340), "Escribe el valor y haz clic fuera de la caja.")
            instructions_max.setSize(10)
            instructions_max.draw(self.win)

            max_val = ""
            while True:
                click = self.win.getMouse()
                x, y = click.getX(), click.getY()
                if 200 <= x <= 400 and 280 <= y <= 310:
                    max_val = self.get_text_input()
                    input_text_max.setText(max_val)
                else:
                    break

            # Guardar el filtro
            self.filters[variable] = {"min": min_val, "max": max_val}
        self.ask_continue()

    def get_text_input(self):
        # Debido a las limitaciones de graphics.py, no podemos capturar texto directamente.
        # Como alternativa, podemos solicitar al usuario que ingrese el texto en la consola.
        # Esta no es una solución ideal, pero es una limitación de graphics.py.
        win_text = Text(Point(300, 370), "Ingrese el texto en la consola y presione Enter.")
        win_text.draw(self.win)
        self.win.update()
        value = input("Ingrese el valor: ")
        win_text.undraw()
        return value

    def ask_continue(self):
        # Preguntar si el usuario desea agregar más filtros
        prompt = Text(Point(300, 200), "¿Desea agregar otro filtro?")
        prompt.draw(self.win)
        yes_button = Rectangle(Point(200, 230), Point(250, 260))
        yes_button.setFill("green")
        yes_button.draw(self.win)
        yes_label = Text(yes_button.getCenter(), "Sí")
        yes_label.draw(self.win)

        no_button = Rectangle(Point(350, 230), Point(400, 260))
        no_button.setFill("red")
        no_button.draw(self.win)
        no_label = Text(no_button.getCenter(), "No")
        no_label.draw(self.win)

        self.win.update()

        while True:
            click = self.win.getMouse()
            x, y = click.getX(), click.getY()
            if 200 <= x <= 250 and 230 <= y <= 260:
                # Sí, agregar otro filtro
                prompt.undraw()
                yes_button.undraw()
                yes_label.undraw()
                no_button.undraw()
                no_label.undraw()
                self.main_menu()
                return
            elif 350 <= x <= 400 and 230 <= y <= 260:
                # No, finalizar
                prompt.undraw()
                yes_button.undraw()
                yes_label.undraw()
                no_button.undraw()
                no_label.undraw()
                self.show_query()
                return

    def show_query(self):
        # Construir la consulta SQL basada en los filtros
        query = "SELECT * FROM your_table_name WHERE 1=1"  # Reemplaza 'your_table_name' con el nombre real de tu tabla

        for var, criteria in self.filters.items():
            if "exact" in criteria:
                query = add_exact_match_clause(query, var, criteria["exact"])
            elif "starts_with" in criteria:
                query = add_starts_with_clause(query, var, criteria["starts_with"])
            elif "ends_with" in criteria:
                query = add_ends_with_clause(query, var, criteria["ends_with"])
            elif "min" in criteria and "max" in criteria:
                query = add_between_clause(query, var, criteria["min"], criteria["max"])

        # Mostrar la consulta al usuario
        self.win.clear()
        title = Text(Point(300, 50), "Consulta SQL Generada")
        title.setSize(16)
        title.draw(self.win)

        query_text = Text(Point(300, 200), query)
        query_text.setSize(12)
        query_text.draw(self.win)

        instructions = Text(Point(300, 350), "Haz clic en cualquier lugar para salir.")
        instructions.setSize(10)
        instructions.draw(self.win)

        self.win.update()
        self.win.getMouse()
        self.win.close()

def main():
    gui = FilterGUI()
    
    

