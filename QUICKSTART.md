# Démarrage Rapide - Anonymous Seedphrase

## Installation (2 minutes)

```bash
# 1. Le setup est déjà fait ! Vérifiez avec :
ls -la

# 2. Pour relancer le setup si nécessaire :
./setup.sh
```

## Lancer l'application

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Lancer l'application
streamlit run src/app/main.py
```

L'application s'ouvrira automatiquement dans votre navigateur : http://localhost:8501

## Tests

```bash
# Activer l'environnement (si pas déjà fait)
source .venv/bin/activate

# Lancer les tests
pytest

# Avec rapport détaillé
pytest -v --cov=src --cov-report=term-missing
```

## Workflow typique

### 1. Chiffrer
- Onglet "🔒 Chiffrer"
- Entrez votre seed phrase (12-24 mots)
- Choisissez un mot de passe fort (min 8 caractères)
- Téléchargez le fichier `.seedphrase`

### 2. Sauvegarder
- Copiez le fichier dans 3+ endroits différents
- Notez le mot de passe séparément

### 3. Déchiffrer (quand nécessaire)
- Onglet "🔓 Déchiffrer"
- Uploadez le fichier `.seedphrase`
- Entrez le mot de passe
- Votre seed phrase s'affiche

## Commandes utiles

```bash
# Activer l'environnement
source .venv/bin/activate

# Lancer l'app
streamlit run src/app/main.py

# Lancer les tests
pytest

# Voir la couverture de code
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Ajouter une dépendance
# 1. Modifier pyproject.toml
# 2. Recompiler
pip-compile -o requirements.txt --extra dev pyproject.toml
pip-sync requirements.txt

# Linter le code
black src/
ruff check src/
```

## Sécurité - Checklist rapide

Avant d'utiliser avec de vraies seed phrases :

- [ ] J'ai testé avec une seed phrase de test
- [ ] J'ai vérifié que le chiffrement/déchiffrement fonctionne
- [ ] J'ai choisi un mot de passe fort et mémorable
- [ ] J'ai sauvegardé le mot de passe dans 2+ endroits
- [ ] Je sais où je vais sauvegarder les fichiers chiffrés
- [ ] Personne ne peut voir mon écran
- [ ] Je comprends que le mot de passe ne peut PAS être récupéré s'il est oublié

## Documentation complète

- `README.md` - Documentation technique complète
- `docs/GUIDE_UTILISATEUR.md` - Guide détaillé avec bonnes pratiques

## Support

Questions ? Ouvrez une issue sur GitHub !

---

**Prêt à commencer ?** Lancez `streamlit run src/app/main.py` et testez avec une seed phrase de test !
