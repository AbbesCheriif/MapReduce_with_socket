import socket
from collections import Counter

# Fonction map pour compter les mots dans une partie du texte
def map_word_count(text_chunk):
    words = text_chunk.split()
    return Counter(words)

# Configurer le serveur
host = '0.0.0.0'  # Écouter sur toutes les interfaces
port = 5001  # Port à utiliser

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Serveur en écoute sur le port {port}...")
   
    while True:
        client_socket, addr = server_socket.accept()
        with client_socket:
            print(f"Connexion acceptée de {addr}")
            data = client_socket.recv(4096).decode()  # Recevoir les données
            print(f"Texte reçu: {data}")
            result = map_word_count(data)  # Compter les mots
            client_socket.sendall(str(result).encode())  # Envoyer le résultat au client