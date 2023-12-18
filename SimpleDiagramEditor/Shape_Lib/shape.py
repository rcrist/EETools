class Shape:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.fill_color = "cyan"
        self.border_color = "black"
        self.border_width = 3

        self.id = None
        self.is_selected = False
        self.is_drawing = False
        self.sel_list = []
        self.conn_list = []
        self.line_list = []
        self.selector = None

    def check_selector_hit(self, x, y):
        for sel in self.sel_list:
            if sel.selector_hit_test(x, y):
                return sel
        return None

    def check_connector_hit(self, x, y):
        for conn in self.conn_list:
            if conn.connector_hit_test(x, y):
                return conn
        return None

    def move_connected_lines(self):
        for connection in self.line_list:
            for connector in self.conn_list:
                if connector == connection.connector_obj:
                    # print(connector, connection.line_obj, "Match")
                    if connection.line_end == "begin":
                        connection.line_obj.x1 = connector.x
                        connection.line_obj.y1 = connector.y
                    elif connection.line_end == "end":
                        connection.line_obj.x2 = connector.x
                        connection.line_obj.y2 = connector.y

