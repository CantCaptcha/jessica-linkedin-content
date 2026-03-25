#!/usr/bin/env python3
"""
Secure Password Manager - AES-256-GCM Encrypted

This script encrypts and decrypts password files using strong encryption.
Only you (with the master password) can access the passwords.
"""

import sys
import os
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Configuration
PASSWORD_FILE = Path.home() / '.openclaw' / 'workspace' / 'secrets' / 'passwords.enc'
WORKSPACE = Path.home() / '.openclaw' / 'workspace'

def generate_key(password: str, salt: bytes = None) -> tuple:
    """
    Generate a Fernet key from a password.

    Args:
        password: User's master password
        salt: Optional salt for key derivation

    Returns:
        tuple: (fernet_key, salt)
    """
    if salt is None:
        salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(
        kdf.derive(password.encode())
    )

    return key, salt

def encrypt_passwords(password: str, data: str) -> bytes:
    """
    Encrypt passwords with Fernet.

    Args:
        password: User's master password
        data: Plaintext data to encrypt

    Returns:
        bytes: Encrypted data (includes salt and IV)
    """
    # Generate key
    key, salt = generate_key(password)

    # Initialize Fernet with key
    fernet = Fernet(key)

    # Encrypt
    encrypted = fernet.encrypt(data.encode())

    # Combine salt + encrypted data
    result = salt + encrypted

    return result

def decrypt_passwords(password: str, encrypted_data: bytes) -> str:
    """
    Decrypt passwords with Fernet.

    Args:
        password: User's master password
        encrypted_data: Encrypted data (salt + ciphertext)

    Returns:
        str: Decrypted plaintext
    """
    # Extract salt and encrypted data
    salt = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    # Generate key from password and salt
    key, _ = generate_key(password, salt)

    # Initialize Fernet with key
    fernet = Fernet(key)

    # Decrypt
    decrypted = fernet.decrypt(ciphertext)

    return decrypted.decode()

def init_password_file():
    """Initialize encrypted password file."""
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    WORKSPACE / 'secrets' / 'passwords.enc'
    PASSWORD_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("🔐 Create your master password")
    password = input("Enter master password: ")
    confirm = input("Confirm master password: ")

    if password != confirm:
        print("❌ Passwords don't match!")
        sys.exit(1)

    if len(password) < 8:
        print("❌ Password must be at least 8 characters!")
        sys.exit(1)

    # Initialize with empty file
    encrypted = encrypt_passwords(password, "")
    PASSWORD_FILE.write_bytes(encrypted)

    print("✓ Password file created!")
    print(f"  Location: {PASSWORD_FILE}")
    print("  Use 'add' command to add passwords, 'get' to retrieve them")

def add_password(master_password: str, service: str, username: str, account: str, stored_password: str):
    """
    Add a password to the encrypted file.

    Args:
        master_password: Master password for encryption
        service: Service name (e.g., 'gmail', 'github')
        username: Username or email
        account: Account identifier (optional)
        stored_password: The password to store
    """
    # Decrypt existing data
    encrypted_data = PASSWORD_FILE.read_bytes()
    data = decrypt_passwords(master_password, encrypted_data)

    # Parse existing entries
    entries = []
    if data:
        entries = [e.strip() for e in data.split('\n') if e.strip()]

    # Add new entry
    entry = f"{service}:{username}:{account}:{stored_password}"
    entries.append(entry)

    # Re-encrypt
    new_data = '\n'.join(entries)
    encrypted = encrypt_passwords(master_password, new_data)
    PASSWORD_FILE.write_bytes(encrypted)

    print(f"✓ Added password for {service}")

def get_password(password: str, service: str, username: str):
    """
    Retrieve a password from the encrypted file.

    Args:
        password: Master password
        service: Service name
        username: Username or email
    """
    # Decrypt existing data
    encrypted_data = PASSWORD_FILE.read_bytes()
    data = decrypt_passwords(password, encrypted_data)

    # Parse entries
    entries = [e.strip() for e in data.split('\n') if e.strip()]

    # Find matching entry
    for entry in entries:
        parts = entry.split(':')
        if len(parts) >= 3:
            if parts[0] == service and parts[1] == username:
                account = parts[2] if len(parts) > 2 else ""
                pwd = parts[3] if len(parts) > 3 else ""

                if pwd:
                    print(f"✓ Password for {service} ({username})")
                    print(f"  Account: {account}")
                    print(f"  Password: {pwd}")
                    return pwd
                else:
                    print(f"⚠️  No password found for {service} ({username})")
                    return None

    print(f"❌ No password found for {service} ({username})")
    return None

def list_passwords(password: str):
    """
    List all stored passwords.

    Args:
        password: Master password
    """
    encrypted_data = PASSWORD_FILE.read_bytes()
    data = decrypt_passwords(password, encrypted_data)

    if not data:
        print("✓ No passwords stored")
        return

    entries = [e.strip() for e in data.split('\n') if e.strip()]

    print("📋 Stored Passwords:")
    for entry in entries:
        parts = entry.split(':')
        if len(parts) >= 2:
            service = parts[0]
            username = parts[1]
            print(f"  • {service}: {username}")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 password_manager.py init       - Create password file")
        print("  python3 password_manager.py add <args> - Add password")
        print("  python3 password_manager.py get <args> - Get password")
        print("  python3 password_manager.py list       - List all passwords")
        sys.exit(1)

    command = sys.argv[1]

    # Get master password (for commands that need it)
    password = None
    if command in ['add', 'get', 'list']:
        if not PASSWORD_FILE.exists():
            print("❌ Password file not found! Run 'init' first.")
            sys.exit(1)

        print("🔐 Enter master password:")
        password = input("> ")

    # Initialize
    if command == 'init':
        init_password_file()

    # Add password
    elif command == 'add':
        if len(sys.argv) < 5:
            print("Usage: python3 password_manager.py add <service> <username> [account] [password]")
            sys.exit(1)

        service = sys.argv[2]
        username = sys.argv[3]
        account = sys.argv[4] if len(sys.argv) > 4 else ""
        pwd = sys.argv[5] if len(sys.argv) > 5 else ""

        if not pwd:
            pwd = input("Enter password: ")

        add_password(password, service, username, account, pwd)

    # Get password
    elif command == 'get':
        if len(sys.argv) < 4:
            print("Usage: python3 password_manager.py get <service> <username>")
            sys.exit(1)

        service = sys.argv[2]
        username = sys.argv[3]
        get_password(password, service, username)

    # List passwords
    elif command == 'list':
        list_passwords(password)

    else:
        print(f"❌ Unknown command: {command}")

if __name__ == '__main__':
    main()
