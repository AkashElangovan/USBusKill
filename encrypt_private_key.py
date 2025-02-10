import hashlib
import base64
from cryptography.fernet import Fernet
import subprocess

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

def encrypt_key(private_key, serial_number):
    key = hashlib.sha256(serial_number.encode()).digest()
    cipher = Fernet(base64.urlsafe_b64encode(key))
    return cipher.encrypt(private_key)

# Load private key
with open('private_key.pem', 'rb') as f:
    private_key = f.read()

# Encrypt private key
encrypted_key = encrypt_key(private_key, serial_number)

# Save encrypted key to USB drive
with open(f'{drive_letter}:/encrypted_private_key.pem', 'wb') as f:
    f.write(encrypted_key)

print("Private key encrypted and saved to USB drive.")