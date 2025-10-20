#!/bin/bash

# ==============================================================================
# SETUP SCRIPT POUR ANONYMOUS SEEDPHRASE
# Script cross-platform (macOS, Linux, Windows/Git Bash)
# Crée l'environnement virtuel, installe pip-tools et les dépendances
# ==============================================================================

set -e  # Arrêt en cas d'erreur

echo "🚀 Démarrage du setup pour Anonymous Seedphrase"
echo ""

# ==============================================================================
# 1. DÉTECTION DE L'OS
# ==============================================================================
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos";;
        Linux*)     echo "linux";;
        MINGW*|MSYS*|CYGWIN*)  echo "windows";;
        *)          echo "unknown";;
    esac
}

OS_TYPE=$(detect_os)
echo "🖥️  Système détecté : $OS_TYPE"
echo ""

# ==============================================================================
# 2. RECHERCHE DE PYTHON 3.13
# ==============================================================================
find_python() {
    # Liste des commandes Python possibles
    local python_commands=("python3.13" "python3" "python")

    for cmd in "${python_commands[@]}"; do
        if command -v "$cmd" &> /dev/null; then
            # Vérifier la version
            local version=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
            if [[ "$version" == "3.13" ]]; then
                echo "$cmd"
                return 0
            fi
        fi
    done

    return 1
}

echo "🔍 Recherche de Python 3.13..."
if PYTHON_CMD=$(find_python); then
    echo "✅ Python 3.13 trouvé : $PYTHON_CMD"
    PYTHON_VERSION=$("$PYTHON_CMD" --version)
    echo "   Version complète : $PYTHON_VERSION"
else
    echo "❌ Python 3.13 non trouvé."
    echo "   Veuillez installer Python 3.13 et réessayer."
    echo "   Téléchargement : https://www.python.org/downloads/"
    exit 1
fi
echo ""

# ==============================================================================
# 3. VÉRIFICATION DU FICHIER pyproject.toml
# ==============================================================================
if [ ! -f "pyproject.toml" ]; then
    echo "❌ pyproject.toml introuvable dans le dossier courant."
    exit 1
fi
echo "✅ pyproject.toml trouvé"
echo ""

# ==============================================================================
# 4. CRÉATION DE L'ENVIRONNEMENT VIRTUEL
# ==============================================================================
if [ -d ".venv" ]; then
    echo "✅ L'environnement virtuel .venv existe déjà."
else
    echo "🔧 Création de l'environnement virtuel (.venv)..."
    "$PYTHON_CMD" -m venv .venv
    if [ ! -d ".venv" ]; then
        echo "❌ Échec de la création de l'environnement virtuel."
        exit 1
    fi
    echo "✅ Environnement virtuel créé avec succès."
fi
echo ""

# ==============================================================================
# 5. ACTIVATION DE L'ENVIRONNEMENT VIRTUEL
# ==============================================================================
echo "⚙️  Activation de l'environnement virtuel..."
if [ "$OS_TYPE" = "windows" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi
echo "✅ Environnement virtuel activé."
echo ""

# ==============================================================================
# 6. MISE À JOUR DE PIP ET INSTALLATION DE PIP-TOOLS
# ==============================================================================
echo "📦 Mise à jour de pip..."
python -m pip install --upgrade pip --quiet
echo "✅ pip mis à jour."
echo ""

echo "📦 Installation de pip-tools..."
python -m pip install pip-tools --quiet
echo "✅ pip-tools installé."
echo ""

# ==============================================================================
# 7. COMPILATION DES DÉPENDANCES (prod + dev)
# ==============================================================================
echo "🧩 Compilation du requirements.txt depuis pyproject.toml..."
echo "   (incluant les dépendances de développement)"
pip-compile -q -o requirements.txt --extra dev pyproject.toml
echo "✅ requirements.txt généré."
echo ""

# ==============================================================================
# 8. INSTALLATION DES DÉPENDANCES
# ==============================================================================
echo "📥 Installation des dépendances..."
pip-sync requirements.txt --quiet
echo "✅ Dépendances installées."
echo ""

# ==============================================================================
# 9. CRÉATION DES DOSSIERS DU PROJET
# ==============================================================================
echo "📁 Création de la structure de dossiers..."
mkdir -p src/app
mkdir -p src/crypto
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p docs
mkdir -p data
mkdir -p logs
echo "✅ Structure de dossiers créée."
echo ""

# ==============================================================================
# 10. CRÉATION DES FICHIERS __init__.py
# ==============================================================================
echo "📄 Création des fichiers __init__.py..."
touch src/__init__.py
touch src/app/__init__.py
touch src/crypto/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
echo "✅ Fichiers __init__.py créés."
echo ""

# ==============================================================================
# 11. INSTRUCTIONS FINALES
# ==============================================================================
echo "✅ Setup terminé avec succès !"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📌 PROCHAINES ÉTAPES :"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
if [ "$OS_TYPE" = "windows" ]; then
    echo "1️⃣  Activer l'environnement (Git Bash) :"
    echo "   source .venv/Scripts/activate"
    echo ""
    echo "   OU dans CMD/PowerShell :"
    echo "   .venv\\Scripts\\activate"
else
    echo "1️⃣  Activer l'environnement :"
    echo "   source .venv/bin/activate"
fi
echo ""
echo "2️⃣  Lancer l'application Streamlit :"
echo "   streamlit run src/app/main.py"
echo ""
echo "3️⃣  Lancer les tests :"
echo "   pytest"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
