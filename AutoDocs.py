import os
from tkinter import messagebox
import customtkinter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = customtkinter.CTk() # Crear ventana vacía

def crearTexto(app, contenido, letra, tamano):
    label = customtkinter.CTkLabel(app,
        text=contenido,                # Texto a ingresar (String)
        font=(letra,tamano),           # Tipo de letra (Arial/Roboto/Consolas/etc) y tamaño (12-14-16-etc)
        text_color=("black", "white")) # Color del texto
    return label

def crearTextoColor(app, contenido, letra, tamano, colorTexto):
    label = customtkinter.CTkLabel(app,
        text=contenido,        # Texto a ingresar (String)
        font=(letra,tamano),   # Tipo de letra (Arial/Roboto/Consolas/etc) y tamaño (12-14-16-etc)
        text_color=colorTexto) # Color del texto (white-black-gray-etc)
    return label

def cambiar_tema():
    actual = customtkinter.get_appearance_mode()
    if actual == "Dark":
        customtkinter.set_appearance_mode("Light")
    else:
        customtkinter.set_appearance_mode("Dark")

def menu():
    # Inicializar ventana
    customtkinter.set_appearance_mode("Dark")
    app.iconbitmap(os.path.join(BASE_DIR, 'AutoDocs.ico')) # Cambiar icono
    app.title("AutoDocs") # Cambiar titulo de la ventana
    
    # Tamaño de la ventana
    ancho = 800
    alto = 500
    x = (app.winfo_screenwidth() // 2) - (ancho // 2)
    y = (app.winfo_screenheight() // 2) - (alto // 2)
    app.geometry(f"{ancho}x{alto}+{x}+{y}")

    # ------------ Ajustes personalizados de la ventana ------------
    # --- Posiciones ---
    POS_TITULO = (0.31, 0.06)
    POS_TEMA = (0.04, 0.07)
    POS_SALIR = (0.65, 0.76)
    
    # Titulo AutoDocs
    titulo = crearTexto(app, "Bienvenido(a) a AutoDocs", "Consolas", 27)
    titulo.place(relx=POS_TITULO[0], rely=POS_TITULO[1])
    
    # Ajustes del Tema (Modo Claro-Oscuro)
    cambiarTema = customtkinter.CTkButton(app,
                            text="Cambiar apariencia",             # Texto del botón
                            command=cambiar_tema,                  # Función a realizar
                            text_color=("black","white"),          # Color del texto
                            fg_color=("#bacad4","gray"),         # Color del botón
                            hover_color=("#aebdc6","#666666")) # Color sobre el mouse
    cambiarTema.place(relx=POS_TEMA[0], rely=POS_TEMA[1])
    
    # Cerrar el programa (Botón de Salir)
    def salir():
        if messagebox.askyesno("Salir", "¿Está seguro(a) que desea salir?"):
            app.destroy()
    botonSalir = customtkinter.CTkButton(app,
                text="Salir",            # Título de la ventana
                command=salir,           # Función a ejecutar
                fg_color="#ba6258",    # Rojo
                hover_color="#7f342d", # Rojo oscuro al pasar el mouse
                text_color="white")      # Color del texto
    botonSalir.place(relx=POS_SALIR[0], rely=POS_SALIR[1])

    app.mainloop() # Loop que mantiene la ventana abierta

menu()