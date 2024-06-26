##
##  main.py
##  SNMPy
##
##  Created by 0xGuigui on 13/03/2024.
##  Contributor(s): 0xGuigui
##

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import argparse
import json
import os
import markdown
import re
import time
import csv
import re
import tkinter.filedialog as filedialog
import datetime

try:
    import tkinter as tk
    from tkinter import messagebox
    import ttkthemes
    import tkinter.ttk as ttk
    GUI_MODE = True
except ImportError:
    GUI_MODE = False

SENTMAILS = "sent.json"
saved_server = None
saved_port = None
saved_username = None
saved_password = None
sent_emails: dict = {}
smpty_adr = "127.0.0.1"
smpty_port = "9900"

def save_mail(email: str, email_id: int):
    new_mail = {
        "id": email_id,
        "timestamp": str(datetime.datetime.now().timestamp()),
    }
    email_user = email.split('@')[0]
    if sent_emails.keys().__contains__(email_user) is False:
        sent_emails[email_user] = [new_mail]
    else:
        cur_list: list = sent_emails[email_user]
        cur_list.append(new_mail)
        sent_emails[email_user] = cur_list
    saving_file = open(SENTMAILS, "w")
    saving_file.write(json.dumps(sent_emails))
    saving_file.close()


def prepare_mail(email: str, html_body: str, email_id: int):
    if html_body.find("http://%SMPTYSERVERADRESS%:%SMPTYSERVERPORT%/smtpy/%SMPTYEMAILUSER%/%SMTPYEMAILID%") != 1:
        email_user = email.split('@')[0]
        html_body = html_body.replace('%SMPTYSERVERADRESS%', smpty_adr)
        html_body = html_body.replace('%SMPTYSERVERPORT%', smpty_port)
        html_body = html_body.replace('%SMPTYEMAILUSER%', email_user)
        html_body = html_body.replace('%SMTPYEMAILID%', str(email_id))
    return html_body

def send_mail(server, port, username, password, sender_name, to_emails, cc_emails, subject, body, delay):
    try:
        server = smtplib.SMTP(server, port)
        server.starttls()
        server.login(username, password)

        for email in to_emails:
            email_id = random.randint(1000000000, 2147483647)
            msg = MIMEMultipart()
            msg['From'] = f"{sender_name} <{username}>"
            msg['To'] = email
            msg['Subject'] = subject

            # Convert Markdown to HTML
            html_body = markdown.markdown(body)
            html_body = prepare_mail(email, html_body, email_id)
            msg.attach(MIMEText(html_body, 'html'))

            server.sendmail(username, email, msg.as_string())
            time.sleep(delay)  # Ajoutez une pause ici
            save_mail(email, email_id)

        server.quit()
    except smtplib.SMTPAuthenticationError:
        raise RuntimeError("Authentication failed. Please check your username and password.")
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Failed to send email: {e}")

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email address")

def submit_form(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description="Send email from CLI or GUI")
        parser.add_argument("-cli", action="store_true", help="Run in CLI mode")
        args = parser.parse_args()

    if args.cli:
        load_credentials()
        server = input("Server [press ENTER to use saved credentials]: ") or saved_server
        port = int(input("Port [press ENTER to use saved credentials]: ") or saved_port)
        username = input("Email [press ENTER to use saved credentials]: ") or saved_username
        password = input("Password [press ENTER to use saved credentials]: ") or saved_password
        sender_name = input("Sender Name: ")
        to_emails = input("To Email(s) (comma-separated): ").split(',')
        cc_emails = []
        subject = input("Subject: ")
        body = input("Body: ")
    else:
        server = server_entry.get()
        port = int(port_entry.get())
        username = username_entry.get()
        password = password_entry.get()
        sender_name = sender_name_entry.get()
        to_emails = [email.strip() for email in to_email_entry.get().split(',')]
        cc_emails = []
        subject = subject_entry.get()
        body = body_entry.get("1.0", "end-1c")

    try:
        validate_email(username)
        if not password:
            raise ValueError("Password cannot be empty")
        for email in to_emails:
            validate_email(email)
    except ValueError as e:
        error_message = f"Invalid input: {e}"
        if args.cli:
            print("Error:", error_message)
        else:
            messagebox.showerror("Error", error_message)
        return

    try:
        delay = int(delay_entry.get())
        send_mail(server, port, username, password, sender_name, to_emails, cc_emails, subject, body, delay)
        success_message = "Email sent successfully"
        if args.cli:
            print(success_message)
        else:
            messagebox.showinfo("Success", success_message)
            if save_credentials_var.get():
                save_credentials(server, port, username, password)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        if args.cli:
            print("Error:", error_message)
        else:
            messagebox.showerror("Error", error_message)

def load_credentials():
    global saved_server, saved_port, saved_username, saved_password, server_entry, port_entry, username_entry, password_entry, server_combo
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                if key == 'SERVER':
                    saved_server = value
                    if GUI_MODE:
                        server_entry.delete(0, tk.END)  # Effacer le contenu actuel
                        server_entry.insert(0, value)
                elif key == 'PORT':
                    saved_port = int(value)
                    if GUI_MODE:
                        port_entry.delete(0, tk.END)  # Effacer le contenu actuel
                        port_entry.insert(0, value)
                elif key == 'EMAIL':
                    saved_username = value
                    if GUI_MODE:
                        username_entry.delete(0, tk.END)  # Effacer le contenu actuel
                        username_entry.insert(0, value)
                elif key == 'PASSWORD':
                    saved_password = value
                    if GUI_MODE:
                        password_entry.delete(0, tk.END)  # Effacer le contenu actuel
                        password_entry.insert(0, value)
    if GUI_MODE:
            if saved_server and saved_port and saved_username and saved_password:
                save_credentials_var.set(1)

    if GUI_MODE and saved_server:
        server_combo.set("Custom")
        on_server_selected(None)

def on_closing():
    if not save_credentials_var.get() and os.path.exists('.env'):
        os.remove('.env')
    root.destroy()

def save_credentials(server, port, username, password):
    credentials = f"SERVER={server}\nPORT={port}\nEMAIL={username}\nPASSWORD={password}"
    with open('.env', 'w') as f:
        f.write(credentials)

def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
    else:
        password_entry.config(show="")

def load_email_list():
    email_list_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
    if email_list_file:
        emails = []
        if email_list_file.endswith('.csv'):
            with open(email_list_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    emails.extend([email.strip() for email in row if email.strip()])
        else:
            with open(email_list_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip():  # Check if line is not empty
                        emails.extend([email.strip() for email in re.split(',|;', line) if email.strip()])

        to_email_entry.delete(0, tk.END)
        to_email_entry.insert(0, ', '.join(emails))

def load_file_content():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html"), ("Text files", "*.txt"), ("Markdown files", "*.md")])
    if file_path:
        with open(file_path, 'r') as f:
            content = f.read()
            body_entry.delete("1.0", "end-1c")
            body_entry.insert("1.0", content)

def on_server_selected(event):
    if server_combo.get() == "Custom":
        server_label.grid(row=1, column=0, padx=5, pady=5)
        server_entry.grid(row=1, column=1, padx=5, pady=5)
        port_label.grid(row=2, column=0, padx=5, pady=5)
        port_entry.grid(row=2, column=1, padx=5, pady=5)
        if saved_server and saved_port and not server_entry.get() and not port_entry.get():
            server_entry.insert(0, saved_server)
            port_entry.insert(0, saved_port)
    else:
        server_label.grid_remove()
        server_entry.grid_remove()
        port_label.grid_remove()
        port_entry.grid_remove()
        server = SERVER_PORT_MAPPING[server_combo.get()]["server"]
        port = SERVER_PORT_MAPPING[server_combo.get()]["port"]
        server_entry.delete(0, tk.END)
        server_entry.insert(0, server)
        port_entry.delete(0, tk.END)
        port_entry.insert(0, port)

SERVER_PORT_MAPPING = {
    "Google": {"server": "smtp.gmail.com", "port": 587},
    "Yahoo": {"server": "smtp.mail.yahoo.com", "port": 465},
    "Microsoft": {"server": "smtp.office365.com", "port": 587},
}


if os.path.isfile(os.getcwd() + "/" + SENTMAILS) is False:
    open_file = open(SENTMAILS, "w")
    open_file.write("{}")
    open_file.close()
open_file = open(SENTMAILS, "r")
if open_file is False:
    print("Couldn't load sent.json")
    exit(1)
sent_emails.update(json.loads(open_file.read()))
open_file.close()
random.seed(datetime.datetime.now().timestamp())

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Send email from CLI or GUI")
        parser.add_argument("-cli", action="store_true", help="Run in CLI mode")
        args = parser.parse_args()

        if args.cli:
            try:
                submit_form(args)
            except RuntimeError as e:
                print("Error:", str(e))
        else:
            if GUI_MODE:
                root = ttkthemes.ThemedTk(theme="equilux")
                root.resizable(False, False)
                root.title("SNMPy")

                form_frame = ttk.Frame(root, padding=(20, 10))
                form_frame.grid(row=0, column=0, sticky='ew')

                button_frame = ttk.Frame(root, padding=(0, 10))
                button_frame.grid(row=1, column=0, sticky='ew')

                server_label = ttk.Label(form_frame, text="Server:")
                server_label.grid(row=0, column=0, padx=5, pady=5)
                server_combo = ttk.Combobox(form_frame, values=list(SERVER_PORT_MAPPING.keys()) + ["Custom"], state="readonly")
                server_combo.grid(row=0, column=1, padx=5, pady=5)
                server_combo.bind("<<ComboboxSelected>>", on_server_selected)

                server_entry = ttk.Entry(form_frame)
                port_entry = ttk.Entry(form_frame)

                port_label = ttk.Label(form_frame, text="Port:")

                sender_name_label = ttk.Label(form_frame, text="Sender Name:")
                sender_name_label.grid(row=3, column=0, padx=5, pady=5)
                sender_name_entry = ttk.Entry(form_frame)
                sender_name_entry.grid(row=3, column=1, padx=5, pady=5)

                username_label = ttk.Label(form_frame, text="Email:")
                username_label.grid(row=4, column=0, padx=5, pady=5)
                username_entry = ttk.Entry(form_frame)
                username_entry.grid(row=4, column=1, padx=5, pady=5)

                password_label = ttk.Label(form_frame, text="Password:")
                password_label.grid(row=5, column=0, padx=5, pady=5)
                password_entry = ttk.Entry(form_frame, show="*")
                password_entry.grid(row=5, column=1, padx=5, pady=5)

                show_password_var = tk.BooleanVar()
                show_password_checkbox = ttk.Checkbutton(form_frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility)
                show_password_checkbox.grid(row=5, column=2, padx=5, pady=5)

                to_email_label = ttk.Label(form_frame, text="To Email(s):")
                to_email_label.grid(row=6, column=0, padx=5, pady=5)
                to_email_entry = ttk.Entry(form_frame)
                to_email_entry.grid(row=6, column=1, padx=5, pady=5)

                delay_label = ttk.Label(form_frame, text="Delay between emails (seconds):")
                delay_label.grid(row=9, column=0, padx=5, pady=5)
                delay_entry = ttk.Entry(form_frame)
                delay_entry.grid(row=9, column=1, padx=5, pady=5)

                subject_label = ttk.Label(form_frame, text="Subject:")
                subject_label.grid(row=7, column=0, padx=5, pady=5)
                subject_entry = ttk.Entry(form_frame)
                subject_entry.grid(row=7, column=1, padx=5, pady=5)

                body_label = ttk.Label(form_frame, text="Body:")
                body_label.grid(row=8, column=0, padx=5, pady=5)
                body_entry = tk.Text(form_frame, height=10, width=40)
                body_entry.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

                submit_button = ttk.Button(button_frame, text="Send Email", command=submit_form)
                submit_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

                save_credentials_var = tk.IntVar()
                save_credentials_checkbox = ttk.Checkbutton(button_frame, text="Save Credentials", variable=save_credentials_var)
                save_credentials_checkbox.pack(side=tk.RIGHT, padx=5, pady=5, expand=True)

                load_email_list_button = ttk.Button(button_frame, text="Load Email List", command=load_email_list)
                load_email_list_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

                load_file_button = ttk.Button(button_frame, text="Load File", command=load_file_content)
                load_file_button.pack(side=tk.LEFT, padx=5, pady=5, expand=True)

                load_credentials()

                root.protocol("WM_DELETE_WINDOW", on_closing)  # Move this line before root.mainloop()
                root.mainloop()
            else:
                print("Tkinter module is not available, please run in CLI mode.")
    except KeyboardInterrupt:
        print("\nExiting...")
