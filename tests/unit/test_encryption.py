"""
Tests unitaires pour le module de chiffrement.
"""

import os
import tempfile
from pathlib import Path

import pytest
from cryptography.fernet import InvalidToken

from src.crypto.encryption import SeedPhraseEncryptor


class TestSeedPhraseEncryptor:
    """Tests pour la classe SeedPhraseEncryptor."""

    def setup_method(self):
        """Configure chaque test."""
        self.encryptor = SeedPhraseEncryptor()
        self.test_seedphrase = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        self.test_password = "SecurePassword123!"

    def test_encrypt_seedphrase_success(self):
        """Test le chiffrement d'une seed phrase valide."""
        encrypted_data, metadata = self.encryptor.encrypt_seedphrase(
            self.test_seedphrase, self.test_password
        )

        assert encrypted_data is not None
        assert isinstance(encrypted_data, bytes)
        assert len(encrypted_data) > 0

        assert "salt" in metadata
        assert "algorithm" in metadata
        assert "version" in metadata
        assert metadata["algorithm"] == "Fernet-AES128-CBC-HMAC"

    def test_encrypt_empty_seedphrase_raises_error(self):
        """Test que le chiffrement d'une seed phrase vide lève une erreur."""
        with pytest.raises(ValueError, match="ne peut pas être vide"):
            self.encryptor.encrypt_seedphrase("", self.test_password)

        with pytest.raises(ValueError, match="ne peut pas être vide"):
            self.encryptor.encrypt_seedphrase("   ", self.test_password)

    def test_encrypt_short_password_raises_error(self):
        """Test qu'un mot de passe trop court lève une erreur."""
        with pytest.raises(ValueError, match="au moins 8 caractères"):
            self.encryptor.encrypt_seedphrase(self.test_seedphrase, "short")

    def test_decrypt_seedphrase_success(self):
        """Test le déchiffrement avec le bon mot de passe."""
        # Chiffrer
        encrypted_data, metadata = self.encryptor.encrypt_seedphrase(
            self.test_seedphrase, self.test_password
        )

        # Déchiffrer
        decrypted = self.encryptor.decrypt_seedphrase(
            encrypted_data, self.test_password, metadata
        )

        assert decrypted == self.test_seedphrase

    def test_decrypt_wrong_password_raises_error(self):
        """Test que le déchiffrement avec un mauvais mot de passe échoue."""
        encrypted_data, metadata = self.encryptor.encrypt_seedphrase(
            self.test_seedphrase, self.test_password
        )

        with pytest.raises(InvalidToken):
            self.encryptor.decrypt_seedphrase(
                encrypted_data, "WrongPassword123!", metadata
            )

    def test_decrypt_empty_data_raises_error(self):
        """Test que le déchiffrement de données vides lève une erreur."""
        metadata = {"salt": "dGVzdHNhbHQ="}  # Base64 encoded "testsalt"

        with pytest.raises(ValueError, match="ne peuvent pas être vides"):
            self.encryptor.decrypt_seedphrase(b"", self.test_password, metadata)

    def test_decrypt_missing_salt_raises_error(self):
        """Test que le déchiffrement sans sel dans les métadonnées échoue."""
        encrypted_data, _ = self.encryptor.encrypt_seedphrase(
            self.test_seedphrase, self.test_password
        )

        with pytest.raises(ValueError, match="sel manquant"):
            self.encryptor.decrypt_seedphrase(
                encrypted_data, self.test_password, {}
            )

    def test_save_and_load_encrypted_file(self):
        """Test la sauvegarde et le chargement de fichiers chiffrés."""
        # Chiffrer
        encrypted_data, metadata = self.encryptor.encrypt_seedphrase(
            self.test_seedphrase, self.test_password
        )

        # Sauvegarder dans un fichier temporaire
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".seedphrase"
        ) as tmp_file:
            tmp_filepath = tmp_file.name

        try:
            self.encryptor.save_encrypted_file(encrypted_data, metadata, tmp_filepath)

            # Charger le fichier
            loaded_encrypted, loaded_metadata = self.encryptor.load_encrypted_file(
                tmp_filepath
            )

            # Vérifier que les données sont identiques
            assert loaded_encrypted == encrypted_data
            assert loaded_metadata == metadata

            # Déchiffrer pour vérifier l'intégrité
            decrypted = self.encryptor.decrypt_seedphrase(
                loaded_encrypted, self.test_password, loaded_metadata
            )
            assert decrypted == self.test_seedphrase

        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(tmp_filepath):
                os.unlink(tmp_filepath)

    def test_load_invalid_file_raises_error(self):
        """Test que le chargement d'un fichier invalide lève une erreur."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt"
        ) as tmp_file:
            tmp_file.write("Invalid content")
            tmp_filepath = tmp_file.name

        try:
            with pytest.raises(ValueError, match="Format de fichier invalide"):
                self.encryptor.load_encrypted_file(tmp_filepath)
        finally:
            os.unlink(tmp_filepath)

    def test_validate_seedphrase_format_valid_12_words(self):
        """Test la validation d'une seed phrase de 12 mots."""
        seedphrase = " ".join(["word"] * 12)
        is_valid, message = self.encryptor.validate_seedphrase_format(seedphrase)

        assert is_valid is True
        assert message == "Format valide"

    def test_validate_seedphrase_format_valid_24_words(self):
        """Test la validation d'une seed phrase de 24 mots."""
        seedphrase = " ".join(["word"] * 24)
        is_valid, message = self.encryptor.validate_seedphrase_format(seedphrase)

        assert is_valid is True

    def test_validate_seedphrase_format_invalid_length(self):
        """Test la validation d'une seed phrase avec un nombre invalide de mots."""
        seedphrase = " ".join(["word"] * 10)
        is_valid, message = self.encryptor.validate_seedphrase_format(seedphrase)

        assert is_valid is False
        assert "10 mot(s)" in message

    def test_validate_seedphrase_format_invalid_characters(self):
        """Test la validation d'une seed phrase avec des caractères invalides."""
        seedphrase = "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
        is_valid, message = self.encryptor.validate_seedphrase_format(seedphrase)

        assert is_valid is False
        assert "caractères invalides" in message

    def test_encryption_deterministic_with_same_salt(self):
        """Test que le chiffrement avec le même sel produit des résultats différents."""
        # Chiffrer deux fois la même seed phrase
        encrypted_1, metadata_1 = self.encryptor.encrypt_seedphrase(
            self.test_seedphrase, self.test_password
        )
        encrypted_2, metadata_2 = self.encryptor.encrypt_seedphrase(
            self.test_seedphrase, self.test_password
        )

        # Les sels doivent être différents (générés aléatoirement)
        assert metadata_1["salt"] != metadata_2["salt"]

        # Les données chiffrées doivent être différentes
        assert encrypted_1 != encrypted_2

        # Mais les deux doivent se déchiffrer correctement
        decrypted_1 = self.encryptor.decrypt_seedphrase(
            encrypted_1, self.test_password, metadata_1
        )
        decrypted_2 = self.encryptor.decrypt_seedphrase(
            encrypted_2, self.test_password, metadata_2
        )

        assert decrypted_1 == self.test_seedphrase
        assert decrypted_2 == self.test_seedphrase
