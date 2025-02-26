from tkinter import *
from tkinter import messagebox
import os
import re
import hashlib
import pygame  # Biblioteca para reproduzir música
import speedtest  # Para o teste de velocidade
import threading  # Para executar o teste de velocidade em uma thread separada

# Inicializa o pygame para reprodução de áudio
pygame.mixer.init()

# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Email validation function
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Função para tocar música
def play_music(file_path):
    pygame.mixer.music.load(file_path)  # Carrega o arquivo de música
    pygame.mixer.music.play(-1)  # Repete a música indefinidamente
    pygame.mixer.music.set_volume(0.02)  # Define o volume para 2%

# Função para exibir a tela de funcionalidades
def functionality_screen():
    func_window = Toplevel(screen)
    func_window.title("Funcionalidades")
    func_window.geometry("1280x720+150+80")
    func_window.configure(bg="#2C3E50")

    # Frame para as funcionalidades
    func_frame = Frame(func_window, bg="#34495E", width=800, height=500, bd=10, relief="solid")
    func_frame.pack(padx=20, pady=20)

    # Título
    func_label = Label(func_frame, text="Escolha uma Funcionalidade", font=("Helvetica", 40, "bold"), fg="#ECF0F1", bg="#34495E")
    func_label.pack(pady=20)

    # Botões para as funcionalidades
    Button(
        func_frame,
        text="Speed Test",
        font=("Helvetica", 20),
        bg="#16A085",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=speed_test_screen  # Abre a tela de teste de velocidade
    ).pack(pady=10)

    Button(
        func_frame,
        text="Calculadora IMC",
        font=("Helvetica", 20),
        bg="#F39C12",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=imc_screen  # Abre a tela de IMC
    ).pack(pady=10)

    Button(
        func_frame,
        text="Conversor de Medidas",
        font=("Helvetica", 20),
        bg="#16A085",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=conversor_screen  # Abre a tela de conversor de medidas
    ).pack(pady=10)

    Button(
        func_frame,
        text="Chatbot",
        font=("Helvetica", 20),
        bg="#F39C12",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=chatbot_screen  # Abre a tela do chatbot
    ).pack(pady=10)

    # Botão para fechar a janela e parar a música
    Button(
        func_frame,
        text="Fechar",
        font=("Helvetica", 20),
        bg="#E74C3C",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=lambda: [pygame.mixer.music.stop(), func_window.destroy()]  # Para a música e fecha a janela
    ).pack(pady=20)

# Função para abrir a tela do Speed Test
def speed_test_screen():
    speed_window = Toplevel(screen)
    speed_window.title("Speed Test")
    speed_window.geometry("600x400+150+80")
    speed_window.configure(bg="#2C3E50")

    # Labels para exibir os resultados
    global download_label, upload_label, ping_label
    download_label = Label(speed_window, text="Download Speed: Not Tested", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50")
    download_label.pack(pady=10)

    upload_label = Label(speed_window, text="Upload Speed: Not Tested", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50")
    upload_label.pack(pady=10)

    ping_label = Label(speed_window, text="Ping: Not Tested", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50")
    ping_label.pack(pady=10)

    # Botão para iniciar o teste de velocidade
    Button(
        speed_window,
        text="Testar Velocidade",
        font=("Helvetica", 16),
        bg="#16A085",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=lambda: threading.Thread(target=test_speed).start()  # Executa o teste em uma thread separada
    ).pack(pady=20)

# Função para testar a velocidade da internet
def test_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000
    ping = st.results.ping

    # Atualiza os labels com os resultados
    download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")
    upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
    ping_label.config(text=f"Ping: {ping} ms")

# Função para abrir a tela do IMC
def imc_screen():
    imc_window = Toplevel(screen)
    imc_window.title("Calculadora IMC")
    imc_window.geometry("600x400+150+80")
    imc_window.configure(bg="#2C3E50")

    # Labels e campos de entrada
    Label(imc_window, text="Peso (kg):", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50").pack(pady=10)
    weight_entry = Entry(imc_window, font=("Helvetica", 16))
    weight_entry.pack(pady=10)

    Label(imc_window, text="Altura (m):", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50").pack(pady=10)
    height_entry = Entry(imc_window, font=("Helvetica", 16))
    height_entry.pack(pady=10)

    # Label para exibir o resultado
    result_label = Label(imc_window, text="IMC: ", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50")
    result_label.pack(pady=10)

    # Função para calcular o IMC
    def calculate_imc():
        try:
            weight = float(weight_entry.get())
            height = float(height_entry.get())
            imc = weight / (height ** 2)
            result_label.config(text=f"IMC: {imc:.2f}")
        except ValueError:
            result_label.config(text="Erro: Insira valores válidos.")

    # Botão para calcular o IMC
    Button(
        imc_window,
        text="Calcular IMC",
        font=("Helvetica", 16),
        bg="#16A085",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=calculate_imc
    ).pack(pady=20)

# Função para abrir a tela do Conversor de Medidas
def conversor_screen():
    conversor_window = Toplevel(screen)
    conversor_window.title("Conversor de Medidas")
    conversor_window.geometry("600x400+150+80")
    conversor_window.configure(bg="#2C3E50")

    # Labels e campos de entrada
    Label(conversor_window, text="Valor:", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50").pack(pady=10)
    value_entry = Entry(conversor_window, font=("Helvetica", 16))
    value_entry.pack(pady=10)

    Label(conversor_window, text="De:", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50").pack(pady=10)
    from_unit = StringVar(value="Metros")
    from_menu = OptionMenu(conversor_window, from_unit, "Metros", "Kilômetros", "Milhas")
    from_menu.config(font=("Helvetica", 16), bg="#16A085", fg="white")
    from_menu.pack(pady=10)

    Label(conversor_window, text="Para:", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50").pack(pady=10)
    to_unit = StringVar(value="Kilômetros")
    to_menu = OptionMenu(conversor_window, to_unit, "Metros", "Kilômetros", "Milhas")
    to_menu.config(font=("Helvetica", 16), bg="#16A085", fg="white")
    to_menu.pack(pady=10)

    # Label para exibir o resultado
    result_label = Label(conversor_window, text="Resultado: ", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50")
    result_label.pack(pady=10)

    # Função para converter as medidas
    def convert_units():
        try:
            value = float(value_entry.get())
            from_u = from_unit.get()
            to_u = to_unit.get()

            if from_u == "Metros" and to_u == "Kilômetros":
                result = value / 1000
            elif from_u == "Kilômetros" and to_u == "Metros":
                result = value * 1000
            elif from_u == "Metros" and to_u == "Milhas":
                result = value * 0.000621371
            elif from_u == "Milhas" and to_u == "Metros":
                result = value / 0.000621371
            else:
                result = value  # Se as unidades forem iguais

            result_label.config(text=f"Resultado: {result:.2f} {to_u}")
        except ValueError:
            result_label.config(text="Erro: Insira um valor válido.")

    # Botão para converter
    Button(
        conversor_window,
        text="Converter",
        font=("Helvetica", 16),
        bg="#16A085",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=convert_units
    ).pack(pady=20)

# Função para abrir a tela do Chatbot
def chatbot_screen():
    chatbot_window = Toplevel(screen)
    chatbot_window.title("Chatbot")
    chatbot_window.geometry("600x400+150+80")
    chatbot_window.configure(bg="#2C3E50")

    # Label para exibir as mensagens
    chat_label = Label(chatbot_window, text="Bem-vindo ao Chatbot!", font=("Helvetica", 16), fg="#ECF0F1", bg="#2C3E50")
    chat_label.pack(pady=10)

    # Campo de entrada para o usuário
    user_entry = Entry(chatbot_window, font=("Helvetica", 16))
    user_entry.pack(pady=10)

    # Função para responder às perguntas
    def chatbot_responder():
        pergunta = user_entry.get().lower()
        respostas = {
            'olá': 'Olá! Como posso ajudar você hoje?',
            'tudo bem': 'Estou bem, obrigado por perguntar!',
            'qual é o seu nome?': 'Eu sou um chatbot criado para ajudar!',
            'adeus': 'Até logo! Foi bom conversar com você.',
            'qual é a sua função?': 'Eu sou um chatbot para responder perguntas simples.',
            'como você está?': 'Eu sou um programa, mas estou pronto para ajudar!',
            'me fale sobre o clima': 'Infelizmente, não sei o clima, mas posso te ajudar a encontrar a previsão!',
            'qual é a capital do brasil?': 'A capital do Brasil é Brasília.',
            'quem é o presidente do brasil?': 'Atualmente, o presidente do Brasil é Luiz Inácio Lula da Silva.',
        }

        resposta = respostas.get(pergunta, "Desculpe, não entendi sua pergunta. Pode reformular?")
        chat_label.config(text=f"Chatbot: {resposta}")

    # Botão para enviar a pergunta
    Button(
        chatbot_window,
        text="Enviar",
        font=("Helvetica", 16),
        bg="#16A085",
        fg="white",
        bd=0,
        relief="flat",
        width=20,
        height=2,
        command=chatbot_responder
    ).pack(pady=20)

# Register new user
def register():
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()

    # Check if fields are empty
    if not all([name, email, password, confirm_password]):
        messagebox.showerror("Error", "All fields must be filled!")
        return

    # Check if email is valid
    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format!")
        return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords don't match!")
        return

    # Check if email is already registered
    if user_exists(email):
        messagebox.showerror("Error", "Email already registered!")
        return

    # Hash password and save user to file
    hashed_password = hash_password(password)
    save_user(name, email, hashed_password)
    messagebox.showinfo("Success", "Registration successful!")

    # Clear fields
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    entry_password.delete(0, END)
    entry_confirm_password.delete(0, END)

    # Fecha a tela de registro e abre a tela de login
    reg_screen.destroy()
    main_screen()

# Check if user already exists
def user_exists(email):
    if not os.path.exists("users.txt"):
        return False

    with open("users.txt", "r") as file:
        for line in file:
            stored_name, stored_email, stored_password = line.strip().split(",")
            if stored_email == email:
                return True
    return False

# Save user data to file
def save_user(name, email, password):
    with open("users.txt", "a") as file:
        file.write(f"{name},{email},{password}\n")

# Login function
def login():
    user = entry_username.get()
    password = entry_password.get()

    # Check if the file exists
    if not os.path.exists("users.txt"):
        messagebox.showerror("Error", "No users found!")
        return

    # Read users from the file
    with open("users.txt", "r") as file:
        for line in file:
            stored_name, stored_email, stored_password = line.strip().split(",")
            if user == stored_name and hash_password(password) == stored_password:
                messagebox.showinfo("Success", f"Welcome, {stored_name}!")
                # Toca a música ao fazer login
                play_music("lofi_music.mp3")  # Substitua pelo caminho da sua música
                # Exibe a tela de funcionalidades
                functionality_screen()
                return

    messagebox.showerror("Invalid", "Wrong username or password")

# Login screen
def main_screen():
    global screen, entry_username, entry_password

    screen = Tk()
    screen.geometry("1280x720+150+80")
    screen.configure(bg="#2C3E50")
    screen.title("Login System")

    # Login frame
    login_frame = Frame(screen, bg="#34495E", width=800, height=400, bd=10, relief="solid")
    login_frame.pack(padx=20, pady=20)

    # Title
    login_label = Label(login_frame, text="Welcome!", font=("Helvetica", 40, "bold"), fg="#ECF0F1", bg="#34495E")
    login_label.pack(pady=50)

    # Username and password fields
    Label(login_frame, text="Enter your Username:", font=("Helvetica", 20), fg="white", bg="#34495E").pack(pady=5)
    entry_username = Entry(login_frame, font=("Helvetica", 20), width=25, bd=3, relief="flat", fg="#2C3E50", bg="#ECF0F1")
    entry_username.pack(pady=10)

    Label(login_frame, text="Enter your Password:", font=("Helvetica", 20), fg="white", bg="#34495E").pack(pady=5)
    entry_password = Entry(login_frame, font=("Helvetica", 20), width=25, bd=3, relief="flat", fg="#2C3E50", bg="#ECF0F1", show="*")
    entry_password.pack(pady=10)

    # Buttons
    Button(login_frame, text="Login", font=("Helvetica", 20), bg="#16A085", fg="white", bd=0, relief="flat", width=15, height=2, command=login).pack(pady=10)
    Button(login_frame, text="Register", font=("Helvetica", 20), bg="#F39C12", fg="white", bd=0, relief="flat", width=15, height=2, command=register_screen).pack(pady=10)

    screen.mainloop()

# Register screen
def register_screen():
    global reg_screen, entry_name, entry_email, entry_password, entry_confirm_password

    reg_screen = Toplevel(screen)
    reg_screen.title("Register")
    reg_screen.geometry("1280x720+150+80")
    reg_screen.configure(bg="#2C3E50")
    reg_screen.resizable(False, False)

    # Frame for registration
    reg_frame = Frame(reg_screen, bg="#34495E", width=800, height=500, bd=10, relief="solid")
    reg_frame.pack(padx=20, pady=20)

    # Title
    reg_label = Label(reg_frame, text="Register", font=("Helvetica", 40, "bold"), fg="#ECF0F1", bg="#34495E")
    reg_label.pack(pady=20)

    # Input fields with labels
    Label(reg_frame, text="Name:", font=("Helvetica", 20), fg="white", bg="#34495E").pack(pady=5)
    entry_name = Entry(reg_frame, font=("Helvetica", 20), width=25, bd=3, relief="flat", fg="#2C3E50", bg="#ECF0F1")
    entry_name.pack(pady=10)

    Label(reg_frame, text="Email:", font=("Helvetica", 20), fg="white", bg="#34495E").pack(pady=5)
    entry_email = Entry(reg_frame, font=("Helvetica", 20), width=25, bd=3, relief="flat", fg="#2C3E50", bg="#ECF0F1")
    entry_email.pack(pady=10)

    Label(reg_frame, text="Password:", font=("Helvetica", 20), fg="white", bg="#34495E").pack(pady=5)
    entry_password = Entry(reg_frame, font=("Helvetica", 20), width=25, bd=3, relief="flat", fg="#2C3E50", bg="#ECF0F1", show="*")
    entry_password.pack(pady=10)

    Label(reg_frame, text="Confirm Password:", font=("Helvetica", 20), fg="white", bg="#34495E").pack(pady=5)
    entry_confirm_password = Entry(reg_frame, font=("Helvetica", 20), width=25, bd=3, relief="flat", fg="#2C3E50", bg="#ECF0F1", show="*")
    entry_confirm_password.pack(pady=10)

    # Register button
    Button(reg_frame, text="Register", font=("Helvetica", 20), bg="#16A085", fg="white", bd=0, relief="flat", width=15, height=2, command=register).pack(pady=20)

# Start the login screen
main_screen()