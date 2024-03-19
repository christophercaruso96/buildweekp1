#import dei moduli esterni
#socket --> introdotta per la gestione della connessione socket
#ipaddress --> introdotta per la validazione dell'ip
import socket, ipaddress

#funzione per la validazione dell'indirizzo ip inserito
def is_valid_ip(ip_address):
    #se l'ip è valido ritorna True
    try:
        #ip_address riceve in input la stringa dell'ip e se non è valido genera una eccezione
        ipaddress.ip_address(ip_address)
        return True
    #se entra in exception restituisce false
    except ValueError:
        #chiedo all'utenet di inserire un IP valido
        print("Inserisci una stringa con indirizzo IP valido (e.g. 192.168.1.6) \n")
        return False
    
#funzione per la scansione multiporta su un target specifico
def scanning_port(ip, min_port, max_port, protocol):
    #verifica del protocollo richiesto per la creazione dell'istanza socket 
    if(protocol == "TCP" or protocol == "tcp"):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif(protocol == "UDP" or protocol == "udp"):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        print ("Il protocollo richiesto non è valido!\n")
    #iterazione dalla porta minima alla porta massima richiesta
    for port in range(low_port, high_port + 1):
        #esegue la connessione porta per porta
        status = s.connect_ex((ip_target, port))
        #se la connessione è OK stampa OPEN altrimenti CLOSED
        #connect_ex ritorna 0 in caso di successo
        if (status == 0):
             print ('Porta ', port, ' ', protocol, ' OPEN')
        else:
            print ('Porta ', port, ' ', protocol, ' CLOSED')
    #chiusura della connessione
    s.close()


#Input IP target con validazione
while True:
    #input dall'utente per la stringa ip_target
    ip_target = str(input("Inserisci l'indirizzo IP del target:\n"))
    #esce dall'iterazione solo se l'ip è valido (call function is_valid_ip definita in precedenza)
    if (is_valid_ip(ip_target)):
        break

print ("Inserisci il range di porte da scansionare (0-65535) \n")

#Input porte con validazione
while True:
    #medesimo principio dell'input relativo all'ip target
    try:
        low_port = int(input("Inserisci la porta minima (range: 0-65535) del target:\n"))
    except ValueError:
        print("Inserisci una porta valida nel range 0-65535 \n")
    #esce dall'iterazione solo se viene inserito un intero che rientri nel range 
    if(0 <= low_port <= 65535):
        break

while True:
    #medesimo principio dell'input relativo all'ip target
    try:
        high_port = int(input("Inserisci la porta massima (range: 0-65535) maggiore della precedente:\n"))
    except ValueError:
        print("Inserisci una porta valida nel range 0-65535, maggiore della porta minima\n")
    #esce dall'iterazione solo se viene inserito un intero che rientri nel range 
    if(low_port < high_port <= 65535):
        break

print ('Scanning host ', ip_target, ' from port ', low_port, ' to port ', high_port, '\n ')

#chiamata funzione per la scansione sia per porte TCP che per porte UDP
scanning_port(ip_target, low_port, high_port, "TCP")
scanning_port(ip_target, low_port, high_port, "UDP")

#EVENTUALE MODIFICA:
#chiedere all'utente il formato output
#1 - solo porte OPEN, 2 - solo porte CLOSED, 3 - entrambe  
