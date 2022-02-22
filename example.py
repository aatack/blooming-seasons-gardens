from garden.elements.arrow import Arrow
from garden.elements.bed import Bed
from garden.elements.label import Label
from garden.elements.plant import Plant
from garden.garden import Garden
from trickle.window import Window

plant = Plant("Tulip", 0.08, red=0.8, green=0.4)
arrow = Arrow(0.1, 0.1, 0.4, 0.4)
label = Label("Tulip", horizontal=0.45, vertical=0.45)
bed = Bed([plant, arrow, label], horizontal=0.8, vertical=0.8)

garden = Garden(bed)

window = Window()

window.run(garden.component)
