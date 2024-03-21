### IMPORT MODULI ESTERNI

#import dei moduli esterni
#socket --> introdotta per la gestione della connessione socket
#ipaddress --> introdotta per la validazione dell'ip
import socket, ipaddress

### DEFINIZIONE FUNZIONI

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
def scanning_port(ip, min_port, max_port, protocol_in, format):
    for port in range(low_port, high_port + 1):
        #verifica del protocollo richiesto per la creazione dell'istanza socket 
        if(protocol_in == "TCP" or protocol_in == "tcp"):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif(protocol_in == "UDP" or protocol_in == "udp"):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print ("Il protocollo richiesto non è valido!\n")
            return 0
        #iterazione dalla porta minima alla porta massima richiesta
        #esegue la connessione porta per porta
        status = s.connect_ex((ip_target, port))
        #se la connessione è OK stampa OPEN altrimenti CLOSED
        #connect_ex ritorna 0 in caso di successo
        #gli if sulla variabile format servono a verificare il formato di output scelto dall'utente
        if (status == 0):
             if(format == 1 or format == 3):
                print ('Porta ', port, ' ', protocol_in, ' OPEN')
        else:
            if(format == 2 or format == 3):
                print ('Porta ', port, ' ', protocol_in, ' CLOSED')
        #chiusura della connessione
        s.close()

### DICHIARAZIONE VARIABILI E CHECK INPUT UTENTE

#dichiarazione variabili per input utente
ip_target = ""
low_port = -1
high_port = -1
choise_out = 0

#Input IP target con validazione
while True:
    #input dall'utente per la stringa ip_target
    ip_target = str(input("Inserisci l'indirizzo IP del target:\n"))
    #esce dall'iterazione solo se l'ip è valido (call function is_valid_ip definita in precedenza)
    if (is_valid_ip(ip_target)):
        break

#Input Porta min con validazione
while True:
    #medesimo principio dell'input relativo all'ip target
    try:
        low_port = int(input("Inserisci la porta minima (range: 0-65534):\n"))
    except ValueError:
        print("Inserisci una porta valida! \n")
    #esce dall'iterazione solo se viene inserito un intero che rientri nel range UDP
    if(low_port != -1):
        if(0 <= low_port <= 65535):
            break

#Input Porta max con validazione
while True:
    #medesimo principio dell'input relativo agli altri check input
    try:
        high_port = int(input("Inserisci la porta massima (range: 0-65535) maggiore della precedente:\n"))
    except ValueError:
        print("Inserisci una porta valida nel range 0-65535, maggiore della porta minima\n")
    #esce dall'iterazione solo se viene inserito un intero che rientri nel range 
    if(low_port < high_port <= 65535):
        break

#Input scelta output
while True:
    #medesimo principio dell'input relativo agli altri check input
    try:
        choise_out = int(input("Scegli il formato output:\n1- Porte OPEN\n2- Porte CLOSED\n3- Tutte le porte\n"))
    except ValueError:
        print("Inserisci un valore numerico tra 1 e 3!\n")
    #esce dall'iterazione solo se viene inserito un intero che rientri nel range 
    if(choise_out == 1 or choise_out == 2 or choise_out == 3):
        break


### CORPO PRINCIPALE DEL CODICE

print ('Scanning host ', ip_target, ' from port ', low_port, ' to port ', high_port, '\n ')

#chiamata funzione per la scansione sia per porte TCP che per porte UDP
scanning_port(ip_target, low_port, high_port, "TCP", choise_out)
scanning_port(ip_target, low_port, high_port, "UDP", choise_out)
