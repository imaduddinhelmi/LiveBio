# Quick Start Guide - WebStreamPro

## Langkah Cepat Setup & Running

### 1. Install Dependencies

```bash
cd webstreampro
npm install
npm install -g pm2
```

### 2. Setup Environment

```bash
copy .env.example .env
```

Edit `.env` jika perlu mengubah port atau session secret.

### 3. Jalankan dengan PM2

```bash
npm run pm2:start
```

atau

```bash
pm2 start ecosystem.config.js
```

### 4. Akses Web Interface

Buka browser: `http://localhost:3000`

### 5. Setup Authentication

1. Upload `client_secret.json` dari Google Cloud Console
2. Klik "Login with Google"
3. Authorize aplikasi
4. Pilih channel YouTube

### 6. Mulai Gunakan!

- Upload Excel untuk batch create broadcasts
- Upload video langsung atau schedule
- Monitor scheduled tasks
- Lihat upcoming broadcasts

## PM2 Commands

```bash
pm2 status                    # Lihat status
pm2 logs webstreampro        # Lihat logs
pm2 restart webstreampro     # Restart
pm2 stop webstreampro        # Stop
pm2 delete webstreampro      # Hapus dari PM2
```

## Auto-Start saat Boot

```bash
pm2 startup
pm2 save
```

## Troubleshooting Cepat

**Port sudah digunakan?**
- Edit `.env`, ubah `PORT=3000` ke port lain

**PM2 error?**
- Coba: `npm install -g pm2 --force`

**Upload gagal?**
- Pastikan folder `data/` dan `uploads/` ada dan writable

**Authentication error?**
- Pastikan redirect URI di Google Console: `http://localhost:3000/api/auth/callback`

## Need Help?

Baca `README.md` untuk dokumentasi lengkap.
