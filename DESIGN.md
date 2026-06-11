# 🎨 SITARA - Design System & UI/UX Guidelines

## 📐 Design Principles

### 1.User-Centered Design
-Desain difokuskan pada kebutuhan pengguna (Admin, Dokter, Terapis, Orang Tua)
-Interface yang intuitif dan mudah dipahami

### 2.Accessibility
-Kontras warna yang memadai
-Typography yang readable
-Navigasi yang jelas

### 3. Consistency
-Konsistensi visual di seluruh halaman
-pattern yang sama untuk interaksi serupa

---

## 🎨 Color Palette

### Primary Colors css
--primary-color: #2563eb;        /* Biru utama */
--primary-dark: #1e40af;         /* Biru gelap */
--primary-light: #3b82f6;        /* Biru terang */
--secondary-color: #10b981;      /* Hijau sukses */
--warning-color: #f59e0b;        /* Kuning peringatan */
--danger-color: #ef4444;         /* Merah error */
--gray-50: #f9fafb;              /* Background */
--gray-100: #f3f4f6;             /* Border light */
--gray-200: #e5e7eb;             /* Border */
--gray-600: #4b5563;             /* Text secondary */
--gray-800: #1f2937;             /* Text primary */
--gray-900: #111827;             /* Heading */
--status-menunggu: #fbbf24;      /* Kuning */
--status-dipanggil: #06b6d4;     /* Cyan */
--status-proses: #3b82f6;        /* Biru */
--status-selesai: #10b981;       /* Hijau */
--status-batal: #6b7280;         /* Abu-abu */

### fontfamily
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'Fira Code', 'Courier New', monospace;

### fontsize
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */

### spacingsystem
--spacing-1: 0.25rem;    /* 4px */
--spacing-2: 0.5rem;     /* 8px */
--spacing-3: 0.75rem;    /* 12px */
--spacing-4: 1rem;       /* 16px */
--spacing-5: 1.25rem;    /* 20px */
--spacing-6: 1.5rem;     /* 24px */
--spacing-8: 2rem;       /* 32px */
--spacing-10: 2.5rem;    /* 40px */
--spacing-12: 3rem;      /* 48px */

### buttons
<!-- Primary Button -->
<button class="btn btn-primary">Simpan</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">Batal</button>

<!-- Danger Button -->
<button class="btn btn-danger">Hapus</button>

<!-- Small Button -->
<button class="btn btn-sm">Kecil</button>

### card
<div class="card">
  <div class="card-header">Judul</div>
  <div class="card-body">Konten</div>
</div>

### forms
<div class="form-group">
  <label for="input">Label</label>
  <input type="text" id="input" class="form-control" placeholder="Placeholder">
  <small class="form-text">Helper text</small>
</div>

### tables
<table class="table">
  <thead>
    <tr><th>Kolom 1</th><th>Kolom 2</th></tr>
  </thead>
  <tbody>
    <tr><td>Data 1</td><td>Data 2</td></tr>
  </tbody>
</table>

### status
<span class="badge badge-success">Selesai</span>
<span class="badge badge-warning">Menunggu</span>
<span class="badge badge-danger">Batal</span>

### responsivebreakpoints
/* Mobile */
@media (max-width: 640px) { }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }