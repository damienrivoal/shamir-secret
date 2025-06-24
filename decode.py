from Crypto.Protocol.SecretSharing import Shamir
import hashlib

try:
    from prompt_toolkit import prompt
except ImportError:
    print("Erreur : prompt_toolkit n'est pas installé. Installez-le avec 'pip install prompt_toolkit'.")
    exit(1)

# Paramètres
n = 5  # nombre total de parts générées à l'encodage
k = 3  # seuil minimal pour la reconstruction

# Saisie des parts fusionnées de k participants (hash + data)
indices = []
all_fusions = []
for i in range(k):
    previous = ""
    while True:
        if previous:
            part_hex = prompt(f"Saisir une portion du secret (édition possible, Entrée pour valider) : ", default=previous).strip()
        else:
            part_hex = prompt(f"Saisir une portion du secret (édition possible, Entrée pour valider) : ").strip()
        if not part_hex and previous:
            part_hex = previous
        else:
            previous = part_hex
        try:
            part_bytes = bytes.fromhex(part_hex)
        except Exception:
            print("Format hexadécimal invalide. Veuillez vérifier et ressaisir :")
            print(f"Votre saisie : {part_hex}")
            continue
        if len(part_bytes) < 33 or (len(part_bytes)-32) % 16 != 0:
            print("Longueur de part invalide. Veuillez vérifier et ressaisir :")
            print(f"Votre saisie : {part_hex}")
            continue
        hashval = part_bytes[:32]
        fusion = part_bytes[32:]
        found = False
        for idx in range(1, n+1):
            index_byte = idx.to_bytes(1, 'big')
            if hashlib.sha256(index_byte + fusion).digest() == hashval:
                print(f"Numéro de part identifié = {idx}")
                indices.append(idx)
                all_fusions.append(fusion)
                found = True
                break
        if not found:
            print("Index non reconnu (hash non valide). Veuillez vérifier et ressaisir :")
            print(f"Votre saisie : {part_hex}")
            continue
        break

# Déterminer le nombre de blocs (chaque bloc = 16 octets)
data_len = len(all_fusions[0])
nb_blocs = data_len // 16

# Reconstruction bloc par bloc
recovered_bytes = b''
for bloc_idx in range(nb_blocs):
    shares_for_bloc = []
    for i in range(k):
        index = indices[i]
        part = all_fusions[i][bloc_idx*16:(bloc_idx+1)*16]
        shares_for_bloc.append((index, part))
    recovered_bloc = Shamir.combine(shares_for_bloc)
    recovered_bytes += recovered_bloc

# Décoder en texte (enlève les éventuels \0 de padding)
recovered_text = recovered_bytes.rstrip(b'\0').decode('utf-8', errors='replace')
print("\nSecret reconstitué :", recovered_text)

input("\nRecopier le secret sur un papier (pas de photo ni de copie numérique) puis appuyer sur Entrée pour quitter...")
