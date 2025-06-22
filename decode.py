from Crypto.Protocol.SecretSharing import Shamir
import hashlib

# Paramètres
n = 5  # nombre total de parts générées à l'encodage
k = 3  # seuil minimal pour la reconstruction

# Saisie des parts fusionnées de k participants (hash + data)
indices = []
all_fusions = []
for i in range(k):
    part_hex = input(f"Saisir une portion du secret (peu importe les majuscules/minuscules) : ").strip()
    part_bytes = bytes.fromhex(part_hex)
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
        print(f"Index non reconnu (hash non valide)")
        raise ValueError("Impossible de retrouver l'index d'une part : hash non valide")

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
