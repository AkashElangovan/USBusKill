
<div align="center">
  
# USBusKill
  
</div>

## Description

This repository hosts a simple Proof of Concept for a "BusKill" mechanism. The core idea is to automatically lock a computer when a specific USB drive is removed, enhancing physical security. The provided scripts and files simulate a challenge-response authentication system with encryption to prevent unauthorized access.

## Features

*   **USB Monitoring:** Continuously monitors for insertion and removal of a designated USB drive.
*   **Automatic Locking:** Locks the workstation upon USB drive removal.
*   **Challenge-Response:** Implements a cryptographic challenge-response system for USB verification.
*   **Key Encryption:** Encrypts the private key stored on the USB drive using the drive's serial number.
*   **Logging:** Records USB insertion and removal events.

## Table of Contents

*   [Description](#description)
*   [Features](#features)
*   [Installation](#installation)
*   [Usage](#usage)
*   [Dependencies](#dependencies)
*   [Contribution](#contribution)
*   [License](#license)
*   [Contact](#contact)

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/AkashElangovan/USBusKill.git
    cd USBusKill
    ```

2.  Install the required dependencies:

    ```bash
    pip install cryptography wmi
    ```

## Usage

1.  **Generate Keys:** Generate a public and private key pair for the USB authentication. Example keys are provided, but it is highly recommended to generate your own for security.
2.  **Encrypt Private Key:** Run `encrypt_private_key.py` to encrypt the private key using the USB drive's serial number.
    *   Modify the `drive_letter` variable in the script to match the drive letter of your USB drive.
    *   Place the `private_key.pem` file in the same directory as the script.

    ```bash
    python encrypt_private_key.py
    ```

3.  **Place Files on USB:** The `encrypt_private_key.py` script automatically saves the `encrypted_private_key.pem` to the root directory of your specified USB drive.

4.  **Monitor USB:** Run `monitor_usb.py` to monitor the USB drive.  The script will lock the computer when the drive is removed.
    *   Modify the `get_usb_drive_letter()` function in the script to correctly identify your USB drive.

    ```bash
    python monitor_usb.py
    ```

5.  **Verification:** Run `verify_usb.py` to simulate the USB verification process.
    *   This script generates a challenge, writes it to the USB drive, waits for a signed response, and verifies the signature.

    ```bash
    python verify_usb.py
    ```

**Important Considerations:**

*   The `monitor_usb.py` script must be running for the auto-lock feature to work.
*   Ensure the USB drive letter is correctly configured in all scripts.
*   The provided scripts are for demonstration purposes; adapt them to your specific security requirements.

## Dependencies

*   **Python 3.x**
*   **cryptography:** For cryptographic operations (encryption, signing, verification).
*   **wmi:** For monitoring USB device events on Windows.

## Contribution

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Submit a pull request with a clear description of your changes.


```
