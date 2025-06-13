import os
import sys
# DON'T CHANGE THIS PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import json

# Import models
from models.user import db, User, TourGuide, Country, City, Trip, Review, ContactRequest
from models.user import Visitor, ForumCategory, ForumPost, ForumReply

# Import routes
from routes.user import user_bp
from routes.guide import guide_bp
from routes.admin import admin_bp
from routes.forum import forum_bp

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/auth')
app.register_blueprint(guide_bp, url_prefix='/guide')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(forum_bp, url_prefix='/forum')

# Custom filter for JSON parsing
@app.template_filter('from_json')
def from_json_filter(value):
    if value:
        try:
            return json.loads(value)
        except:
            return []
    return []

# Main routes
@app.route('/')
def index():
    # Get featured guides
    featured_guides = TourGuide.query.filter_by(is_featured=True, is_approved=True).limit(6).all()
    
    # Get countries for search
    countries = Country.query.all()
    
    return render_template('index.html', 
                         featured_guides=featured_guides,
                         countries=countries)

@app.route('/search')
def search():
    # Get search parameters
    country_id = request.args.get('country_id', type=int)
    city_id = request.args.get('city_id', type=int)
    keyword = request.args.get('keyword', '')
    sort = request.args.get('sort', 'rating')
    
    # Build query
    query = TourGuide.query.filter_by(is_approved=True)
    
    if country_id:
        query = query.filter_by(country_id=country_id)
    
    if city_id:
        query = query.filter_by(city_id=city_id)
    
    if keyword:
        query = query.filter(
            db.or_(
                TourGuide.bio_ar.contains(keyword),
                TourGuide.bio_en.contains(keyword),
                TourGuide.specializations.contains(keyword)
            )
        )
    
    # Apply sorting
    if sort == 'rating':
        query = query.order_by(TourGuide.rating.desc())
    elif sort == 'price_low':
        query = query.order_by(TourGuide.hourly_rate.asc())
    elif sort == 'price_high':
        query = query.order_by(TourGuide.hourly_rate.desc())
    elif sort == 'experience':
        query = query.order_by(TourGuide.experience_years.desc())
    
    guides = query.all()
    
    # Get countries and cities for filters
    countries = Country.query.all()
    cities = []
    if country_id:
        cities = City.query.filter_by(country_id=country_id).all()
    
    return render_template('search.html',
                         guides=guides,
                         countries=countries,
                         cities=cities,
                         selected_country=country_id,
                         selected_city=city_id,
                         keyword=keyword)

@app.route('/guide/<int:guide_id>')
def guide_profile(guide_id):
    guide = TourGuide.query.get_or_404(guide_id)
    
    # Get guide's trips
    trips = Trip.query.filter_by(guide_id=guide_id, is_active=True).all()
    
    # Get reviews
    reviews = Review.query.filter_by(guide_id=guide_id, is_approved=True).order_by(Review.created_at.desc()).limit(10).all()
    
    return render_template('guide_profile.html',
                         guide=guide,
                         trips=trips,
                         reviews=reviews)

@app.route('/contact-guide/<int:guide_id>', methods=['POST'])
def contact_guide(guide_id):
    try:
        data = request.get_json()
        
        contact_request = ContactRequest(
            guide_id=guide_id,
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            travel_dates=data.get('travel_dates'),
            group_size=data.get('group_size'),
            message=data.get('message')
        )
        
        db.session.add(contact_request)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم إرسال طلبك بنجاح! سيتواصل معك المرشد قريباً.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'حدث خطأ في إرسال الطلب.'
        })

@app.route('/api/cities/<int:country_id>')
def get_cities(country_id):
    cities = City.query.filter_by(country_id=country_id).all()
    return jsonify([{
        'id': city.city_id,
        'name_ar': city.name_ar,
        'name_en': city.name_en
    } for city in cities])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms():
    return render_template('terms.html', current_date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Add sample data if tables are empty
        if Country.query.count() == 0:
            # Add countries
            countries_data = [
                {'name_ar': 'مصر', 'name_en': 'Egypt', 'code': 'EG'},
                {'name_ar': 'السعودية', 'name_en': 'Saudi Arabia', 'code': 'SA'},
                {'name_ar': 'الإمارات العربية المتحدة', 'name_en': 'United Arab Emirates', 'code': 'AE'},
                {'name_ar': 'الأردن', 'name_en': 'Jordan', 'code': 'JO'},
                {'name_ar': 'لبنان', 'name_en': 'Lebanon', 'code': 'LB'},
                {'name_ar': 'تركيا', 'name_en': 'Turkey', 'code': 'TR'},
                {'name_ar': 'فرنسا', 'name_en': 'France', 'code': 'FR'},
                {'name_ar': 'إيطاليا', 'name_en': 'Italy', 'code': 'IT'},
                {'name_ar': 'إسبانيا', 'name_en': 'Spain', 'code': 'ES'},
                {'name_ar': 'المملكة المتحدة', 'name_en': 'United Kingdom', 'code': 'GB'}
            ]
            
            for country_data in countries_data:
                country = Country(**country_data)
                db.session.add(country)
            
            db.session.commit()
            
            # Add cities
            cities_data = [
                # Egypt
                {'name_ar': 'القاهرة', 'name_en': 'Cairo', 'country_id': 1},
                {'name_ar': 'الإسكندرية', 'name_en': 'Alexandria', 'country_id': 1},
                {'name_ar': 'الأقصر', 'name_en': 'Luxor', 'country_id': 1},
                {'name_ar': 'أسوان', 'name_en': 'Aswan', 'country_id': 1},
                # Saudi Arabia
                {'name_ar': 'الرياض', 'name_en': 'Riyadh', 'country_id': 2},
                {'name_ar': 'جدة', 'name_en': 'Jeddah', 'country_id': 2},
                {'name_ar': 'مكة المكرمة', 'name_en': 'Mecca', 'country_id': 2},
                {'name_ar': 'المدينة المنورة', 'name_en': 'Medina', 'country_id': 2},
                # UAE
                {'name_ar': 'دبي', 'name_en': 'Dubai', 'country_id': 3},
                {'name_ar': 'أبوظبي', 'name_en': 'Abu Dhabi', 'country_id': 3},
                {'name_ar': 'الشارقة', 'name_en': 'Sharjah', 'country_id': 3},
                # Jordan
                {'name_ar': 'عمان', 'name_en': 'Amman', 'country_id': 4},
                {'name_ar': 'البتراء', 'name_en': 'Petra', 'country_id': 4},
                {'name_ar': 'العقبة', 'name_en': 'Aqaba', 'country_id': 4},
                # Lebanon
                {'name_ar': 'بيروت', 'name_en': 'Beirut', 'country_id': 5},
                {'name_ar': 'طرابلس', 'name_en': 'Tripoli', 'country_id': 5},
                # Turkey
                {'name_ar': 'إسطنبول', 'name_en': 'Istanbul', 'country_id': 6},
                {'name_ar': 'أنقرة', 'name_en': 'Ankara', 'country_id': 6},
                {'name_ar': 'كابادوكيا', 'name_en': 'Cappadocia', 'country_id': 6},
                # France
                {'name_ar': 'باريس', 'name_en': 'Paris', 'country_id': 7},
                {'name_ar': 'نيس', 'name_en': 'Nice', 'country_id': 7},
                {'name_ar': 'ليون', 'name_en': 'Lyon', 'country_id': 7},
                # Italy
                {'name_ar': 'روما', 'name_en': 'Rome', 'country_id': 8},
                {'name_ar': 'ميلان', 'name_en': 'Milan', 'country_id': 8},
                {'name_ar': 'البندقية', 'name_en': 'Venice', 'country_id': 8},
                # Spain
                {'name_ar': 'مدريد', 'name_en': 'Madrid', 'country_id': 9},
                {'name_ar': 'برشلونة', 'name_en': 'Barcelona', 'country_id': 9},
                {'name_ar': 'إشبيلية', 'name_en': 'Seville', 'country_id': 9},
                # UK
                {'name_ar': 'لندن', 'name_en': 'London', 'country_id': 10},
                {'name_ar': 'مانشستر', 'name_en': 'Manchester', 'country_id': 10},
                {'name_ar': 'إدنبرة', 'name_en': 'Edinburgh', 'country_id': 10}
            ]
            
            for city_data in cities_data:
                city = City(**city_data)
                db.session.add(city)
            
            db.session.commit()
        
        # Add forum categories if they don't exist
        if ForumCategory.query.count() == 0:
            categories_data = [
                {
                    'name_ar': 'تجارب السفر',
                    'name_en': 'Travel Experiences',
                    'description_ar': 'شارك تجاربك السياحية والذكريات الجميلة',
                    'description_en': 'Share your travel experiences and beautiful memories',
                    'icon': 'fas fa-plane',
                    'sort_order': 1
                },
                {
                    'name_ar': 'نصائح السفر',
                    'name_en': 'Travel Tips',
                    'description_ar': 'نصائح مفيدة للمسافرين من ذوي الخبرة',
                    'description_en': 'Useful tips for travelers from experienced people',
                    'icon': 'fas fa-lightbulb',
                    'sort_order': 2
                },
                {
                    'name_ar': 'الوجهات السياحية',
                    'name_en': 'Tourist Destinations',
                    'description_ar': 'مناقشة أفضل الوجهات السياحية حول العالم',
                    'description_en': 'Discuss the best tourist destinations around the world',
                    'icon': 'fas fa-map-marked-alt',
                    'sort_order': 3
                },
                {
                    'name_ar': 'أسئلة وأجوبة',
                    'name_en': 'Questions & Answers',
                    'description_ar': 'اطرح أسئلتك واحصل على إجابات من المجتمع',
                    'description_en': 'Ask questions and get answers from the community',
                    'icon': 'fas fa-question-circle',
                    'sort_order': 4
                },
                {
                    'name_ar': 'التصوير السياحي',
                    'name_en': 'Travel Photography',
                    'description_ar': 'شارك صورك السياحية ونصائح التصوير',
                    'description_en': 'Share your travel photos and photography tips',
                    'icon': 'fas fa-camera',
                    'sort_order': 5
                }
            ]
            
            for category_data in categories_data:
                category = ForumCategory(**category_data)
                db.session.add(category)
            
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)

