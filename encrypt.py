import pandas as pd #type :ignore
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Function to encrypt CSV data
def encrypt_csv(input_csv_path, output_enc_path, key):
    try:
        # Step 1: Read the CSV file with an encoding that handles non-UTF-8 characters
        df = pd.read_csv(input_csv_path, encoding='ISO-8859-1')  # Try using a different encoding if necessary
        
        # Step 2: Convert the DataFrame to a string (for encryption)
        csv_data = df.to_csv(index=False)
        
        # Step 3: Initialize AES cipher in CBC mode
        cipher = AES.new(key, AES.MODE_CBC)
        
        # Step 4: Pad the CSV data to match AES block size
        padded_data = pad(csv_data.encode(), AES.block_size)
        
        # Step 5: Encrypt the data
        encrypted_data = cipher.encrypt(padded_data)
        
        # Step 6: Write the encrypted data and IV (Initialization Vector) to a file
        with open(output_enc_path, 'wb') as file:
            # Write the initialization vector (IV) followed by the encrypted data
            file.write(cipher.iv + encrypted_data)
        
        print(f"File encrypted and saved to {output_enc_path}")
    
    except Exception as e:
        print(f"Error encrypting file: {e}")

# Function to decrypt CSV data
def decrypt_csv(input_enc_path, output_dec_path, key):
    try:
        # Step 1: Read the encrypted file
        with open(input_enc_path, 'rb') as file:
            # Read the IV (Initialization Vector) and encrypted data
            iv = file.read(16)  # AES block size is 16 bytes for CBC mode
            encrypted_data = file.read()
        
        # Step 2: Initialize AES cipher with the IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Step 3: Decrypt the data
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        # Step 4: Convert the decrypted data back to a string
        decrypted_csv = decrypted_data.decode()
        
        # Step 5: Write the decrypted CSV data back to a new file
        with open(output_dec_path, 'w') as file:
            file.write(decrypted_csv)
        
        print(f"File decrypted and saved to {output_dec_path}")
    
    except Exception as e:
        print(f"Error decrypting file: {e}")

# Generate a 256-bit AES key
key = os.urandom(32)

# Encrypt and decrypt two CSV files (example paths)
input_csv_path_1 = 'energy_dataset.csv'  # Replace with actual path
input_csv_path_2 = 'weather_features.csv'  # Replace with actual path
output_enc_path_1 = 'energy_dataset_encrypted.enc'
output_enc_path_2 = 'weather_features_encrypted.enc'
output_dec_path_1 = 'energy_dataset_decrypted.csv'
output_dec_path_2 = 'weather_features_decrypted.csv'

# Encrypt CSV files
encrypt_csv(input_csv_path_1, output_enc_path_1, key)
encrypt_csv(input_csv_path_2, output_enc_path_2, key)

# Decrypt CSV files to check if everything is working
decrypt_csv(output_enc_path_1, output_dec_path_1, key)
decrypt_csv(output_enc_path_2, output_dec_path_2, key)
