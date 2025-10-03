# 📦 Flask Stock Tracking System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-Contact%20Maintainers-lightgrey.svg)](https://github.com/Ayatar/FlaskStockTrackingApp)

> **EN:** A responsive Flask dashboard to manage products, categories, stock movements, and business reports from a single place.
>
> **TR:** Ürünleri, kategorileri, stok hareketlerini ve raporları tek bir panelden yöneten duyarlı bir Flask uygulaması.

---

## 📑 Table of Contents

- [English Documentation](#english)
- [Türkçe Dokümantasyon](#türkçe)

---

## English

### 🎯 Overview

The Flask Stock Tracking System helps small and medium teams stay on top of inventory. It centralizes product records, category management, stock inflow/outflow workflows, and produces PDF/Excel reports and analytics dashboards powered by SQLAlchemy.

### ✨ Features

- ✅ Product and category CRUD with Flask-WTF forms and SQLAlchemy models
- 📊 Stock movement workflows with automatic history and critical stock alerts
- 📱 Dashboard with key metrics, charts, and mobile-friendly responsive tables
- 📤 Export options: Excel product lists and PDF dashboard summaries
- 🔍 Analytics module for trend insights, filtering, and searching
- 🔒 Built-in CSRF protection, security headers, and environment-driven settings

### 🛠️ Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF
- **Frontend:** Bootstrap 5, Font Awesome, custom responsive CSS
- **Data/Reports:** SQLite (default), pandas, openpyxl, reportlab
- **Testing:** pytest, coverage

### 📋 Prerequisites

- Python 3.10 or newer (developed with Python 3.12)
- Git (optional, for cloning)
- A virtual environment tool (e.g., `python -m venv`)

### ⚙️ Environment Variables

Create a `.env` file in the project root (sample values below). All variables are optional; defaults live in `config.py`.

```env
SECRET_KEY=change-me-to-random-string
DATABASE_URL=sqlite:///stok.db
SESSION_COOKIE_SECURE=false
REMEMBER_COOKIE_SECURE=false
WTF_CSRF_TIME_LIMIT=3600
```

### 🚀 Quick Start

#### Installation

```powershell
# Clone the repository
git clone https://github.com/Ayatar/FlaskStockTrackingApp.git
cd FlaskStockTrackingApp

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

SQLite is used by default. On first launch, the application seeds three example categories.

#### Running the Application

```powershell
# Option 1: Run directly with Python
python app.py

# Option 2: Use Flask CLI
$env:FLASK_APP = "app.py"
flask run
```

Visit **http://127.0.0.1:5000** to access the dashboard.

### 🧪 Running Tests

```powershell
# Quick smoke test suite
python tests\run_tests_fixed.py

# Full test suite with pytest (install test dependencies first)
pip install -r test_requirements.txt
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html
```

### 📂 Project Structure

```
FlaskStockTrackingApp/
├── app.py                  # Flask application with routes and reporting
├── config.py               # Environment-driven configuration
├── models.py               # SQLAlchemy models (Product, Category, StockMovement)
├── forms.py                # Flask-WTF form definitions
├── requirements.txt        # Production dependencies
├── test_requirements.txt   # Test dependencies
├── .env                    # Environment variables (create from .env.example)
├── .gitignore             # Git ignore rules
│
├── templates/              # Jinja2 templates
│   ├── base.html          # Base layout with responsive sidebar
│   ├── index.html         # Dashboard with metrics and charts
│   ├── product_list.html  # Product management
│   ├── category_list.html # Category management
│   ├── stock_movement.html# Stock inflow/outflow
│   ├── reports.html       # Report generation
│   └── analytics.html     # Analytics dashboard
│
├── static/
│   ├── css/
│   │   └── main.css       # Custom responsive styles
│   └── js/
│       └── product_list.js# Client-side interactions
│
├── tests/                  # Automated test suite
│   ├── test_models.py     # Model tests
│   ├── test_forms.py      # Form validation tests
│   ├── test_routes.py     # Route integration tests
│   └── run_tests_fixed.py # Test runner
│
└── instance/               # Instance-specific files (generated)
    └── stok.db            # SQLite database (auto-created)
```


### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📄 License

No explicit license file is included. Contact the maintainers before reusing the source code.

### 📧 Contact

- **Repository:** [FlaskStockTrackingApp](https://github.com/Ayatar/FlaskStockTrackingApp)
- **Issues:** [Report a bug](https://github.com/Ayatar/FlaskStockTrackingApp/issues)

---

## Türkçe

### 🎯 Genel Bakış

Flask Stok Takip Sistemi, küçük ve orta ölçekli ekiplerin stoklarını kontrol altında tutmasına yardımcı olur. Ürün kayıtlarını, kategori yönetimini, stok giriş/çıkış süreçlerini tek noktada toplar ve SQLAlchemy tarafından desteklenen PDF/Excel raporları ile analiz panelleri üretir.

### ✨ Özellikler

- ✅ Flask-WTF formları ve SQLAlchemy modelleriyle ürün ve kategori CRUD işlemleri
- 📊 Otomatik hareket geçmişi ve kritik stok uyarılarıyla stok işlemleri
- 📱 Önemli metrikler, grafikler ve mobil uyumlu duyarlı tablolar içeren gösterge paneli
- 📤 Dışa aktarım seçenekleri: Excel ürün listeleri ve PDF gösterge paneli özetleri
- 🔍 Filtreleme, arama ve trend analizleri için analitik modül
- 🔒 CSRF koruması, güvenlik başlıkları ve ortama göre şekillenen ayarlar

### 🛠️ Teknoloji Paketi

- **Sunucu:** Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF
- **Ön Yüz:** Bootstrap 5, Font Awesome, özel responsive CSS
- **Veri/Raporlama:** SQLite (varsayılan), pandas, openpyxl, reportlab
- **Test:** pytest, coverage

### 📋 Ön Koşullar

- Python 3.10 veya üzeri (proje Python 3.12 ile geliştirildi)
- Git (isteğe bağlı, depoyu klonlamak için)
- Sanal ortam aracı (örneğin `python -m venv`)

### ⚙️ Ortam Değişkenleri

Proje kök dizininde bir `.env` dosyası oluşturun (aşağıdaki örnek değerleri uyarlayabilirsiniz). Tüm alanlar isteğe bağlıdır; varsayılanlar `config.py` dosyasında tanımlıdır.

```env
SECRET_KEY=rastgele-guvenli-bir-anahtar
DATABASE_URL=sqlite:///stok.db
SESSION_COOKIE_SECURE=false
REMEMBER_COOKIE_SECURE=false
WTF_CSRF_TIME_LIMIT=3600
```

### 🚀 Hızlı Başlangıç

#### Kurulum

```powershell
# Depoyu klonlayın
git clone https://github.com/Ayatar/FlaskStockTrackingApp.git
cd FlaskStockTrackingApp

# Sanal ortam oluşturun ve etkinleştirin
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

Varsayılan olarak SQLite kullanılır. Uygulama ilk çalıştığında üç örnek kategori ekler.

#### Uygulamayı Çalıştırma

```powershell
# Seçenek 1: Python ile doğrudan çalıştırın
python app.py

# Seçenek 2: Flask CLI kullanın
$env:FLASK_APP = "app.py"
flask run
```

Tarayıcıda **http://127.0.0.1:5000** adresine giderek gösterge paneline ulaşabilirsiniz.

### 🧪 Testleri Çalıştırma

```powershell
# Hızlı kontrol test paketi
python tests\run_tests_fixed.py

# pytest ile tam test paketi (önce test bağımlılıklarını kurun)
pip install -r test_requirements.txt
pytest

# Kapsam raporu ile testleri çalıştırın
pytest --cov=. --cov-report=html
```

### 📂 Proje Yapısı

```
FlaskStockTrackingApp/
├── app.py                  # Flask uygulaması ve raporlama akışları
├── config.py               # Ortam temelli ayarlar
├── models.py               # SQLAlchemy modelleri (Ürün, Kategori, Hareket)
├── forms.py                # Flask-WTF form tanımları
├── requirements.txt        # Üretim bağımlılıkları
├── test_requirements.txt   # Test bağımlılıkları
├── .env                    # Ortam değişkenleri (.env.example'dan oluşturun)
├── .gitignore             # Git ignore kuralları
│
├── templates/              # Jinja2 şablonları
│   ├── base.html          # Duyarlı kenar çubuğu ile temel düzen
│   ├── index.html         # Metrikler ve grafikler içeren gösterge paneli
│   ├── product_list.html  # Ürün yönetimi
│   ├── category_list.html # Kategori yönetimi
│   ├── stock_movement.html# Stok giriş/çıkış
│   ├── reports.html       # Rapor oluşturma
│   └── analytics.html     # Analitik paneli
│
├── static/
│   ├── css/
│   │   └── main.css       # Özel duyarlı stiller
│   └── js/
│       └── product_list.js# İstemci tarafı etkileşimler
│
├── tests/                  # Otomatik test paketi
│   ├── test_models.py     # Model testleri
│   ├── test_forms.py      # Form doğrulama testleri
│   ├── test_routes.py     # Route entegrasyon testleri
│   └── run_tests_fixed.py # Test çalıştırıcı
│
└── instance/               # Örneğe özel dosyalar (otomatik oluşturulur)
    └── stok.db            # SQLite veritabanı (otomatik oluşturulur)
```


### 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen Pull Request göndermekten çekinmeyin.

### 📄 Lisans

Depoda açık bir lisans dosyası bulunmuyor. Kaynak kodunu kullanmadan önce geliştiricilerle iletişime geçin.

### 📧 İletişim

- **Depo:** [FlaskStockTrackingApp](https://github.com/Ayatar/FlaskStockTrackingApp)
- **Sorunlar:** [Hata bildirin](https://github.com/Ayatar/FlaskStockTrackingApp/issues)

---

<div align="center">
  <p>Made with ❤️ using Flask</p>
  <p>⭐ Star this repo if you find it helpful!</p>
</div>