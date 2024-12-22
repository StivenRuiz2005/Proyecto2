% Parámetros
int: n;                        
int: num_actuales;             
int: num_nuevas;               

array[1..num_actuales, 1..2] of int: actuales;
array[1..n, 1..n] of int: poblacion;          
array[1..n, 1..n] of int: entorno;            

% Variables
array[1..num_nuevas, 1..2] of var 1..n: nuevas;

% Función para calcular la suma de población en un área
function int: suma_poblacion_actual(int: x, int: y) =
    sum(vx in max(1, x-1)..min(n, x+1),
        vy in max(1, y-1)..min(n, y+1))
        (poblacion[vx, vy]);

function int: suma_entorno_actual(int: x, int: y) =
    sum(vx in max(1, x-1)..min(n, x+1),
        vy in max(1, y-1)..min(n, y+1))
        (entorno[vx, vy]);

function var int: suma_poblacion_nueva(var int: x, var int: y) =
    sum(vx in max(1, x-1)..min(n, x+1),
        vy in max(1, y-1)..min(n, y+1))
        (poblacion[vx, vy]);

function var int: suma_entorno_nueva(var int: x, var int: y) =
    sum(vx in max(1, x-1)..min(n, x+1),
        vy in max(1, y-1)..min(n, y+1))
        (entorno[vx, vy]);

% Restricciones
constraint
    forall(i in 1..num_nuevas, j in 1..num_actuales)(
        abs(nuevas[i, 1] - actuales[j, 1]) > 1 \/ abs(nuevas[i, 2] - actuales[j, 2]) > 1
    )
    /\
    forall(i, j in 1..num_nuevas where i < j)(
        abs(nuevas[i, 1] - nuevas[j, 1]) > 1 \/ abs(nuevas[i, 2] - nuevas[j, 2]) > 1
    )
    /\
    forall(i in 1..num_nuevas)(
        suma_poblacion_nueva(nuevas[i, 1], nuevas[i, 2]) >= 25 /\
        suma_entorno_nueva(nuevas[i, 1], nuevas[i, 2]) >= 20
    );

% Ganancia inicial (localizaciones actuales)
int: ganancia_inicial = sum(i in 1..num_actuales)
    (suma_poblacion_actual(actuales[i,1], actuales[i,2]) + 
     suma_entorno_actual(actuales[i,1], actuales[i,2]));

% Variables para la función objetivo
array[1..num_nuevas] of var int: ganancias_nuevas = 
    [suma_poblacion_nueva(nuevas[i, 1], nuevas[i, 2]) + 
     suma_entorno_nueva(nuevas[i, 1], nuevas[i, 2]) | i in 1..num_nuevas];

% Función objetivo
var int: ganancia_total = sum(ganancias_nuevas);

solve maximize ganancia_total;

output [ 
    show(ganancia_inicial), "\n",
    show(ganancia_total + ganancia_inicial), "\n",
    join("\n", [show(actuales[i, 1]) ++ " " ++ show(actuales[i, 2]) | i in 1..num_actuales]), "\n",
    join("\n", [show(nuevas[i, 1]) ++ " " ++ show(nuevas[i, 2]) | i in 1..num_nuevas])
];