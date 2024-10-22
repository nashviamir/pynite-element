from pynite_element.solvers import DefaultSolver


solver = DefaultSolver.from_json("E:\\python packages\\pynite-element\\usage\\data.json")

solver.solve()
solver.plot()

print("displacements: ", solver.displacements_results, sep="\n")
print("forces: ", solver.forces_results, sep="\n")
     