# Partage de Secret de Shamir (Python)

## Installation pour débutant

### 1. Installer Python

- Rendez-vous sur https://www.python.org/downloads/ et téléchargez la version adaptée à votre système (Windows, Mac, Linux).
- Suivez les instructions d'installation. Sur Windows, cochez la case "Add Python to PATH" lors de l'installation.

### 2. Télécharger les fichiers du projet

- Téléchargez ou clonez ce dépôt (bouton "Code" > "Download ZIP" ou via `git clone`).
- Placez-vous dans le dossier du projet avec votre terminal ou invite de commandes.

### 3. Installer les dépendances

Ouvrez un terminal dans le dossier du projet et tapez :

```bash
pip install -r requirements.txt
```

Cela installera automatiquement tout ce qu'il faut pour faire fonctionner les scripts.

### 4. Utiliser les scripts

#### Encoder un secret

```bash
python encode.py
```
- Saisissez le texte à protéger.
- Les parts générées s'affichent à l'écran.

#### Décoder un secret

```bash
python decode.py
```
- Saisissez les parts (copier-coller, édition facilitée grâce à prompt_toolkit).
- Le secret reconstitué s'affichera si les parts sont valides.

---

## Dépendances
- Python 3.x
- pycryptodome
- prompt_toolkit

---

> _Projet éducatif et démonstratif. N'utilisez pas en production sans audit de sécurité._

## Principe de base

🔐 **Partage de secret** : Divisez un secret (texte ou entier) en plusieurs parts, de sorte qu'il faille un nombre minimal de parts pour le reconstituer.

Ce projet contient deux scripts Python (`encode.py` et `decode.py`) pour implémenter le schéma de partage de secret de Shamir. Il permet de diviser un secret textuel en plusieurs parts, de telle sorte qu'un nombre minimum de parts est nécessaire pour le reconstituer.

Cette méthode est idéale pour la sauvegarde de secrets importants (clés de chiffrement, mots de passe maîtres, etc.) en répartissant le risque sur plusieurs supports ou personnes.

## Fonctionnalités

- **Encodage (`encode.py`)**:
  - Prend un texte secret (jusqu'à 1000 caractères).
  - Divise le secret en `n` parts (par défaut 5).
  - Affiche chaque part sous forme d'une chaîne hexadécimale unique. L'index de la part est "caché" dans un hash pour éviter qu'il soit évident.

- **Décodage (`decode.py`)**:
  - Demande à l'utilisateur de saisir `k` parts (par défaut 3).
  - Vérifie l'intégrité et l'index de chaque part grâce au hash.
  - Reconstitue le secret original si les parts sont valides.

## Comment utiliser les scripts

### Prérequis

- Python 3
- La bibliothèque `pycryptodome`

Installez la dépendance avec pip :
```bash
pip install pycryptodome
```

### 1. Générer les parts

Exécutez le script d'encodage :
```bash
python encode.py
```
- Saisissez le texte que vous souhaitez protéger.
- Le script affichera `n` parts uniques. **Recopiez chaque part avec la plus grande attention sur un support sécurisé et durable (par exemple, du papier de qualité). Ne les stockez pas numériquement et ne les photographiez pas.**

### 2. Reconstituer le secret

Exécutez le script de décodage :
```bash
python decode.py
```
- Saisissez `k` parts différentes lorsque le script vous le demande. L'ordre n'a pas d'importance.
- Si les parts sont correctes, le secret original sera affiché.

## Créer des exécutables (.exe)

Vous pouvez transformer ces scripts en exécutables autonomes pour Windows avec PyInstaller.

1. **Installez PyInstaller** :
   ```bash
   pip install pyinstaller
   ```

2. **Créez l'exécutable** (par exemple pour `decode.py`) :
   ```bash
   pyinstaller --onefile decode.py
   ```

L'exécutable sera disponible dans le dossier `dist`. 