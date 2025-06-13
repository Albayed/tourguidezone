# خطوات النشر السريع - TourGuideZone

## ملخص سريع للنشر على SmarterASP.NET

### 1. تحضير الملفات (5 دقائق)
- فك ضغط ملف `TourGuideZone_Complete.zip`
- تأكد من وجود جميع الملفات

### 2. رفع الملفات (10 دقائق)
- استخدم FTP أو File Manager
- ارفع جميع الملفات إلى مجلد `wwwroot`

### 3. إعداد المتغيرات (5 دقائق)
```bash
SECRET_KEY=your-secret-key-here
SITE_URL=https://yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
```

### 4. اختبار الموقع (10 دقائق)
- اذهب إلى عنوان موقعك المؤقت
- تأكد من عمل جميع الصفحات
- جرب التسجيل والبحث

### 5. ربط النطاق (15 دقيقة)
- أضف النطاق في Control Panel
- إعداد DNS Records
- تفعيل SSL

### 6. الانتهاء! 🎉
موقعك جاهز للاستخدام على `https://yourdomain.com`

---

## الملفات المطلوبة في الحزمة:

✅ **ملفات التطبيق:**
- main.py, app.py, config.py
- requirements.txt, Procfile
- مجلدات: models/, routes/, templates/, static/

✅ **التوثيق:**
- DEPLOYMENT_GUIDE.md (دليل مفصل)
- README.md (دليل المطور)
- QUICK_START.md (هذا الملف)

✅ **الإعدادات:**
- .gitignore
- متغيرات البيئة
- إعدادات قاعدة البيانات

---

## روابط مهمة:

- **SmarterASP.NET Control Panel**: https://cp.smarterasp.net
- **دليل النشر المفصل**: DEPLOYMENT_GUIDE.md
- **دليل المطور**: README.md

---

**للمساعدة**: راجع DEPLOYMENT_GUIDE.md للتفاصيل الكاملة

