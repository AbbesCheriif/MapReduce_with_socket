import time
import socket
from collections import Counter

# Le texte à traiter (peut être beaucoup plus long)
text = "fog computing is great for distributed computing fog computing reduces load on cloud distributed computing involves multiple machines"

def divide_text(text):
    words = text.split()
    third_index = len(words) // 3
    two_third_index = 2 * third_index
    return (' '.join(words[:third_index]), 
            ' '.join(words[third_index:two_third_index]), 
            ' '.join(words[two_third_index:]))

def map_word_count(text_chunk):
    words = text_chunk.split()
    return Counter(words)

def send_to_machine(ip, port, text_chunk):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(text_chunk.encode())  # Envoyer le texte
        response = s.recv(4096)  # Recevoir la réponse
    return response.decode()  # Retourner la réponse

def merge_results(*results):
    final_count = Counter()
    for result in results:
        final_count.update(result)
    return final_count

def distributed_version():
    # Diviser le texte en trois parties
    local_text, remote_text_2, remote_text_3 = divide_text(text)
    
    # Mesurer le temps de traitement distribué
    start_time = time.time()

    # Traiter la première partie localement
    local_result = map_word_count(local_text)

    # Envoyer la deuxième partie à Machine 2 et obtenir le résultat
    remote_result_2 = send_to_machine("192.168.1.33", 5001, remote_text_2)
    remote_result_2 = Counter(eval(remote_result_2))

    # Envoyer la troisième partie à Machine 3 et obtenir le résultat
    remote_result_3 = send_to_machine("192.168.1.106", 5001, remote_text_3)
    remote_result_3 = Counter(eval(remote_result_3))

    # Fusionner les résultats des trois parties
    final_result = merge_results(local_result, remote_result_2, remote_result_3)
    
    distributed_time = time.time() - start_time  # Temps total
    return final_result, distributed_time

def local_only_version():
    # Mesurer le temps de traitement local
    start_time = time.time()
    
    # Traiter tout le texte localement
    local_result = map_word_count(text)
    time.sleep(0.2)
    
    local_time = time.time() - start_time  # Temps total
    return local_result, local_time

def main():
    # Exécuter la version distribuée
    distributed_result, distributed_time = distributed_version()
    
    # Exécuter la version locale uniquement
    local_result, local_time = local_only_version()

    # Retourner les résultats de la version distribuée, ainsi que les temps d'exécution
    return distributed_result, distributed_time, local_time
