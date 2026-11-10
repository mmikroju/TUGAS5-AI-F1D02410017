# Sistem Pakar Sederhana: Hama dan Penyakit Tanaman Cabai

Tugas 5 Kecerdasan Buatan (Materi 5)

## 1. Identitas

- Nama: Muhammad Mikroju Raseprian Sahid
- NIM: F1D02410017

## 2. Topik dan cara menjalankan

Topik: diagnosis awal hama dan penyakit tanaman cabai. Program menanyakan sembilan gejala dan kondisi, lalu menyimpulkan hama atau penyakit yang kemungkinan menyerang beserta alasannya.

- Bahasa pemrograman: Python 3.14 (ubah sesuai versi di komputer Anda)
- Tidak ada pustaka tambahan (hanya modul bawaan `json` dan `sys`)
- File: `sistem_pakar.py` (program) dan `kb_cabai.json` (basis pengetahuan)

Cara menjalankan: simpan kedua file di satu folder, buka terminal di folder itu, lalu ketik:

    python sistem_pakar.py

Jawab setiap pertanyaan dengan `y` (ya) atau `t` (tidak). Program membaca `kb_cabai.json` secara bawaan. Berkas aturan lain dapat dipakai dengan `python sistem_pakar.py nama_file.json`.

## 3. Sumber dan tabel aturan

- S1: Meilin, Araz. "Hama dan Penyakit pada Tanaman Cabai serta Pengendaliannya." Balai Pengkajian Teknologi Pertanian (BPTP) Jambi, Badan Penelitian dan Pengembangan Pertanian, Kementerian Pertanian, 2014. https://repository.pertanian.go.id/bitstream/handle/123456789/10254/14bookcabe.pdf (diakses 9 Nov 2026). Salinan: `referensi/S1-Meilin-2014-Hama-dan-Penyakit-Cabai.pdf`
- S2: Sari, Noorkomala dan Kasiamdari, Rina Sri. "Identifikasi dan Uji Patogenisitas Colletotrichum spp. dari Cabai Merah (Capsicum annuum): Kasus di Kricaan, Magelang, Jawa Tengah." Jurnal Ilmu Pertanian Indonesia, vol 26 no 2, hlm 243-250, April 2021, IPB University. https://journal.ipb.ac.id/index.php/JIPI/article/download/27516/21546 (diakses 9 Nov 2026). Salinan: `referensi/S2-Sari-Kasiamdari-2021-Colletotrichum-Cabai.pdf`

Fakta dasar yang ditanyakan ke pengguna adalah kondisi yang tidak pernah menjadi hasil aturan lain. Sisanya diturunkan oleh program.

Aturan : IF ==> THEN (Sumber)
----------------------------
1. R1 : ada bercak keperakan di permukaan bawah daun muda **AND** daun muda keriting atau mengkerut ==> tanaman terserang thrips (S1)
2. R2 : ada titik hitam di pangkal buah **AND** buah menguning pucat, membusuk, lalu jatuh ==> buah terserang lalat buah (S1)
3. R3 : buah berbercak kecil hitam yang sedikit cekung ==> gejala awal antraknosa pada buah (S1, S2)
4. R4 : gejala awal antraknosa pada buah **OR** buah berkerut, lunak, dan membusuk ==> buah terserang antraknosa (S1, S2)
5. R5 : daun bawah layu dan menguning **AND** pangkal batang atau akar cokelat dan tertutup hifa putih seperti kapas ==> tanaman terserang layu fusarium (S1)
6. R6 : sedang musim kemarau ==> waspada: populasi thrips, kutu daun, dan tungau cenderung meningkat di musim kemarau (S1)

Ada 6 aturan dan 5 kesimpulan akhir (thrips, lalat buah, antraknosa, layu fusarium, dan peringatan musim kemarau). Aturan yang memakai hasil aturan lain: R4 memakai hasil R3.

## 4. Metode: forward chaining

Saya memilih forward chaining (FC). Alasannya, pengguna mengetahui gejala yang terlihat di tanaman, lalu kesimpulan ditarik dari fakta itu. Sumber juga menjelaskan gejala sebagai ciri yang mengarah ke jenis hama atau penyakit, sehingga cocok dijalankan sebagai aturan maju.

Cara kerja program: memori diisi fakta yang dijawab "ya" oleh pengguna. Lalu program mengulang: cari aturan yang syaratnya terpenuhi oleh memori (mode "dan" berarti semua syarat harus ada, mode "atau" berarti salah satu cukup) dan hasilnya belum ada di memori, ambil aturan pertama, tambahkan hasilnya ke memori, dan catat aturan asalnya. Perulangan berhenti ketika tidak ada aturan baru. Catatan asal hasil dipakai untuk menampilkan alasan. Kesimpulan akhir adalah hasil yang tidak dipakai sebagai syarat aturan lain.

## 5. Tiga kasus uji

**Kasus 1: musim kemarau, bercak keperakan di bawah daun muda, dan daun muda keriting (jawaban y untuk pertanyaan 1, 2, 9).** Program menjalankan R1 dan R6. Kesimpulannya: tanaman terserang thrips dan peringatan populasi hama meningkat di musim kemarau.

![Kasus 1](screenshot/Kasus1.png)

**Kasus 2: buah berbercak kecil hitam yang sedikit cekung dan buah berkerut, lunak, membusuk (jawaban y untuk pertanyaan 5 dan 6).** Program menjalankan R3 lalu R4. Kesimpulannya: buah terserang antraknosa, dengan alasan yang menelusuri R4 sampai R3.

![Kasus 2](screenshot/Kasus2.png)

**Kasus 3 (negatif): hanya daun muda keriting (jawaban y untuk pertanyaan 2 saja).** Gejala bercak keperakan tidak ada, jadi R1 tidak terpenuhi. Tidak ada aturan yang cocok, sehingga program menampilkan bahwa tidak ada kesimpulan.

![Kasus 3](screenshot/Kasus3.png)

## 6. Batas keberlakuan

Pengetahuan dalam program ini berasal dari dua sumber: buku Meilin (2014) yang diterbitkan BPTP Jambi, Kementerian Pertanian, tentang hama dan penyakit cabai, dan artikel Sari dan Kasiamdari (2021) tentang antraknosa pada buah cabai merah di Kricaan, Magelang. Program hanya dimaksudkan sebagai saran awal untuk mengenali thrips, lalat buah, antraknosa, dan layu fusarium dari gejala yang terlihat, serta mengingatkan bahwa populasi hama tertentu cenderung meningkat di musim kemarau. Hama dan penyakit lain tidak tercakup, gejala dapat mirip antarpenyakit, beberapa penyakit dapat menyerang bersamaan, dan program tidak menggantikan pemeriksaan penyuluh pertanian atau uji laboratorium, sehingga hasilnya bukan keputusan akhir. Catatan yang sama ditampilkan oleh program di akhir setiap keluaran.

## 7. Penggunaan alat bantu AI

Saya memakai AI Claude sebagai alat bantu dalam memandu pengerjaan tugas ini. Claude membantu memberikan contoh kode untuk menyusun struktur `sistem_pakar.py`, berkas `kb_cabai.json`.
