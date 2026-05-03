import tkinter as tk
import threading
import time
import json
import random
from datetime import datetime

activo = False
thread_bot = None

# cargar config con seguridad
def cargar_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"❌ Error cargando config: {e}")
        return {
            "intervalo_segundos": 5,
            "mensajes": ["Error en config"]
        }

# log seguro en UI
def log(texto):
    ahora = datetime.now().strftime("%H:%M:%S")
    output.insert(tk.END, f"[{ahora}] {texto}\n")
    output.see(tk.END)

# función segura para escribir desde thread
def log_safe(texto):
    ventana.after(0, log, texto)

# loop del bot
def loop_bot():
    global activo

    config = cargar_config()
    intervalo = config["intervalo_segundos"]
    mensajes = config["mensajes"]

    log_safe("🚀 Bot iniciado")

    while activo:
        mensaje = random.choice(mensajes)
        log_safe(f"📩 {mensaje}")
        time.sleep(intervalo)

    log_safe("🛑 Bot detenido")

# iniciar bot
def iniciar():
    global activo, thread_bot

    if activo:
        log("⚠️ Ya está activo")
        return

    activo = True
    thread_bot = threading.Thread(target=loop_bot, daemon=True)
    thread_bot.start()

# parar bot
def parar():
    global activo
    activo = False

# cerrar app
def cerrar():
    global activo
    activo = False
    ventana.destroy()

# --- UI ---
ventana = tk.Tk()
ventana.title("Mi Bot IA PRO")
ventana.geometry("500x400")

titulo = tk.Label(ventana, text="🤖 BOT CONTROL PRO", font=("Arial", 16))
titulo.pack(pady=10)

btn_frame = tk.Frame(ventana)
btn_frame.pack()

btn_iniciar = tk.Button(btn_frame, text="Iniciar", width=10, command=iniciar)
btn_iniciar.grid(row=0, column=0, padx=5)

btn_parar = tk.Button(btn_frame, text="Parar", width=10, command=parar)
btn_parar.grid(row=0, column=1, padx=5)

btn_salir = tk.Button(btn_frame, text="Salir", width=10, command=cerrar)
btn_salir.grid(row=0, column=2, padx=5)

output = tk.Text(ventana, height=15, width=60)
output.pack(pady=10)

ventana.protocol("WM_DELETE_WINDOW", cerrar)

ventana.mainloop()