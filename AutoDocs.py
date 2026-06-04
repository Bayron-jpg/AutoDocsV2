import os
from tkinter import messagebox
import customtkinter

# ------------------ Configuración General ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = customtkinter.CTk() # Crear ventana vacía
ICON_LIGHT = os.path.join(BASE_DIR, "AutoDocsLight.ico")
ICON_DARK = os.path.join(BASE_DIR, "AutoDocsDark.ico")
ventana_acerca = None

# ------------------ Funciones ------------------
def crearTexto(app, contenido, letra, tamano):
    label = customtkinter.CTkLabel(app,
        text=contenido,                # Texto a ingresar (String)
        font=(letra,tamano),           # Tipo de letra (Arial/Roboto/Consolas/etc) y tamaño (12-14-16-etc)
        text_color=("black", "white")) # Color del texto
    return label

def cambiar_tema():
    actual = customtkinter.get_appearance_mode()
    if actual == "Dark":
        customtkinter.set_appearance_mode("Light")
        app.iconbitmap(ICON_LIGHT)
    else:
        customtkinter.set_appearance_mode("Dark")
        app.iconbitmap(ICON_DARK)

# ------------------ Ventanas ------------------
def menu():
    # Inicializar ventana
    customtkinter.set_appearance_mode("Dark")
    app.iconbitmap(ICON_DARK) # Cambiar icono
    app.title("AutoDocs") # Cambiar titulo de la ventana
    
    # Ajustes de la ventana
    ancho = 800
    alto = 500
    x = (app.winfo_screenwidth() // 2) - (ancho // 2)
    y = (app.winfo_screenheight() // 2) - (alto // 2)
    app.geometry(f"{ancho}x{alto}+{x}+{y}")
    app.resizable(False, False)  # Ancho, Alto

    # ------------ Ajustes personalizados de la ventana ------------
    # --- Posiciones ---
    POS_TITULO = (0.20, 0.19)
    POS_TEMA = (0.03, 0.05)
    POS_SALIR = (0.62, 0.76)
    POS_ACERCA = (0.20, 0.76)
    POS_CREAR = (0.12, 0.45)
    POS_CONVERTIR = (0.54, 0.45)
    
    # Ajustes del Tema (Modo Claro-Oscuro)
    cambiarTema = customtkinter.CTkButton(app,
        text="Cambiar Tema",                   # Texto del botón
        command=cambiar_tema,                  # Función a realizar
        text_color=("black","white"),          # Color del texto
        fg_color=("#cecece","gray"),         # Color del botón
        hover_color=("#c0c0c0","#666666")) # Color sobre el mouse
    cambiarTema.place(relx=POS_TEMA[0], rely=POS_TEMA[1])

    # Titulo AutoDocs
    titulo = crearTexto(app, "Bienvenido(a) a AutoDocs", "Consolas", 36)
    titulo.place(relx=POS_TITULO[0], rely=POS_TITULO[1])
    
    # Botón Crear Plantilla (Azul, grande, izquierda)
    botonCrear = customtkinter.CTkButton(app,
        text="Crear Plantilla",
        command=None,
        fg_color="#2980b9",
        hover_color="#1a6a9a",
        text_color=("#f0f0f0","white"),
        width=270,
        height=110,
        font=("Consolas", 24))
    botonCrear.place(relx=POS_CREAR[0], rely=POS_CREAR[1])

    # Botón Convertir a PDF (Naranja-rojo, grande, derecha del anterior)
    botonConvertir = customtkinter.CTkButton(app,
        text="Convertir a PDF",
        command=None,
        fg_color="#e05a2b",
        hover_color="#b84a20",
        text_color=("#f0f0f0","white"),
        width=270,
        height=110,
        font=("Consolas", 24))
    botonConvertir.place(relx=POS_CONVERTIR[0], rely=POS_CONVERTIR[1])
    
    # Botón Acerca De
    botonAcercaDe = customtkinter.CTkButton(app,
        text = "Acerca de",                    # Texto del botón
        command=acercaDe,                      # Función a realizar
        fg_color=("#cecece","gray"),         # Color del botón
        hover_color=("#c0c0c0","#666666"), # Color sobre el mouse
        text_color=("black","white"),          # Color del texto
        height=35)          
    botonAcercaDe.place(relx=POS_ACERCA[0], rely=POS_ACERCA[1])
    
    # Cerrar el programa (Botón de Salir)
    def salir():
        if messagebox.askyesno("Salir", "¿Está seguro(a) que desea salir?"):
            app.destroy()
    botonSalir = customtkinter.CTkButton(app,
        text="Salir",            # Título de la ventana
        command=salir,           # Función a ejecutar
        fg_color="#ba6258",    # Rojo
        hover_color="#7f342d", # Rojo oscuro al pasar el mouse
        text_color="white",   # Color del texto
        height=35)      # Alto en píxeles
    botonSalir.place(relx=POS_SALIR[0], rely=POS_SALIR[1])

    app.mainloop() # Loop que mantiene la ventana abierta

def acercaDe():
    # --- Posiciones ---
    POS_AUTODOCS = (0.35, 0.03)
    POS_SUBTITULO = (0.35, 0.09)
    POS_TEXTOACERCADE = (0.07, 0.21)
    POS_SALIR = (0.32, 0.83)
    
    global ventana_acerca

    if ventana_acerca is None or not ventana_acerca.winfo_exists():
        # Crear y ajustar ventana
        ventana_acerca = customtkinter.CTkToplevel(app)
        ventana_acerca.transient(app)  # Vincula a la ventana principal
        ventana_acerca.grab_set()      # Impide interactuar con la principal
        ventana_acerca.focus_force()   # Le da foco inmediatamente
        ventana_acerca.title("Acerca de")
        ventana_acerca.resizable(False, False)  # Impide agrandar o achicar la ventana
        ancho = 400
        alto = 500
        x = app.winfo_x() + (app.winfo_width() - ancho) // 2
        y = app.winfo_y() + (app.winfo_height() - alto) // 2
        ventana_acerca.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana_acerca.update_idletasks()
        # Obtener el modo actual (Claro/Oscuro)
        icono = ICON_DARK if customtkinter.get_appearance_mode() == "Dark" else ICON_LIGHT
        ventana_acerca.after(200, lambda: ventana_acerca.iconbitmap(icono))
        
        autoDocs = crearTexto(ventana_acerca, "AutoDocs", "Consolas", 28)
        autoDocs.place(relx=POS_AUTODOCS[0], rely=POS_AUTODOCS[1])
        
        subtitulo = crearTexto(ventana_acerca, "Versión 1.0.0", "Consolas", 16)
        subtitulo.place(relx=POS_SUBTITULO[0], rely=POS_SUBTITULO[1])
        
        texto = customtkinter.CTkLabel(
        ventana_acerca,
        text="Aplicación para automatizar la creación\n"
             "de documentos Word repetitivos.\n\n"
            "Proyecto personal desarrollado en\n"
            "Python.\n\n\n"
            "Desarrollado por:\n"
            "Bayron Urrutia\n\n"
            "© 2026",
        font=("Consolas", 16),
        justify="left")
        texto.place(relx=POS_TEXTOACERCADE[0], rely=POS_TEXTOACERCADE[1])
        
        botonSalir = customtkinter.CTkButton(ventana_acerca,
                text="Cerrar",            # Título de la ventana
                command=ventana_acerca.destroy,   # Función a ejecutar
                fg_color="#ba6258",    # Rojo
                hover_color="#7f342d", # Rojo oscuro al pasar el mouse
                text_color="white",      # Color del texto
                height=35)               # Alto en píxeles
        botonSalir.place(relx=POS_SALIR[0], rely=POS_SALIR[1])
        
    else:
        ventana_acerca.focus()
# ------------------ Inicio ------------------
menu()