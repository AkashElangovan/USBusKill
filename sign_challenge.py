from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import hashlib
import base64
from cryptography.fernet import Fernet
import subprocess

def decrypt_key(encrypted_key, serial_number):
    key = hashlib.sha256(serial_number.encode()).digest()
    cipher = Fernet(base64.urlsafe_b64encode(key))
    return cipher.decrypt(encrypted_key)

# Get USB volume serial number
def get_volume_serial_number(drive_letter):
    # Run the 'vol' command to get the volume serial number
    result = subprocess.run(f"vol {drive_letter}:", capture_output=True, text=True, shell=True)
    output = result.stdout
    # Extract the serial number from the output
    for line in output.splitlines():
        if "Serial Number" in line:
            return line.split()[-1]
    return None

# Specify the drive letter of the USB drive
drive_letter = "D"  # Replace with the correct drive letter

# Get the volume serial number
serial_number = get_volume_serial_number(drive_letter)
if not serial_number:
    raise Exception("Volume serial number not found!")

# Load encrypted private key
with open(f'{drive_letter}:/encrypted_private_key.pem', 'rb') as f:
    encrypted_key = f.read()

# Decrypt private key
private_key = serialization.load_pem_private_key(
    decrypt_key(encrypted_key, serial_number),
    password=None
)

# Read the challenge from the PC
with open(f'{drive_letter}:/challenge.bin', 'rb') as f:
    challenge = f.read()

# Sign the challenge
signature = private_key.sign(
    challenge,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Save the signed response
with open(f'{drive_letter}:/signed_response.bin', 'wb') as f:
    f.write(signature)

print("Challenge signed and response saved.")