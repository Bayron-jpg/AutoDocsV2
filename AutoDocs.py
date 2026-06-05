import os
import threading
import customtkinter
from tkinter import filedialog, messagebox
import docx2pdf

# ------------------ Configuración General ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = customtkinter.CTk()                               # Crear ventana vacía
ICON_LIGHT = os.path.join(BASE_DIR, "Iconos","AutoDocsLight.ico")# Icono con fondo blanco
ICON_DARK = os.path.join(BASE_DIR, "Iconos","AutoDocsDark.ico")  # Icono con fondo negro
ventana_acerca = None
ventana_plantilla = None
ventana_pdf = None

# ------------------ Funciones ------------------
def crearTexto(app, contenido, letra, tamano):
    label = customtkinter.CTkLabel(app,
        text=contenido,                # Texto a ingresar (String)
        font=(letra,tamano),           # Tipo de letra (Arial/Roboto/Consolas/etc) y tamaño (12-14-16-etc)
        text_color=("black", "white")) # Color del texto
    return label

def crearTextoColor(app, contenido, letra, tamano, colorTexto):
    label = customtkinter.CTkLabel(app,
        text=contenido,                # Texto a ingresar (String)
        font=(letra,tamano),           # Tipo de letra (Arial/Roboto/Consolas/etc) y tamaño (12-14-16-etc)
        text_color=(colorTexto))       # Color del texto
    return label

def cambiar_tema():
    actual = customtkinter.get_appearance_mode() # Obtener modo actual
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
    app.iconbitmap(ICON_DARK)     # Cambiar icono
    app.title("AutoDocs (1.0.0)") # Cambiar el titulo superior de la ventana
    
    # Ajustes de la ventana
    ancho = 800
    alto = 500
    x = (app.winfo_screenwidth() // 2) - (ancho // 2)
    y = (app.winfo_screenheight() // 2) - (alto // 2)
    app.geometry(f"{ancho}x{alto}+{x}+{y}")
    app.resizable(False, False) # Impide modificar el ancho y el alto

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
    
    # Botón Crear Plantilla
    botonCrear = customtkinter.CTkButton(app,
        text="Crear Plantilla",           # Texto del botón
        command=crearPlantilla,           # Función a realizar
        fg_color="#2980b9",             # Color del botón
        hover_color="#1a6a9a",          # Color sobre el mouse
        text_color=("#f0f0f0","white"), # Color del texto
        width=270,                        # Ancho del botón
        height=110,                       # Alto del botón
        font=("Consolas", 24))            # Tipo de letra y tamaño del texto
    botonCrear.place(relx=POS_CREAR[0], rely=POS_CREAR[1])

    # Botón Convertir a PDF
    botonConvertir = customtkinter.CTkButton(app,
        text="Convertir a PDF",          # Texto del botón
        command=convertirPdf,            # Función a realizar
        fg_color="#e05a2b",            # Color del botón
        hover_color="#84371B",         # Color sobre el mouse
        text_color=("#f0f0f0","white"),# Color del texto
        width=270,                       # Ancho del botón
        height=110,                      # Alto del botón
        font=("Consolas", 24))           # Tipo de letra y tamaño del texto
    botonConvertir.place(relx=POS_CONVERTIR[0], rely=POS_CONVERTIR[1])
    
    # Botón Acerca De
    botonAcercaDe = customtkinter.CTkButton(app,
        text = "Acerca de",                    # Texto del botón
        command=acercaDe,                      # Función a realizar
        fg_color=("#cecece","gray"),         # Color del botón
        hover_color=("#c0c0c0","#666666"), # Color sobre el mouse
        text_color=("black","white"),          # Color del texto
        height=35)                             # Alto del botón
    botonAcercaDe.place(relx=POS_ACERCA[0], rely=POS_ACERCA[1])
    
    # Cerrar el programa (Botón de Salir)
    def salir():
        if messagebox.askyesno("Salir", "¿Está seguro(a) que desea salir?"):
            app.destroy() # Terminar la aplicación

    botonSalir = customtkinter.CTkButton(app,
        text="Salir",            # Título de la ventana
        command=salir,           # Función a ejecutar
        fg_color="#ba5858",    # Color del botón
        hover_color="#7f2d2d", # Color sobre el mouse
        text_color="white",      # Color del texto
        height=35)               # Alto del botón
    botonSalir.place(relx=POS_SALIR[0], rely=POS_SALIR[1])

    app.bind("<Escape>", lambda e: salir()) # Si pulsa Escape pide confirmación para cerrar la aplicación
    app.mainloop() # Loop que mantiene la ventana abierta

def crearPlantilla():
    # --- Posiciones ---
    POS_TITULO = (0.28, 0.05)
    POS_TEXTOACERCADE = (0.07, 0.21)
    POS_VOLVER = (0.43, 0.83)
    
    global ventana_plantilla

    if ventana_plantilla is None or not ventana_plantilla.winfo_exists():
        # ------ Crear y ajustar ventana ------
        ventana_plantilla = customtkinter.CTkToplevel(app)
        ventana_plantilla.transient(app)             # Vincula a la ventana principal
        ventana_plantilla.grab_set()                 # Impide interactuar con la principal
        ventana_plantilla.focus_force()              # Le da foco inmediatamente
        ventana_plantilla.title("Creando Plantilla") # Cambiar el titulo superior de la ventana   
        ventana_plantilla.resizable(False, False)    # Impide agrandar o achicar la ventana

        # Ajustes de la ventana
        ancho = 1000
        alto = 600
        x = app.winfo_x() + (app.winfo_width() - ancho) // 2
        y = app.winfo_y() + (app.winfo_height() - alto) // 2
        ventana_plantilla.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Fuerza a que la ventana termine de crearse para aplicar el icono
        ventana_plantilla.update_idletasks()
        ventana_plantilla.bind("<Escape>", lambda e: ventana_plantilla.destroy()) # Si pulsa Escape se cierra la ventana
        
        # Obtener el modo actual (Claro/Oscuro)
        icono = ICON_DARK if customtkinter.get_appearance_mode() == "Dark" else ICON_LIGHT
        ventana_plantilla.after(200, lambda: ventana_plantilla.iconbitmap(icono)) # Espera 200ms para cambiar el icono
        
        autoDocs = crearTexto(ventana_plantilla, "Crear Plantilla de Documentos", "Consolas", 28)
        autoDocs.place(relx=POS_TITULO[0], rely=POS_TITULO[1])
        
        texto = customtkinter.CTkLabel(
            ventana_plantilla,
            text="Ventana de plantilla",
            font=("Consolas", 16), # Tamaño y tipo de letra
            justify="left")        # Alineamiento del texto a la izquierda
        texto.place(relx=POS_TEXTOACERCADE[0], rely=POS_TEXTOACERCADE[1])
        
        botonVolver = customtkinter.CTkButton(ventana_plantilla,
                text="Volver",                     # Título de la ventana
                command=ventana_plantilla.destroy, # Función a ejecutar
                fg_color="#ba6258",              # Color del botón
                hover_color="#7f342d",           # Color sobre el mouse
                text_color="white",                # Color del texto
                height=35)                         # Alto del botón
        botonVolver.place(relx=POS_VOLVER[0], rely=POS_VOLVER[1])
        
    else:
        ventana_plantilla.focus()
        
def convertirPdf():
    # --- Posiciones ---
    POS_TITULO = (0.15, 0.09)
    POS_ARCHIVO = (0.40, 0.41)
    POS_VOLVER = (0.43, 0.83)
    POS_SELECCIONAR = (0.19, 0.41)
    POS_CONVERTIR = (0.41, 0.56)
    
    global ventana_pdf

    if ventana_pdf is None or not ventana_pdf.winfo_exists():
        # ------ Crear y ajustar ventana ------
        ventana_pdf = customtkinter.CTkToplevel(app)
        ventana_pdf.transient(app)                             # Vincula a la ventana principal
        ventana_pdf.grab_set()                                 # Impide interactuar con la principal
        ventana_pdf.focus_force()                              # Le da foco inmediatamente
        ventana_pdf.title("Convirtiendo Documento Word a PDF") # Cambiar el titulo superior de la ventana   
        ventana_pdf.resizable(False, False)                    # Impide agrandar o achicar la ventana

        # Ajustes de la ventana
        ancho = 800
        alto = 500
        x = app.winfo_x() + (app.winfo_width() - ancho) // 2
        y = app.winfo_y() + (app.winfo_height() - alto) // 2
        ventana_pdf.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Fuerza a que la ventana termine de crearse para aplicar el icono
        ventana_pdf.update_idletasks()
        ventana_pdf.bind("<Escape>", lambda e: ventana_pdf.destroy()) # Si pulsa Escape se cierra la ventana
        
        # Obtener el modo actual (Claro/Oscuro)
        icono = ICON_DARK if customtkinter.get_appearance_mode() == "Dark" else ICON_LIGHT
        ventana_pdf.after(200, lambda: ventana_pdf.iconbitmap(icono)) # Espera 200ms para cambiar el icono

        # --- Título ---
        titulo = crearTexto(ventana_pdf, "Convertir Documento Word a PDF", "Consolas", 34)
        titulo.place(relx=POS_TITULO[0], rely=POS_TITULO[1])

        # --- Archivo seleccionado ---
        archivoSeleccionado = crearTexto(ventana_pdf, "Ningún archivo seleccionado", "Consolas", 12)
        archivoSeleccionado.place(relx=POS_ARCHIVO[0], rely=POS_ARCHIVO[1])

        # --- Función seleccionar archivo ---
        def seleccionarArchivo():
            archivo = filedialog.askopenfilename(
                title="Seleccionar documento Word",
                filetypes=[("Documentos Word", "*.docx *.doc")]
            )
            if archivo:
                archivoSeleccionado.configure(text=os.path.basename(archivo))
                botonConvertir.configure(state="normal")
                botonConvertir.archivo_path = archivo

        # --- Función convertir ---
        def convertir():
            archivo = botonConvertir.archivo_path
    
            # Deshabilitar botones mientras convierte
            botonConvertir.configure(state="disabled", text="Convirtiendo...")
            botonSeleccionar.configure(state="disabled")
    
            def proceso():
                try:
                    docx2pdf.convert(archivo)
                    ruta_pdf = os.path.splitext(archivo)[0] + ".pdf"
                    ventana_pdf.after(0, lambda: exito(ruta_pdf))
                except Exception as e:
                    ventana_pdf.after(0, lambda: error(str(e)))
    
            def exito(ruta):
                botonConvertir.configure(state="disabled", text="Convertir a PDF")  # Deshabilitar y resetear texto
                botonSeleccionar.configure(state="normal")
                archivoSeleccionado.configure(text="Ningún archivo seleccionado")    # Vaciar label
                messagebox.showinfo("PDF Generado satisfactoriamente", f"PDF generado correctamente.\n\nGuardado en:\n{ruta}")

            def error(e):
                botonConvertir.configure(state="normal", text="Convertir a PDF")
                botonSeleccionar.configure(state="normal")
                messagebox.showerror("Error", f"No se pudo convertir:\n{e}")

            threading.Thread(target=proceso, daemon=True).start()

        # --- Botón seleccionar ---
        botonSeleccionar = customtkinter.CTkButton(ventana_pdf,
            text="Seleccionar archivo",
            command=seleccionarArchivo,
            fg_color=("#cecece","gray"),
            hover_color=("#c0c0c0","#666666"),
            text_color=("black","white"),
            height=35)
        botonSeleccionar.place(relx=POS_SELECCIONAR[0], rely=POS_SELECCIONAR[1])

        # --- Botón convertir (deshabilitado hasta seleccionar archivo) ---
        botonConvertir = customtkinter.CTkButton(ventana_pdf,
            text="Convertir a PDF",
            command=convertir,
            fg_color="#e05a2b",
            hover_color="#b84a20",
            text_color="white",
            height=35,
            state="disabled")
        botonConvertir.place(relx=POS_CONVERTIR[0], rely=POS_CONVERTIR[1])
        
        
        
        botonVolver = customtkinter.CTkButton(ventana_pdf,
                text="Volver",               # Título de la ventana
                command=ventana_pdf.destroy, # Función a ejecutar
                fg_color="#ba6258",        # Color del botón
                hover_color="#7f342d",     # Color sobre el mouse
                text_color="white",          # Color del texto
                height=35)                   # Alto del botón
        botonVolver.place(relx=POS_VOLVER[0], rely=POS_VOLVER[1])
        
    else:
        ventana_pdf.focus()

def acercaDe():
    # --- Posiciones ---
    POS_AUTODOCS = (0.35, 0.03)
    POS_TEXTOACERCADE = (0.07, 0.21)
    POS_SALIR = (0.32, 0.83)
    
    global ventana_acerca

    if ventana_acerca is None or not ventana_acerca.winfo_exists():
        # ------ Crear y ajustar ventana ------
        ventana_acerca = customtkinter.CTkToplevel(app)
        ventana_acerca.transient(app)           # Vincula a la ventana principal
        ventana_acerca.grab_set()               # Impide interactuar con la principal
        ventana_acerca.focus_force()            # Le da foco inmediatamente
        ventana_acerca.title("Acerca de")       # Cambiar el titulo superior de la ventana   
        ventana_acerca.resizable(False, False)  # Impide agrandar o achicar la ventana

        # Ajustes de la ventana
        ancho = 400
        alto = 500
        x = app.winfo_x() + (app.winfo_width() - ancho) // 2
        y = app.winfo_y() + (app.winfo_height() - alto) // 2
        ventana_acerca.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Fuerza a que la ventana termine de crearse para aplicar el icono
        ventana_acerca.update_idletasks()
        ventana_acerca.bind("<Escape>", lambda e: ventana_acerca.destroy()) # Si pulsa Escape se cierra la ventana
        
        # Obtener el modo actual (Claro/Oscuro)
        icono = ICON_DARK if customtkinter.get_appearance_mode() == "Dark" else ICON_LIGHT
        ventana_acerca.after(200, lambda: ventana_acerca.iconbitmap(icono)) # Espera 200ms para cambiar el icono
        
        autoDocs = crearTexto(ventana_acerca, "AutoDocs", "Consolas", 28)
        autoDocs.place(relx=POS_AUTODOCS[0], rely=POS_AUTODOCS[1])
        
        texto = customtkinter.CTkLabel(
            ventana_acerca,
            text="Aplicación para automatizar la creación\n"
                "de documentos Word repetitivos.\n\n"
                "Proyecto personal desarrollado en\n"
                "Python.\n\n\n"
                "Desarrollado por:\n"
                "Bayron Urrutia\n\n"
                "© 2026",
            font=("Consolas", 16), # Tamaño y tipo de letra
            justify="left")        # Alineamiento del texto a la izquierda
        texto.place(relx=POS_TEXTOACERCADE[0], rely=POS_TEXTOACERCADE[1])
        
        botonSalir = customtkinter.CTkButton(ventana_acerca,
                text="Volver",                  # Título de la ventana
                command=ventana_acerca.destroy, # Función a ejecutar
                fg_color="#ba6258",           # Color del botón
                hover_color="#7f342d",        # Color sobre el mouse
                text_color="white",             # Color del texto
                height=35)                      # Alto del botón
        botonSalir.place(relx=POS_SALIR[0], rely=POS_SALIR[1])
        
    else:
        ventana_acerca.focus()
# ------------------ Inicio ------------------
menu()
