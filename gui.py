from logic import *
import customtkinter as CTk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import time


class Graph_frame(CTk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.graphic = CTk.CTkFrame(self)
        self.graphic.pack(expand=True, fill=BOTH)


    def draw(self, G, curveEdges, straightEdges, edge_colors1, edge_colors2, edge_labels):

        for widget in self.graphic.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(4, 4), dpi=115)
        pos = nx.circular_layout(G)

        nx.draw(G, pos, with_labels=True, node_size=1000, node_color="white", 
                edgecolors='black', font_size=12, font_weight="bold", width=0, arrowsize=0.01, ax=ax)
        nx.draw_networkx_edges(G, pos,edgelist=curveEdges, connectionstyle="arc3,rad=0.15",
                               edge_color=edge_colors1, arrowsize=13, node_size=1000, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=straightEdges, edge_color=edge_colors2, 
                               width=1, arrowsize=13, node_size=1000, ax=ax)

        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v):edge_labels[(u,v)] for (u,v) in curveEdges}, 
                                     connectionstyle="arc3,rad=0.16", ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v):edge_labels[(u,v)] for (u,v) in straightEdges}, 
                                     connectionstyle="arc3", ax=ax)

        canvas = FigureCanvasTkAgg(fig, master=self.graphic)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


class Input_View(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.flag = 0

        self.frame_1 = CTk.CTkFrame(self, height=20)
        self.frame_1.pack(padx = 4, pady = 12, ipadx = 8, ipady = 10, side = TOP)

        self.open_button = CTk.CTkButton(self.frame_1, text="Get the code from file", font=("Arial", 16), command=self.open_file)
        self.open_button.grid(row = 0, stick='w', columnspan=2, padx=100, pady=10)

        self.label = CTk.CTkLabel(self.frame_1, text="Enter the code:", font=("Arial", 16), )
        self.label.grid(row = 1, column = 0, stick = 'w', padx=10, pady=10)


        self.entry = CTk.CTkEntry(self.frame_1, width=230)
        self.entry.grid(row = 1, column = 1, padx = 5,stick = 'w', pady = 10)
        
        self.clear_button = CTk.CTkButton(self.frame_1, height=20, width=20, text='X', 
                                          fg_color="#4B5945", hover_color="#66785F", command=self.clear_text)
        self.clear_button.grid(row = 1, column = 3, stick = 'e')


        self.button = CTk.CTkButton(self.frame_1, text="Start", font=("Arial", 16), command=lambda: self.start(master))
        self.button.grid(row = 2, columnspan=2, padx=10, pady=5)

        self.frame_2 = CTk.CTkFrame(self)
        self.frame_2.pack(padx = 4, pady = 4, fill='both', side=TOP, expand=True)

        self.frames = CTk.CTkFrame(self.frame_2, height=60,)
        self.frames.pack(padx = 4, pady = 4, fill='x', side=TOP)

        self.labels = CTk.CTkLabel(self.frames, text="Полученное множество S:", font=("Arial", 15))
        self.labels.place(relx=0.01, rely=0.01)

        self.framesol = CTk.CTkFrame(self.frame_2, height=60,)
        self.framesol.pack(padx=4, pady=4, fill='x', side=TOP)

        self.labelsol = CTk.CTkLabel(self.framesol, text="Решение о взаимной однозначности кода:", font=("Arial", 15))
        self.labelsol.place(relx=0.01, rely=0.01)

        self.framew = CTk.CTkFrame(self.frame_2, height=60, fg_color="transparent")
        self.framew.pack(padx=4, pady=4, fill='x', side=TOP)



    def start(self, master):
        # if self.flag == 0:
        #     V = self.entry.get()
        # else:
        #     V = self.content

        V = self.entry.get()

        start_time = time.perf_counter()
        G, fl, Sl, cE, sE, ec1, ec2, el, w = markov_alg(V)
        end_time = time.perf_counter()
        print(f"Execution time: {end_time - start_time:.6f} seconds")

        textt = None
        colour = None
        if fl == 1:
            textt="Код является взаимно-однозначным."
            colour="#4E6C50"
        else:
            textt="Код не является взаимно-однозначным."
            colour="#EA5455"

        if (len(self.framesol.winfo_children())>1):

            self.framesol.winfo_children()[1].destroy()
            self.frames.winfo_children()[1].destroy()
                
        self.labels2 = CTk.CTkLabel (self.frames, 
                                     text="S = {" + ", ".join(Sl) + "}", font=("Arial", 16), fg_color="transparent")
        self.labels2.place(relx=0.01, rely=0.5)

        self.labelsol2 = CTk.CTkLabel (self.framesol, 
                                       text=textt, font=("Arial", 16), fg_color=colour, corner_radius=5)
        self.labelsol2.place(relx=0.01, rely=0.5)

        
        if fl == 0:
            for widget in self.framew.winfo_children():
                widget.destroy()

            self.framew.configure(fg_color="#2B2B2B")

            self.labelw = CTk.CTkLabel(self.framew, 
                                       text="Слово, допускающее две расшифровки:", font=("Arial", 15))
            self.labelw.place(relx=0.01, rely=0.01)

            self.labelw2 = CTk.CTkLabel (self.framew, text=w, font=("Arial", 16))
            self.labelw2.place(relx=0.01, rely=0.5)

        else:
            for widget in self.framew.winfo_children():
                widget.destroy()
            self.framew.configure(fg_color="transparent")

        
        
        # self.graphic.draw(G, cE, sE, ec1, ec2, el)
        self.flag = 0
        self.entry.insert(0, "")


    def open_file(self):
   
        self.file_path = filedialog.askopenfilename(
            title="Выберите файл", 
            filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*"))
        )
    
        if self.file_path: 
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
                # self.content = self.content[:-1]
                self.flag = 1
                self.entry.delete(0, CTk.END)
                self.entry.insert(0, self.content)
        
        print(self.content)
                

    def clear_text(self):
        self.entry.delete(0, CTk.END)




class App(CTk.CTk):

    def __init__(self):
        super().__init__()
        CTk.set_appearance_mode("system")

        self.geometry("980x549+200+150")
        self.title("Алгоритм Маркова распознавания взаимной однозначности алфавитного кодирования")

        self.input_frame = Input_View(master=self)
        self.input_frame.place(relx = 0.005, rely =0.005, relwidth = 0.41, relheight = 0.99)


        self.graph_frame = Graph_frame(master=self)
        self.graph_frame.place(relx = 0.415, rely = 0.005, relwidth=0.58, relheigh = 0.99)

        self.input_frame.graphic = self.graph_frame
        

