from appJar import gui
from PIL import Image, ImageTk
import cv2
import platform
import os
import pyqrcode


def reset():
    photo = ImageTk.PhotoImage(Image.open("lightrail.png"))
    app.reloadImageData("pic", photo, fmt="PhotoImage")
    app.setEntry("input_output", "")


def scan():
    scanned_qr = read_qr_with_camera()
    app.setEntry("input_output", scanned_qr)
    change_qr(scanned_qr)


def generate():
    qr_string = app.getEntry("input_output")
    change_qr(qr_string)


def change_qr(qr_string):
    qr_data = pyqrcode.create(qr_string)
    qr_data.png('temp_generated.png', scale=5)
    im = Image.open('temp_generated.png')
    width, height = im.size
    # print(f"The image is {width} by {height}")
    # TODO: too big? if w/h > etc...
    app.setImageSize("pic", width, height)

    photo = ImageTk.PhotoImage(Image.open("temp_generated.png"))

    # finally
    app.reloadImageData("pic", photo, fmt="PhotoImage")


def read_qr_with_camera():
    # Read the key
    if platform.system() == "Windows":
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # adding the ,cv2.CAP_DSHOW fixed it!!!!!!!
    else:
        cam = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cam.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            # return data
            # print("QR Code detected-->", data)
            break
        cv2.imshow("QR Reader - Press ESC to Exit", img)
        # if cv2.waitKey(1) == ord("q"): (this is the old way - next line allows esc or Q/q
        ch = cv2.waitKey(1)
        if ch == 27 or ch == ord('q') or ch == ord('Q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    # Convert the scanned data to a dictionary!
    return data


with gui("LightRail v0.1", "550x550", bg='#282828', fg="white",
         font={'size': 16, 'family': "Roboto Light"}) as app:
    app.enableEnter(generate)
    app.setPadding([10, 10])
    app.setInPadding([10, 10])
    if not os.path.exists("lightrail.png"):
        qr_data = pyqrcode.create("Lightrail QR")
        qr_data.png('lightrail.png', scale=5)
    photo = ImageTk.PhotoImage(Image.open("lightrail.png"))
    app.addImageData("pic", photo, fmt="PhotoImage")
    app.label("status", "LightRail", font={'size': 20, 'family': "Roboto Light"})
    app.entry("input_output", label=False, focus=True)
    app.setLabelFg("status", "white")
    app.setButtonFont(family="Roboto Light", size=20)
    app.buttons(["Generate", "Scan", "Reset", "Quit"], [generate, scan, reset, app.stop])
