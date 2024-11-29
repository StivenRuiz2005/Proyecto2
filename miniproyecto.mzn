% Parámetros
int: n;                        % Dimensión de la matriz
int: num_actuales;             % Número de localizaciones actuales
int: num_nuevas;               % Número de localizaciones nuevas a ubicar

array[1..num_actuales, 1..2] of int: actuales; % Coordenadas actuales
array[1..n, 1..n] of int: poblacion;          % Matriz de segmento de población
array[1..n, 1..n] of int: entorno;            % Matriz de entorno empresarial

% Variables
array[1..num_nuevas, 1..2] of var 1..n: nuevas; % Coordenadas nuevas

% Función para calcular la suma de población en un área
function var int: suma_poblacion(var int: x, var int: y) =
    sum([poblacion[vx, vy] | 
        vx in max(1, x-1)..min(n, x+1), 
        vy in max(1, y-1)..min(n, y+1)]);

% Función para calcular la suma de entorno en un área
function var int: suma_entorno(var int: x, var int: y) =
    sum([entorno[vx, vy] | 
        vx in max(1, x-1)..min(n, x+1), 
        vy in max(1, y-1)..min(n, y+1)]);

% Restricciones
constraint
    % Las nuevas localizaciones no deben ser contiguas a las actuales
    forall(i in 1..num_nuevas, j in 1..num_actuales)(
        abs(nuevas[i, 1] - actuales[j, 1]) > 1 \/ abs(nuevas[i, 2] - actuales[j, 2]) > 1
    )
    /\
    % Las nuevas localizaciones no deben ser contiguas entre sí
    forall(i, j in 1..num_nuevas where i < j)(
        abs(nuevas[i, 1] - nuevas[j, 1]) > 1 \/ abs(nuevas[i, 2] - nuevas[j, 2]) > 1
    )
    /\
    % El segmento de población y el entorno empresarial en cada punto deben cumplir los mínimos
    forall(i in 1..num_nuevas)(
        suma_poblacion(nuevas[i, 1], nuevas[i, 2]) >= 25 /\
        suma_entorno(nuevas[i, 1], nuevas[i, 2]) >= 20
    );

% Variables para la función objetivo
array[1..num_nuevas] of var int: ganancias_poblacion = 
    [suma_poblacion(nuevas[i, 1], nuevas[i, 2]) | i in 1..num_nuevas];

array[1..num_nuevas] of var int: ganancias_entorno = 
    [suma_entorno(nuevas[i, 1], nuevas[i, 2]) | i in 1..num_nuevas];

% Función objetivo
var int: ganancia_total = sum(ganancias_poblacion) + sum(ganancias_entorno);

solve maximize ganancia_total;

% Salida
output [
    "Ganancia total: ", show(ganancia_total), "\n",
    "Nuevas localizaciones:\n",
    concat([show(nuevas[i, 1]) ++ " " ++ show(nuevas[i, 2]) ++ "\n" | i in 1..num_nuevas])
];