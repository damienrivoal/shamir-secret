from Crypto.Protocol.SecretSharing import Shamir
import hashlib

# Saisie d'un texte à partager
texte = input("Entrez le texte à partager (max 1000 caractères UTF-8) : ")
texte = texte[:1000]
secret_bytes = texte.encode('utf-8')

# Découper en blocs de 16 octets
blocs = [secret_bytes[i:i+16] for i in range(0, len(secret_bytes), 16)]
if len(blocs[-1]) < 16:
    blocs[-1] = blocs[-1].ljust(16, b'\0')

n = 6  # nombre de parts
k = 2  # seuil

# Générer les parts pour chaque bloc
all_shares = [[] for _ in range(n)]  # all_shares[i] = liste des parts du participant i
for bloc_idx, bloc in enumerate(blocs):
    shares = Shamir.split(k, n, bloc)
    for i, (idx, share) in enumerate(shares):
        all_shares[i].append(share)

# Pour chaque participant, calculer hash(index_byte + fusion) + fusion
for i, parts in enumerate(all_shares):
    fusion = b''.join(parts)
    index_byte = (i+1).to_bytes(1, 'big')
    hashval = hashlib.sha256(index_byte + fusion).digest()
    part_with_hash = hashval + fusion
    print(f"\nPart unique pour le participant {i+1} (hash + data) :\n{part_with_hash.hex()}")

# Reconstruction à partir des parts des k premiers participants (pour test)
recovered_bytes = b''
for bloc_idx in range(len(blocs)):
    shares_for_bloc = []
    for i in range(k):
        fusion = b''.join(all_shares[i])
        index = i+1
        part = fusion[bloc_idx*16:(bloc_idx+1)*16]
        shares_for_bloc.append((index, part))
    recovered_bloc = Shamir.combine(shares_for_bloc)
    recovered_bytes += recovered_bloc

# Décoder en texte (enlève les éventuels \0 de padding)
recovered_text = recovered_bytes.rstrip(b'\0').decode('utf-8', errors='replace')
print("\nTexte reconstitué :", recovered_text)
print("Identique ?", recovered_text == texte)

input("\nRecopier les parts sur un support sécurisé et durable (peu importe les majuscules/minuscules) puis appuyer sur Entrée pour quitter...")