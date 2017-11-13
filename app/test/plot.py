
from app.services.core import *

projectNo = 'K043-2015-5'
sections = find_sections(projectNo)
section = sections[10]
section.set_paper()
layers = section.draw_sectionLine(find_layers(projectNo))
