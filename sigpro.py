from scipy.signal import butter, filtfilt
import numpy as np


def butter_bandpass(lowcut, highcut, fs, order=5):
    """
    Membuat filter bandpass menggunakan fungsi butter dari SciPy.

    Parameters:
        lowcut (float): Frekuensi cutoff bawah.
        highcut (float): Frekuensi cutoff atas.
        fs (float): Sampling rate.
        order (int): Orde filter.

    Returns:
        tuple: Koefisien b dan a dari filter.
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a


def bandpass_filter(data, lowcut, highcut, fs, order=5, axis=0):
    """
    Menerapkan filter bandpass pada data.

    Parameters:
        data (array): Data yang akan difilter.
        lowcut (float): Frekuensi cutoff bawah.
        highcut (float): Frekuensi cutoff atas.
        fs (float): Sampling rate.
        order (int): Orde filter.
        axis (int): Axis untuk filtering.

    Returns:
        array: Data setelah difilter.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return filtfilt(b, a, data, axis=axis)


def extract_rppg_and_respiration(frame, rppg_roi, resp_roi):
    """
    Ekstrak sinyal rPPG dan respirasi dari frame berdasarkan ROI.

    Parameters:
        frame (array): Frame input (grayscale).
        rppg_roi (tuple): ROI untuk rPPG (x, y, w, h).
        resp_roi (tuple): ROI untuk respirasi (x, y, w, h).

    Returns:
        tuple: Sinyal rPPG dan sinyal respirasi.
    """
    h, w = frame.shape[:2]

    # Validasi ROI untuk rPPG
    x1, y1, w1, h1 = rppg_roi
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x1 + w1), min(h, y1 + h1)
    rppg_signal = np.mean(frame[y1:y2, x1:x2], axis=(0, 1))

    # Validasi ROI untuk Respirasi
    x1, y1, w1, h1 = resp_roi
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x1 + w1), min(h, y1 + h1)
    resp_signal = np.mean(frame[y1:y2, x1:x2], axis=(0, 1))

    return rppg_signal, resp_signal
