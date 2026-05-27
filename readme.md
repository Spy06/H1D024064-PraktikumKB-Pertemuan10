Nama: Farhan Hakim
NIM: H1D024064

Implementasi Algoritma Genetika untuk menyelesaikan *Knapsack Problem* sesuai dengan tugas praktikum Pertemuan 10.

## Kombinasi Metode (NIM: H1D024064)
* **Seleksi (Digit Akhir 6):** *Roulette Wheel Selection* (RWS)
* **Crossover (Digit Akhir 4):** *Two-Point Crossover*
* **Mutasi (Hasil Penjumlahan 6 + 4 = 10 -> Akhiran 0):** *Swap Mutation*

## Cara Kerja Kode (Singkat)
1. **Inisialisasi:** Program membangkitkan populasi awal berisi kromosom biner acak (`0` berarti barang tidak dibawa, `1` berarti barang dibawa).
2. **Evaluasi Fitness:** Menghitung total keuntungan dari barang yang terpilih. Jika total bobot melebihi kapasitas tas (`50 kg`), kromosom diberi penalti berupa nilai fitness `0`.
3. **Seleksi (RWS):** Memilih orang tua (*parent*) secara acak proporsional berdasarkan nilai fitnessnya—makin tinggi fitness, makin besar peluang terpilih.
4. **Crossover (Two-Point):** Memotong dua titik pada pasang kromosom orang tua dan menukar bagian tengahnya untuk menghasilkan dua anak (*offspring*) baru.
5. **Mutasi (Swap):** Mengubah variasi gen dengan menukar posisi dua elemen gen secara acak di dalam kromosom anak jika memenuhi nilai probabilitas mutasi.
6. **Looping & Plotting:** Siklus di atas diulang sebanyak generasi yang ditentukan, lalu `matplotlib` memetakan perkembangan nilai fitness tertinggi, terendah, dan rata-rata ke dalam bentuk grafik.