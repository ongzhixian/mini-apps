from graphviz import Digraph

dot = Digraph(comment='The Round Table')
dot.format = 'svg'


dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')


print(dot.source)

dot.render('round-table', view=True)  # doctest: +SKIP