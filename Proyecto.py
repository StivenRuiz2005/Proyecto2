from minizinc import Instance, Model, Solver

"""
Autor: Carlos Stiven Ruiz Rojas
Descripcion: Este archivo contiene el código necesario para resolver el problema planteado en el miniproyecto
Fecha de creación: 28-11-2024
Fecha de última modificación: 28-11-2024
"""


# Asegúrate de tener algo similar a esto
model = Model("miniproyecto.mzn")
solver = Solver.lookup("gecode")  # o el solver que estés usando
instance = Instance(solver, model)

# Configura tus parámetros 
instance["n"] = 15
instance["num_actuales"] = 3
instance["num_nuevas"] = 4

# Corrige la definición de actuales para que sea una matriz 2D
instance["actuales"] = [[6,8], [8,4], [10,10]]

# Usa una lista de listas para poblacion y entorno
instance["poblacion"] = [
    [4,0,1,1,2,2,0,0,4,15,15,4,11,2,1],
    [4,0,3,1,6,2,0,0,4,15,15,4,8,2,1],
    [4,0,3,1,6,2,0,0,4,9,9,4,2,2,2],
    [3,1,2,2,3,1,0,0,4,8,8,4,1,2,2],
    [2,1,1,2,2,1,0,0,4,7,7,4,1,1,2],
    [1,0,1,1,1,1,0,0,4,6,6,4,1,1,1],
    [0,0,0,1,1,0,0,0,4,5,5,4,1,0,1],
    [0,0,0,0,0,0,0,0,4,4,4,4,0,0,0],
    [1,0,0,0,0,0,0,0,4,3,3,4,0,0,0],
    [2,1,1,1,2,2,1,1,4,2,2,4,1,1,1],
    [3,2,2,2,3,3,2,2,4,1,1,4,2,2,2],
    [4,3,3,3,4,4,3,3,4,0,0,4,3,3,3],
    [5,4,4,4,5,5,4,4,4,1,1,4,4,4,4],
    [6,5,5,5,6,6,5,5,4,2,2,4,5,5,5],
    [7,6,6,6,7,7,6,6,4,3,3,4,6,6,6]
]

instance["entorno"] = [
    [0,0,1,1,2,2,4,13,4,16,16,4,2,6,2],
    [0,0,1,1,2,2,4,13,4,16,16,4,2,6,2],
    [0,0,1,10,2,2,4,4,4,16,16,4,2,2,2],
    [1,1,2,2,3,3,4,3,4,15,15,4,1,1,1],
    [2,2,3,3,4,4,4,2,4,14,14,4,1,1,1],
    [2,2,3,3,4,4,4,1,4,13,13,4,1,1,1],
    [2,2,3,3,4,4,4,0,4,12,12,4,1,1,1],
    [3,3,4,4,4,4,4,1,4,11,11,4,2,2,2],
    [4,4,5,5,5,5,4,2,4,10,10,4,3,3,3],
    [5,5,6,6,6,6,5,3,4,9,9,4,4,4,4],
    [6,6,7,7,7,7,6,4,4,8,8,4,5,5,5],
    [7,7,8,8,8,8,7,5,4,7,7,4,6,6,6],
    [8,8,9,9,9,9,8,6,4,6,6,4,7,7,7],
    [9,9,10,10,10,10,9,7,4,5,5,4,8,8,8],
    [10,10,11,11,11,11,10,8,4,4,4,4,9,9,9]
]

try:
    result = instance.solve()
    print(result)
except Exception as e:
    print(f"Error en la resolución: {e}")
    # Si es posible, imprime más detalles
    import traceback
    traceback.print_exc()