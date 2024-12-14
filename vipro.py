import cv2


def get_video_capture(source=0):
    """
    Menginisialisasi video capture dari sumber (kamera atau file).

    Parameters:
        source (int atau str): Jika integer, sumber adalah ID kamera (default: 0). 
                               Jika string, sumber adalah path file video.

    Returns:
        cap (cv2.VideoCapture): Objek video capture.
    """
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise Exception("Tidak bisa membuka video capture!")
    return cap


def draw_roi(frame, rppg_roi, resp_roi):
    """
    Menambahkan kotak ROI (Region of Interest) pada frame video.

    Parameters:
        frame (array): Frame video yang akan digambar.
        rppg_roi (tuple): ROI untuk rPPG (x, y, w, h).
        resp_roi (tuple): ROI untuk respirasi (x, y, w, h).

    Returns:
        frame (array): Frame dengan kotak ROI digambar.
    """
    # Gambar ROI untuk rPPG
    x1, y1, w1, h1 = rppg_roi
    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

    # Gambar ROI untuk Respirasi
    x2, y2, w2, h2 = resp_roi
    cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)

    return frame
