"""
Module de chiffrement et déchiffrement sécurisé pour les seed phrases.

Ce module utilise la bibliothèque cryptography avec l'algorithme Fernet
qui implémente AES-128 en mode CBC avec HMAC pour l'authentification.

La clé de chiffrement est dérivée du mot de passe utilisateur via PBKDF2.
"""

import base64
import json
import os
from datetime import UTC, datetime

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SeedPhraseEncryptor:
    """Classe pour chiffrer et déchiffrer des seed phrases."""

    # Constantes pour PBKDF2
    PBKDF2_ITERATIONS = 600000  # Recommandation OWASP 2023
    SALT_LENGTH = 32  # 256 bits

    def __init__(self):
        """Initialise l'encrypteur."""
        pass

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Dérive une clé de chiffrement à partir d'un mot de passe.

        Utilise PBKDF2-HMAC-SHA256 avec 600,000 itérations.

        Args:
            password: Le mot de passe utilisateur
            salt: Le sel cryptographique (32 bytes)

        Returns:
            La clé dérivée (32 bytes pour Fernet)
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.PBKDF2_ITERATIONS,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt_seedphrase(self, seedphrase: str, password: str) -> tuple[bytes, dict[str, str]]:
        """
        Chiffre une seed phrase avec un mot de passe.

        Args:
            seedphrase: La seed phrase à chiffrer
            password: Le mot de passe de chiffrement

        Returns:
            Un tuple contenant :
            - Les données chiffrées (bytes)
            - Les métadonnées (dict) avec salt, timestamp, etc.

        Raises:
            ValueError: Si la seed phrase ou le mot de passe est vide
        """
        if not seedphrase or not seedphrase.strip():
            raise ValueError("La seed phrase ne peut pas être vide")

        if not password or len(password) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")

        # Générer un sel aléatoire
        salt = os.urandom(self.SALT_LENGTH)

        # Dériver la clé depuis le mot de passe
        key = self._derive_key(password, salt)

        # Créer l'instance Fernet et chiffrer
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(seedphrase.encode())

        # Créer les métadonnées
        metadata = {
            "version": "1.0",
            "algorithm": "Fernet-AES128-CBC-HMAC",
            "kdf": "PBKDF2-HMAC-SHA256",
            "iterations": str(self.PBKDF2_ITERATIONS),
            "salt": base64.b64encode(salt).decode(),
            "timestamp": datetime.now(UTC).isoformat(),
        }

        return encrypted_data, metadata

    def decrypt_seedphrase(
        self, encrypted_data: bytes, password: str, metadata: dict[str, str]
    ) -> str:
        """
        Déchiffre une seed phrase.

        Args:
            encrypted_data: Les données chiffrées
            password: Le mot de passe de déchiffrement
            metadata: Les métadonnées contenant le sel et autres infos

        Returns:
            La seed phrase déchiffrée

        Raises:
            ValueError: Si les paramètres sont invalides
            InvalidToken: Si le mot de passe est incorrect ou les données corrompues
        """
        if not encrypted_data:
            raise ValueError("Les données chiffrées ne peuvent pas être vides")

        if not password:
            raise ValueError("Le mot de passe ne peut pas être vide")

        if "salt" not in metadata:
            raise ValueError("Métadonnées invalides : sel manquant")

        # Récupérer le sel
        salt = base64.b64decode(metadata["salt"])

        # Dériver la clé depuis le mot de passe
        key = self._derive_key(password, salt)

        # Déchiffrer
        fernet = Fernet(key)
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return decrypted_data.decode()
        except InvalidToken as e:
            raise InvalidToken(
                "Échec du déchiffrement. Mot de passe incorrect ou données corrompues."
            ) from e

    def save_encrypted_file(
        self, encrypted_data: bytes, metadata: dict[str, str], filepath: str
    ) -> None:
        """
        Sauvegarde les données chiffrées dans un fichier.

        Le format du fichier est JSON contenant les métadonnées et les données chiffrées.

        Args:
            encrypted_data: Les données chiffrées
            metadata: Les métadonnées
            filepath: Le chemin du fichier de sortie

        Raises:
            IOError: Si l'écriture du fichier échoue
        """
        file_content = {
            "metadata": metadata,
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(file_content, f, indent=2)
        except OSError as e:
            raise OSError(f"Erreur lors de l'écriture du fichier : {e}") from e

    def load_encrypted_file(self, filepath: str) -> tuple[bytes, dict[str, str]]:
        """
        Charge les données chiffrées depuis un fichier.

        Args:
            filepath: Le chemin du fichier chiffré

        Returns:
            Un tuple contenant :
            - Les données chiffrées (bytes)
            - Les métadonnées (dict)

        Raises:
            IOError: Si la lecture du fichier échoue
            ValueError: Si le format du fichier est invalide
        """
        try:
            with open(filepath, encoding="utf-8") as f:
                file_content = json.load(f)
        except OSError as e:
            raise OSError(f"Erreur lors de la lecture du fichier : {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Format de fichier invalide : {e}") from e

        if "metadata" not in file_content or "encrypted_data" not in file_content:
            raise ValueError("Format de fichier invalide : métadonnées ou données manquantes")

        encrypted_data = base64.b64decode(file_content["encrypted_data"])
        metadata = file_content["metadata"]

        return encrypted_data, metadata

    def validate_seedphrase_format(self, seedphrase: str) -> tuple[bool, str]:
        """
        Valide le format d'une seed phrase.

        Vérifie que la seed phrase contient entre 12 et 24 mots.

        Args:
            seedphrase: La seed phrase à valider

        Returns:
            Un tuple (est_valide, message)
        """
        words = seedphrase.strip().split()
        word_count = len(words)

        # Les seed phrases BIP39 standards sont de 12, 15, 18, 21 ou 24 mots
        valid_lengths = [12, 15, 18, 21, 24]

        if word_count not in valid_lengths:
            return (
                False,
                f"Une seed phrase doit contenir {', '.join(map(str, valid_lengths))} mots. "
                f"Vous avez {word_count} mot(s).",
            )

        # Vérifier que chaque mot ne contient que des lettres
        for word in words:
            if not word.isalpha():
                return (
                    False,
                    f"Le mot '{word}' contient des caractères invalides. "
                    "Les mots doivent contenir uniquement des lettres.",
                )

        return True, "Format valide"
