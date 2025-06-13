# TourGuideZone - دليل المطور

## نظرة عامة

TourGuideZone هو منصة شاملة تربط السياح بالمرشدين السياحيين المحليين حول العالم. تم تطوير المنصة باستخدام Flask (Python) مع دعم كامل للغة العربية والإنجليزية.

## الميزات الرئيسية

### 🌍 **منصة عالمية**
- دعم أكثر من 10 دول مع 30+ مدينة
- واجهة متعددة اللغات (العربية والإنجليزية)
- تصميم متجاوب لجميع الأجهزة

### 👥 **إدارة المستخدمين**
- نظام مصادقة متقدم مع أدوار متعددة
- ملفات شخصية للمرشدين مع معرض صور
- نظام تقييمات ومراجعات شامل

### 🔍 **بحث متقدم**
- بحث بالدول والمدن
- فلترة حسب التقييم والسعر والخبرة
- بحث بالكلمات المفتاحية

### 💬 **منتدى تفاعلي**
- تسجيل مبسط للزوار
- 5 أقسام متخصصة
- نظام مشاركات وردود

### 🛡️ **الأمان والإدارة**
- لوحة تحكم إدارية شاملة
- نظام صلاحيات متدرج
- حماية من هجمات CSRF

## التقنيات المستخدمة

### Backend
- **Flask 2.3.3** - إطار العمل الرئيسي
- **SQLAlchemy** - ORM لقاعدة البيانات
- **Flask-Login** - إدارة الجلسات
- **Flask-WTF** - نماذج آمنة

### Frontend
- **Bootstrap 5** - إطار CSS
- **Font Awesome** - الأيقونات
- **jQuery** - JavaScript
- **Cairo Font** - خط عربي

### Database
- **SQLite** (افتراضي) - قاعدة بيانات محلية
- **MySQL** (اختياري) - للمواقع الكبيرة

## هيكل المشروع

```
TourGuideZone/
├── main.py              # الملف الرئيسي
├── app.py               # نقطة دخول الإنتاج
├── config.py            # إعدادات التطبيق
├── requirements.txt     # التبعيات
├── models/
│   └── user.py         # نماذج قاعدة البيانات
├── routes/
│   ├── user.py         # طرق المستخدمين
│   ├── guide.py        # طرق المرشدين
│   ├── admin.py        # طرق الإدارة
│   └── forum.py        # طرق المنتدى
├── templates/          # قوالب HTML
├── static/
│   ├── css/           # ملفات CSS
│   ├── js/            # ملفات JavaScript
│   ├── images/        # الصور
│   └── uploads/       # الملفات المرفوعة
└── docs/              # التوثيق
```

## قاعدة البيانات

### الجداول الرئيسية

#### Users (المستخدمين)
- معلومات المستخدم الأساسية
- أدوار النظام (admin, guide, tourist)
- بيانات المصادقة

#### TourGuides (المرشدين)
- ملفات المرشدين الشخصية
- التخصصات والخبرات
- معلومات التواصل والأسعار

#### Countries & Cities (الجغرافيا)
- قائمة الدول والمدن
- دعم الأسماء بالعربية والإنجليزية

#### Forum (المنتدى)
- أقسام المنتدى
- المشاركات والردود
- نظام الزوار المبسط

#### Reviews & Ratings (التقييمات)
- تقييمات المرشدين
- مراجعات مفصلة
- نظام النجوم

## التثبيت والتشغيل

### متطلبات النظام
- Python 3.8+
- pip (مدير الحزم)
- 500MB مساحة تخزين

### خطوات التثبيت

1. **استنساخ المشروع**:
```bash
# إذا كان لديك Git
git clone [repository-url]
cd TourGuideZone

# أو فك ضغط ملف ZIP
unzip TourGuideZone.zip
cd TourGuideZone
```

2. **إنشاء بيئة افتراضية**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows
```

3. **تثبيت التبعيات**:
```bash
pip install -r requirements.txt
```

4. **تشغيل التطبيق**:
```bash
python main.py
```

5. **الوصول للموقع**:
افتح المتصفح واذهب إلى `http://localhost:5000`

## الإعدادات

### متغيرات البيئة

أنشئ ملف `.env` في المجلد الرئيسي:

```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///tourguidezone.db
SITE_URL=http://localhost:5000
ADMIN_EMAIL=admin@tourguidezone.com

# إعدادات البريد الإلكتروني (اختيارية)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### إعدادات قاعدة البيانات

#### SQLite (افتراضي):
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///tourguidezone.db'
```

#### MySQL:
```python
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/database_name'
```

#### PostgreSQL:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/database_name'
```

## API والطرق

### طرق المصادقة
- `POST /auth/register` - تسجيل مستخدم جديد
- `POST /auth/login` - تسجيل الدخول
- `GET /auth/logout` - تسجيل الخروج

### طرق البحث
- `GET /search` - البحث عن المرشدين
- `GET /api/cities/<country_id>` - جلب مدن البلد

### طرق المرشدين
- `GET /guide/<guide_id>` - عرض ملف المرشد
- `POST /contact-guide/<guide_id>` - طلب تواصل

### طرق المنتدى
- `GET /forum/` - الصفحة الرئيسية للمنتدى
- `POST /forum/register` - تسجيل زائر جديد
- `GET /forum/category/<category_id>` - عرض قسم

### طرق الإدارة
- `GET /admin/dashboard` - لوحة التحكم
- `GET /admin/guides` - إدارة المرشدين
- `POST /admin/approve-guide/<guide_id>` - الموافقة على مرشد

## التخصيص والتطوير

### إضافة لغة جديدة

1. **إنشاء ملفات الترجمة**:
```
Resources/
├── Controllers/
│   ├── HomeController.fr.resx  # فرنسي
│   └── HomeController.de.resx  # ألماني
```

2. **تحديث قاعدة البيانات**:
```python
# إضافة أعمدة اللغة الجديدة
name_fr = db.Column(db.String(100))
name_de = db.Column(db.String(100))
```

3. **تحديث القوالب**:
```html
<!-- إضافة دعم اللغة الجديدة -->
<option value="fr">Français</option>
<option value="de">Deutsch</option>
```

### إضافة ميزات جديدة

#### إضافة نوع مستخدم جديد:

1. **تحديث نموذج User**:
```python
# في models/user.py
ROLES = ['admin', 'guide', 'tourist', 'business']  # إضافة business
```

2. **إنشاء طرق جديدة**:
```python
# إنشاء ملف routes/business.py
from flask import Blueprint
business_bp = Blueprint('business', __name__)

@business_bp.route('/dashboard')
@login_required
def dashboard():
    # كود لوحة تحكم الأعمال
    pass
```

3. **تحديث القوالب**:
```html
<!-- إضافة خيارات للأعمال -->
{% if current_user.role == 'business' %}
    <a href="{{ url_for('business.dashboard') }}">لوحة الأعمال</a>
{% endif %}
```

### تحسين الأداء

#### تحسين قاعدة البيانات:
```python
# إضافة فهارس للبحث السريع
class TourGuide(db.Model):
    __tablename__ = 'tour_guides'
    __table_args__ = (
        db.Index('idx_country_city', 'country_id', 'city_id'),
        db.Index('idx_rating', 'rating'),
    )
```

#### تحسين الاستعلامات:
```python
# استخدام eager loading
guides = TourGuide.query.options(
    db.joinedload(TourGuide.country),
    db.joinedload(TourGuide.city)
).filter_by(is_approved=True).all()
```

#### تحسين الصور:
```python
# ضغط الصور تلقائياً
from PIL import Image

def compress_image(image_path, quality=85):
    with Image.open(image_path) as img:
        img.save(image_path, optimize=True, quality=quality)
```

## الاختبار

### اختبارات الوحدة

إنشاء ملف `tests/test_models.py`:

```python
import unittest
from main import app, db
from models.user import User, TourGuide

class TestModels(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def test_user_creation(self):
        user = User(
            username='testuser',
            email='test@example.com',
            full_name='Test User'
        )
        db.session.add(user)
        db.session.commit()
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

if __name__ == '__main__':
    unittest.main()
```

### اختبارات التكامل

إنشاء ملف `tests/test_routes.py`:

```python
import unittest
from main import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TourGuideZone', response.data)
    
    def test_search_page(self):
        response = self.app.get('/search')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

## الأمان

### أفضل الممارسات الأمنية

1. **حماية كلمات المرور**:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# تشفير كلمة المرور
password_hash = generate_password_hash('user_password')

# التحقق من كلمة المرور
is_valid = check_password_hash(password_hash, 'user_password')
```

2. **حماية من CSRF**:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

3. **تنظيف المدخلات**:
```python
from markupsafe import escape

def clean_input(user_input):
    return escape(user_input.strip())
```

4. **تحديد رفع الملفات**:
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

## النشر

### خيارات النشر

#### 1. SmarterASP.NET (موصى به)
- دعم Python/Flask
- قواعد بيانات متعددة
- SSL مجاني
- دعم فني ممتاز

#### 2. Heroku
```bash
# إنشاء Procfile
echo "web: python app.py" > Procfile

# النشر
heroku create your-app-name
git push heroku main
```

#### 3. DigitalOcean
```bash
# إعداد الخادم
sudo apt update
sudo apt install python3-pip nginx
pip3 install -r requirements.txt

# إعداد Gunicorn
gunicorn --bind 0.0.0.0:5000 main:app
```

#### 4. AWS EC2
- إنشاء instance جديد
- تثبيت Python والتبعيات
- إعداد Load Balancer
- استخدام RDS لقاعدة البيانات

### متغيرات الإنتاج

```bash
# متغيرات مطلوبة للإنتاج
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=your-production-database-url
export SITE_URL=https://yourdomain.com
```

## المراقبة والصيانة

### مراقبة الأداء

```python
# إضافة logging
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@app.before_request
def log_request():
    app.logger.info(f'Request: {request.method} {request.url}')
```

### النسخ الاحتياطية

```bash
#!/bin/bash
# سكريبت النسخ الاحتياطي اليومي

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# نسخ قاعدة البيانات
sqlite3 tourguidezone.db ".backup $BACKUP_DIR/db_backup_$DATE.db"

# نسخ الملفات المرفوعة
tar -czf $BACKUP_DIR/uploads_backup_$DATE.tar.gz static/uploads/

# حذف النسخ القديمة (أكثر من 30 يوم)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

## المساهمة

### إرشادات المساهمة

1. **Fork المشروع**
2. **إنشاء branch جديد**:
```bash
git checkout -b feature/new-feature
```

3. **كتابة الكود مع التوثيق**
4. **إضافة اختبارات**
5. **إرسال Pull Request**

### معايير الكود

- استخدام PEP 8 لـ Python
- توثيق جميع الدوال
- كتابة اختبارات للميزات الجديدة
- استخدام أسماء متغيرات واضحة

## الدعم

### الحصول على المساعدة

- **GitHub Issues**: للمشاكل التقنية
- **البريد الإلكتروني**: support@tourguidezone.com
- **التوثيق**: راجع هذا الدليل أولاً

### الموارد المفيدة

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)
- [Bootstrap Components](https://getbootstrap.com/docs/5.0/components/)
- [Font Awesome Icons](https://fontawesome.com/icons)

---

**تم تطوير TourGuideZone بواسطة Manus AI**

*آخر تحديث: ديسمبر 2024*

