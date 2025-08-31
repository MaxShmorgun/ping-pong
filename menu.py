from customtkinter import *
import sys 

class ConnectWindow(CTk):
    def __init__(self):
        super().__init__()

        self.name = None
        self.host = None
        self.port = None

        
        self.title("Ping-Pong")
        self.geometry("300x400")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a1a")
        
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        CTkLabel(self, text="Підключення до Ping-Pong", 
                 font=("Comic Sans MS", 22, 'bold'),
                 text_color="#f0f0f0").grid(row=0, column=0, pady=(20, 10))

        
        self.host_entry = CTkEntry(self, placeholder_text="Введіть хост", 
                                   height=45, fg_color="#2b2b2b", text_color="#f0f0f0",
                                   border_color="#4f4f4f", border_width=2, corner_radius=10)
        self.host_entry.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

        self.port_entry = CTkEntry(self, placeholder_text="Введіть порт", 
                                   height=45, fg_color="#2b2b2b", text_color="#f0f0f0",
                                   border_color="#4f4f4f", border_width=2, corner_radius=10)
        self.port_entry.grid(row=2, column=0, padx=30, pady=10, sticky="ew")

        
        CTkButton(self, text="Приєднатися", 
                  command=self.open_game, 
                  height=50, font=("Arial", 16, 'bold'),
                  fg_color="#0066cc", hover_color="#0088e8", corner_radius=10).grid(row=3, column=0, pady=20, padx=30, sticky="ew")
        
        
        self.status_label = CTkLabel(self, text="", text_color="#ff4d4d", font=("Arial", 12))
        self.status_label.grid(row=4, column=0, pady=5)

    def open_game(self):
        try:
            self.host = self.host_entry.get() if self.host_entry.get() else "127.0.0.1"
            self.port = int(self.port_entry.get()) if self.port_entry.get() else 8080
            self.destroy()
        except ValueError:
            self.status_label.configure(text="Порт має бути числом!")
            
    
    def on_closing(self):
        print("Вікно меню закрито. Завершення програми.")
        self.destroy()
        sys.exit()    

if __name__ == "__main__":
    app = ConnectWindow()
    app.mainloop()