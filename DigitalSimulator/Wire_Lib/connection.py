class Connection:
    def __init__(self, conn_obj, wire_obj, wire_end):
        self.type = "connection"
        self.connector_obj = conn_obj
        self.wire_obj = wire_obj
        self.wire_end = wire_end      # "begin" or "end"

    def __repr__(self):
        return "Connection Object: " + str(self.connector_obj) + \
               " Line Object: " + str(self.wire_obj) + \
               " Line End: " + self.wire_end

    def reprJson(self):
        return dict(type=self.type, wire_obj=self.wire_obj, wire_end=self.wire_end)
