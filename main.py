"""Kalkulator Posisi Saham (BEI) - aplikasi Kivy yang di-build menjadi APK."""

import json
import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as C

import calc

KV = r"""
#:import C kivy.utils.get_color_from_hex

<Teks@Label>:
    color: C('#9AA4B2')
    font_size: '13sp'
    size_hint_y: None
    height: dp(22)
    text_size: self.size
    halign: 'left'
    valign: 'middle'

<Isian@TextInput>:
    multiline: False
    write_tab: False
    input_type: 'number'
    keyboard_suggestions: False
    font_size: '18sp'
    size_hint_y: None
    height: dp(50)
    padding: [dp(14), (self.height - self.line_height) / 2.0]
    background_normal: ''
    background_active: ''
    background_color: C('#1A212C')
    foreground_color: C('#F2F4F7')
    cursor_color: C('#3DDC97')
    hint_text_color: C('#566070')

<Kolom@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    spacing: dp(4)

<Baris@BoxLayout>:
    judul: ''
    nilai: '-'
    warna: C('#F2F4F7')
    size_hint_y: None
    height: dp(34)
    Label:
        text: root.judul
        color: C('#9AA4B2')
        font_size: '14sp'
        text_size: self.size
        halign: 'left'
        valign: 'middle'
    Label:
        text: root.nilai
        color: root.warna
        font_size: '15sp'
        bold: True
        text_size: self.size
        halign: 'right'
        valign: 'middle'

<Tombol@Button>:
    warna_dasar: C('#232C38')
    warna_tekan: C('#2E3947')
    background_normal: ''
    background_down: ''
    background_color: self.warna_dasar if self.state == 'normal' else self.warna_tekan
    font_size: '16sp'

BoxLayout:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: C('#0E1319')
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: dp(78)
        padding: [dp(18), dp(14), dp(18), dp(8)]
        canvas.before:
            Color:
                rgba: C('#121922')
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'Kalkulator Posisi Saham'
            bold: True
            font_size: '21sp'
            color: C('#F2F4F7')
            text_size: self.size
            halign: 'left'
            valign: 'middle'
        Label:
            text: 'BEI  |  1 lot = 100 lembar  |  posisi beli'
            font_size: '13sp'
            color: C('#3DDC97')
            text_size: self.size
            halign: 'left'
            valign: 'middle'

    ScrollView:
        do_scroll_x: False
        bar_width: dp(3)
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: dp(18)
            spacing: dp(12)

            Kolom:
                Teks:
                    text: 'Modal (Rp)'
                Isian:
                    id: modal
                    hint_text: 'contoh 10.000.000'

            GridLayout:
                cols: 2
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height
                Kolom:
                    Teks:
                        text: 'Risiko per trade (%)'
                    Isian:
                        id: risiko
                        hint_text: '2'
                Kolom:
                    Teks:
                        text: 'Target R:R  (1 : x)'
                    Isian:
                        id: rr
                        hint_text: '2'
                Kolom:
                    Teks:
                        text: 'Harga entry'
                    Isian:
                        id: entry
                        hint_text: '1000'
                Kolom:
                    Teks:
                        text: 'Stop loss'
                    Isian:
                        id: sl
                        hint_text: '950'

            BoxLayout:
                size_hint_y: None
                height: dp(52)
                spacing: dp(12)
                Tombol:
                    text: 'HITUNG'
                    bold: True
                    font_size: '17sp'
                    warna_dasar: C('#22B37A')
                    warna_tekan: C('#1A8C5F')
                    color: C('#0B0F14')
                    on_release: app.hitung()
                Tombol:
                    text: 'Reset'
                    size_hint_x: 0.45
                    color: C('#C9D1DB')
                    on_release: app.reset()

            Label:
                id: pesan
                text: ''
                color: C('#FF6B6B')
                font_size: '14sp'
                size_hint_y: None
                height: self.texture_size[1] if self.text else 0
                text_size: self.width, None
                halign: 'left'

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)
                spacing: dp(2)
                canvas.before:
                    Color:
                        rgba: C('#151C26')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(14)]
                Label:
                    text: 'Jumlah beli'
                    color: C('#9AA4B2')
                    font_size: '13sp'
                    size_hint_y: None
                    height: dp(20)
                    text_size: self.size
                    halign: 'left'
                    valign: 'middle'
                Label:
                    id: lot
                    text: '-'
                    bold: True
                    font_size: '34sp'
                    color: C('#3DDC97')
                    size_hint_y: None
                    height: dp(50)
                    text_size: self.size
                    halign: 'left'
                    valign: 'middle'
                Label:
                    id: lembar
                    text: 'Isi data lalu tekan HITUNG'
                    color: C('#9AA4B2')
                    font_size: '13sp'
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.size
                    halign: 'left'
                    valign: 'middle'
                Widget:
                    size_hint_y: None
                    height: dp(8)
                Baris:
                    id: b_posisi
                    judul: 'Nilai posisi'
                Baris:
                    id: b_risiko
                    judul: 'Risiko maksimal'
                Baris:
                    id: b_sl
                    judul: 'Stop loss'
                Baris:
                    id: b_tp
                    judul: 'Take profit'
                Baris:
                    id: b_rugi
                    judul: 'Rugi jika kena SL'
                Baris:
                    id: b_untung
                    judul: 'Untung jika kena TP'
                Baris:
                    id: b_rr
                    judul: 'R:R aktual'
                Label:
                    id: peringatan
                    text: ''
                    color: C('#FFB547')
                    font_size: '13sp'
                    size_hint_y: None
                    height: self.texture_size[1] + (dp(8) if self.text else 0)
                    text_size: self.width, None
                    halign: 'left'

            Label:
                text: 'Belum termasuk fee broker & pajak. Hanya alat bantu hitung, bukan saran investasi.'
                color: C('#566070')
                font_size: '12sp'
                size_hint_y: None
                height: self.texture_size[1] + dp(8)
                text_size: self.width, None
                halign: 'center'
"""

FIELDS = ("modal", "risiko", "rr", "entry", "sl")
BARIS = ("b_posisi", "b_risiko", "b_sl", "b_tp", "b_rugi", "b_untung", "b_rr")
PUTIH = C("#F2F4F7")
HIJAU = C("#3DDC97")
MERAH = C("#FF6B6B")


def pct(x):
    return f"{x:.1f}".replace(".", ",") + "%"


class KalkulatorApp(App):
    title = "Kalkulator Saham"

    def build(self):
        Window.clearcolor = C("#0E1319")
        try:
            # Geser layar ke atas saat keyboard muncul agar isian tetap terlihat.
            Window.softinput_mode = "below_target"
        except Exception:
            pass
        return Builder.load_string(KV)

    def on_start(self):
        self._muat()

    # ---------- simpan / muat input terakhir ----------
    def _berkas(self):
        return os.path.join(self.user_data_dir, "input_terakhir.json")

    def _muat(self):
        data = {"risiko": "2", "rr": "2"}
        try:
            with open(self._berkas(), encoding="utf-8") as f:
                data.update(json.load(f))
        except Exception:
            pass
        for k in FIELDS:
            self.root.ids[k].text = str(data.get(k, ""))

    def _simpan(self):
        try:
            data = {k: self.root.ids[k].text for k in FIELDS}
            with open(self._berkas(), "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

    # ---------- aksi tombol ----------
    def _tutup_keyboard(self):
        for k in FIELDS:
            self.root.ids[k].focus = False

    def _kosongkan_hasil(self, teks="Isi data lalu tekan HITUNG"):
        ids = self.root.ids
        ids.lot.text = "-"
        ids.lembar.text = teks
        ids.peringatan.text = ""
        for b in BARIS:
            ids[b].nilai = "-"
            ids[b].warna = PUTIH

    def reset(self):
        self._tutup_keyboard()
        ids = self.root.ids
        for k in ("modal", "entry", "sl"):
            ids[k].text = ""
        ids.risiko.text = "2"
        ids.rr.text = "2"
        ids.pesan.text = ""
        self._kosongkan_hasil()
        self._simpan()

    def hitung(self):
        self._tutup_keyboard()
        ids = self.root.ids
        try:
            modal = calc.parse_rupiah(ids.modal.text, "Modal")
            risiko = calc.parse_desimal(ids.risiko.text, "Risiko per trade")
            rr = calc.parse_desimal(ids.rr.text, "Target R:R")
            entry = calc.parse_rupiah(ids.entry.text, "Harga entry")
            sl = calc.parse_rupiah(ids.sl.text, "Stop loss")
            h = calc.hitung(modal, risiko, entry, sl, rr)
        except calc.InputError as e:
            ids.pesan.text = str(e)
            self._kosongkan_hasil("Periksa kembali isian di atas")
            return

        ids.pesan.text = ""
        ids.modal.text = calc.fmt_angka(modal)
        ids.lot.text = f"{calc.fmt_angka(h['lot'])} lot"
        ids.lembar.text = f"{calc.fmt_angka(h['lembar'])} lembar @ {calc.fmt_angka(entry)}"

        ids.b_posisi.nilai = (
            f"{calc.fmt_rp(h['nilai_posisi'])} ({pct(h['porsi_modal'])} modal)"
        )
        ids.b_risiko.nilai = calc.fmt_rp(h["risiko_maks"])
        ids.b_sl.nilai = f"{calc.fmt_angka(sl)} (-{pct(h['sl_pct'])})"
        ids.b_sl.warna = MERAH
        ids.b_tp.nilai = f"{calc.fmt_angka(h['take_profit'])} (+{pct(h['tp_pct'])})"
        ids.b_tp.warna = HIJAU
        ids.b_rugi.nilai = (
            f"-{calc.fmt_rp(h['rugi_jika_sl'])} ({pct(h['rugi_pct_modal'])} modal)"
        )
        ids.b_rugi.warna = MERAH
        ids.b_untung.nilai = f"+{calc.fmt_rp(h['untung_jika_tp'])}"
        ids.b_untung.warna = HIJAU
        ids.b_rr.nilai = "1 : " + f"{h['rr_aktual']:.2f}".replace(".", ",")
        ids.peringatan.text = "\n".join("! " + p for p in h["peringatan"])
        self._simpan()


if __name__ == "__main__":
    KalkulatorApp().run()
