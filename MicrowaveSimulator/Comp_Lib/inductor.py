from pathlib import Path

from Comp_Lib.component import Component


class Inductor(Component):
    """Model for lumped element inductor"""
    def __init__(self, canvas, x1, y1, inductance):
        super().__init__(canvas, x1, y1)
        self.inductance = inductance
        self.type = 'inductor'
        self.filename = Path(__file__).parent / "../images/lumped/inductor_60x30.png"

        self.text = 'L=' + str(inductance) + 'nH'
        self.text_id = None

        self.create()

    def create(self):
        self.create_image(self.filename)
        self.update_bbox()
        self.create_text()
        self.create_selector()
        self.create_connectors()
        self.set_connector_visibility()

    def update(self):
        self.update_position()
        self.update_image(self.filename)
        self.update_bbox()
        self.update_text()
        self.update_selector()
        self.update_connectors()
        self.set_connector_visibility()

    def create_text(self):
        self.text_id = self.canvas.create_text(self.x1, self.y1-30,
                                text=self.text, fill="black",
                                font='Helvetica 10 bold',
                                angle=self.angle, tags="text")

    def update_text(self):
        self.canvas.coords(self.text_id, self.x1, self.y1-30)

    def __repr__(self):
        return ("Type: " + self.type + " x1: " + str(self.x1) + " y1: " + str(self.y1) + " inductance: " +
                str(self.inductance) + " wire list: " + str(self.wire_list.__repr__()))

    def reprJson(self):
        return dict(type=self.type, x1=self.x1, y1=self.y1, angle=self.angle, inductance=self.inductance,
                    wire_list=self.wire_list)
