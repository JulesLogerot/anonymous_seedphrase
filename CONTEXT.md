# CONTEXT - Anonymous Seedphrase Project

> **Fichier de contexte pour reprendre le développement**
> Lisez ce fichier pour comprendre rapidement l'état du projet et reprendre le travail.

---

## 📋 Résumé du projet

**Nom** : Anonymous Seedphrase
**Objectif** : Application de chiffrement sécurisé pour les seed phrases (phrases de récupération) de portefeuilles de cryptomonnaies
**Statut** : ✅ **Version 1.0 - Fonctionnelle et testée**
**Date de création** : Octobre 2025
**Développeur** : Jules

## 🎯 Objectif principal

Permettre aux utilisateurs de chiffrer leurs seed phrases de cryptomonnaies avec un mot de passe fort, puis de télécharger le fichier chiffré pour le stocker en sécurité. L'utilisateur peut ensuite déchiffrer le fichier pour récupérer sa seed phrase.

## ✅ Ce qui a été réalisé (Version 1.0)

### 1. Configuration du projet
- ✅ Structure de dossiers créée (src/, tests/, docs/, data/, logs/)
- ✅ Gestion des dépendances avec `pyproject.toml` + `pip-tools`
- ✅ Script `setup.sh` cross-platform (macOS, Linux, Windows/Git Bash)
- ✅ Environnement virtuel Python 3.13 configuré
- ✅ Git initialisé avec commit complet
- ✅ `.gitignore` configuré (exclut .venv, __pycache__, etc.)

### 2. Module de chiffrement (`src/crypto/encryption.py`)

**Classe** : `SeedPhraseEncryptor`

**Fonctionnalités** :
- Chiffrement de seed phrase avec mot de passe
- Déchiffrement avec validation
- Sauvegarde/chargement de fichiers `.seedphrase` (format JSON)
- Validation du format de seed phrase (12, 15, 18, 21 ou 24 mots)

**Sécurité** :
- **Algorithme** : Fernet (AES-128-CBC + HMAC-SHA256)
- **Dérivation de clé** : PBKDF2-HMAC-SHA256
- **Itérations** : 600,000 (norme OWASP 2023)
- **Sel** : 32 bytes générés aléatoirement
- **Format de fichier** : JSON avec métadonnées (version, algorithme, sel, timestamp)

### 3. Interface Streamlit (`src/app/main.py`)

**Structure** :
- 2 onglets : "🔒 Chiffrer" et "🔓 Déchiffrer"
- Interface responsive et intuitive
- Avertissements de sécurité visibles
- Bouton de téléchargement pour fichiers chiffrés
- Bouton pour effacer la seed phrase déchiffrée de l'écran

**Workflow utilisateur** :
1. Chiffrement : Entrer seed phrase + mot de passe → Télécharger fichier
2. Déchiffrement : Upload fichier + mot de passe → Affichage seed phrase

### 4. Tests (`tests/unit/test_encryption.py`)

**Résultats** :
- ✅ **14 tests** unitaires écrits
- ✅ **14/14 tests passent** avec succès
- ✅ **93% de couverture** de code (module encryption.py)

**Tests couvrent** :
- Chiffrement/déchiffrement avec succès
- Validation des entrées (seed phrase vide, mot de passe court)
- Gestion des erreurs (mauvais mot de passe, fichier corrompu)
- Sauvegarde/chargement de fichiers
- Validation du format de seed phrase
- Non-déterminisme du chiffrement (sels différents)

### 5. Documentation

**Fichiers créés** :
- `README.md` : Documentation technique complète
- `QUICKSTART.md` : Guide de démarrage rapide
- `docs/GUIDE_UTILISATEUR.md` : Guide détaillé avec bonnes pratiques de sécurité
- `CONTEXT.md` : Ce fichier (pour reprendre le développement)

## 🏗️ Architecture technique

### Structure des fichiers

```
anonymous_seedphrase/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py              # Interface Streamlit
│   ├── crypto/
│   │   ├── __init__.py
│   │   └── encryption.py        # Module de chiffrement
│   └── __init__.py
├── tests/
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_encryption.py   # Tests unitaires
│   ├── integration/             # (vide pour l'instant)
│   └── __init__.py
├── docs/
│   └── GUIDE_UTILISATEUR.md
├── data/                         # Fichiers temporaires (gitignored)
├── logs/                         # Logs (gitignored)
├── .venv/                        # Environnement virtuel (gitignored)
├── pyproject.toml               # Config + dépendances
├── requirements.txt             # Dépendances compilées
├── setup.sh                     # Script d'installation
├── .gitignore
├── README.md
├── QUICKSTART.md
└── CONTEXT.md                   # Ce fichier
```

### Dépendances principales

**Production** :
- `streamlit>=1.39.0` - Interface web
- `cryptography>=44.0.0` - Chiffrement

**Développement** :
- `pytest>=8.3.0` - Framework de tests
- `pytest-cov>=6.0.0` - Couverture de code
- `black>=24.0.0` - Formatage de code
- `ruff>=0.8.0` - Linter
- `mypy>=1.13.0` - Type checking

### Technologies utilisées

- **Python 3.13** (version requise)
- **Streamlit** pour l'interface utilisateur
- **cryptography** (bibliothèque de l'équipe PyCA)
- **pytest** pour les tests
- **pip-tools** pour la gestion des dépendances (pip-compile + pip-sync)

## 🔐 Détails de sécurité

### Algorithme de chiffrement

**Fernet** (de la bibliothèque `cryptography`) :
- Chiffrement symétrique
- AES-128 en mode CBC
- Authentification via HMAC-SHA256
- Padding automatique
- Protection contre les attaques par rejeu (timestamp)

### Dérivation de clé (PBKDF2)

```python
Algorithm: PBKDF2-HMAC-SHA256
Iterations: 600,000 (norme OWASP 2023)
Salt: 32 bytes (256 bits) générés aléatoirement
Output: 32 bytes pour la clé Fernet
```

### Format du fichier chiffré

```json
{
  "metadata": {
    "version": "1.0",
    "algorithm": "Fernet-AES128-CBC-HMAC",
    "kdf": "PBKDF2-HMAC-SHA256",
    "iterations": "600000",
    "salt": "<base64>",
    "timestamp": "<ISO8601>"
  },
  "encrypted_data": "<base64>"
}
```

### Garanties de sécurité

✅ **Traitement 100% local** : Aucune donnée n'est envoyée sur un serveur
✅ **Sel unique** : Chaque chiffrement génère un nouveau sel aléatoire
✅ **Protection par mot de passe** : Sans le mot de passe, le fichier est inutilisable
✅ **Authentification** : HMAC détecte toute modification du fichier
✅ **Standards reconnus** : Utilise des primitives cryptographiques bien établies

⚠️ **Point critique** : Le mot de passe ne peut PAS être récupéré s'il est oublié

## 🚀 Comment reprendre le projet

### 1. Relancer l'application

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Lancer l'application Streamlit
streamlit run src/app/main.py
```

→ L'application s'ouvre sur http://localhost:8501

### 2. Lancer les tests

```bash
# Activer l'environnement (si pas déjà fait)
source .venv/bin/activate

# Lancer les tests
pytest

# Avec rapport détaillé
pytest -v --cov=src --cov-report=term-missing

# Générer un rapport HTML
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### 3. Ajouter une dépendance

```bash
# 1. Éditer pyproject.toml (ajouter dans dependencies ou dev)
# 2. Recompiler
pip-compile -o requirements.txt --extra dev pyproject.toml
# 3. Installer
pip-sync requirements.txt
```

### 4. Voir les commits

```bash
git log --oneline
# cb90d3a feat: Implémentation complète de l'application
# 8933524 Initial commit
```

## 💭 Décisions techniques importantes

### Pourquoi Streamlit pour le prototype ?

- **Rapidité** : Prototype fonctionnel en moins de temps
- **Simplicité** : Pas besoin de gérer frontend/backend séparément
- **Tests** : Permet de valider l'UX avant de faire une vraie webapp
- **Migration** : Le module `crypto` est indépendant et réutilisable

### Pourquoi Fernet plutôt qu'AES direct ?

- **Sécurité** : Fernet combine chiffrement + authentification
- **Simplicité** : API haut niveau, moins d'erreurs possibles
- **Standards** : Implémentation reconnue et auditée
- **Timestamp** : Protection contre les attaques par rejeu

### Pourquoi 600,000 itérations PBKDF2 ?

- **Norme OWASP 2023** : Recommandation pour PBKDF2-HMAC-SHA256
- **Balance** : Assez lent pour ralentir le brute-force, assez rapide pour l'UX (~2-3 secondes)
- **Compatible** : Fonctionne sur tous les systèmes sans problème

### Pourquoi Python 3.13 ?

- **Version récente** : Profite des dernières améliorations
- **Performance** : Python 3.13 est plus rapide
- **Support long terme** : Sera supporté pendant plusieurs années

## 📊 Métriques du projet

- **Lignes de code Python** : ~500 lignes
- **Tests** : 14 tests unitaires
- **Couverture** : 93% (encryption.py)
- **Fichiers** : 17 fichiers (hors .venv)
- **Commits Git** : 2 commits
- **Documentation** : 4 fichiers markdown (>1000 lignes)

## 🎯 Prochaines étapes possibles

### Version 1.1 (améliorations mineures)

- [ ] Ajouter un indicateur de force du mot de passe
- [ ] Permettre de copier la seed phrase dans le presse-papier (vrai bouton)
- [ ] Ajouter une option pour chiffrer plusieurs seed phrases en batch
- [ ] Améliorer les messages d'erreur
- [ ] Ajouter des logs (dans le dossier logs/)

### Version 2.0 (interface web complète)

- [ ] Créer une API backend (Flask ou FastAPI)
- [ ] Créer un frontend moderne (React, Vue ou Svelte)
- [ ] Ajouter une base de données (optionnelle, pour multi-utilisateurs)
- [ ] Déployer sur un serveur (Heroku, Render, Railway)
- [ ] Ajouter authentification utilisateur (si multi-users)

### Version 3.0 (fonctionnalités avancées)

- [ ] Application desktop avec Electron ou PyQt
- [ ] Application mobile (React Native ou Flutter)
- [ ] Support de multiples algorithmes de chiffrement (au choix)
- [ ] Génération de QR codes pour les fichiers chiffrés
- [ ] Mode hors ligne complet (PWA)
- [ ] Support de YubiKey pour 2FA
- [ ] Backup automatique sur cloud chiffré

### Améliorations techniques

- [ ] Tests d'intégration (tests/integration/)
- [ ] CI/CD avec GitHub Actions
- [ ] Type hints complets + validation mypy
- [ ] Documentation API (Sphinx)
- [ ] Benchmarks de performance
- [ ] Tests de sécurité (fuzzing, pen-testing)

## 🐛 Problèmes connus / Limitations

### Limitations actuelles

1. **Pas de récupération de mot de passe** : C'est voulu pour la sécurité, mais peut être frustrant
2. **Streamlit non optimal pour production** : Bon pour prototype, mais limité pour déploiement
3. **Pas de support multi-fichiers** : Un seul fichier à la fois
4. **Copie presse-papier basique** : La fonction de copie n'est pas optimale dans Streamlit

### Non-problèmes (fonctionnement normal)

- **Warning pip-tools** : `--strip-extras` sera le défaut en v8.0.0 (peut être ignoré)
- **Tests en ~5-8 secondes** : Normal à cause des 600k itérations PBKDF2
- **Fichier .coverage non gitignored** : Peut être ajouté au .gitignore si désiré

## 💡 Questions fréquentes techniques

### Q : Peut-on changer l'algorithme de chiffrement ?

R : Oui, mais il faudrait modifier `src/crypto/encryption.py`. Le code est modulaire, donc relativement facile à adapter. Il faudrait aussi mettre à jour le format de fichier et les métadonnées.

### Q : Peut-on utiliser ce code dans une autre app ?

R : Oui ! Le module `src/crypto/encryption.py` est totalement indépendant de Streamlit. Il peut être importé dans n'importe quelle application Python.

### Q : Les tests sont-ils suffisants ?

R : Pour une v1.0, oui. Mais pour une production, il faudrait :
- Tests d'intégration (chiffrer puis déchiffrer)
- Tests de sécurité (fuzzing, pen-testing)
- Tests de performance (benchmarks)
- Tests sur différents OS

### Q : Comment déployer sur Streamlit Cloud ?

R :
1. Pousser le code sur GitHub
2. Aller sur share.streamlit.io
3. Connecter le repository
4. Spécifier `src/app/main.py` comme point d'entrée
5. Déployer !

### Q : Pourquoi pas Flask/FastAPI directement ?

R : Décision de prototypage rapide. Streamlit permet de valider l'UX en quelques heures. Le module crypto étant indépendant, il sera facile de migrer vers Flask/FastAPI plus tard.

## 📞 Informations de contact / Support

- **Repository GitHub** : (à définir)
- **Issues** : (à définir)
- **Documentation** : Voir README.md et docs/

## 🔄 Dernière mise à jour

- **Date** : 20 octobre 2025
- **Version** : 1.0
- **Status** : ✅ Fonctionnelle et testée
- **Dernier commit** : `cb90d3a - feat: Implémentation complète de l'application`

---

## 📝 Notes pour la prochaine session

### Si vous voulez continuer avec Streamlit :
1. Testez l'application avec des vraies seed phrases de test
2. Améliorez l'UX (indicateur de force mot de passe, etc.)
3. Ajoutez des tests d'intégration

### Si vous voulez migrer vers Flask/FastAPI :
1. Gardez le module `src/crypto/` tel quel
2. Créez un nouveau dossier `src/api/` pour l'API backend
3. Créez un frontend séparé (React, Vue, ou simple HTML/JS)
4. Utilisez la même logique de chiffrement

### Si vous voulez déployer :
1. **Option 1** : Streamlit Cloud (le plus simple, gratuit)
2. **Option 2** : Docker + VPS (plus de contrôle)
3. **Option 3** : Heroku/Render/Railway (PaaS, facile)

### Si vous avez des questions :
- Relisez ce fichier CONTEXT.md
- Consultez README.md pour les détails techniques
- Consultez QUICKSTART.md pour les commandes rapides
- Lisez le code dans `src/` (bien commenté)

---

**Bon développement ! 🚀**
