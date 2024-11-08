import socket 
import threading

HOST = "127.0.0.1" # Lagrar min lokala ip adress i variabeln HOST
PORT = 12345 # Lagrar en port i variabeln PORT

client_list = [] # En lista där alla kopplingar till de anslutande klienterna kommer förvaras


def broadcast_message (message, conn):
    """
    1. Funktion för att skicka ut inkommande data från en klient som ett meddelande till andra klienter.
    2. Vi itererar över vår lista med anslutna klienter (client_list) och skickar ut datan till alla förutom klienten i fråga (conn).

    3. Ett try/except block inleds där vi kodar av datan för att sedan skicka ut meddelandet. 
    4. Ifall det inte går att skicka ut meddelandet till en klient i listan (ifall den t.ex. har kopplat bort sig) så tas klienten bort från listan. 

    Argument:

    message (str): Detta är meddelandet som ska skickas ut 
    conn (socket): Här har vi kopplingen till klienten som skickar ut meddelandet
    
    """
    for client in client_list:
        if client != conn:
            try:
                client.sendall(message.encode("utf-8"))
            except:
                client_list.remove(client)

                    
def new_client(conn,):
    """
    Hanterar en ny anslutande klient och kommunicerar med de andra klienterna via broadcast_message.

    1. Först tas klientens alias emot och avkodas från den gemensamma socketen (conn).
    2. Klientens alias skrivs ut på servern, och alla andra klienter informeras om att denna klient har anslutit.
    3. Den anslutande klienten läggs till i listan `client_list` som håller reda på alla aktiva klienter.

    4. Sedan försöker servern ta emot meddelanden från klienten i en while-loop. Om inget meddelande tas emot (dvs. klienten stänger anslutningen), avslutas loopen via `break`.
    5. När ett meddelande tas emot, skickas det ut till de andra klienterna via `broadcast_message`, och meddelandet skrivs även ut på servern.
    
    6. Om klienten kopplar bort sig eller om ett nätverksfel uppstår (t.ex. `ConnectionResetError`), informeras de andra klienterna om att klienten har lämnat chatten.

    7. I slutet av funktionen, oavsett om ett fel inträffade eller inte, tas klienten bort från `client_list` och anslutningen stängs.
    """
    
    alias = conn.recv(1024).decode("utf-8")
    print (f"{alias} has joined the server!")
    broadcast_message(f"{alias} has joined the server!",conn)

    client_list.append(conn)
    
    try:
        while True:
            message = conn.recv(1024).decode("utf-8")
            if not message:
                break
            broadcast_message(f"{alias}: {message}",conn)
            print (f"{alias}: {message}")
                
    except ConnectionResetError:
        print (f"{alias} has left the chat!")
        broadcast_message(f"{alias} has left the server!",conn)

    finally: 
        client_list.remove(conn)
        conn.close()





with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
    """
    Skapar en tcp socket med IPv4-anslutning som med hjälp av threading hanterar flera anslutande klienter samtidigt.

    1. Vi binder socketen till den lokala IP-adressen (HOST) och en specifik port (PORT) för att lyssna på inkommande anslutningar.
    2. Ett meddelande skrivs ut för att bekräfta anslutningen till den angivna adressen.
    3. Sedan lyssnar vi efter inkommande anrop och skriver ut att detta är pågående.

    4. Anslutande klienter tas emot med sock.accept() och en ny socket (conn) skapas för kommunikation med klienten
    5. För varje anslutande klient så sätts en ny tråd upp med funktionen new_client som hanterar kommunikaitonen med klienten. 
    """

    sock.bind((HOST,PORT))
    print (f"Server is connected to {HOST}:{PORT}")
    sock.listen()
    print ("Server is listening to inbound calls")


    while True:
        conn, addr = sock.accept()
        threading.Thread(target = new_client,args = (conn,), daemon= False).start()







