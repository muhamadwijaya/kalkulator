"""Uji asap di CI: buka aplikasi (tanpa layar), isi form, tekan HITUNG, cek hasil.

Dijalankan oleh GitHub Actions sebelum build APK, agar error tampilan/KV
ketahuan sebelum aplikasi dipasang di HP. Tidak ikut masuk ke APK.
"""

import os
import sys

os.environ.setdefault("KIVY_NO_ARGS", "1")

from kivy.clock import Clock  # noqa: E402

import main  # noqa: E402

hasil = {"ok": False}


class UjiApp(main.KalkulatorApp):
    def on_start(self):
        super().on_start()
        Clock.schedule_once(self.uji, 0.5)

    def uji(self, _dt):
        ids = self.root.ids
        ids.modal.text = "10.000.000"
        ids.risiko.text = "2"
        ids.rr.text = "2"
        ids.entry.text = "1000"
        ids.sl.text = "950"
        self.hitung()
        assert ids.pesan.text == "", ids.pesan.text
        assert ids.lot.text == "40 lot", ids.lot.text
        assert ids.b_tp.nilai.startswith("1.100"), ids.b_tp.nilai
        assert ids.b_rugi.nilai.startswith("-Rp200.000"), ids.b_rugi.nilai

        ids.sl.text = "1000"
        self.hitung()
        assert "Stop loss" in ids.pesan.text, ids.pesan.text
        assert ids.lot.text == "-", ids.lot.text

        self.reset()
        assert ids.modal.text == "" and ids.risiko.text == "2"

        hasil["ok"] = True
        print("SMOKE TEST OK")
        self.stop()


def batas_waktu(_dt):
    print("SMOKE TEST TIMEOUT")
    os._exit(2)


Clock.schedule_once(batas_waktu, 60)
UjiApp().run()
sys.exit(0 if hasil["ok"] else 1)
