import json
import sys


def muat_kb(nama_file):
    with open(nama_file, encoding="utf-8") as f:
        kb = json.load(f)
    for r in kb["aturan"]:
        if r["mode"] not in ("dan", "atau"):
            sys.exit(f"Aturan {r['id']}: mode harus 'dan' atau 'atau'")
    return kb


def cari_fakta_dasar(aturan):
    """Fakta dasar = syarat yang tidak pernah menjadi hasil (maka) aturan mana pun."""
    hasil = {r["maka"] for r in aturan}
    dasar = []
    for r in aturan:
        for k in r["jika"]:
            if k not in hasil and k not in dasar:
                dasar.append(k)
    return dasar


def tanya_user(dasar):
    print("Jawab y (ya) atau t (tidak).")
    memori = []
    for i, k in enumerate(dasar, start=1):
        while True:
            jawab = input(f"{i}. Apakah {k}? (y/t) > ").strip().lower()
            if jawab in ("y", "t"):
                break
            print("   Ketik y atau t saja.")
        if jawab == "y":
            memori.append(k)
    return memori


def syarat_terpenuhi(aturan, memori):
    ada = [k in memori for k in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)


def forward_chaining(aturan, fakta_awal):
    memori = list(fakta_awal)
    asal = {}     
    riwayat = []   
    while True:
        cocok = [r for r in aturan
                 if r["maka"] not in memori and syarat_terpenuhi(r, memori)]
        if not cocok:
            break
        r = cocok[0]
        memori.append(r["maka"])
        asal[r["maka"]] = r
        riwayat.append((len(riwayat) + 1, r))
    return memori, asal, riwayat


def tulis_alasan(hasil, asal, memori, tingkat=1):
    r = asal[hasil]
    benar = [k for k in r["jika"] if k in memori]
    print("  " * tingkat + f"{hasil}  <- {r['id']} ({', '.join(benar)})")
    for k in benar:
        if k in asal:
            tulis_alasan(k, asal, memori, tingkat + 1)


def main():
    nama_kb = sys.argv[1] if len(sys.argv) > 1 else "kb_cabai.json"
    kb = muat_kb(nama_kb)
    aturan = kb["aturan"]

    print(kb["judul"])
    fakta_awal = tanya_user(cari_fakta_dasar(aturan))

    print()
    print("Fakta awal:", ", ".join(fakta_awal) if fakta_awal else "(tidak ada)")
    print()

    memori, asal, riwayat = forward_chaining(aturan, fakta_awal)
    for no, r in riwayat:
        print(f"Siklus {no}: {r['id']} -> {r['maka']}")
    print(f"Siklus {len(riwayat) + 1}: tidak ada aturan baru, berhenti")
    print()

    dipakai_sebagai_syarat = {k for r in aturan for k in r["jika"]}
    akhir = [h for h in asal if h not in dipakai_sebagai_syarat]

    if not akhir:
        print("Kesimpulan: tidak ada kesimpulan dari jawaban tersebut")
        print()
    for h in akhir:
        print(f"Kesimpulan: {h}")
        print("Alasan:")
        tulis_alasan(h, asal, memori)
        print()
    print("Catatan:", kb["batas"])


if __name__ == "__main__":
    main()
