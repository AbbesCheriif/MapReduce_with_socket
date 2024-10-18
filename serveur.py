import socket
from collections import Counter

# Le texte à traiter (peut être beaucoup plus long)
text = "fog computing is great for distributed computing fog computing reduces load on cloud distributed computing involves multiple machines"

# Diviser le texte en trois parties
def divide_text(text):
    words = text.split()
    third_index = len(words) // 3
    two_third_index = 2 * third_index
    return (' '.join(words[:third_index]), 
            ' '.join(words[third_index:two_third_index]), 
            ' '.join(words[two_third_index:]))

# Fonction map pour compter les mots dans une partie du texte
def map_word_count(text_chunk):
    words = text_chunk.split()
    return Counter(words)

# Envoyer une partie du texte à une autre machine via socket
def send_to_machine(ip, port, text_chunk):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(text_chunk.encode())  # Envoyer le texte
        response = s.recv(4096)  # Recevoir la réponse
    return response.decode()  # Retourner la réponse

# Fusionner les résultats des trois parties
def merge_results(*results):
    final_count = Counter()
    for result in results:
        final_count.update(result)
    return final_count

# Diviser le texte en trois parties
local_text, remote_text_2, remote_text_3 = divide_text(text)

# Traiter la première partie localement
local_result = map_word_count(local_text)

# Envoyer la deuxième partie à Machine 2 et obtenir le résultat
remote_result_2 = send_to_machine("10.25.12.21", 5001, remote_text_2)  # Remplacez par l'IP de Machine 2
remote_result_2 = Counter(eval(remote_result_2))  # Convertir la réponse en Counter

# Envoyer la troisième partie à Machine 3 et obtenir le résultat
remote_result_3 = send_to_machine("10.25.14.179", 5002, remote_text_3)  # Remplacez par l'IP de Machine 3
remote_result_3 = Counter(eval(remote_result_3))  # Convertir la réponse en Counter

# Fusionner les résultats des trois parties
final_result = merge_results(local_result, remote_result_2, remote_result_3)
print(final_result)
