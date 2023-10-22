from lib.Crypto.PublicKey import RSA
from lib.Crypto.Cipher import PKCS1_OAEP
import zlib
import base64
from PIL import Image


class LSB_RSA_watermark:
    def __init__(self):
        pass

    def encrypt_blob(self, blob, public_key):
        rsa_key = RSA.importKey(public_key)
        rsa_key = PKCS1_OAEP.new(rsa_key)
        blob = zlib.compress(blob)
        chunk_size = 470
        offset = 0
        end_loop = False
        encrypted = ""
        while not end_loop:
            chunk = blob[offset:offset + chunk_size]
            if len(chunk) % chunk_size != 0:
                end_loop = True
                chunk += bytes(" " * (chunk_size - len(chunk)), 'utf-8')
            encrypted += str(rsa_key.encrypt(chunk))
            offset += chunk_size
        return base64.b64encode(encrypted.encode('ascii'))

    def embed_image(self, img1, encrypted_watermark):
        # Convert the image to RGBA mode if it's not already
        img1 = img1.convert('RGBA')

        # Get the data of the image
        data = img1.getdata()

        # Create a new list to hold the new pixel values
        new_data = []

        # Iterate over the pixels in the image
        for pixel in data:
            # Perform a bitwise OR operation between the pixel values and the encrypted watermark
            new_pixel = tuple(pixel[i] | encrypted_watermark[i]
                              for i in range(4))

            # Append the new pixel value to the new data
            new_data.append(new_pixel)

        # Put the new data into the image
        img1.putdata(new_data)

        return img1

    def decrypt_blob(self, blob, private_key):
        rsa_key = RSA.importKey(private_key)
        rsa_key = PKCS1_OAEP.new(rsa_key)
        blob = base64.b64decode(blob)
        chunk_size = 470
        offset = 0
        end_loop = False
        decrypted = ""
        while not end_loop:
            chunk = blob[offset:offset + chunk_size]
            if len(chunk) % chunk_size != 0:
                end_loop = True
                chunk += bytes(" " * (chunk_size - len(chunk)), 'utf-8')
            decrypted += str(rsa_key.decrypt(chunk))
            offset += chunk_size
        return zlib.decompress(decrypted)

    def extract_image(self, img):
        # Convert the image to RGBA mode if it's not already
        img = img.convert('RGBA')

        # Get the data of the image
        data = img.getdata()

        # Create a new list to hold the new pixel values
        new_data = []

        # Iterate over the pixels in the image
        for pixel in data:
            # Perform a bitwise AND operation between the pixel values and 255
            new_pixel = tuple(pixel[i] & 255 for i in range(4))

            # Append the new pixel value to the new data
            new_data.append(new_pixel)

        # Put the new data into the image
        img.putdata(new_data)

        return img


background = Image.open("../assets/black_cat.jpg")
watermark = Image.open("../assets/a_watermark.png")

public_rsa = open("./keys/rsa_public.pub", 'rb')
private_rsa = open("./keys/rsa_private.pem", 'rb')

LSB_RSA = LSB_RSA_watermark()
encrypted_watermark = LSB_RSA.encrypt_blob(
    watermark.tobytes(), public_rsa.read())
embedded_watermark_image = LSB_RSA.embed_image(background, encrypted_watermark)
embedded_watermark_image.save('embedded.png')
watermark = Image.open("embedded.png")
extracted_image = LSB_RSA.extract_image(watermark)
extracted_image.save("extracted.png")


public_rsa.close()
private_rsa.close()
