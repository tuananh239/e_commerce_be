
# ===========================================================================================
# AESHelper
# Dev: anh.vu
# ===========================================================================================

# ===========================================================================================

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ===========================================================================================

SECOND = "SECOND"
MILISECOND = "MILISECOND"

# ===========================================================================================

key = b'\x1f\x88V_\xd3%#\x8e\xdb&\x802\x1b\xbb\x8d_'

# Main class ================================================================================
class AESHelper():
    """
        Class này triển khai các phương thức hỗ trợ cho việc mã hóa và giải mã AES
    """

    @staticmethod
    def encrypt_image(image_data, output_path):
        cipher = AES.new(key, AES.MODE_CBC)

        ct_bytes = cipher.encrypt(pad(image_data, AES.block_size))

        with open(output_path, 'wb') as out_file:
            out_file.write(cipher.iv)
            out_file.write(ct_bytes)
    

    @staticmethod
    def decrypt_image(encrypted_data):
        iv = encrypted_data[:16]
        ct_bytes = encrypted_data[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv)

        decrypted_data = unpad(cipher.decrypt(ct_bytes), AES.block_size)

        return decrypted_data