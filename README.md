# Trend Jari - Python Computer Vision Hand Tracking

Proyek Computer Vision interaktif menggunakan **OpenCV** dan **MediaPipe** yang mereplikasi tren viral pelacakan tangan dengan efek visual real-time (Thermal, Glitch Chromatic Aberration, dan Cyberpunk Neon).

---

## Fitur Utama

1. **Tracking 21 Titik Landmark Tangan:**
   - Menghubungkan titik sendi tangan secara real-time dengan palet warna neon custom (Cyan, Pink, Yellow, Green, Magenta).
2. **Ganti Filter Otomatis (Gesture Trigger):**
   - **Sentuh Ujung Jempol & Kelingking**: Program menghitung jarak Euclidean antara landmark `#4` (Thumb Tip) dan landmark `#20` (Pinky Tip). Saat bersentuhan, filter berpindah mode dengan jeda *cooldown*.
3. **Deteksi Pose "Shaka" (Trend Jari):**
   - Mendeteksi ketika jempol dan kelingking terbuka sedangkan ketiga jari tengah (telunjuk, tengah, manis) ditekuk ke arah telapak tangan.
   - Mengaktifkan efek portal aura bercahaya di sekitar tangan.
4. **Efek Visual Real-Time:**
   - **`PORTAL: THERMAL`**: Filter spektrum inframerah/termal (JET heatmap colormap).
   - **`PORTAL: INFERNO`**: Filter spektrum api/panas mendalam.
   - **`GLITCH: CHROMATIC`**: Efek pergeseran channel warna RGB (Cyan/Magenta/Yellow split) dengan scanline glitch horizontal.
   - **`NEON CYBERPUNK`**: Peningkatan saturasi warna dengan garis kontur tepi bercahaya.
   - **`NORMAL`**: Tampilan kamera asli dengan HUD analitik.

---

## Struktur File

```
trend_jari_cv/
│── main.py            # Kode utama aplikasi
│── requirements.txt   # Dependensi (opencv-python, mediapipe, numpy)
│── run.bat            # Script sekali klik untuk menjalankan di Windows
└── README.md          # Panduan proyek
```

---

## Cara Menjalankan

### Cara 1: Menggunakan `run.bat` (Rekomendasi)
Cukup klik ganda file [`run.bat`](file:///C:/Users/Advan/.gemini/antigravity-ide/scratch/trend_jari_cv/run.bat). Script akan otomatis mendeteksi Python di komputer Anda (termasuk instalasi Python di Laragon), menginstal library yang diperlukan, dan menjalankan aplikasi.

### Cara 2: Menjalankan via Terminal / CMD
```bash
cd C:\Users\Advan\.gemini\antigravity-ide\scratch\trend_jari_cv

# Menggunakan Python Laragon jika belum masuk PATH:
"D:\laragon\bin\python\python-3.13\python.exe" -m pip install -r requirements.txt
"D:\laragon\bin\python\python-3.13\python.exe" main.py

# Atau jika Python sudah terdaftar di PATH:
pip install -r requirements.txt
python main.py
```

---

## Kontrol Keyboard & Gestur

| Aksi / Tombol | Fungsi |
| :--- | :--- |
| **Sentuh Jempol & Kelingking** | Berganti ke filter berikutnya secara otomatis |
| **Pose Shaka (Jempol + Kelingking terbuka)** | Mengaktifkan indikator "TREND JARI" & Aura Portal |
| **Tombol `F`** | Ganti filter secara manual |
| **Tombol `Q` / `ESC`** | Keluar dari aplikasi |
