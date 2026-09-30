CREATE DATABASE IF NOT EXISTS db_undangan;
USE db_undangan;

CREATE TABLE IF NOT EXISTS pesanan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_kustomer VARCHAR(100) NOT NULL,
    no_whatsapp VARCHAR(20) NOT NULL,
    jenis_undangan ENUM('Pernikahan', 'Ulang Tahun', 'Acara Perusahaan', 'Lainnya') NOT NULL,
    catatan TEXT,
    tanggal_pesan TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);