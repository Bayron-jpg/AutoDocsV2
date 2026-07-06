import os
from pydoc import doc
import threading
import customtkinter
from tkinter import filedialog, messagebox
import docx2pdf
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

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
    app.title("AutoDocs (1.0.0)") # Cambiar el tituloDoc superior de la ventana
    
    # Ajustes de la ventana
    ancho = 800
    alto = 500
    x = (app.winfo_screenwidth() // 2) - (ancho // 2)
    y = (app.winfo_screenheight() // 2) - (alto // 2)
    app.geometry(f"{ancho}x{alto}+{x}+{y}")
    app.resizable(False, False) # Impide modificar el ancho y el alto

    # ------------ Ajustes personalizados de la ventana ------------
    # --- Posiciones ---
    POS_TITULODOC = (0.24, 0.19)
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

    # TituloDoc AutoDocs
    tituloDoc = crearTexto(app, "Bienvenido(a) a AutoDocs", "Menlo", 36)
    tituloDoc.place(relx=POS_TITULODOC[0], rely=POS_TITULODOC[1])
    
    # Botón Crear Plantilla
    botonCrear = customtkinter.CTkButton(app,
        text="Crear Plantilla",           # Texto del botón
        command=crearPlantilla,           # Función a realizar
        fg_color="#2980b9",             # Color del botón
        hover_color="#1a6a9a",          # Color sobre el mouse
        text_color=("#f0f0f0","white"), # Color del texto
        width=270,                        # Ancho del botón
        height=110,                       # Alto del botón
        font=("Menlo", 24))            # Tipo de letra y tamaño del texto
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
        font=("Menlo", 24))           # Tipo de letra y tamaño del texto
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
    POS_TITULO = (0.27, 0.06)
    POS_GENERARPLANTILLA = (0.66, 0.68)
    POS_VOLVER = (0.41, 0.83)
    POS_TEXTOTITULO = (0.10, 0.20)
    POS_TITULODOC = (0.10, 0.26)
    POS_TEXTOSUBTITULO = (0.38, 0.20)
    POS_SUBTITULODOC = (0.38, 0.26)
    POS_TEXTOESTUDIANTES = (0.66, 0.20)
    POS_ESTUDIANTES = (0.66, 0.26)
    POS_TEXTOPROFESOR = (0.10, 0.35)
    POS_PROFESOR = (0.10, 0.41)
    POS_TEXTOASIGNATURA = (0.38, 0.35)
    POS_ASIGNATURA = (0.38, 0.41)
    POS_TEXTOSECCION = (0.66, 0.35)
    POS_SECCION = (0.66, 0.41)
    POS_TEXTOIMAGEN = (0.10, 0.55)
    POS_BOTONIMAGEN = (0.10, 0.63)
    POS_LABELIMAGEN = (0.29, 0.63)
    POS_TEXTONOMBREARCHIVO = (0.66, 0.53)
    POS_NOMBREARCHIVO = (0.66, 0.59)
    
    global ventana_plantilla
    
    def verificar_largo(texto_futuro, limite):
        return len(texto_futuro) <= limite
    
    
    def estilo(run, size=14, bold=False):
        run.font.name = "Arial"
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(0, 0, 0)
        run.bold = bold
        
    def agregar_linea(doc, etiqueta, valor, espacio_antes=0):
        p = doc.add_paragraph()

        run1 = p.add_run(etiqueta)
        estilo(run1, bold=True)

        run2 = p.add_run(valor)
        estilo(run2)

        p.paragraph_format.space_before = Pt(espacio_antes)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        return p
    
    def generarDoc(tituloDoc, subtituloDoc, estudiantes, profesor, asignatura, seccion, botonSeleccionarImagen, nombreArchivo):
        textoTitulo = tituloDoc.get().strip()
        if not textoTitulo:
            messagebox.showwarning("Campo vacío", "Por favor, escriba un título antes de generar el documento.")
            return
        
        textoSubtitulo = subtituloDoc.get().strip()
        
        textoEstudiantes = estudiantes.get().strip()
        if not textoEstudiantes:
            messagebox.showwarning("Campo vacío", "Por favor, escriba almenos un estudiante.")
            return
        
        textoProfesor = profesor.get().strip()
        if not textoProfesor:
            messagebox.showwarning("Campo vacío", "Por favor, escriba almenos un profesor(a).")
            return
        
        textoAsignatura = asignatura.get().strip()
        if not textoAsignatura:
            messagebox.showwarning("Campo vacío", "Por favor, escriba almenos una asignatura.")
            return

        textoSeccion = seccion.get().strip()
        
        nombre = nombreArchivo.get().strip()
        if not nombre:
            nombre = "Documento"  # Nombre por defecto
                
        ruta = os.path.join(BASE_DIR, f"{nombre}.docx")
        doc = Document()

        # === ENCABEZADO (Opcional) ===
        if hasattr(botonSeleccionarImagen, 'imagen_path'):
            section = doc.sections[0]
            header = section.header
            header_paragraph = header.paragraphs[0]
            run_header = header_paragraph.add_run()
            run_header.add_picture(botonSeleccionarImagen.imagen_path, width=Inches(2.94))
            header_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            header_paragraph.paragraph_format.left_indent = 0
            header_paragraph.paragraph_format.space_before = 0
            header_paragraph.paragraph_format.space_after = 0

        # Eliminar párrafo vacío inicial
        if doc.paragraphs:
            p = doc.paragraphs[0]._element
            p.getparent().remove(p)

        # === Título ===
        titulo = doc.add_heading(textoTitulo, level=0)
        titulo.paragraph_format.space_before = Pt(120)
        titulo.paragraph_format.space_after = Pt(0)  # Sin espacio después

        run = titulo.runs[0]
        run.font.name = "Arial"
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        run.font.size = Pt(52)
        run.font.color.rgb = RGBColor(0, 0, 0)
        titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Borrar línea bajo el título
        pPr = titulo._element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'nil')
        pBdr.append(bottom)
        pPr.append(pBdr)

        # === Subtítulo (Opcional) ===
        if textoSubtitulo:
            parrafo = doc.add_paragraph()
            run_sub = parrafo.add_run(textoSubtitulo)
            estilo(run_sub)
            parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
            parrafo.paragraph_format.space_before = Pt(0)
            parrafo.paragraph_format.space_after = Pt(0)

        # === Datos (empujados al fondo con espacio) ===
        lineas = [("Estudiantes: ", textoEstudiantes), ("Profesor(a): ", textoProfesor), ("Asignatura: ", textoAsignatura)]
        if textoSeccion:
            lineas.append(("Sección: ", textoSeccion))

        # Primera línea con espacio grande para empujar al fondo
        primera = True
        for etiqueta, valor in lineas:
            p = doc.add_paragraph()
            run1 = p.add_run(etiqueta)
            estilo(run1, bold=True)
            run2 = p.add_run(valor)
            estilo(run2)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if primera:
                p.paragraph_format.space_before = Pt(270)  # Empuja al fondo
                primera = False
            else:
                p.paragraph_format.space_before = Pt(0)

        doc.save(ruta)
        
        # Mostrar mensaje con la ruta
        messagebox.showinfo(
        "Documento generado",
        f"El documento se generó correctamente.\n\nRuta:\n{ruta}")
        
    if ventana_plantilla is None or not ventana_plantilla.winfo_exists():
        # ------ Crear y ajustar ventana ------
        ventana_plantilla = customtkinter.CTkToplevel(app)
        ventana_plantilla.transient(app)             # Vincula a la ventana principal
        ventana_plantilla.grab_set()                 # Impide interactuar con la principal
        ventana_plantilla.focus_force()              # Le da foco inmediatamente
        ventana_plantilla.title("Creando Plantilla") # Cambiar el tituloDoc superior de la ventana   
        ventana_plantilla.resizable(False, False)    # Impide agrandar o achicar la ventana
        
        # --- Validaciones ---
        # Para el título (límite 60)
        cmd_titulo = (ventana_plantilla.register(lambda p: verificar_largo(p, 60)), '%P')

        # Para subtítulo (límite 125)
        cmd_subtitulo = (ventana_plantilla.register(lambda p: verificar_largo(p, 125)), '%P')

        # Para estudiantes (límite 50)
        cmd_estudiantes = (ventana_plantilla.register(lambda p: verificar_largo(p, 50)), '%P')
        
        # Para profesor (límite 44)
        cmd_profesor = (ventana_plantilla.register(lambda p: verificar_largo(p, 44)), '%P')
        
        # Para asignatura (límite 44)
        cmd_asignatura = (ventana_plantilla.register(lambda p: verificar_largo(p, 44)), '%P')
        
        # Para seccion (límite 30)
        cmd_seccion = (ventana_plantilla.register(lambda p: verificar_largo(p, 30)), '%P')

        # Ajustes de la ventana
        ancho = 800
        alto = 500
        x = app.winfo_x() + (app.winfo_width() - ancho) // 2
        y = app.winfo_y() + (app.winfo_height() - alto) // 2
        ventana_plantilla.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Fuerza a que la ventana termine de crearse para aplicar el icono
        ventana_plantilla.update_idletasks()
        ventana_plantilla.bind("<Escape>", lambda e: ventana_plantilla.destroy()) # Si pulsa Escape se cierra la ventana
        
        # Obtener el modo actual (Claro/Oscuro)
        icono = ICON_DARK if customtkinter.get_appearance_mode() == "Dark" else ICON_LIGHT
        ventana_plantilla.after(200, lambda: ventana_plantilla.iconbitmap(icono)) # Espera 200ms para cambiar el icono
        
        autoDocs = crearTexto(ventana_plantilla, "Crear Plantilla de Documento", "Menlo", 28)
        autoDocs.place(relx=POS_TITULO[0], rely=POS_TITULO[1])
        
        # --- Titulo ---
        textoTitulo = crearTexto(ventana_plantilla,
                                 "1.Título del documento",
                                 "Consolas",
                                 16)
        textoTitulo.place(relx=POS_TEXTOTITULO[0], rely=POS_TEXTOTITULO[1])
        
        tituloDoc = customtkinter.CTkEntry(
            ventana_plantilla,
            placeholder_text="Escribir título...",
            width=200,
            height=35,
            validate="key",
            validatecommand=cmd_titulo) # Limite 60
        tituloDoc.place(relx=POS_TITULODOC[0], rely=POS_TITULODOC[1])

        # --- Subtitulo ---
        textoSubTitulo = crearTexto(ventana_plantilla,
                                 "2.Subtítulo",
                                 "Consolas",
                                 16)
        textoSubTitulo.place(relx=POS_TEXTOSUBTITULO[0], rely=POS_TEXTOSUBTITULO[1])
        
        subtituloDoc = customtkinter.CTkEntry(
            ventana_plantilla,
            placeholder_text="(Opcional)",
            width=200,
            height=35,
            validate="key",
            validatecommand=cmd_subtitulo)  # límite 80
        subtituloDoc.place(relx=POS_SUBTITULODOC[0], rely=POS_SUBTITULODOC[1])

        # --- Estudiantes ---
        textoEstudiantes = crearTexto(ventana_plantilla,
                                 "3.Estudiantes",
                                 "Consolas",
                                 16)
        textoEstudiantes.place(relx=POS_TEXTOESTUDIANTES[0], rely=POS_TEXTOESTUDIANTES[1])
        
        estudiantes = customtkinter.CTkEntry(
            ventana_plantilla,
            placeholder_text="Ej: Pedro - Juan - Sofía",
            width=200,
            height=35,
            validate="key",
            validatecommand=cmd_estudiantes)  # límite 50
        estudiantes.place(relx=POS_ESTUDIANTES[0], rely=POS_ESTUDIANTES[1])

        # --- Profesor ---
        textoProfesor = crearTexto(ventana_plantilla,
                                 "4.Profesor(a)",
                                 "Consolas",
                                 16)
        textoProfesor.place(relx=POS_TEXTOPROFESOR[0], rely=POS_TEXTOPROFESOR[1])
        
        profesor = customtkinter.CTkEntry(
            ventana_plantilla,
            placeholder_text="Nombre del profesor(a)",
            width=200,
            height=35,
            validate="key",
            validatecommand=cmd_profesor)  # límite 44
        profesor.place(relx=POS_PROFESOR[0], rely=POS_PROFESOR[1])

        # --- Asignatura ---
        textoAsignatura = crearTexto(ventana_plantilla,
                                 "5.Asignatura",
                                 "Consolas",
                                 16)
        textoAsignatura.place(relx=POS_TEXTOASIGNATURA[0], rely=POS_TEXTOASIGNATURA[1])
        
        asignatura = customtkinter.CTkEntry(
            ventana_plantilla,
            placeholder_text="Ej: Fundamentos de Software",
            width=200,
            height=35,
            validate="key",
                    validatecommand=cmd_asignatura)  # límite 44
        asignatura.place(relx=POS_ASIGNATURA[0], rely=POS_ASIGNATURA[1])

        # --- Sección ---
        textoSeccion = crearTexto(ventana_plantilla,
                                 "6.Sección",
                                 "Consolas",
                                 16)
        textoSeccion.place(relx=POS_TEXTOSECCION[0], rely=POS_TEXTOSECCION[1])
        
        seccion = customtkinter.CTkEntry(
            ventana_plantilla,
            placeholder_text="(Opcional) Ej: 008D",
            width=200,
            height=35,
            validate="key",
            validatecommand=cmd_seccion)  # límite 30
        seccion.place(relx=POS_SECCION[0], rely=POS_SECCION[1])
        
        # Encabezado
        textoImagen = crearTexto(ventana_plantilla, "Seleccionar imagen de encabezado", "Consolas", 16)
        textoImagen.place(relx=POS_TEXTOIMAGEN[0], rely=POS_TEXTOIMAGEN[1])

        labelImagen = crearTexto(ventana_plantilla, "(Opcional)", "Consolas", 12)
        labelImagen.place(relx=POS_LABELIMAGEN[0], rely=POS_LABELIMAGEN[1])

        def seleccionarImagen():
            imagen = filedialog.askopenfilename(
                title="Seleccionar imagen de encabezado",
                filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
                    )
            if imagen:
                labelImagen.configure(text=os.path.basename(imagen))
                botonSeleccionarImagen.imagen_path = imagen

        textoNombreArchivo = crearTexto(ventana_plantilla, "Nombre del archivo", "Consolas", 16)
        textoNombreArchivo.place(relx=POS_TEXTONOMBREARCHIVO[0], rely=POS_TEXTONOMBREARCHIVO[1])

        nombreArchivo = customtkinter.CTkEntry(
            ventana_plantilla,
            placeholder_text="(Opcional) Ej: Informe N°1",
            width=200,
            height=35)
        nombreArchivo.place(relx=POS_NOMBREARCHIVO[0], rely=POS_NOMBREARCHIVO[1])
        
        botonSeleccionarImagen = customtkinter.CTkButton(ventana_plantilla,
            text="Explorar Archivos",
            command=seleccionarImagen,
            fg_color=("#cecece","gray"),
            hover_color=("#c0c0c0","#666666"),
            text_color=("black","white"),
            height=35)
        botonSeleccionarImagen.place(relx=POS_BOTONIMAGEN[0], rely=POS_BOTONIMAGEN[1])

        botonGenerarDoc = customtkinter.CTkButton(ventana_plantilla,
                text="Generar Plantilla",             # Nombre del botón
                command=lambda: generarDoc(tituloDoc, subtituloDoc, estudiantes, profesor, asignatura, seccion, botonSeleccionarImagen, nombreArchivo),# Función a ejecutar
                fg_color="#437791",                 # Color del botón
                hover_color="#386379",              # Color sobre el mouse
                text_color="white",                   # Color del texto
                height=55,                            # Alto del botón
                width=190)                            # Ancho del botón
        botonGenerarDoc.place(relx=POS_GENERARPLANTILLA[0], rely=POS_GENERARPLANTILLA[1])
        
        botonVolver = customtkinter.CTkButton(ventana_plantilla,
                text="Volver",                     # Nombre del botón
                command=ventana_plantilla.destroy, # Función a ejecutar
                fg_color="#ba6258",              # Color del botón
                hover_color="#7f342d",           # Color sobre el mouse
                text_color="white",                # Color del texto
                height=35)                         # Alto del botón
        botonVolver.place(relx=POS_VOLVER[0], rely=POS_VOLVER[1])
        
        # --- Función para rellenar con datos de prueba ---
        def rellenarPrueba():
            tituloDoc.delete(0, "end")        
            tituloDoc.insert(0, "Informe Gestión de Biblioteca")
    
            subtituloDoc.delete(0, "end")
            subtituloDoc.insert(0, "Etapa 1: Análisis de Requisitos del Sistema")
    
            estudiantes.delete(0, "end")
            estudiantes.insert(0, "Bayron Urrutia - José Ibarra")
    
            profesor.delete(0, "end")
            profesor.insert(0, "Elliana Mallén González")
    
            asignatura.delete(0, "end")
            asignatura.insert(0, "Ingeniería de Requisitos")
    
            seccion.delete(0, "end")
            seccion.insert(0, "008D")
            
            nombreArchivo.delete(0, "end")
            nombreArchivo.insert(0, "Informe_Biblioteca")
        
        # --- Botón datos de prueba (NUEVO) ---
        botonPrueba = customtkinter.CTkButton(ventana_plantilla,
            text="Datos de Prueba",        # NUEVO: botón para rellenar campos
            command=rellenarPrueba,        # NUEVO: llama la función de prueba
            fg_color=("#cecece", "gray"),  # NUEVO: mismo estilo que botones neutros
            hover_color=("#c0c0c0", "#666666"), # NUEVO
            text_color=("black", "white"), # NUEVO
            height=35)                     # NUEVO
        botonPrueba.place(relx=0.41, rely=0.75)  # NUEVO: posición debajo del volver
        
    else:
        ventana_plantilla.focus()
        
def convertirPdf():
    # --- Posiciones ---
    POS_TITULODOC = (0.18, 0.09)
    POS_ARCHIVO = (0.40, 0.44)
    POS_SELECCIONAR = (0.19, 0.43)
    POS_VOLVER = (0.41, 0.83)
    POS_CONVERTIR = (0.41, 0.56)
    POS_TEXTOARCHIVO = (0.19, 0.34)
    
    global ventana_pdf

    if ventana_pdf is None or not ventana_pdf.winfo_exists():
        # ------ Crear y ajustar ventana ------
        ventana_pdf = customtkinter.CTkToplevel(app)
        ventana_pdf.transient(app)                             # Vincula a la ventana principal
        ventana_pdf.grab_set()                                 # Impide interactuar con la principal
        ventana_pdf.focus_force()                              # Le da foco inmediatamente
        ventana_pdf.title("Convertir Documento Word a PDF") # Cambiar el tituloDoc superior de la ventana   
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
        tituloDoc = crearTexto(ventana_pdf, "Convertir Documento Word a PDF", "Menlo", 34)
        tituloDoc.place(relx=POS_TITULODOC[0], rely=POS_TITULODOC[1])

        # -- Texto seleccion de archivo ---
        textoArchivo = crearTexto(ventana_pdf, "Seleccionar archivo PDF a convertir", "Consolas", 16)
        textoArchivo.place(relx=POS_TEXTOARCHIVO[0], rely=POS_TEXTOARCHIVO[1])
        
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
            fg_color="#437791",
            hover_color="#386379",
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
    POS_GENERARPLANTILLA = (0.07, 0.21)
    POS_SALIR = (0.32, 0.83)
    
    global ventana_acerca

    if ventana_acerca is None or not ventana_acerca.winfo_exists():
        # ------ Crear y ajustar ventana ------
        ventana_acerca = customtkinter.CTkToplevel(app)
        ventana_acerca.transient(app)           # Vincula a la ventana principal
        ventana_acerca.grab_set()               # Impide interactuar con la principal
        ventana_acerca.focus_force()            # Le da foco inmediatamente
        ventana_acerca.title("Acerca de")       # Cambiar el tituloDoc superior de la ventana   
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
                "Python con CustomTkinter, Python-Docx y\n"
                "Docx2Pdf.\n\n\n"
                "Desarrollado por:\n"
                "Bayron Urrutia\n\n"
                "© 2026",
            font=("Consolas", 16), # Tamaño y tipo de letra
            justify="left")        # Alineamiento del texto a la izquierda
        texto.place(relx=POS_GENERARPLANTILLA[0], rely=POS_GENERARPLANTILLA[1])
        
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
