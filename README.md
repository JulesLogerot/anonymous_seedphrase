# Anonymous Seedphrase - Outil de Chiffrement de Seed Phrases

Application de chiffrement sécurisé pour les seed phrases (phrases de récupération) de portefeuilles de cryptomonnaies.

## Description

Cette application permet de chiffrer et sécuriser vos seed phrases de cryptomonnaies avec un algorithme de chiffrement robuste. Toutes les opérations de chiffrement/déchiffrement sont effectuées localement - aucune donnée n'est jamais envoyée sur un serveur.

## Fonctionnalités

- **Chiffrement sécurisé** : Chiffrez votre seed phrase avec un mot de passe
- **Déchiffrement** : Récupérez votre seed phrase à partir du fichier chiffré
- **Export de fichier** : Téléchargez le fichier chiffré pour le stocker en sécurité
- **Interface intuitive** : Interface utilisateur simple avec Streamlit
- **Validation** : Vérification automatique du format de la seed phrase (12, 15, 18, 21 ou 24 mots)

## Sécurité

L'application utilise :
- **Chiffrement** : Fernet (AES-128 en mode CBC avec HMAC SHA-256)
- **Dérivation de clé** : PBKDF2-HMAC-SHA256 avec 600,000 itérations (norme OWASP 2023)
- **Sel aléatoire** : 32 bytes générés de manière cryptographiquement sécurisée
- **Traitement local** : Aucune donnée n'est stockée ou envoyée sur un serveur
- **Tests complets** : 14 tests unitaires avec couverture de code à 93%

## Prérequis

- Python 3.13 ou supérieur
- macOS, Linux ou Windows (avec Git Bash)

## Installation

### Méthode automatique (recommandée)

```bash
# Clonez le repository
git clone <https://github.com/JulesLogerot/anonymous_seedphrase.git>
cd anonymous_seedphrase

# Exécutez le script de setup (crée l'environnement, installe les dépendances)
./setup.sh
```

Le script `setup.sh` va :
1. Détecter automatiquement Python 3.13 sur votre système
2. Créer un environnement virtuel (.venv)
3. Installer pip-tools
4. Compiler et installer toutes les dépendances
5. Créer la structure de dossiers nécessaire

### Méthode manuelle

```bash
# Créer l'environnement virtuel
python3.13 -m venv .venv

# Activer l'environnement
source .venv/bin/activate  # macOS/Linux
# OU
.venv\Scripts\activate     # Windows

# Installer pip-tools
pip install pip-tools

# Compiler les dépendances
pip-compile -o requirements.txt --extra dev pyproject.toml

# Installer les dépendances
pip-sync requirements.txt
```

## Utilisation

### Lancer l'application

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Lancer l'application Streamlit
streamlit run src/app/main.py
```

L'application s'ouvrira dans votre navigateur à l'adresse : http://localhost:8501

### Chiffrer une seed phrase

1. Allez dans l'onglet "🔒 Chiffrer une seed phrase"
2. Entrez votre seed phrase (12-24 mots séparés par des espaces)
3. Choisissez un mot de passe fort (minimum 8 caractères)
4. Confirmez le mot de passe
5. Cliquez sur "Chiffrer"
6. Téléchargez le fichier `.seedphrase` généré

### Déchiffrer une seed phrase

1. Allez dans l'onglet "🔓 Déchiffrer une seed phrase"
2. Uploadez votre fichier `.seedphrase`
3. Entrez le mot de passe utilisé lors du chiffrement
4. Cliquez sur "Déchiffrer"
5. Votre seed phrase s'affichera à l'écran

## Structure du projet

```
anonymous_seedphrase/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py              # Application Streamlit
│   ├── crypto/
│   │   ├── __init__.py
│   │   └── encryption.py        # Module de chiffrement/déchiffrement
│   └── __init__.py
├── tests/
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_encryption.py   # Tests unitaires
│   ├── integration/
│   │   └── __init__.py
│   └── __init__.py
├── data/                         # Dossier pour fichiers temporaires
├── docs/                         # Documentation
├── logs/                         # Logs de l'application
├── pyproject.toml               # Configuration du projet et dépendances
├── requirements.txt             # Dépendances compilées
├── setup.sh                     # Script d'installation automatique
├── .gitignore                   # Fichiers à ignorer par Git
└── README.md                    # Ce fichier
```

## Tests

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Exécuter les tests
pytest

# Avec rapport de couverture détaillé
pytest --cov=src --cov-report=html
```

Les tests couvrent :
- Chiffrement et déchiffrement
- Validation de seed phrases
- Gestion des erreurs
- Sauvegarde et chargement de fichiers
- Cas limites et erreurs

## Avertissements de sécurité

⚠️ **IMPORTANT** :

- **Ne partagez JAMAIS** votre seed phrase avec qui que ce soit
- **Conservez plusieurs copies** de votre fichier chiffré dans des endroits sûrs différents
- **N'oubliez PAS** votre mot de passe de chiffrement - il ne peut pas être récupéré
- **Testez d'abord** avec une seed phrase de test avant d'utiliser vos vraies seed phrases
- **Vérifiez** que personne ne regarde par-dessus votre épaule lors de l'utilisation
- **Fermez** l'application et le navigateur après utilisation

## Conseils de stockage

Pour une sécurité maximale :
1. Sauvegardez le fichier chiffré dans plusieurs endroits :
   - Clé USB stockée en lieu sûr
   - Service cloud chiffré (Dropbox, Google Drive, etc.)
   - Disque dur externe
2. Notez le mot de passe séparément et conservez-le en sécurité
3. Testez régulièrement le déchiffrement pour vous assurer que tout fonctionne

## Technologies utilisées

- **Python 3.13** - Langage de programmation
- **Streamlit** - Framework pour l'interface web
- **cryptography** - Bibliothèque de chiffrement
- **pytest** - Framework de tests
- **pip-tools** - Gestion des dépendances

## Développement

### Ajouter de nouvelles dépendances

```bash
# Ajouter une dépendance dans pyproject.toml
# Puis recompiler et réinstaller
pip-compile -o requirements.txt --extra dev pyproject.toml
pip-sync requirements.txt
```

### Lancer en mode développement

```bash
streamlit run src/app/main.py --server.runOnSave true
```

## Roadmap / Améliorations futures

- [ ] Support du chiffrement de fichiers multiples
- [ ] Interface web complète (Flask/FastAPI) pour déploiement
- [ ] Application mobile (React Native)
- [ ] Support de multiples algorithmes de chiffrement
- [ ] Génération de QR codes pour les fichiers chiffrés
- [ ] Mode hors ligne complet (PWA)

## Licence

MIT License - Libre d'utilisation, modification et distribution

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer une nouvelle fonctionnalité
- Soumettre une pull request

## Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

---

**Note** : Cette application est un outil de sécurité personnel. Assurez-vous de bien comprendre son fonctionnement avant de l'utiliser avec de vraies seed phrases contenant des fonds importants.