import tkinter as tk
from tkinter import *
import socket
import threading
import time



utenti = []
class GUI:
    client_socket = None
    last_received_message = None

    def __init__(self,master):
        self.initialize_socket()
        self.listen_for_incoming_messages_in_a_thread()
        self.start()

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = '93.36.215.16'
        remote_port = 6969
        self.client_socket.connect((remote_ip, remote_port))

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
        thread.start()
    
    def comandologin(self):
        global fhome
        self.entry_calciatore.tkraise() 
        self.button_calciatore.tkraise()
        self.fintro = tk.Label(root, bg="#1b5e16")
        self.fintro.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        scroll = Scrollbar(root)
        #self.fhome = Listbox(root, bg="black", fg="white", font=("Abadi", 12) ,yscrollcommand=scroll.set)
        #self.fhome.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        #self.entry_username = tk.Entry(root, font = ("Abadi", 12))
        #self.entry_username.place(relwidth= 0.3, relheight = 0.06, relx = 0.22, rely = 0.55)
        #self.entry_username.tkraise()
        
        userusername = self.entry_username.get()
        if len(userusername) != 0:
            auserusername = userusername
            self.fhome.tkraise()
            label_user = Label(root)
            label_user.config(font=("Harlow Solid Italic", 22, 'bold'), bg="#fffd91", fg="#1b5e16")
            label_user["text"] = ("Benvenuto " + auserusername)
            label_user.place(relwidth=0.65, relheight=0.1, relx = 0.05, rely = 0.72)
            #aauserusername =  "--".join(auserusername)
            aauserusername = auserusername.replace(" ", "***")
            data =  ("Joined: " + aauserusername ).encode('utf-8')
            self.client_socket.send(data)
            athread = threading.Thread(target=self.waitandraise)
            athread.start()
            #time.sleep(4) 
            #in a new thread, then 
            #self.entry_calciatore.tkraise() 
            #self.button_calciatore.tkraise()

    def waitandraise(self):
        time.sleep(5)
        self.entry_calciatore.tkraise() 
        self.button_calciatore.tkraise()
        #self.label_intro.config(text = "Inizia solo dopo che si sono collegati tutti i giocatori")
        self.label_intro.tkraise() 
        time.sleep(5)
        self.fhome.tkraise()
            
            


    def comandohome(self):
        self.fhome.tkraise() 
        self.entry_calciatore.tkraise() 
        self.button_calciatore.tkraise()

            
    def comando_calciatore(self):
        global typed
        global calciatore_offerto
        calciatore_offerto = self.entry_calciatore.get()
        if len(calciatore_offerto) != 0:
            calciatore_offerto1 = calciatore_offerto.replace(" ", "***")
            nomenome = self.entry_username.get()
            nomenome = nomenome.replace(" ", "***")
            message = ("nome_calciatore " + nomenome + " " + calciatore_offerto1).encode('utf-8')
            self.client_socket.send(message)

            

        ##### send calciatore_offerto, entry.config(state='disabled'), global calciatoreofferto------- quando ricevo messaggio venduto raise label calciatore

        
        
        
    def enterKey(self, so): ###MANDA MESSAGGIO###
        global typed
        typed = self.entry.get()                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        if len(typed) != 0:
            
            #self.manda_messaggio()
            #self.fhome.insert(END, typed)MANDA MESSAGGIO
            senders_name = self.entry_username.get()
            senders_name = senders_name.replace(" ", "***") + ": "
            #senders_name = self.entry_username.get().strip() + ": "
            #senders_name = senders_name.replace(" ", "***")
            #data = self.entry.get(1.0, 'end').strip()
            #print(typed)
            data = typed.strip()
            #print(data)
            message = ("offerta " + senders_name + data).encode('utf-8')
            #self.fhome.insert('end', message.decode('utf-8') + '\n')
            self.fhome.yview(END)
            self.client_socket.send(("offerta " + senders_name + data).encode('utf-8'))
            #self.entry.delete(1.0, 'end')
            #return 'break'
            self.fhome.see(tk.END)
            self.entry.delete(0, 'end')


            

    #def manda_messaggio(self, so):
        #senders_name = self.entry_username.get().strip() + ": "
        #data = typed.strip()
        #message = ("offerta " + senders_name + data).encode('utf-8')
        #self.fhome.yview(END)
        #self.client_socket.send(("offerta " + senders_name + data).encode('utf-8'))
        #self.fhome.see(tk.END)
        #self.entry.delete(0, 'end')

        

    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')
            print(message)
            # self.fhome.insert('end', message + '\n')
            # self.fhome.yview(END)
            if message[0:6] == str("Joined"):
                user = message.replace("***", " ")
                print(user)
                print(message)
                #message = user + " has joined"
                self.fhome.insert('end', user + '\n')
                self.fhome.yview(END)

            if message [0:6] == str("pnizio"):
                print("skrrrrrrskr")
                message = message[7:]
                self.fhome.insert('end', message + '\n')
                self.fhome.yview(END)
                self.button_calciatore.config(state='normal')
                self.entry_calciatore.config(state='normal')
                self.entry['state'] = 'disabled'
                self.label_calciatore['text'] = " "
                print("skrrrrrrskr")

            if message [0:6] == str("inizio"):
                message = message[7:]
                print(message.strip())
                message = message.replace("***", " ")
                self.fhome.insert('end', message + '\n')
                self.fhome.yview(END)
                self.entry.config(state = 'normal')
                self.button_calciatore.config(state='disabled')
                self.entry_calciatore.delete(0, 'end')
                self.entry_calciatore.config(state='disabled')


                
            #if message [0:6] == str("inizio"):
                #print("skrrrrrrskr")
                #message = message[7:]
                #self.fhome.insert('end', message + '\n')
                #self.fhome.yview(END)
                #self.button_calciatore.config(state='normal')
                #self.entry_calciatore.config(state='normal')
                #self.entry['state'] = 'disabled'
                #self.label_calciatore['text'] = none 
                #print("skrrrrrrskr")
                

            if  message[0:7] == str("offerta"):
                message = message[8:]
                message = message.replace ("***", " ")
                self.fhome.insert('end', message + '\n')
                self.fhome.yview(END)

            if message [0:15] == str("nome_calciatore"):
                print("aoao")
                message = (message[16:])
                player_offre = message.split()[0]
                player_offre = player_offre.replace("***", " ")
                nomecalciatore = message.split()[1]
                nomecalciatore = nomecalciatore.replace("***", " ")
                self.label_calciatore.config(text = nomecalciatore)
                




                #self.label_calciatore.tkraise()


            if message [0:13] == str("Il calciatore"):
                print("aooooooooao")
                totale = 0
                self.fhome.yview(END)
                calciatore_offerto = message.split()[2]
                prezzo = message.split()[7]
                calciatore_offerto = str(calciatore_offerto.replace("***", " "))
                print(calciatore_offerto)
                offerente = message.split()[9]
                offerente = str(offerente.replace("***", " "))
                offerente = (offerente[:-1])
                print(offerente)
                message = message.replace("***", " ")
                self.fhome.insert('end', message + '\n')

                
                #self.entry_calciatore.config(state='normal')
                #self.button_calciatore.config(state='normal')
                #self.entry_calciatore.delete(0, 'end')
                #self.label_calciatore.config(text = " ")
                #self.entry.config(state = 'disabled')

                if offerente == player1:
                    for i in range(3):
                        self.f1.delete('end')
                    self.f1.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f1.insert(END, "-----------------------")
                    self.f1.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f1.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player2:
                    for i in range(3):
                        self.f2.delete('end')
                    self.f2.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f2.insert(END, "-----------------------")
                    self.f2.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f2.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player3:
                    for i in range(3):
                        self.f3.delete('end')
                    self.f3.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale
                    self.f3.insert(END, "-----------------------")
                    self.f3.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f3.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player4:
                    for i in range(3):
                        self.f4.delete('end')
                    self.f4.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f4.insert(END, "-----------------------")
                    self.f4.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f4.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player5:
                    for i in range(3):
                        self.f5.delete('end')
                    self.f5.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f5.insert(END, "-----------------------")
                    self.f5.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f5.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player6:
                    for i in range(3):
                        self.f6.delete('end')
                    self.f6.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f6.insert(END, "-----------------------")
                    self.f6.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f6.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player7:
                    for i in range(3):
                        self.f7.delete('end')
                    self.f7.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f7.insert(END, "-----------------------")
                    self.f7.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f7.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player8:
                    for i in range(3):
                        self.f8.delete('end')
                    self.f8.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f8.insert(END, "-----------------------")
                    self.f8.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f8.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player9:
                    for i in range(3):
                        self.f9.delete('end')
                    self.f9.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f9.insert(END, "-----------------------")
                    self.f9.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f9.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                if offerente == player10:
                    for i in range(3):
                        self.f10.delete('end')
                    self.f10.insert(END, calciatore_offerto + "  " + prezzo)
                    #prezzo = int(message.split()[7])
                    totale = totale + int(prezzo)
                    rimanenti = 350 - totale 
                    self.f10.insert(END, "-----------------------")
                    self.f10.insert(END, "Totale speso:" + "    " + str(totale))
                    self.f10.insert(END, "Crediti rimanenti:" + "    " + str(rimanenti))
                offerente = " "
                


            if message[2:13] == "listautenti":
                message = message.split()
     
                player1 = str(message[1])
                player1 = player1.replace("***", " ")
                player1 = player1[2:-3] 
                self.openPlayer1.config(text = player1)
                player2 = str(message[2])
                player2 = player2.replace("***", " ")
                player2 = player2[2:-3]
                self.openPlayer2.config(text = player2)
                player3 = str(message[3])
                player3 = player3.replace("***", " ")
                player3 = player3[2:-3]
                self.openPlayer3.config(text = player3)
                player4 = str(message[4])
                player4 = player4.replace("***", " ")
                player4 = player4[2:-3]
                self.openPlayer4.config(text = player4)
                player5 = str(message[5])
                player5 = player5.replace("***", " ")
                player5 = player5[2:-3]
                self.openPlayer5.config(text = player5)
                player6 = str(message[6])
                player6 = player6.replace("***", " ")
                player6 = player6[2:-3]
                self.openPlayer6.config(text = player6)
                player7 = str(message[7])
                player7 = player7.replace("***", " ")
                player7 = player7[2:-3]
                self.openPlayer7.config(text = player7)
                player8 = str(message[8])
                player8 = player8.replace("***", " ")
                player8 = player8[2:-3]
                self.openPlayer8.config(text = player8)
                player9 = str(message[9])
                player9 = player9.replace("***", " ")
                player9 = player9[2:-3]
                self.openPlayer9.config(text = player9)
                player10 = str(message[10])
                player10 = player10.replace("***", " ")
                player10 = player10[2:-3]
                self.openPlayer10.config(text = player10)


            #else:
                #print(message[2:13])
                #message = message.split(" ")
                #message = str(" ".join(message[1:]))
                #self.fhome.insert('end', message[8:] + '\n')
                #self.fhome.yview(END)

        so.close()

    def start(self):
        root.title("FANTASTA")
        root.configure(background='#263D42')
        canvas = tk.Canvas(root, height=600, width=700, bg="#263D42")
        canvas.pack()
        scroll = Scrollbar(root)

        global fhome
        self.fhome = Listbox(root, bg="black", fg="white", font=("Abadi", 12) ,yscrollcommand=scroll.set)
        ##fhome.config(font=("Bauhaus 93")
        self.fhome.place(relwidth=0.65, relheight=0.70, relx=0.05, rely=0.05)
  
        
        #self.label_calciatore = Label(root, bg="black", fg = "white", font=("Abadi", 15))
        #self.label_calciatore.place(relwidth= 0.9, relheight = 0.07, relx = 0.25, rely = 0.75)

        f0 = Frame(root, bg="#263D42")
        f0.place(relwidth=1, relheight=1, relx=0.0, rely=0.0)
        self.label_intro = Label(root, fg = "#263D42", bg="#fffd91", font=("Britannic Bold", 12), text = "INIZIA SOLO DOPO CHE SI SONO COLLEGATI TUTTI I GIOCATORI")
        self.label_intro.place(relwidth=0.65, relheight=0.02, relx = 0.05, rely = 0.725)


        self.f1 = Listbox(root, bg="red", fg="white", font=("Abadi", 15))
        self.f1.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f1.insert(END, "-----------------------")
        self.f1.insert(END, "Totale speso:" + "    ")
        self.f1.insert(END, "Crediti rimanenti: 350")

        self.f2 = Listbox(root, bg="blue", fg="white", font=("Abadi", 15))
        self.f2.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f2.insert(END, "-----------------------")
        self.f2.insert(END, "Totale speso:" + "    ")
        self.f2.insert(END, "Crediti rimanenti: 350")

        self.f3 = Listbox(root, bg="yellow", fg="white", font=("Abadi", 15))
        self.f3.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f3.insert(END, "-----------------------")
        self.f3.insert(END, "Totale speso:" + "    ")
        self.f3.insert(END, "Crediti rimanenti: 350")

        self.f4 = Listbox(root, bg="gray", fg="white", font=("Abadi", 15))
        self.f4.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f4.insert(END, "-----------------------")
        self.f4.insert(END, "Totale speso:" + "    ")
        self.f4.insert(END, "Crediti rimanenti: 350")

        self.f5 = Listbox(root, bg="black", fg="white", font=("Abadi", 15))
        self.f5.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f5.insert(END, "-----------------------")
        self.f5.insert(END, "Totale speso:" + "    ")
        self.f5.insert(END, "Crediti rimanenti: 350")

        self.f6 = Listbox(root, bg="red", fg="white", font=("Abadi", 15))
        self.f6.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f6.insert(END, "-----------------------")
        self.f6.insert(END, "Totale speso:" + "    ")
        self.f6.insert(END, "Crediti rimanenti: 350")

        self.f7 = Listbox(root, bg="blue", fg="white", font=("Abadi", 15))
        self.f7.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f7.insert(END, "-----------------------")
        self.f7.insert(END, "Totale speso:" + "    ")
        self.f7.insert(END, "Crediti rimanenti: 350")

        self.f8 = Listbox(root, bg="green", fg="white", font=("Abadi", 15))
        self.f8.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f8.insert(END, "-----------------------")
        self.f8.insert(END, "Totale speso:" + "    ")
        self.f8.insert(END, "Crediti rimanenti: 350")

        self.f9 = Listbox(root, bg="yellow", fg="white", font=("Abadi", 15))
        self.f9.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f9.insert(END, "-----------------------")
        self.f9.insert(END, "Totale speso:" + "    ")
        self.f9.insert(END, "Crediti rimanenti: 350")

        self.f10 = Listbox(root, bg="gray", fg="white", font=("Abadi", 15))
        self.f10.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)
        self.f10.insert(END, "-----------------------")
        self.f10.insert(END, "Totale speso:" + "    ")
        self.f10.insert(END, "Crediti rimanenti: 350")

        self.entry_calciatore = tk.Entry(root, font = ("Abadi", 12), bg="black", fg = "white", disabledforeground="white", disabledbackground="black")
        self.entry_calciatore.place(relwidth= 0.45, relheight = 0.07, relx = 0.25, rely = 0.75)

        self.button_calciatore = tk.Button(root, text="SUBMIT",font =("Bauhaus 93", 17, ), padx=100, pady=10, fg="#fffd91", bg="black", command = self.comando_calciatore)
        self.button_calciatore.place(relwidth=0.20, relheight=0.07, relx = 0.05, rely = 0.75)

        ##backround_image = tk.PhotoImage(file='png1.gif')
        ##fintro = tk.Label(root, image=backround_image)
        fintro = tk.Label(root, bg="#1b5e16")
        fintro.place(relwidth=0.65, relheight=0.77, relx=0.05, rely=0.05)


        self.openPlayer1 = tk.Button(root, text="Player 1", font =("Bauhaus 93", 14, ), padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f1.tkraise())        
        self.openPlayer1.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.05)

        self.openPlayer2 = tk.Button(root, text="Player 2", font =("Bauhaus 93", 14, ),padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f2.tkraise())
        self.openPlayer2.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.13)

        self.openPlayer3 = tk.Button(root, text="Player 3",font =("Bauhaus 93", 14, ),padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f3.tkraise())
        self.openPlayer3.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.21)

        self.openPlayer4 = tk.Button(root, text="Player 4", font =("Bauhaus 93", 14, ),padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f4.tkraise())
        self.openPlayer4.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.29)

        self.openPlayer5 = tk.Button(root, text="Player 5", font =("Bauhaus 93", 14, ), padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f5.tkraise())
        self.openPlayer5.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.37)

        self.openPlayer6 = tk.Button(root, text="Player 6",font =("Bauhaus 93", 14, ),padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f6.tkraise())
        self.openPlayer6.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.45)

        self.openPlayer7 = tk.Button(root, text="Player 7", font =("Bauhaus 93", 14), padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f7.tkraise())
        self.openPlayer7.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.53)

        self.openPlayer8 = tk.Button(root, text="Player 8",font =("Bauhaus 93", 14, ), padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f8.tkraise())
        self.openPlayer8.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.61)

        self.openPlayer9 = tk.Button(root, text="Player 9", font =("Bauhaus 93", 14, ), padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f9.tkraise())
        self.openPlayer9.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.69)

        self.openPlayer10 = tk.Button(root, text="Player 10", font =("Bauhaus 93", 14, ), padx=100, pady=10, fg="#1b5e16", bg="#fffd91", command=lambda:self.f10.tkraise())
        self.openPlayer10.place(relwidth=0.18, relheight=0.05, relx = 0.765, rely = 0.77)

        self.openHome = tk.Button(root, text="HOME", font =("TINspireKeysTouch", 20, 'bold'), pady=10, fg="#1b5e16", bg='#fffd91', command=self.comandohome)
        self.openHome.place(relwidth=0.18, relheight=0.06, relx = 0.765, rely = 0.85)

        self.entry = tk.Entry(root, font = ("Abadi", 12), bg="black", fg="white")
        self.entry.place(relwidth= 0.45, relheight = 0.06, relx = 0.25, rely = 0.85)
        self.entry.bind("<Return>", self.enterKey)

        self.entry_username = tk.Entry(root, font = ("Abadi", 12))
        self.entry_username.place(relwidth= 0.3, relheight = 0.06, relx = 0.22, rely = 0.55)



        

        self.button_username = tk.Button(fintro, text="Inserisci nome utente", padx=100, pady=10, font=("Bauhaus 93", 14), fg="#1b5e16", bg="#fffd91", command = self.comandologin )
        ##button_username.config(font="Bauhaus 93")
        self.button_username.place(relwidth=0.43, relheight=0.07, relx = 0.28, rely = 0.79)

        self.label_calciatore = Label(root, bg="black", fg = "white", font=("Abadi", 15))
        self.label_calciatore.place(relwidth= 0.20, relheight = 0.06, relx = 0.05, rely = 0.85)
        





if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.mainloop()
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
