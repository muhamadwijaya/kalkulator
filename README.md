# Kalkulator Posisi Saham (Python → APK)

Aplikasi Android kecil yang ditulis dengan Python (Kivy) untuk menghitung
jumlah lot saham BEI dari modal, risiko per trade, harga entry, stop loss,
dan target risk:reward.

## Build APK lewat Google Colab (bisa dari HP)

[![Buka di Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/muhamadwijaya/kalkulator/blob/main/build_apk_colab.ipynb)

Buka tautan di atas, pilih **Runtime → Run all**, tunggu 20–40 menit, lalu APK
terunduh atau tersimpan ke Google Drive. Pasang di HP Android (izinkan
"Instal dari sumber tidak dikenal").

## Build lewat GitHub Actions (kalau Actions aktif)

Setiap push ke `main` menjalankan GitHub Actions (`.github/workflows/build-apk.yml`):

1. Uji logika (`calc.py`) dan uji asap tampilan (`smoke_test.py`) tanpa layar.
2. Build APK dengan [Buildozer](https://github.com/kivy/buildozer) (python-for-android).
3. Menerbitkan APK sebagai Release.

## File

- `main.py`: tampilan Kivy
- `calc.py`: rumus (fraksi harga BEI, lot, TP/SL)
- `buildozer.spec`: pengaturan paket Android

Belum termasuk fee broker & pajak. Hanya alat bantu hitung, bukan saran investasi.
