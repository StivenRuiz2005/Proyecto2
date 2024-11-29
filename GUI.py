import customtkinter as ctk
from tkinter import filedialog
import os
from minizinc import Model, Instance, Solver

"""
Autor: Carlos Stiven Ruiz Rojas
Descripcion: Este archivo contiene el código necesario para resolver el problema planteado en el miniproyecto
Fecha de creación: 28-11-2024
Fecha de última modificación: 28-11-2024
"""

class Aplicacion(ctk.CTk):  
    def __init__(self):
        super().__init__()

        self.title("Ingeniería de Sistemas al Infinito")
        self.geometry("400x300")

        self.archivo_seleccionado = ctk.StringVar()

        self.btn_seleccionar = ctk.CTkButton(self, text="Seleccionar archivo .txt", command=self.seleccionar_archivo)
        self.btn_seleccionar.pack(pady=10)

        self.lbl_archivo = ctk.CTkLabel(self, text="Ningún archivo seleccionado")
        self.lbl_archivo.pack(pady=5)

        self.opciones = ["gecode", "cbc", "chuffed"]
        self.combo_opciones = ctk.CTkComboBox(self, values=self.opciones)
        self.combo_opciones.pack(pady=10)

        self.btn_resultados = ctk.CTkButton(self, text="Resultados", command=self.procesar_resultados)
        self.btn_resultados.pack(pady=10)

        self.lbl_resultados = ctk.CTkLabel(self, text="")
        self.lbl_resultados.pack(pady=5)

        self.btn_descargar = ctk.CTkButton(self, text="Descargar resultados", command=self.descargar_resultados)
        self.btn_descargar.pack(pady=10)

        # Variables para almacenar los datos procesados
        self.localizaciones = []
        self.matriz_poblacion = []
        self.matriz_empresarial = []
        self.num_programas = 0
        self.tamano_matriz = 0
        self.solver = ""

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivo de texto", "*.txt")])
        if archivo:
            self.archivo_seleccionado.set(archivo)
            self.lbl_archivo.configure(text=f"Archivo seleccionado: {os.path.basename(archivo)}")
            self.leer_archivo(archivo)

    def leer_archivo(self, archivo):
        with open(archivo, 'r') as file:
            lines = file.readlines() 

        num_localizaciones = int(lines[0].strip())
        localizaciones = []

        # Leer las localizaciones ya establecidas
        for i in range(1, num_localizaciones + 1):
            x, y = map(int, lines[i].strip().split())
            localizaciones.append((x, y))

        tamano_matriz = int(lines[num_localizaciones + 1].strip()) 

        matriz_poblacion = []
        for i in range(num_localizaciones + 2, num_localizaciones + 2 + tamano_matriz):
            fila = list(map(int, lines[i].strip().split()))
            matriz_poblacion.append(fila)

        matriz_empresarial = []
        for i in range(num_localizaciones + 2 + tamano_matriz, num_localizaciones + 2 + 2 * tamano_matriz):
            fila = list(map(int, lines[i].strip().split())) 
            matriz_empresarial.append(fila)

        num_programas = int(lines[num_localizaciones + 2 + 2 * tamano_matriz].strip())

        self.localizaciones = localizaciones
        self.matriz_poblacion = matriz_poblacion
        self.matriz_empresarial = matriz_empresarial
        self.num_programas = num_programas
        self.tamano_matriz = tamano_matriz

    def procesar_resultados(self):
        if not self.archivo_seleccionado.get():
            self.lbl_resultados.configure(text="Por favor, seleccione un archivo primero")
            return
        
        opcion_seleccionada = self.combo_opciones.get()
        if opcion_seleccionada == "gecode":
            self.solver = "gecode"
        elif opcion_seleccionada == "cbc":
            self.solver = "cbc"
        elif opcion_seleccionada == "chuffed":
            self.solver = "chuffed"

        # Configura los parámetros de MiniZinc con los datos leídos
        model = Model("miniproyecto.mzn")
        solver = Solver.lookup(self.solver)  # o el solver que estés usando
        instance = Instance(solver, model)

        # Configura los parámetros
        instance["n"] = self.tamano_matriz
        instance["num_actuales"] = len(self.localizaciones)
        instance["num_nuevas"] = self.num_programas

        # Corrige la definición de actuales para que sea una matriz 2D
        instance["actuales"] = self.localizaciones

        # Usa una lista de listas para población y entorno
        instance["poblacion"] = self.matriz_poblacion
        instance["entorno"] = self.matriz_empresarial

        # Resuelve el modelo
        try:
            result = instance.solve()
            self.lbl_resultados.configure(text=f"Resultado procesado con éxito: {result}")
        except Exception as e:
            self.lbl_resultados.configure(text="Error en la resolución.")
            import traceback
            traceback.print_exc()

    def descargar_resultados(self):
        if not self.archivo_seleccionado.get():
            self.lbl_resultados.configure(text="No hay resultados para descargar.")
            return

        archivo_salida = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
        if archivo_salida:
            # Aquí iría la lógica para guardar los resultados en el archivo
            with open(archivo_salida, 'w') as f:
                f.write(f"Resultados del procesamiento con {self.combo_opciones.get()}")
            self.lbl_resultados.configure(text=f"Resultados guardados en {os.path.basename(archivo_salida)}")


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
