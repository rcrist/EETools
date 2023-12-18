class Circuit(object):
    def __init__(self, circuit_list, wire_list):
        self.type = "circuit"
        self.circuit_list = circuit_list
        self.wire_list = wire_list

    def __repr__(self):
        return ("Type: " + self.type + " Circuit List: " + str(self.circuit_list.__repr__()) + " Wire List: " +
                str(self.wire_list.__repr__()))

    def reprJson(self):
        return dict(type=self.type, circuit_list=self.circuit_list, wire_list=self.wire_list)
