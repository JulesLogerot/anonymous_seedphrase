# Guide Utilisateur - Anonymous Seedphrase

## Introduction

Bienvenue dans Anonymous Seedphrase, votre outil de chiffrement sécurisé pour les seed phrases de cryptomonnaies.

## Qu'est-ce qu'une seed phrase ?

Une seed phrase (ou phrase de récupération) est une série de 12 à 24 mots qui permet de récupérer l'accès à un portefeuille de cryptomonnaies. C'est l'élément le plus important de votre sécurité crypto :

- Quiconque possède votre seed phrase possède vos cryptos
- Si vous perdez votre seed phrase, vous perdez définitivement vos cryptos
- Elle doit être conservée en sécurité et secrète

## Pourquoi chiffrer votre seed phrase ?

Le chiffrement ajoute une couche de sécurité supplémentaire :

1. **Protection contre le vol** : Même si quelqu'un trouve votre fichier chiffré, il ne peut pas l'utiliser sans le mot de passe
2. **Sauvegarde sécurisée** : Vous pouvez sauvegarder votre seed phrase dans le cloud sans risque
3. **Redondance** : Vous pouvez créer plusieurs copies du fichier chiffré dans différents endroits

## Installation

### Étape 1 : Cloner le repository

```bash
git clone <url-du-repository>
cd anonymous_seedphrase
```

### Étape 2 : Exécuter le script de setup

```bash
./setup.sh
```

Ce script va automatiquement :
- Détecter Python 3.13 sur votre système
- Créer un environnement virtuel
- Installer toutes les dépendances nécessaires

## Utilisation

### Lancer l'application

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Lancer l'application
streamlit run src/app/main.py
```

Votre navigateur s'ouvrira automatiquement sur http://localhost:8501

### Chiffrer votre seed phrase

#### Étape 1 : Préparer votre seed phrase

Assurez-vous d'avoir :
- Votre seed phrase complète (12, 15, 18, 21 ou 24 mots)
- Les mots doivent être séparés par des espaces
- Aucun caractère spécial ou chiffre dans les mots

#### Étape 2 : Dans l'application

1. Allez dans l'onglet "🔒 Chiffrer une seed phrase"
2. Entrez votre seed phrase dans le champ texte
3. Choisissez un **mot de passe FORT** :
   - Minimum 8 caractères
   - Mélange de majuscules, minuscules, chiffres et symboles
   - Facile à retenir pour vous mais difficile à deviner
4. Confirmez le mot de passe
5. Cliquez sur "🔒 Chiffrer"

#### Étape 3 : Télécharger le fichier

1. Cliquez sur "📥 Télécharger le fichier chiffré"
2. Le fichier `encrypted_seedphrase.seedphrase` sera téléchargé
3. Sauvegardez ce fichier dans plusieurs endroits sûrs

### Déchiffrer votre seed phrase

#### Étape 1 : Dans l'application

1. Allez dans l'onglet "🔓 Déchiffrer une seed phrase"
2. Cliquez sur "Browse files" et sélectionnez votre fichier `.seedphrase`
3. Entrez le mot de passe que vous avez utilisé pour chiffrer
4. Cliquez sur "🔓 Déchiffrer"

#### Étape 2 : Récupérer votre seed phrase

1. Votre seed phrase s'affichera à l'écran
2. Notez-la immédiatement dans un endroit sûr
3. Vérifiez que personne ne regarde par-dessus votre épaule
4. Une fois notée, cliquez sur "🗑️ Effacer la seed phrase de l'écran"
5. Fermez l'application et le navigateur

## Bonnes pratiques de sécurité

### Avant de chiffrer

- ✅ Testez d'abord avec une seed phrase de test (pas vos vraies cryptos)
- ✅ Vérifiez que personne ne vous observe
- ✅ Fermez toutes les applications de partage d'écran
- ✅ Désactivez les captures d'écran automatiques

### Choisir un bon mot de passe

**BON** mot de passe :
- `MonChat@Miaou2024!` (facile à retenir, difficile à deviner)
- `J'aim3L3sPiz$as!` (phrase personnelle avec substitutions)

**MAUVAIS** mot de passe :
- `password123` (trop simple)
- `123456` (trop court et prévisible)
- Votre date de naissance (facile à deviner)

### Sauvegarder le fichier chiffré

Sauvegardez votre fichier dans **AU MOINS 3 ENDROITS DIFFÉRENTS** :

1. **Clé USB** stockée dans un coffre-fort ou un endroit sûr
2. **Cloud chiffré** (Dropbox, Google Drive, iCloud)
3. **Disque dur externe** dans un autre lieu physique

### Sauvegarder le mot de passe

**Option 1 : Gestionnaire de mots de passe**
- Utilisez un gestionnaire comme 1Password, Bitwarden, LastPass
- Stockez-le dans une catégorie sécurisée

**Option 2 : Note physique**
- Écrivez-le sur papier
- Stockez dans un coffre-fort
- Faites une copie dans un autre lieu

**NE JAMAIS** :
- ❌ Envoyer le mot de passe par email
- ❌ Le stocker dans un fichier texte non chiffré
- ❌ Le partager avec qui que ce soit
- ❌ L'oublier (il ne peut pas être récupéré !)

## Que faire en cas de problème ?

### "Mot de passe incorrect"

- Vérifiez les majuscules/minuscules
- Vérifiez qu'il n'y a pas d'espaces avant/après
- Essayez sur un autre ordinateur
- Si vraiment oublié : **il n'y a pas de récupération possible**

### "Format de fichier invalide"

- Assurez-vous d'uploader un fichier `.seedphrase` généré par cette application
- Vérifiez que le fichier n'est pas corrompu
- Essayez de télécharger à nouveau depuis votre backup

### "La seed phrase est invalide"

- Vérifiez le nombre de mots (12, 15, 18, 21 ou 24)
- Assurez-vous qu'il n'y a que des lettres (pas de chiffres)
- Vérifiez l'orthographe de chaque mot

## FAQ

### Est-ce que mes données sont envoyées sur Internet ?

**NON**. Tout le chiffrement et déchiffrement se fait localement sur votre ordinateur. Aucune donnée n'est jamais envoyée à un serveur.

### Puis-je utiliser cette application hors ligne ?

Oui ! Une fois installée, l'application fonctionne complètement hors ligne.

### Le fichier chiffré peut-il être hacké ?

Avec un mot de passe fort, il faudrait des millions d'années pour casser le chiffrement AES-128 avec les ordinateurs actuels. La sécurité dépend de la force de votre mot de passe.

### Que se passe-t-il si j'oublie mon mot de passe ?

Il n'y a **AUCUN MOYEN** de récupérer le mot de passe ou de déchiffrer le fichier. C'est pourquoi il est crucial de :
- Choisir un mot de passe mémorable
- Le sauvegarder dans plusieurs endroits sûrs
- Tester le déchiffrement avant de supprimer votre seed phrase originale

### Puis-je chiffrer plusieurs seed phrases ?

Oui ! Chiffrez chaque seed phrase séparément avec des mots de passe différents (ou le même, c'est vous qui choisissez).

### Le format `.seedphrase` est-il standard ?

Non, c'est un format spécifique à cette application. Le fichier est en JSON et contient les métadonnées du chiffrement et les données chiffrées.

## Exemple d'utilisation complète

### Scénario : Sécuriser la seed phrase d'un nouveau wallet

1. **Vous créez un nouveau wallet Metamask**
   - Vous notez la seed phrase sur papier : "word1 word2 word3 ... word12"

2. **Vous la chiffrez avec cette application**
   - Vous lancez l'app
   - Vous entrez la seed phrase
   - Vous choisissez le mot de passe : `MesSats@2024!`
   - Vous téléchargez `encrypted_seedphrase.seedphrase`

3. **Vous sauvegardez le fichier chiffré**
   - Copie 1 : Clé USB dans votre coffre-fort
   - Copie 2 : Google Drive
   - Copie 3 : Disque dur externe chez vos parents

4. **Vous sauvegardez le mot de passe**
   - Dans votre gestionnaire de mots de passe (1Password)
   - Sur papier dans votre coffre-fort

5. **Vous testez le déchiffrement**
   - Vous uploadez le fichier
   - Vous entrez le mot de passe
   - ✅ Ça fonctionne ! La seed phrase s'affiche correctement

6. **Vous sécurisez le papier original**
   - Option 1 : Détruisez-le (vous avez les backups chiffrés)
   - Option 2 : Gardez-le aussi dans le coffre-fort

7. **Dans 6 mois, vous testez à nouveau**
   - Vous déchiffrez le fichier pour vérifier
   - ✅ Tout fonctionne toujours !

## Support

Pour toute question :
- Consultez d'abord cette documentation
- Vérifiez les issues sur GitHub
- Ouvrez une nouvelle issue si nécessaire

---

**Rappel final** : La sécurité de vos cryptomonnaies dépend de la sécurité de votre seed phrase. Prenez le temps de bien comprendre et appliquer ces bonnes pratiques !
