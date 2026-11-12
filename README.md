# Kalkulator Posisi Saham (Python → APK)

Aplikasi Android kecil yang ditulis dengan Python (Kivy) untuk menghitung
jumlah lot saham BEI dari modal, risiko per trade, harga entry, stop loss,
dan target risk:reward.

## Unduh APK

Buka tab **Releases** di repo ini dan unduh file `.apk` terbaru, lalu pasang di HP
Android (izinkan "Instal dari sumber tidak dikenal").

## Cara kerja build

Setiap push ke `main` menjalankan GitHub Actions (`.github/workflows/build-apk.yml`):

1. Uji logika (`calc.py`) dan uji asap tampilan (`smoke_test.py`) tanpa layar.
2. Build APK dengan [Buildozer](https://github.com/kivy/buildozer) (python-for-android).
3. Menerbitkan APK sebagai Release.

## File

- `main.py`: tampilan Kivy
- `calc.py`: rumus (fraksi harga BEI, lot, TP/SL)
- `buildozer.spec`: pengaturan paket Android

Belum termasuk fee broker & pajak. Hanya alat bantu hitung, bukan saran investasi.
