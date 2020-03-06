"""Creates QR class"""
# Acknowledgement
# This code is adapted from:
# https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
# & Matthew Bolger
import time
# Disable pylint error about packages not being found locally
# pylint: disable=E0401
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar

# pylint: disable=R0903
class QR:
    """This module handles QR Code scanning to allow for the returning of books."""
    @staticmethod
    def scan_qr():
        """Scans a QR Code and returns the data from it

        Returns:
            str: Returns the contents of the QR Code as a string."""

        print("Preparing camera...")
        video_stream = VideoStream(src=0).start()
        time.sleep(2.0)
        print("Camera ready! Please scan your book.")
        loop = True

        while loop == True:
            frame = video_stream.read()
            frame = imutils.resize(frame, width=400)

            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                book_scanned = barcode_data

                if book_scanned != "":
                    loop = False
        
        video_stream.stop()

        return book_scanned
