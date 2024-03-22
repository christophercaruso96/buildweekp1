### IMPORT MODULI ESTERNI

#import della funzione brute_force e is_valid_ip definita nel modulo chipherlib
from cipherlib import is_valid_ip, scanning_port

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
    #esce dall'iterazione solo se l'ip è valido (call function is_valid_ip definita nel modulo chipherlib)
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
        if(0 <= low_port <= 65534):
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
