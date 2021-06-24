from PIL import Image
import os


def transparent(filename):
    """
    changes colors of photo mask.

    Parameters
    ----------
    filename
        name of file
    
    """
    img = Image.open('folium_test/data/mask_png/' + filename)
    img = img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    pngName = filename.split("_")
    pngYear = pngName[4][:4]
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (255, 255, 255, 0)

            if pngYear == "2017":
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (0, 245, 212, 255)
            elif pngYear == "2018":
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (0, 187, 249, 255)
            elif pngYear == "2019":
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (241, 91, 181, 255)

    img.save("folium_test/data/x/" + filename, "PNG")


if __name__ == "__main__":

    for filename in os.listdir("folium_test/data/mask_png"):
        if filename.endswith(".png"):
            transparent(filename)
        else:
            continue
