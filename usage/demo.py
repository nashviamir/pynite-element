from pynite_element.solvers import DefaultSolver


solver = DefaultSolver.from_json("E:\\python packages\\pynite-element\\usage\\data.json")

solver.solve()
solver.plot()
     