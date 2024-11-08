import socket
import threading


HOST = "127.0.0.1" # lagrar min lokala ip adress i variabeln HOST
PORT = 12345 # Lagrar en port i variabeln PORT
online = True # En boolean variabeln skapas för att se ifall klienten fortfarande är online.

def recieve_message(sock):
    """
    Funktion för att ta emot meddelanden från andra klienter genom vår server.

    1. Vi tar emot inkommande data för att sedan avkoda och lagra den i variabeln data.
    2. Om det inte finns någon data eller om datan slutar strömma in så avslutas while loopen.
    3. Ifall ett undantag inträffar, t.ex. att anslutningen förloras så fångas det upp i vårt except block och loopen avslutas.
    
    """
    while True:
        try:
            data = sock.recv(1024).decode("utf-8")
            if not data:
                break
            print (data)
        
        except:
            break


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
    """
    Skapar en TCP-socket med IPv4-anslutning som med hjälp av threading hanterar flera klienter samtidigt.

    1. Vi ansluter vår socket till ip adressen och porten som angivits i variablerna HOST och PORT.
    2. Klienten får välja sitt alias och sedan kodas aliaset från utf-8 till bytes och skickas ut.

    3. En tråd skapas med funktionen receive_message och startas. 

    4. En while loop inleds så länge klienten är online. 
    5. Klienten får ange ett meddelande som ska skickas ut. Ifall klienten enbart trycker [ENTER] så avslutas loopen och servern skriver ut det.
  
    """
    sock.connect((HOST,PORT))

    alias = input("Vad heter du? ")
    sock.sendall(alias.encode("utf-8"))

    recieve_thread = threading.Thread(target= recieve_message, args= (sock,), daemon= True  )
    recieve_thread.start()

    while online:
        message = input("")
        if message == "":
            online = False
            print ("You have logged off")
            break

        sock.sendall(message.encode("utf-8"))