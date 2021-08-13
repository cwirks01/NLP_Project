import pyanx
import site

chart = pyanx.Pyanx()

tyrion = chart.add_node(entity_type='Person', label='Tyrion')  # n0
tywin = chart.add_node(entity_type='Person', label='Tywin')  # n1
jaime = chart.add_node(entity_type='Person', label='Jaime')  # n2
cersei = chart.add_node(entity_type='Woman', label='Cersei')  # n3

chart.add_edge(tywin, tyrion, 'Father of')
chart.add_edge(jaime, tyrion, 'Brother of')
chart.add_edge(cersei, tyrion, 'Sister of')

probe = 'test_probe.anx'

print(pyanx.__file__)
chart.create(probe)
