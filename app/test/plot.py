
from app.services.core import *

sections = find_sections('K205-2017')
section = sections[int(1)]
section = section
paper = section.set_paper()
curves = section.stroke()
hLines = section.hLines
fill = section.fill()
