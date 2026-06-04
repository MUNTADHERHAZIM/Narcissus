# شاليه النرجس - Narjis Chalet Website

<div align="center">

![شاليه النرجس](https://img.shields.io/badge/شاليه_النرجس-Django-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=for-the-badge&logo=bootstrap)

**موقع Django احترافي لعرض وحجز شاليه النرجس باللغة العربية**

</div>

---

## 📋 المحتويات

- [نظرة عامة](#-نظرة-عامة)
- [المميزات](#-المميزات)
- [المتطلبات](#-المتطلبات)
- [التثبيت](#-التثبيت)
- [التشغيل](#-التشغيل)
- [هيكل المشروع](#-هيكل-المشروع)
- [لوحة الإدارة](#-لوحة-الإدارة)
- [إضافة البيانات](#-إضافة-البيانات)
- [النشر](#-النشر)

---

## 🏠 نظرة عامة

موقع شاليه النرجس هو تطبيق ويب مبني بـ Django لعرض معلومات الشاليه وإدارة الحجوزات. يتميز بتصميم عصري متجاوب ودعم كامل للغة العربية.

### الصفحات المتوفرة:
- **الصفحة الرئيسية**: سلايدر صور احترافي ومعلومات الشاليه
- **معرض الصور**: عرض جميع الصور مع Lightbox
- **تفاصيل الشاليه**: المميزات والأسعار ومواعيد التوفر
- **صفحة الحجز**: نموذج حجز مع التحقق من التواريخ
- **اتصل بنا**: نموذج تواصل ومعلومات الاتصال

---

## ✨ المميزات

### المميزات التقنية:
- ✅ Django 4.x مع أفضل الممارسات
- ✅ تصميم متجاوب مع Bootstrap 5 RTL
- ✅ دعم كامل للغة العربية
- ✅ لوحة إدارة مخصصة بالعربي
- ✅ نظام حجوزات متكامل
- ✅ التحقق من تداخل التواريخ
- ✅ معرض صور مع GLightbox
- ✅ تقويم التوفر مع Flatpickr
- ✅ رسائل تنبيه ديناميكية

### مميزات الحجز:
- ✅ التحقق من صحة البيانات
- ✅ منع الحجز في تواريخ محجوزة مسبقاً
- ✅ حساب السعر الإجمالي تلقائياً
- ✅ تأكيد وإلغاء الحجوزات من لوحة الإدارة

---

## 📋 المتطلبات

- Python 3.10 أو أحدث
- pip (مدير حزم Python)
- Git (اختياري)

---

## 🚀 التثبيت

### 1. استنساخ المشروع أو الانتقال للمجلد:

```bash
cd "شاليه النرجس"
```

### 2. إنشاء بيئة افتراضية:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المتطلبات:

```bash
pip install -r requirements.txt
```

### 4. تطبيق migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. إنشاء مستخدم مدير:

```bash
python manage.py createsuperuser
```

اتبع التعليمات لإدخال:
- اسم المستخدم
- البريد الإلكتروني
- كلمة المرور

---

## ▶️ التشغيل

### تشغيل خادم التطوير:

```bash
python manage.py runserver
```

### الوصول للموقع:
- **الموقع**: http://127.0.0.1:8000/
- **لوحة الإدارة**: http://127.0.0.1:8000/admin/

---

## 📁 هيكل المشروع

```
شاليه النرجس/
├── narjis_chalet/          # مشروع Django الرئيسي
│   ├── __init__.py
│   ├── settings.py         # إعدادات المشروع
│   ├── urls.py             # روابط URL الرئيسية
│   ├── wsgi.py
│   └── asgi.py
│
├── chalet/                 # تطبيق الشاليه
│   ├── __init__.py
│   ├── apps.py             # تكوين التطبيق
│   ├── models.py           # نماذج قاعدة البيانات
│   ├── views.py            # عروض الصفحات
│   ├── urls.py             # روابط التطبيق
│   ├── forms.py            # نماذج الإدخال
│   ├── admin.py            # إعدادات لوحة الإدارة
│   └── templates/          # قوالب HTML
│       ├── base.html
│       └── chalet/
│           ├── index.html
│           ├── gallery.html
│           ├── chalet_detail.html
│           ├── booking.html
│           ├── booking_success.html
│           └── contact.html
│
├── static/                 # الملفات الثابتة
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── media/                  # ملفات المستخدم (الصور)
│   └── chalet_images/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔧 لوحة الإدارة

### الوصول للوحة الإدارة:
1. افتح: http://127.0.0.1:8000/admin/
2. سجل الدخول بحساب المدير

### الأقسام المتوفرة:

#### 📦 إدارة الشاليهات
- إضافة/تعديل/حذف الشاليهات
- إضافة صور متعددة لكل شاليه
- إضافة مزايا الشاليه

#### 📅 إدارة الحجوزات
- عرض جميع الحجوزات
- البحث بالاسم والتاريخ
- تأكيد أو إلغاء الحجوزات
- تصفية حسب الحالة

#### 💬 رسائل الاتصال
- عرض رسائل الزوار
- وضع علامة مقروءة

---

## 📝 إضافة البيانات

### إضافة شاليه جديد:
1. اذهب إلى لوحة الإدارة
2. اضغط على "الشاليهات" ثم "إضافة شاليه"
3. املأ البيانات:
   - اسم الشاليه
   - الوصف
   - الموقع
   - سعر الليلة
   - أقصى عدد نزلاء
4. أضف الصور من قسم "صور الشاليه"
5. أضف المميزات من قسم "مزايا الشاليه"
6. احفظ الشاليه

### تحميل الصور:
- الصور يجب أن تكون بصيغة: JPG, PNG, WebP
- الحجم الموصى به: 1920x1080 للسلايدر
- حدد صورة واحدة كـ "صورة رئيسية"

---

## 🌐 النشر (Production)

### إعدادات الإنتاج:

1. **تعديل settings.py**:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-production-secret-key'
```

2. **جمع الملفات الثابتة**:
```bash
python manage.py collectstatic
```

3. **استخدام PostgreSQL** (اختياري):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'narjis_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### خيارات الاستضافة:
- **PythonAnywhere**: مجاني للمشاريع الصغيرة
- **Railway**: سهل الاستخدام
- **Heroku**: شائع ومستقر
- **DigitalOcean**: للمشاريع الكبيرة
- **AWS/GCP**: للمشاريع المؤسسية

---

## 🛠️ الأوامر المفيدة

```bash
# إنشاء migrations جديدة
python manage.py makemigrations

# تطبيق migrations
python manage.py migrate

# إنشاء مستخدم مدير
python manage.py createsuperuser

# فتح shell Django
python manage.py shell

# جمع الملفات الثابتة
python manage.py collectstatic

# التحقق من المشاكل
python manage.py check
```

---

## 📞 الدعم والتواصل

للاستفسارات والدعم الفني، يرجى التواصل عبر:
- 📧 البريد الإلكتروني: info@narjis-chalet.com
- 📱 الهاتف: +964 XXX XXX XXXX

---

## 📄 الترخيص

هذا المشروع للاستخدام الشخصي والتجاري.

---

<div align="center">

**MUNTADHER HAZIM المطور**

</div>
