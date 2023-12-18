class Connection:
    def __init__(self, comp_conn, wire_name, wire_end):
        self.type = "connection"
        self.comp_conn = comp_conn   # in1, out
        self.wire_name = wire_name        # wire string name
        self.wire_end = wire_end         # "begin" or "end"

    def __repr__(self):
        return "Connector Name: " + self.comp_conn + \
               " Wire Name: " + self.wire_name + \
               " Wire End: " + self.wire_end

    def reprJson(self):
        return dict(type=self.type, comp_conn=self.comp_conn, wire_name=self.wire_name, wire_end=self.wire_end)
