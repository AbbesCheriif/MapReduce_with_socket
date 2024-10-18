import tkinter
import customtkinter
import serveur  # Importer server.py pour utiliser la fonction main()

customtkinter.set_appearance_mode("Dark")  # Modes: "System", "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Word Count With Socket Connexion")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Dark mode / Light mode option
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Button to trigger the word count
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Count Words", command=self.start_word_count)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        # Scrollable frame for progress bars
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Word Count Results", height=350)
        self.scrollable_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.progressbars = []

        # Labels to display execution times
        self.execution_time_distributed_label = customtkinter.CTkLabel(self, text="Execution Time (Distributed): N/A")
        self.execution_time_distributed_label.grid(row=1, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")
        
        self.execution_time_local_label = customtkinter.CTkLabel(self, text="Execution Time (Local Only): N/A")
        self.execution_time_local_label.grid(row=2, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def start_word_count(self):
        # Appeler la fonction main() du fichier server.py pour obtenir les résultats et les temps d'exécution
        try:
            word_data, distributed_time, local_time = serveur.main()  # Appel direct à la fonction main() du serveur

            # Clear existing progress bars
            for pb in self.progressbars:
                pb.destroy()

            self.progressbars.clear()

            # Display word counts with progress bars
            for word, count in word_data.items():
                label = customtkinter.CTkLabel(self.scrollable_frame, text=f"{word}: {count}")
                label.grid(padx=10, pady=10, sticky="w")
                progress = customtkinter.CTkProgressBar(self.scrollable_frame)
                progress.set(count / 100)  # Supposons que le count est un pourcentage sur 100
                progress.grid(padx=10, pady=10, sticky="ew")
                self.progressbars.append(progress)

            # Update the execution time labels
            self.execution_time_distributed_label.configure(text=f"Execution Time (Distributed): {distributed_time:.4f} seconds")
            self.execution_time_local_label.configure(text=f"Execution Time (Local Only): {local_time:.4f} seconds")

        except Exception as e:
            print(f"Error while fetching word count: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
