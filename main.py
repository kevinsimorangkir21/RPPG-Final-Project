import cv2
import numpy as np
import matplotlib.pyplot as plt
from sigpro import bandpass_filter, extract_rppg_and_respiration
from vipro import get_video_capture, draw_roi, detect_face

# Konfigurasi
fs = 30  # Sampling rate
lowcut_rppg, highcut_rppg = 0.7, 4.0  # Frekuensi rPPG
lowcut_resp, highcut_resp = 0.1, 0.5  # Frekuensi respirasi
signal_length = fs * 10  # Simpan data selama 10 detik
rppg_data = []
resp_data = []

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1)

# Inisialisasi Video dan Deteksi Wajah
cap = get_video_capture()
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ROI Awal
rppg_roi = (100, 100, 300, 300)  # x, y, w, h
resp_roi = (400, 400, 300, 300)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Konversi frame ke grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Deteksi wajah
        face = detect_face(gray, face_cascade)
        if face is not None:
            x, y, w, h = face
            rppg_roi = (x, y * 2, w, int(h / 2))  # Bagian atas wajah untuk rPPG
            # Bagian bawah wajah untuk respirasi
            resp_roi = (x - 125, y * 2 + int(h / 2), w * 2, int(h / 2))

        # Ekstraksi sinyal
        rppg_signal, resp_signal = extract_rppg_and_respiration(
            gray, rppg_roi, resp_roi)
        rppg_data.append(np.mean(rppg_signal))
        resp_data.append(np.mean(resp_signal))

        # Simpan hanya data terbaru
        if len(rppg_data) > signal_length:
            rppg_data.pop(0)
            resp_data.pop(0)

        # Filter sinyal
        if len(rppg_data) >= signal_length:
            filtered_rppg = bandpass_filter(
                np.array(rppg_data), lowcut_rppg, highcut_rppg, fs)
            filtered_resp = bandpass_filter(
                np.array(resp_data), lowcut_resp, highcut_resp, fs)

            # Update visualisasi
            ax1.clear()
            ax1.plot(filtered_rppg, label="rPPG Signal")
            ax1.legend()

            ax2.clear()
            ax2.plot(filtered_resp, label="Respiration Signal")
            ax2.legend()

            plt.pause(0.01)

        # Tampilkan frame dengan ROI
        frame = draw_roi(frame, rppg_roi, resp_roi)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna.")
finally:
    cap.release()
    cv2.destroyAllWindows()
