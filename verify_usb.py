import os
import time
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import subprocess

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

# Load public key
with open('public_key.pem', 'rb') as f:
    public_key = serialization.load_pem_public_key(f.read())

# Generate a random challenge
challenge = os.urandom(32)  # 32 bytes = 256 bits

# Write the challenge to the USB drive
with open(f'{drive_letter}:/challenge.bin', 'wb') as f:
    f.write(challenge)

print("Challenge written to USB drive. Waiting for signed response...")

# Wait for the signed response to appear
signed_response_path = f'{drive_letter}:/signed_response.bin'
while not os.path.exists(signed_response_path):
    time.sleep(1)  # Check every second

# Read the signed response from the USB drive
with open(signed_response_path, 'rb') as f:
    signed_response = f.read()

# Verify the signature
try:
    public_key.verify(
        signed_response,
        challenge,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("USB Verified! Access granted.")
except Exception:
    print("USB Verification Failed! Locking system...")
    os.system("rundll32.exe user32.dll,LockWorkStation")  # Lock the system