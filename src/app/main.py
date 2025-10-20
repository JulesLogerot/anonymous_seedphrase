"""
Application Streamlit pour le chiffrement et déchiffrement de seed phrases.

Cette application permet de chiffrer et déchiffrer de manière sécurisée
les seed phrases de portefeuilles de cryptomonnaies.
"""

import io
import os
import sys
import tempfile
from pathlib import Path

import streamlit as st
from cryptography.fernet import InvalidToken

# Ajouter le répertoire parent au path pour importer le module crypto
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.crypto.encryption import SeedPhraseEncryptor


def init_session_state():
    """Initialise les variables de session."""
    if "encrypted_data" not in st.session_state:
        st.session_state.encrypted_data = None
    if "metadata" not in st.session_state:
        st.session_state.metadata = None
    if "decrypted_seedphrase" not in st.session_state:
        st.session_state.decrypted_seedphrase = None


def main():
    """Fonction principale de l'application."""
    # Configuration de la page
    st.set_page_config(
        page_title="Anonymous Seedphrase Encryptor",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    init_session_state()

    # En-tête
    st.title("🔐 Anonymous Seedphrase Encryptor")
    st.markdown(
        """
        Chiffrez et sécurisez vos seed phrases de cryptomonnaies avec un chiffrement AES-128.

        **Sécurité** : Vos données sont chiffrées localement et ne sont jamais envoyées sur un serveur.
        """
    )

    # Avertissement de sécurité
    st.warning(
        """
        ⚠️ **Avertissements importants :**
        - Ne partagez JAMAIS votre seed phrase avec qui que ce soit
        - Conservez plusieurs copies de votre fichier chiffré dans des endroits sûrs
        - N'oubliez PAS votre mot de passe - il ne peut pas être récupéré
        - Testez d'abord avec une seed phrase de test avant d'utiliser vos vraies seed phrases
        """
    )

    st.markdown("---")

    # Créer deux onglets
    tab1, tab2 = st.tabs(["🔒 Chiffrer une seed phrase", "🔓 Déchiffrer une seed phrase"])

    encryptor = SeedPhraseEncryptor()

    # ========== ONGLET 1 : CHIFFREMENT ==========
    with tab1:
        st.header("Chiffrer votre seed phrase")

        st.markdown(
            """
            Entrez votre seed phrase et un mot de passe fort pour la chiffrer.
            Vous pourrez ensuite télécharger le fichier chiffré.
            """
        )

        # Zone de texte pour la seed phrase
        seedphrase_input = st.text_area(
            "Seed phrase",
            height=100,
            placeholder="Entrez votre seed phrase (12, 15, 18, 21 ou 24 mots séparés par des espaces)",
            help="Entrez les mots de votre seed phrase séparés par des espaces",
        )

        # Champ mot de passe
        password_encrypt = st.text_input(
            "Mot de passe de chiffrement",
            type="password",
            help="Choisissez un mot de passe fort (minimum 8 caractères). N'oubliez pas ce mot de passe !",
        )

        # Confirmation du mot de passe
        password_encrypt_confirm = st.text_input(
            "Confirmez le mot de passe",
            type="password",
            help="Entrez à nouveau le mot de passe",
        )

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            encrypt_button = st.button("🔒 Chiffrer", type="primary", use_container_width=True)

        # Bouton de chiffrement
        if encrypt_button:
            # Validations
            if not seedphrase_input.strip():
                st.error("❌ Veuillez entrer une seed phrase")
            elif not password_encrypt:
                st.error("❌ Veuillez entrer un mot de passe")
            elif password_encrypt != password_encrypt_confirm:
                st.error("❌ Les mots de passe ne correspondent pas")
            else:
                # Valider le format de la seed phrase
                is_valid, message = encryptor.validate_seedphrase_format(seedphrase_input)

                if not is_valid:
                    st.error(f"❌ {message}")
                else:
                    try:
                        # Chiffrer la seed phrase
                        with st.spinner("Chiffrement en cours..."):
                            encrypted_data, metadata = encryptor.encrypt_seedphrase(
                                seedphrase_input, password_encrypt
                            )

                        # Stocker dans la session
                        st.session_state.encrypted_data = encrypted_data
                        st.session_state.metadata = metadata

                        st.success("✅ Seed phrase chiffrée avec succès !")
                        st.info(f"📊 Métadonnées : {metadata['algorithm']}")

                    except ValueError as e:
                        st.error(f"❌ Erreur : {e}")
                    except Exception as e:
                        st.error(f"❌ Erreur inattendue : {e}")

        # Bouton de téléchargement (si données chiffrées disponibles)
        if st.session_state.encrypted_data is not None:
            st.markdown("---")
            st.success("✅ Fichier prêt à être téléchargé")

            # Créer un fichier temporaire pour le téléchargement
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".seedphrase"
            ) as tmp_file:
                encryptor.save_encrypted_file(
                    st.session_state.encrypted_data,
                    st.session_state.metadata,
                    tmp_file.name,
                )
                tmp_filepath = tmp_file.name

            # Lire le fichier pour le téléchargement
            with open(tmp_filepath, "rb") as f:
                file_bytes = f.read()

            # Nettoyer le fichier temporaire
            os.unlink(tmp_filepath)

            with col2:
                st.download_button(
                    label="📥 Télécharger le fichier chiffré",
                    data=file_bytes,
                    file_name="encrypted_seedphrase.seedphrase",
                    mime="application/json",
                    use_container_width=True,
                )

            st.info(
                """
                📌 **Conseils de sécurité :**
                - Sauvegardez ce fichier dans plusieurs endroits sûrs (clé USB, cloud chiffré, etc.)
                - Notez votre mot de passe séparément et conservez-le en sécurité
                - Testez le déchiffrement avant d'effacer votre seed phrase originale
                """
            )

    # ========== ONGLET 2 : DÉCHIFFREMENT ==========
    with tab2:
        st.header("Déchiffrer votre seed phrase")

        st.markdown(
            """
            Uploadez votre fichier chiffré et entrez le mot de passe pour récupérer votre seed phrase.
            """
        )

        # Upload du fichier
        uploaded_file = st.file_uploader(
            "Fichier chiffré",
            type=["seedphrase", "json"],
            help="Sélectionnez le fichier .seedphrase que vous avez téléchargé lors du chiffrement",
        )

        # Champ mot de passe
        password_decrypt = st.text_input(
            "Mot de passe de déchiffrement",
            type="password",
            help="Entrez le mot de passe que vous avez utilisé pour chiffrer la seed phrase",
            key="password_decrypt",
        )

        # Bouton de déchiffrement
        decrypt_button = st.button("🔓 Déchiffrer", type="primary")

        if decrypt_button:
            if uploaded_file is None:
                st.error("❌ Veuillez uploader un fichier chiffré")
            elif not password_decrypt:
                st.error("❌ Veuillez entrer le mot de passe")
            else:
                try:
                    # Sauvegarder temporairement le fichier uploadé
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".seedphrase"
                    ) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_filepath = tmp_file.name

                    # Charger et déchiffrer
                    with st.spinner("Déchiffrement en cours..."):
                        encrypted_data, metadata = encryptor.load_encrypted_file(
                            tmp_filepath
                        )

                        decrypted_seedphrase = encryptor.decrypt_seedphrase(
                            encrypted_data, password_decrypt, metadata
                        )

                    # Nettoyer le fichier temporaire
                    os.unlink(tmp_filepath)

                    # Stocker dans la session
                    st.session_state.decrypted_seedphrase = decrypted_seedphrase

                    st.success("✅ Seed phrase déchiffrée avec succès !")

                except InvalidToken:
                    st.error(
                        "❌ Mot de passe incorrect ou fichier corrompu. Veuillez réessayer."
                    )
                except ValueError as e:
                    st.error(f"❌ Erreur : {e}")
                except Exception as e:
                    st.error(f"❌ Erreur inattendue : {e}")

        # Afficher la seed phrase déchiffrée (si disponible)
        if st.session_state.decrypted_seedphrase is not None:
            st.markdown("---")
            st.success("✅ Voici votre seed phrase déchiffrée :")

            # Afficher dans un code block pour faciliter la copie
            st.code(st.session_state.decrypted_seedphrase, language=None)

            # Bouton pour copier dans le presse-papier
            if st.button("📋 Copier dans le presse-papier"):
                st.write(
                    """
                    <script>
                    navigator.clipboard.writeText('"""
                    + st.session_state.decrypted_seedphrase
                    + """');
                    </script>
                    """,
                    unsafe_allow_html=True,
                )
                st.info("✅ Copié ! (utilisez Ctrl+C / Cmd+C manuellement si nécessaire)")

            st.warning(
                """
                ⚠️ **Attention :**
                - Notez cette seed phrase immédiatement
                - Ne la partagez avec personne
                - Fermez cette page une fois la seed phrase notée
                - Assurez-vous que personne ne regarde par-dessus votre épaule
                """
            )

            # Bouton pour effacer de la mémoire
            if st.button("🗑️ Effacer la seed phrase de l'écran", type="secondary"):
                st.session_state.decrypted_seedphrase = None
                st.rerun()

    # Pied de page
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>🔐 Anonymous Seedphrase Encryptor v1.0</p>
            <p style='font-size: 0.8em;'>
                Chiffrement : Fernet (AES-128-CBC + HMAC) |
                Dérivation de clé : PBKDF2-HMAC-SHA256 (600,000 itérations)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
