class Connection:
    def __init__(self, conn_obj, line_obj, line_end):
        self.connector_obj = conn_obj
        self.line_obj = line_obj
        self.line_end = line_end      # "begin" or "end"

    def __repr__(self):
        return "Connection Object: " + self.connector_obj.name + \
               " Connection Object Location: " + str(self.connector_obj.x) + ", " + str(self.connector_obj.y) + \
               " Line Object Points: " + str(self.line_obj.points) + \
               " Line End: " + self.line_end
