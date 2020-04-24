import socket
import threading
import time

offertattuale = int(1)
start = time.time()+10000000
listautenti = ["listautenti"]
numeropartecipanti = 1 + 10

class ChatServer:
    clients_list = []
    offertattuale = int(0)

    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        self.create_listening_server()

    def create_listening_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_ip = '192.168.1.116'
        local_port = 6969
        # this will allow you to immediately restart a TCP server
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind(('192.168.1.116', 6969))
        print("Listening for incoming messages..")
        self.server_socket.listen(5)
        self.receive_messages_in_a_new_thread()

    def receive_messages(self, so):
        global offertattuale
        global start
        global end
        global offerente
        while True:
            #print("end-start: " + str(end-start))
            incoming_buffer = so.recv(512)

            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode('utf-8')
            print(self.last_received_message)
            print(self.last_received_message[0:14])

            if self.last_received_message[0:7] == str("offerta"):
                global offertattuale
                global offerente
                global calciatore
                end = time.time()

                nuovaofferta = str(self.last_received_message.split()[2])
                print(nuovaofferta)
                offerente = " "
                offerente = self.last_received_message.split()[1]
                nuovaofferta = int(nuovaofferta)
                print(nuovaofferta)
                print(end-start)
                while end - start < 5:
                    if nuovaofferta > offertattuale:
                        offertattuale = nuovaofferta
                        start = time.time()
                        self.broadcast_to_all_clients(so)
                        print("OK")
                        break
                    else:
                        self.broadcast_to_one_client(so)
                        print("prrrr")
                        break
                else:

                    self.calciatore_venduto(so)
                    #offerente = ("")
                    #offertattuale = 1
                    #calciatore = ("")
                    start = time.time()+ 100000

            if self.last_received_message[0:6] == str("Joined"):
                listautenti.append(self.last_received_message.split()[1:])
                print("skrskr")
                self.broadcast_to_all_clients(so)
                if len(listautenti) == numeropartecipanti:
                    for client in self.clients_list:
                        socket, (ip, port) = client
                        #stringautenti = "--".join(str(listautenti))
                        #stringautenti = "listautenti" + listautenti
                        #socket.sendall(listautenti.encode('utf-8'))
                        stringautenti = str(listautenti)
                        socket.sendall(stringautenti.encode('utf-8'))

            if self.last_received_message[0:15] == str("nome_calciatore"):
                global nomecalciatore
                global player_offre
                player_offre = self.last_received_message.split()[1]
                print(player_offre)
                nomecalciatore = self.last_received_message.split()[2]
                print(nomecalciatore)
                self.inizio_asta(so)
                print("aoao")

                # utenteuno =
            #else:
            #    self.broadcast_to_all_clients(so)
            #    print("aooooo")
            #print(self.last_received_message.split()[1])
            #self.broadcast_to_all_clients(so)  # send to all clients

        so.close()

    def inizio_asta(self, senders_socket):
        global start
        for client in self.clients_list:
            socket, (ip, port) = client
            socket.sendall(self.last_received_message.encode('utf-8'))
            mess = f"inizio L'asta per {nomecalciatore} è iniziata"
            socket.sendall(mess.encode('utf-8'))
            time.sleep(1)
            #mes = ""
            mess1 = f"offerta {player_offre}: 1 "
            socket.sendall(mess1.encode('utf-8'))
            #mess1 = ""
            start = time.time()

    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            socket.sendall(self.last_received_message.encode('utf-8'))

    def broadcast_to_one_client(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is senders_socket:
                mess = f"offerta Offerta non valida, l'offerta attuale è: {offertattuale}"
                socket.sendall(mess.encode('utf-8'))
                break

    def calciatore_venduto(self,senders_socket):
        global nomecalciatore
        global offertattuale
        global offertavinciente
        global offertavincente
        global offerente
        for client in self.clients_list:
            socket, (ip, port) = client
            calciatorio_vendutio  = "Il calciatore " + str(nomecalciatore) + " è stato venduto per " + str(offertattuale) + " a " + str(offerente)
            socket.sendall(calciatorio_vendutio.encode('utf-8'))
            #nomecalciatore = ""
            #offerente = " "
            #calciatorio_vendutio = " "
            time.sleep(1)

            for i in range(numeropartecipanti):
                if i !=0:
                    #chiamatore = f"pnizio tocca a {str(listautenti[i])[2:-2]} chiamare il prossimo calciatore"
                    aaa = str(listautenti[i])[2:-2]
                    aaaa = user = aaa.replace("***", " ")
                    chiamatore = f"pnizio tocca a {aaaa} chiamare il prossimo calciatore"
                    socket.sendall(chiamatore.encode('utf-8'))
                    i = i+1
                    break

        offertattuale = 1




    def broadcast_stickers(self,senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            stringautenti = "--".join(listautenti)

            socket.sendall(stringautenti.encode('utf-8'))
            print(stringautenti)




    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(client)
            print('Connected to ', ip, ':', str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)



if __name__ == "__main__":
    ChatServer()


