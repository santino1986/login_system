import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Necesitarás instalar Pillow: pip install pillow
import mysql.connector
import requests
import subprocess
import time

# Conectar a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="Santy",       # Cambia esto por tu usuario de MySQL
    password="Mundi@l1986",  # Cambia esto por tu contraseña de MySQL
    database="login_system"
)

cursor = db.cursor()

# Función para enviar eventos a la API
def enviar_evento_api(evento, usuario, alimentador):
    url = "https://webhook.site/7f97ab5c-c308-4969-8bd6-165c4ef0608a"  # Cambia esto por la URL de tu API
    data = {
        "evento": evento,
        "usuario": usuario,
        "alimentador": alimentador
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Genera una excepción si la respuesta no es 200 OK
        print(f"Evento '{evento}' enviado exitosamente para el usuario '{usuario}', alimentador '{alimentador}'")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar evento a la API: {e}")

# Función de login
def login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    alimentador = "01"  # Puedes cambiar este valor para cada alimentador

    # Consulta en la base de datos
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s", (usuario, contrasena))
    result = cursor.fetchone()
    
    if result:
        messagebox.showinfo("Login exitoso", f"Bienvenido, {usuario} en alimentador {alimentador}!")
        enviar_evento_api("login", usuario, alimentador)  # Enviar evento de login a la API
        abrir_programa_escaneo(usuario, alimentador)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrecta.")

# Función para abrir el programa de escaneo (simulado con Bloc de notas)
def abrir_programa_escaneo(usuario, alimentador):
    # Ruta del Bloc de notas
    programa_escaneo_path = "notepad.exe"
    proceso = subprocess.Popen(programa_escaneo_path)

    # Esperar hasta que el Bloc de notas se cierre
    while proceso.poll() is None:
        time.sleep(1)  # Esperar un segundo antes de verificar de nuevo

    # Logout cuando se cierra el programa de escaneo
    logout(usuario, alimentador)

# Función de logout
def logout(usuario, alimentador):
    enviar_evento_api("logout", usuario, alimentador)  # Enviar evento de logout a la API
    messagebox.showinfo("Logout", f"{usuario} se ha deslogueado en el alimentador {alimentador}.")
    root.quit()  # Cierra la aplicación completa

# Función para registrar un nuevo usuario
def registrar_usuario():
    usuario = entry_nuevo_usuario.get()
    contrasena = entry_nueva_contrasena.get()
    
    # Insertar el nuevo usuario en la base de datos
    try:
        cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)", (usuario, contrasena))
        db.commit()
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
        ventana_registro.destroy()
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "El nombre de usuario ya existe.")

# Función para abrir la ventana de registro
def abrir_ventana_registro():
    global ventana_registro, entry_nuevo_usuario, entry_nueva_contrasena

    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registrar Usuario")
    ventana_registro.geometry("300x200")
    ventana_registro.configure(bg="#f2f2f2")

    tk.Label(ventana_registro, text="Nuevo Nombre de Usuario:", bg="#f2f2f2", fg="#333333").pack(pady=5)
    entry_nuevo_usuario = tk.Entry(ventana_registro)
    entry_nuevo_usuario.pack()

    tk.Label(ventana_registro, text="Nueva Contraseña:", bg="#f2f2f2", fg="#333333").pack(pady=5)
    entry_nueva_contrasena = tk.Entry(ventana_registro, show="*")
    entry_nueva_contrasena.pack()

    tk.Button(ventana_registro, text="Registrar", command=registrar_usuario, bg="#990000", fg="white").pack(pady=20)

# Crear la ventana principal de login
root = tk.Tk()
root.title("Login Urbano")
root.geometry("400x400")
root.configure(bg="#333333")  # Fondo gris oscuro

# Etiquetas y campos de entrada
tk.Label(root, text="Nombre de Usuario:", bg="#333333", fg="white", font=("Arial", 12)).pack(pady=5)
entry_usuario = tk.Entry(root, font=("Arial", 12))
entry_usuario.pack()

tk.Label(root, text="Contraseña:", bg="#333333", fg="white", font=("Arial", 12)).pack(pady=5)
entry_contrasena = tk.Entry(root, show="*", font=("Arial", 12))
entry_contrasena.pack()

# Botones de Login y Registro
tk.Button(root, text="Iniciar Sesión", command=login, bg="#990000", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Registrar Usuario", command=abrir_ventana_registro, bg="#666666", fg="white", font=("Arial", 12)).pack(pady=10)

root.mainloop()
