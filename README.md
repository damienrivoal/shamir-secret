# Secret de Shamir (JavaScript)

Ce projet propose une **implémentation simple du partage de secret de Shamir** (schéma \((k, n)\)) en JavaScript, avec une interface web pour encoder et décoder des secrets textuels.

---

## 🚀 Fonctionnalités

- 🔐 **Partage de secret** : Divisez un secret (texte ou entier) en plusieurs parts, de sorte qu'il faille un nombre minimal de parts pour le reconstituer.
- 🖥️ **Interface web** : Encodez et décodez facilement vos secrets via une page HTML conviviale.
- 🌍 **Compatible Unicode** : Les secrets peuvent contenir des accents, emojis, etc.

---

## 📦 Utilisation rapide

### En ligne de commande (Node.js)

```bash
node shamir.js
```

Cela exécutera un test autonome de partage et de reconstitution d'un secret.

### Interface web

Ouvrez `shamir.html` dans votre navigateur pour accéder à l'encodeur/décodeur graphique.

---

## 📝 Exemple d'utilisation

1. **Encoder** :
   - Entrez un secret, choisissez le nombre de parts à générer (`n`) et le nombre minimum requis pour reconstituer (`k`).
   - Téléchargez les parts générées.
2. **Décoder** :
   - Chargez au moins `k` fichiers de parts et récupérez le secret original.

---

## 📁 Fichiers

- `shamir.js` : Implémentation du schéma de Shamir (logique principale).
- `shamir.html` : Interface web pour encoder/décoder.
- `shamir.code-workspace` : Fichier de configuration pour VS Code.

---

## ℹ️ À propos

- **Auteur** : _À compléter_
- **Licence** : _À compléter (ex : MIT, GPL, etc.)_

---

> _Projet éducatif et démonstratif. N'utilisez pas en production sans audit de sécurité._ 