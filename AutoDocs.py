import os
import customtkinter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def texto(app, tex, letra, size):
    
    label = customtkinter.CTkLabel(app,
    text= tex,
    font=(letra, size), # Fuente y tamaño
    text_color="gray" # Color del texto
    )
    label.pack(pady=20)   

def cambiar_tema():
    actual = customtkinter.get_appearance_mode()
    if actual == "Dark":
        customtkinter.set_appearance_mode("Light")
    else:
        customtkinter.set_appearance_mode("Dark")


def menu():
    app = customtkinter.CTk() # Crear ventana vacía
    app.iconbitmap(os.path.join(BASE_DIR, 'AutoDocs.ico')) #Cambiar icono
    app.title("AutoDocs") # Cambiar titulo
    
    # Tamaño y Posición
    ancho = 800
    alto = 500
    x = (app.winfo_screenwidth() // 2) - (ancho // 2)
    y = (app.winfo_screenheight() // 2) - (alto // 2)
    app.geometry(f"{ancho}x{alto}+{x}+{y}")

    texto(app, "《 ✪  Bienvenido a AutoDocs  ✪ 》", "Roboto", 24)

    boton = customtkinter.CTkButton(app, text="🌙 Cambiar Tema", command=cambiar_tema,
                                     fg_color="gray", hover_color="#5a5a5a")
    boton.place(x=10, y=10)

    app.mainloop() # Loop que mantiene la ventana abierta

menu()
