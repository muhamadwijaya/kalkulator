"""Logika kalkulator posisi saham IDX (tanpa Kivy, agar mudah dites).

Aturan yang dipakai:
- 1 lot = 100 lembar.
- Fraksi harga BEI: <200 = Rp1, 200-<500 = Rp2, 500-<2.000 = Rp5,
  2.000-<5.000 = Rp10, >=5.000 = Rp25. Harga minimum Rp1.
- Hanya posisi beli (long): stop loss harus di bawah harga entry.
- Belum termasuk fee broker dan pajak.
"""

import math
import re


class InputError(ValueError):
    """Input pengguna tidak valid; pesannya ditampilkan apa adanya."""


def fraksi(harga):
    """Fraksi (tick) harga BEI untuk harga tertentu."""
    if harga < 200:
        return 1
    if harga < 500:
        return 2
    if harga < 2000:
        return 5
    if harga < 5000:
        return 10
    return 25


def bulatkan_bawah(harga):
    """Bulatkan ke bawah ke fraksi yang sah."""
    t = fraksi(harga)
    return max(1, int(math.floor(harga / t)) * t)


def sesuai_fraksi(harga):
    return harga >= 1 and harga % fraksi(harga) == 0


def parse_rupiah(teks, nama):
    """'10.000.000', 'Rp 10,000,000', '10000000' -> 10000000 (int)."""
    angka = re.sub(r"[^0-9]", "", teks or "")
    if not angka:
        raise InputError(f"{nama} belum diisi.")
    nilai = int(angka)
    if nilai <= 0:
        raise InputError(f"{nama} harus lebih dari 0.")
    return nilai


def parse_desimal(teks, nama):
    """'1,5' atau '1.5' -> 1.5"""
    t = (teks or "").strip().replace("%", "").replace(" ", "").replace(",", ".")
    if not t:
        raise InputError(f"{nama} belum diisi.")
    try:
        nilai = float(t)
    except ValueError:
        raise InputError(f"{nama} tidak valid: {teks}")
    if nilai <= 0:
        raise InputError(f"{nama} harus lebih dari 0.")
    return nilai


def fmt_rp(nilai):
    tanda = "-" if nilai < 0 else ""
    return f"{tanda}Rp{abs(round(nilai)):,}".replace(",", ".")


def fmt_angka(nilai):
    return f"{round(nilai):,}".replace(",", ".")


def hitung(modal, risiko_pct, entry, stop_loss, rr):
    """Hitung ukuran posisi. Semua argumen sudah berupa angka."""
    if risiko_pct > 100:
        raise InputError("Risiko per trade maksimal 100%.")
    if stop_loss >= entry:
        raise InputError("Stop loss harus di bawah harga entry (posisi beli).")

    peringatan = []
    for nama, h in (("Harga entry", entry), ("Stop loss", stop_loss)):
        if not sesuai_fraksi(h):
            peringatan.append(
                f"{nama} {fmt_angka(h)} tidak sesuai fraksi Rp{fraksi(h)}."
            )

    risiko_maks = modal * risiko_pct / 100.0
    risiko_per_lembar = entry - stop_loss
    lot_by_risiko = int(risiko_maks // (risiko_per_lembar * 100))
    lot_by_modal = int(modal // (entry * 100))
    lot = min(lot_by_risiko, lot_by_modal)
    dibatasi_modal = lot_by_modal < lot_by_risiko

    if lot <= 0:
        if lot_by_modal <= 0:
            raise InputError(
                f"Modal tidak cukup untuk 1 lot (butuh {fmt_rp(entry * 100)})."
            )
        raise InputError(
            "Risiko terlalu kecil untuk 1 lot. Perbesar risiko % "
            "atau dekatkan stop loss."
        )

    lembar = lot * 100
    nilai_posisi = lembar * entry
    tp = bulatkan_bawah(entry + rr * risiko_per_lembar)
    rugi = lembar * risiko_per_lembar
    untung = lembar * (tp - entry)

    if dibatasi_modal:
        peringatan.append("Jumlah lot dibatasi modal, bukan oleh risiko.")

    return {
        "lot": lot,
        "lembar": lembar,
        "risiko_maks": risiko_maks,
        "risiko_per_lembar": risiko_per_lembar,
        "nilai_posisi": nilai_posisi,
        "porsi_modal": nilai_posisi / modal * 100.0,
        "take_profit": tp,
        "rugi_jika_sl": rugi,
        "rugi_pct_modal": rugi / modal * 100.0,
        "untung_jika_tp": untung,
        "rr_aktual": (tp - entry) / risiko_per_lembar,
        "sl_pct": risiko_per_lembar / entry * 100.0,
        "tp_pct": (tp - entry) / entry * 100.0,
        "peringatan": peringatan,
    }
