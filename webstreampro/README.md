# WebStreamPro

Web-based YouTube Live Stream Management System - Versi web dari AutoLiveBio yang dapat dijalankan menggunakan PM2.

## Fitur

- 🔐 OAuth2 Authentication dengan Google
- 📺 Multi-channel support (kelola multiple channel YouTube)
- 📊 Import broadcast data dari Excel
- 🚀 Batch creation YouTube Live broadcasts
- ⏰ Scheduler untuk batch broadcasts
- 📹 Video upload dengan scheduling
- 🖼️ Upload thumbnails
- 📋 Lihat upcoming broadcasts
- 🌐 Web-based interface (accessible dari browser)
- 🔄 Persistent dengan PM2

## Persyaratan

- Node.js 14.x atau lebih tinggi
- npm atau yarn
- PM2 (untuk production deployment)
- Google Cloud Console project dengan YouTube Data API v3 enabled
- OAuth 2.0 credentials (client_secret.json)

## Instalasi

### 1. Install Dependencies

```bash
cd webstreampro
npm install
```

### 2. Install PM2 (Global)

```bash
npm install -g pm2
```

### 3. Setup Environment

Copy file `.env.example` menjadi `.env`:

```bash
copy .env.example .env
```

Edit file `.env` sesuai kebutuhan:

```env
PORT=3000
SESSION_SECRET=your-secret-key-change-this-to-something-secure
NODE_ENV=production
```

### 4. Setup Google OAuth2

**📖 Detailed Guide:** See [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md) for step-by-step instructions with screenshots.

**Quick Steps:**

1. Buka [Google Cloud Console](https://console.cloud.google.com)
2. Buat project baru atau pilih project yang ada
3. Enable YouTube Data API v3
4. Setup OAuth consent screen (External, add yourself as test user)
5. Buat OAuth 2.0 credentials (Web Application)
6. Tambahkan Authorized redirect URIs:
   - `http://localhost:3000/api/auth/callback`
   - ⚠️ Must match exactly! No trailing slash!
7. Download `client_secret.json`

**❓ Having Issues?** Check [TROUBLESHOOTING_AUTH.md](TROUBLESHOOTING_AUTH.md)

## Menjalankan Aplikasi

### Mode Development

```bash
npm run dev
```

### Mode Production dengan PM2

#### Start aplikasi:

```bash
npm run pm2:start
```

atau

```bash
pm2 start ecosystem.config.js
```

#### Stop aplikasi:

```bash
npm run pm2:stop
```

atau

```bash
pm2 stop webstreampro
```

#### Restart aplikasi:

```bash
npm run pm2:restart
```

atau

```bash
pm2 restart webstreampro
```

#### Lihat logs:

```bash
npm run pm2:logs
```

atau

```bash
pm2 logs webstreampro
```

#### Lihat status:

```bash
npm run pm2:status
```

atau

```bash
pm2 status
```

#### Setup PM2 untuk auto-start saat boot:

```bash
pm2 startup
pm2 save
```

## Penggunaan

### 1. Akses Web Interface

Buka browser dan akses:

```
http://localhost:3000
```

### 2. Authentication

1. Klik tab "Authentication"
2. Upload file `client_secret.json` yang sudah didownload dari Google Cloud Console
3. Klik "Upload"
4. Klik "Login with Google"
5. Ikuti proses OAuth flow di browser
6. Pilih channel YouTube yang ingin digunakan

### 3. Create Broadcasts

#### Menggunakan Excel File:

1. Klik tab "Broadcasts"
2. Upload file Excel dengan format yang sesuai
3. Klik "Parse Excel" untuk preview
4. Pilih:
   - "Create All Now" untuk membuat semua broadcast sekarang
   - "Schedule Batch" untuk menjadwalkan pembuatan broadcast

#### Format Excel:

Required columns:
- `title`: Judul broadcast
- `description`: Deskripsi broadcast
- `tags`: Tags dipisahkan dengan koma
- `categoryId`: YouTube category ID (default: 20 untuk Gaming)
- `privacyStatus`: public, unlisted, atau private

Optional columns:
- `scheduledStartDate`: Format YYYY-MM-DD
- `scheduledStartTime`: Format HH:MM (24-hour)
- `thumbnailPath`: Path ke file thumbnail
- `streamId`: ID stream yang sudah ada (untuk reuse)
- `streamKey`: Custom stream key
- `latency`: normal, low, ultraLow
- `enableDvr`: TRUE/FALSE (default: TRUE)
- `enableEmbed`: TRUE/FALSE (default: TRUE)
- `recordFromStart`: TRUE/FALSE (default: TRUE)
- `madeForKids`: TRUE/FALSE (default: FALSE)
- `containsSyntheticMedia`: TRUE/FALSE (default: FALSE)
- `enableMonetization`: TRUE/FALSE (default: FALSE)

### 4. Upload Video

1. Klik tab "Video Upload"
2. Pilih file video
3. (Optional) Pilih thumbnail
4. Isi informasi video (title, description, tags, etc.)
5. Pilih:
   - "Upload Now" untuk upload langsung
   - "Schedule Upload" untuk menjadwalkan upload

### 5. View Scheduled Tasks

1. Klik tab "Scheduled Tasks"
2. Lihat scheduled batches dan scheduled uploads
3. Klik "Refresh" untuk update
4. Klik "Cancel" untuk membatalkan task yang pending
5. Klik "Clear Completed" untuk membersihkan task yang sudah selesai

### 6. View Upcoming Broadcasts

1. Klik tab "Upcoming Broadcasts"
2. Klik "Refresh" untuk melihat daftar upcoming broadcasts
3. Lihat informasi detail setiap broadcast

## Struktur Proyek

```
webstreampro/
├── src/
│   ├── services/          # Service layer
│   │   ├── AuthService.js
│   │   ├── YouTubeService.js
│   │   ├── VideoUploader.js
│   │   └── BatchScheduler.js
│   ├── routes/            # API routes
│   │   ├── auth.js
│   │   ├── broadcasts.js
│   │   └── videos.js
│   ├── middleware/        # Express middleware
│   │   └── auth.js
│   └── utils/             # Utilities
│       ├── config.js
│       └── excelParser.js
├── public/                # Frontend files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── index.html
├── data/                  # Data storage
│   ├── tokens/           # OAuth tokens
│   └── client_secret.json
├── uploads/              # Uploaded files
├── logs/                 # PM2 logs
├── server.js             # Main server file
├── ecosystem.config.js   # PM2 configuration
├── package.json
└── .env                  # Environment variables
```

## API Endpoints

### Authentication

- `POST /api/auth/upload-client-secret` - Upload client secret file
- `GET /api/auth/login` - Get OAuth login URL
- `GET /api/auth/callback` - OAuth callback
- `GET /api/auth/status` - Check authentication status
- `POST /api/auth/select-channel` - Select active channel
- `GET /api/auth/accounts` - Get all accounts
- `POST /api/auth/switch-account` - Switch account
- `POST /api/auth/logout` - Logout

### Broadcasts

- `POST /api/broadcasts/parse-excel` - Parse Excel file
- `POST /api/broadcasts/create` - Create single broadcast
- `POST /api/broadcasts/create-batch` - Create multiple broadcasts
- `POST /api/broadcasts/schedule-batch` - Schedule batch creation
- `GET /api/broadcasts/scheduled-batches` - Get scheduled batches
- `POST /api/broadcasts/cancel-batch/:batchId` - Cancel scheduled batch
- `DELETE /api/broadcasts/clear-completed-batches` - Clear completed batches
- `GET /api/broadcasts/upcoming` - Get upcoming broadcasts

### Videos

- `POST /api/videos/upload` - Upload video immediately
- `POST /api/videos/schedule-upload` - Schedule video upload
- `GET /api/videos/scheduled-uploads` - Get scheduled uploads
- `POST /api/videos/cancel-upload/:index` - Cancel scheduled upload
- `DELETE /api/videos/clear-completed-uploads` - Clear completed uploads
- `POST /api/videos/start-scheduler` - Start video upload scheduler
- `POST /api/videos/stop-scheduler` - Stop video upload scheduler

## Troubleshooting

### Port sudah digunakan

Jika port 3000 sudah digunakan, edit file `.env`:

```env
PORT=8080
```

### PM2 tidak bisa start

Pastikan PM2 terinstall secara global:

```bash
npm install -g pm2
```

### Authentication error

1. Pastikan `client_secret.json` sudah benar
2. Pastikan redirect URI di Google Cloud Console sudah benar
3. Pastikan YouTube Data API v3 sudah enabled

### Upload gagal

1. Pastikan folder `uploads/` dan `data/` sudah dibuat
2. Pastikan ada permission untuk write ke folder tersebut

## Tips Production

### 1. Gunakan HTTPS

Untuk production, sebaiknya gunakan HTTPS. Anda bisa menggunakan reverse proxy seperti Nginx dengan SSL certificate.

### 2. Ubah SESSION_SECRET

Pastikan mengubah `SESSION_SECRET` di file `.env` dengan string yang secure dan unik.

### 3. Set NODE_ENV

```env
NODE_ENV=production
```

### 4. Monitor dengan PM2

```bash
pm2 monit
```

### 5. Auto-restart saat crash

PM2 sudah menghandle auto-restart, tapi pastikan konfigurasi di `ecosystem.config.js` sudah benar.

### 6. Log Rotation

PM2 punya built-in log rotation, atau bisa menggunakan pm2-logrotate:

```bash
pm2 install pm2-logrotate
```

## License

MIT

## Support

Untuk bantuan atau pertanyaan, silakan buka issue di repository ini.
