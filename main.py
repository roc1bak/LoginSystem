from tkinter import *
from tkinter import messagebox
import os
import re
import hashlib
import speedtest
import threading

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def back_to_login(current_window):
    current_window.destroy()
    main_screen()

def open_new_window(old_window, next_func):
    old_window.destroy()
    next_func()

def functionality_screen():
    func_window = Toplevel(screen)
    func_window.title("Funcionalidades")
    func_window.geometry("1280x720+150+80")
    func_window.configure(bg="#2C3E50")
    func_window.protocol("WM_DELETE_WINDOW", lambda: back_to_login(func_window))
    
    func_frame = Frame(func_window, bg="#34495E", width=800, height=500, bd=10, relief="solid")
    func_frame.pack(padx=20, pady=20)
    Label(func_frame, text="Escolha uma Funcionalidade", font=("Helvetica", 40, "bold"), fg="#ECF0F1", bg="#34495E").pack(pady=20)
    
    buttons = [
        ("Speed Test", "#16A085", lambda: open_new_window(func_window, speed_test_screen)),
        ("Calculadora IMC", "#F39C12", lambda: open_new_window(func_window, imc_screen)),
        ("Conversor de Medidas", "#16A085", lambda: open_new_window(func_window, conversor_screen)),
        ("Chatbot", "#F39C12", lambda: open_new_window(func_window, chatbot_screen))
    ]
    
    for text, color, cmd in buttons:
        Button(func_frame, text=text, font=("Helvetica", 20), bg=color, fg="white", bd=0, relief="flat", width=20, height=2, command=cmd).pack(pady=10)
    
    Button(func_frame, text="Sair / Logout", font=("Helvetica", 20), bg="#E74C3C", fg="white", bd=0, relief="flat", width=20, height=2, command=lambda: back_to_login(func_window)).pack(pady=20)

def speed_test_screen():
    window = Toplevel(screen)
    window.title("Speed Test")
    window.geometry("600x400+150+80")
    window.configure(bg="#2C3E50")
    window.protocol("WM_DELETE_WINDOW", lambda: open_new_window(window, functionality_screen))
    
    global download_label, upload_label, ping_label
    download_label = Label(window, text="Download: --", font=("Helvetica", 16), fg="white", bg="#2C3E50")
    download_label.pack(pady=10)
    upload_label = Label(window, text="Upload: --", font=("Helvetica", 16), fg="white", bg="#2C3E50")
    upload_label.pack(pady=10)
    ping_label = Label(window, text="Ping: --", font=("Helvetica", 16), fg="white", bg="#2C3E50")
    ping_label.pack(pady=10)
    
    Button(window, text="Testar", bg="#16A085", fg="white", command=lambda: threading.Thread(target=test_speed, daemon=True).start()).pack(pady=10)
    Button(window, text="Voltar", bg="#E74C3C", fg="white", command=lambda: open_new_window(window, functionality_screen)).pack()

def test_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        d, u, p = st.download()/1e6, st.upload()/1e6, st.results.ping
        download_label.config(text=f"Download: {d:.2f} Mbps")
        upload_label.config(text=f"Upload: {u:.2f} Mbps")
        ping_label.config(text=f"Ping: {p} ms")
    except: messagebox.showerror("Erro", "Falha no teste.")

def imc_screen():
    window = Toplevel(screen)
    window.title("IMC")
    window.geometry("600x400+150+80")
    window.configure(bg="#2C3E50")
    window.protocol("WM_DELETE_WINDOW", lambda: open_new_window(window, functionality_screen))
    
    weight_entry = Entry(window, font=("Helvetica", 16))
    weight_entry.pack(pady=10)
    height_entry = Entry(window, font=("Helvetica", 16))
    height_entry.pack(pady=10)
    res_label = Label(window, text="IMC: ", font=("Helvetica", 16), fg="white", bg="#2C3E50")
    res_label.pack(pady=10)
    
    def calc():
        try:
            w = float(weight_entry.get().replace(',', '.'))
            h = float(height_entry.get().replace(',', '.'))
            imc = w / (h**2)
            res_label.config(text=f"IMC: {imc:.2f}")
        except: res_label.config(text="Erro de entrada")
        
    Button(window, text="Calcular", bg="#16A085", fg="white", command=calc).pack(pady=10)
    Button(window, text="Voltar", bg="#E74C3C", fg="white", command=lambda: open_new_window(window, functionality_screen)).pack()

def conversor_screen():
    window = Toplevel(screen)
    window.title("Conversor")
    window.geometry("600x450+150+80")
    window.configure(bg="#2C3E50")
    window.protocol("WM_DELETE_WINDOW", lambda: open_new_window(window, functionality_screen))
    
    val_entry = Entry(window, font=("Helvetica", 16))
    val_entry.pack(pady=10)
    f_unit, t_unit = StringVar(value="Metros"), StringVar(value="Kilômetros")
    OptionMenu(window, f_unit, "Metros", "Kilômetros", "Milhas").pack()
    OptionMenu(window, t_unit, "Metros", "Kilômetros", "Milhas").pack()
    res_label = Label(window, text="Resultado: ", font=("Helvetica", 16), fg="white", bg="#2C3E50")
    res_label.pack(pady=10)
    
    def conv():
        try:
            v = float(val_entry.get().replace(',', '.'))
            factors = {"Metros": 1.0, "Kilômetros": 1000.0, "Milhas": 1609.34}
            res = v * (factors[f_unit.get()] / factors[t_unit.get()])
            res_label.config(text=f"Resultado: {res:.2f}")
        except: res_label.config(text="Erro")
        
    Button(window, text="Converter", bg="#16A085", fg="white", command=conv).pack(pady=10)
    Button(window, text="Voltar", bg="#E74C3C", fg="white", command=lambda: open_new_window(window, functionality_screen)).pack()

def chatbot_screen():
    window = Toplevel(screen)
    window.title("Chatbot")
    window.geometry("600x400+150+80")
    window.configure(bg="#2C3E50")
    window.protocol("WM_DELETE_WINDOW", lambda: open_new_window(window, functionality_screen))
    
    lbl = Label(window, text="Olá!", font=("Helvetica", 16), fg="white", bg="#2C3E50")
    lbl.pack(pady=10)
    ent = Entry(window, font=("Helvetica", 16))
    ent.pack(pady=10)
    
    def resp():
        p = ent.get().lower()
        r = {"olá": "Oi!", "tudo bem": "Sim!", "capital": "Brasília"}
        lbl.config(text=f"Bot: {r.get(p, 'Não entendi')}")
        
    Button(window, text="Enviar", bg="#16A085", fg="white", command=resp).pack(pady=10)
    Button(window, text="Voltar", bg="#E74C3C", fg="white", command=lambda: open_new_window(window, functionality_screen)).pack()

def register():
    n, e, p, c = entry_name.get(), entry_email.get(), entry_password.get(), entry_confirm_password.get()
    if not all([n, e, p, c]) or p != c or not is_valid_email(e) or user_exists(e):
        messagebox.showerror("Erro", "Dados inválidos ou e-mail já existe")
        return
    save_user(n, e, hash_password(p))
    messagebox.showinfo("Sucesso", "Registrado!")
    back_to_login(reg_screen)

def user_exists(email):
    if not os.path.exists("users.txt"): return False
    with open("users.txt", "r") as f:
        for line in f:
            d = line.strip().split(",")
            if len(d) >= 2 and d[1] == email: return True
    return False

def save_user(n, e, p):
    with open("users.txt", "a") as f: f.write(f"{n},{e},{p}\n")

def login():
    u, p = entry_username.get(), entry_password.get()
    if not os.path.exists("users.txt"): return
    hp = hash_password(p)
    with open("users.txt", "r") as f:
        for line in f:
            d = line.strip().split(",")
            if len(d) == 3 and u == d[0] and hp == d[2]:
                screen.withdraw()
                functionality_screen()
                return
    messagebox.showerror("Erro", "Login inválido")

def main_screen():
    global screen, entry_username, entry_password
    try:
        if screen.winfo_exists(): screen.deiconify()
    except:
        screen = Tk()
        screen.geometry("1280x720+150+80")
        screen.configure(bg="#2C3E50")
        screen.title("Login System")
        
        f = Frame(screen, bg="#34495E", bd=10, relief="solid")
        f.pack(pady=50)
        Label(f, text="Login", font=("Helvetica", 30), fg="white", bg="#34495E").pack(pady=20)
        entry_username = Entry(f, font=("Helvetica", 20))
        entry_username.pack(pady=10)
        entry_password = Entry(f, font=("Helvetica", 20), show="*")
        entry_password.pack(pady=10)
        Button(f, text="Login", bg="#16A085", fg="white", width=15, command=login).pack(pady=5)
        Button(f, text="Registrar", bg="#F39C12", fg="white", width=15, command=register_screen).pack(pady=5)
        screen.mainloop()

def register_screen():
    global reg_screen, entry_name, entry_email, entry_password, entry_confirm_password
    screen.withdraw()
    reg_screen = Toplevel(screen)
    reg_screen.geometry("1280x720+150+80")
    reg_screen.configure(bg="#2C3E50")
    reg_screen.protocol("WM_DELETE_WINDOW", lambda: back_to_login(reg_screen))
    
    f = Frame(reg_screen, bg="#34495E", bd=10, relief="solid")
    f.pack(pady=20)
    entry_name = Entry(f, font=("Helvetica", 18)); entry_name.pack(pady=5)
    entry_email = Entry(f, font=("Helvetica", 18)); entry_email.pack(pady=5)
    entry_password = Entry(f, font=("Helvetica", 18), show="*"); entry_password.pack(pady=5)
    entry_confirm_password = Entry(f, font=("Helvetica", 18), show="*"); entry_confirm_password.pack(pady=5)
    Button(f, text="Registrar", bg="#16A085", fg="white", command=register).pack(pady=10)
    Button(f, text="Voltar", bg="#E74C3C", fg="white", command=lambda: back_to_login(reg_screen)).pack()

if __name__ == "__main__":
    main_screen()