from PIL import Image
import os
from random import uniform, choice, randint
from requests import get
from bs4 import BeautifulSoup as bsoup


def augumentation(directory, r=None, copy=1, rotate=40, width_strech=0.2, #create [copy] copies of images in [directory] using random params in range. [diff] let the diffrences to not be too small
                  height_strech=0.2, shear=0.3, horizontal_flip=True,
                  vertical_flip=False, diff=0.1):
    #########CHECK_ERRORS#################3

    if os.path.exists(os.path.join(os.getcwd(), directory)):
        directory = os.path.join(os.getcwd(), directory)

    else:
        raise FileNotFoundError("No such file or directory: \"{}\"".format(directory))

    #########

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(
                ".bmp"):
            for repeat in range(copy):
                image = Image.open(os.path.join(directory, filename)).copy()
                m_p = sorted(image.getcolors(maxcolors=256 * 256 * 256), key=lambda x: x[0])[-1][1]

                if width_strech or height_strech:  # rozciąganie
                    width, height = image.size
                   # print(width, height)
                    if width_strech:
                        width = randomize((1 - width_strech) * width, diff, width, (1 + width_strech) * width, t="i")

                    if height_strech:
                        height = randomize((1 - height_strech) * height, diff, height, (1 + height_strech) * height,
                                           t="i")
                    image = image.resize((width, height))

                if rotate:  # obracanie
                    angle = randomize(-rotate, diff, 0, rotate)
                    image = image.rotate(angle, fillcolor=m_p)

                if shear:  # przycinanie
                    width, height = image.size
                    print(width, height)

                    bounds = (randint(0, round((shear / 2) * width)), randint(0, round((shear / 2) * height)),
                              randint(round((1 - shear / 2) * width), width),
                              randint(round((1 - shear / 2) * height), height))
                    print(bounds)
                    image = image.crop(bounds)

                if horizontal_flip:  # obrót lewo prawo
                    if randint(0, 1):
                        image = image.transpose(method=Image.FLIP_LEFT_RIGHT)

                if vertical_flip:  # obrót góra dół
                    if randint(0, 1):
                        image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
                image.save(os.path.join(directory, f"a{repeat+1}{filename}"))

                image.close()


def randomize(small, diff, center, big, t="f"):  # zwraca losową licbę float z zakresu (small,(1-diff)*center) U ((1+deff)*center,big)
    # jest uczciwy dla symetrycznych przedziałów
    if t == "f":
        return choice([uniform(small, (1 - diff) * center), uniform((1 + diff) * center, big)])
    elif t == "i":
        return round(choice([uniform(small, (1 - diff) * center), uniform((1 + diff) * center, big)]))
    else:
        raise AttributeError("Parameter t must be \"f\" (float type) or \"i\" (int type)")


####################################################################

def google_download(word, directory):  # Download images of given word, good for debbuging

    gurl = "https://www.google.com/search?tbm=isch"

    def url_to_jpg(url, i, d):  # transform url to image an create file image{i}
        im = get(url)
        with open(os.path.join(d, "image{}.png".format(i)), "wb") as f:
           f.write(im.content)

    def word_to_url(w):  # returns google searched images urls of received word
        x = get(gurl, params={"q": w}).text
        with open("test.html", "w") as test:
            test.write(x)

        soup = bsoup(x, "html.parser")

        links = []
        for image in soup.findAll("img", class_="t0fcAb"):
            links.append(image['src'])

        return links

    t = word_to_url(word)
    for index, i in enumerate(t, start=1):
        url_to_jpg(i, index, directory)


if __name__ == "__main__":
    pass
