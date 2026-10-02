from PIL import Image

MARQUEUR = "#####"

def cacher_message(image_path, message, save_path):
    if not message:
        return False, "Message vide"

    secret = message + MARQUEUR
    binary_msg = ''.join(format(ord(c), '08b') for c in secret)

    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    # Vérification capacité
    if len(binary_msg) > width * height * 3:
        return False, "Message trop long pour cette image"

    data_idx = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            rgb = [r, g, b]

            for i in range(3):
                if data_idx < len(binary_msg):
                    rgb[i] = (rgb[i] & ~1) | int(binary_msg[data_idx])
                    data_idx += 1

            pixels[x, y] = tuple(rgb)

            if data_idx >= len(binary_msg):
                break
        if data_idx >= len(binary_msg):
            break

    img.save(save_path, "PNG")
    return True, "Message caché avec succès"


def extraire_message(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size

        binary_data = ""

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)

        decoded_text = ""

        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) < 8:
                break

            decoded_text += chr(int(byte, 2))

            if decoded_text.endswith(MARQUEUR):
                return True, decoded_text[:-len(MARQUEUR)]

        return False, "Aucun message trouvé"

    except Exception as e:
        return False, f"Erreur : {e}"