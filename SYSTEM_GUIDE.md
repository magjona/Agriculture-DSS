# Farm Decision Support System (FarmDSS) - Complete Guide

## 🌾 System Overview

FarmDSS is an **AI-powered agricultural decision support system** specifically designed for Ugandan smallholder farmers. It provides intelligent crop recommendations based on farm conditions, precise layman-friendly agricultural knowledge, and a complete farm management platform.

### Key Features:
- ✅ **Farmer Dashboard**: Login/Register with username and secure passwords (4+ characters)
- ✅ **AI Crop Recommendations**: Smart recommendations based on soil type, rainfall, location, and water availability
- ✅ **18 Ugandan Crops**: Pre-loaded with comprehensive AI knowledge for each crop
- ✅ **Manager Dashboard**: Edit crops, update agricultural knowledge, manage all farmer accounts
- ✅ **Layman-Friendly Knowledge**: Plain English explanations suitable for farmers with minimal education
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile devices

---

## 👨‍🌾 Farmer Dashboard Features

### 1. **Sign Up / Register**
**URL**: `http://localhost:8000/signup/`

**Requirements for Registration**:
- ✓ **Username**: Must be unique (system suggests alternatives if taken)
- ✓ **Email**: Valid email address
- ✓ **Password**: Minimum 4 characters, must match confirmation
- ✓ **Phone Number**: Optional
- ✓ **Location**: Select from 16 Ugandan districts
- ✓ **First Farm Details**:
  - Farm name (unique identifier)
  - Farm size in acres
  - Soil type (Loamy, Sandy, Clayey, Silty)
  - Water source (Rain-fed, Irrigation, Well, Borehole, etc.)

**Username Suggestions**: If your preferred username exists, the system suggests alternatives like:
- `username12`
- `username_5`
- `farm_username`

### 2. **Login**
**URL**: `http://localhost:8000/login/`

**Login Options**:
- Enter your registered **username** OR
- Enter your registered **farm name**
- Enter your **password**

### 3. **Dashboard Home**
**URL**: `http://localhost:8000/dashboard/`

**Features**:
- 🌤️ **Weather Information**: Real-time weather for your location
  - Temperature and conditions
  - Humidity and rainfall type
  - Agricultural forecast
  
- 🏡 **My Farms**: View all your registered farms
  - See farm details (size, soil type, water source)
  - Click "AI Recommend" to generate crop recommendations
  
- 💡 **AI Recommendations**: 
  - Displays recommended crops based on your farm conditions
  - Shows AI reasoning (confidence level and evidence)
  - Detailed agricultural knowledge for each crop
  - Layman-friendly explanations

### 4. **Add Multiple Farms**
**URL**: `http://localhost:8000/add-farm/`

- Register additional farms to your account
- Each farm can have different characteristics
- Generate independent recommendations for each farm

### 5. **AI Crop Recommendations**
**How It Works**:

The system analyzes your farm against 18 Ugandan crops using these criteria:

| Factor | Weight | Analysis |
|--------|--------|----------|
| **Soil Match** | 40% | Compares your soil type vs. crop's ideal soil |
| **Water/Season** | 30% | Matches rainfall pattern and planting season |
| **Weather** | 20% | Current weather suitability |
| **Location** | 10% | Crop thriving regions in Uganda |

**Recommendation Quality**:
- **HIGH**: Score 75%+ - Very suitable for your farm
- **MEDIUM**: Score 50-74% - Suitable with proper management
- Only crops scoring 50%+ are recommended

---

## 👔 Manager Dashboard Features

### 1. **Access Requirements**
**URL**: `http://localhost:8000/manager/`

- Requires admin account (`is_staff=True`)
- Use Django admin to create manager accounts
- The app can also store a separate `Manager` profile model for manager metadata
- Contact system administrator for access

### 2. **Admin Functions**

#### **Manage Crops**
- View all 18 pre-loaded Ugandan crops
- **Edit Crop Knowledge**:
  - Crop name and ideal soil type
  - Planting season and expected yield
  - Description
  - **AI Knowledge Base**:
    - Factors favorin growth (soil, climate, water)
    - Layman knowledge (simple farmer-friendly explanations)
    - Preferred Ugandan regions
  
- **Add New Crops**: Create custom crops specific to your region
- **Delete Crops**: Remove crops from system

#### **Manage Farms**
- View all farmer accounts and their farms
- Edit farm details
- Add new farms for farmers
- Delete farms
- Track farms by location

#### **View Recommendations**
- See all recommendations generated for farmers
- Filter by Ugandan location
- Edit recommendation details
- Delete outdated recommendations

#### **Dashboard Statistics**
- Total farmers registered
- Total farms in system
- Total crops available
- Total recommendations generated

---

## 🌽 Available Ugandan Crops (18 Total)

### Staple Foods & Cereals
1. **Maize (Longe 5)** - 25-35 bags/acre - March/August
2. **Rice** - 4-6 tons milled rice/acre - June-July
3. **Sorghum** - 15-20 bags/acre - March-May
4. **Millet** - 10-15 bags/acre - March-May

### Protein Sources
5. **Beans (Kidney & Pinto)** - 8-15 bags/acre - March/September
6. **Groundnuts** - 1-2 tons/acre - April-May

### Staple Foods - Root Crops
7. **Cassava** - 10-20 tons/acre - Year-round
8. **Irish Potatoes** - 15-25 tons/acre - March/August
9. **Sweet Potatoes** - 10-20 tons/acre - Year-round
10. **Matooke (Bananas)** - 400-800 bunches/year - Year-round

### Export & Cash Crops
11. **Robusta Coffee** - 1500-2500 kg/acre - April-June
12. **Sunflower** - 1-2 tons seed/acre - April-May

### Vegetables
13. **Tomatoes** - 15-25 tons/acre - Year-round
14. **Cabbage** - 20-40 tons/acre - July-September
15. **Onions** - 8-12 tons/acre - June-July

### Additional Crops
16. **Sesame** - 0.5-1.5 tons/acre - March-April
17. **Pumpkins & Squash** - 15-30 tons/acre - September-October

---

## 🚀 Getting Started - Step by Step

### For Farmers:

1. **Visit the Landing Page**
   - URL: `http://localhost:8000/`
   - Click "Sign Up" or "Login"

2. **Create Your Account**
   - Choose unique username
   - Enter email and strong password
   - Add your location (select from Ugandan districts)
   - Enter your first farm details

3. **Generate Recommendations**
   - Go to Dashboard
   - Click "AI Recommend" on any farm
   - Review your personalized recommendations
   - Read "Farmer Knowledge" for layman-friendly explanations

4. **Add More Farms**
   - Click "Add Farm" in sidebar
   - Enter farm details
   - Get independent recommendations for each farm

### For Managers:

1. **Log in to Django Admin**
   - URL: `http://localhost:8000/admin/`
   - Create superuser: `python manage.py createsuperuser`

2. **Access Manager Dashboard**
   - Navigate to Manager Area in sidebar
   - View statistics and system overview

3. **Update Crop Knowledge**
   - Click "Manage Crops"
   - Edit each crop to add/update knowledge
   - Focus on "Factors Favoring" and "Layman Knowledge"

4. **Monitor Farmer Activity**
   - View registered farmers
   - Track farms by location
   - Review generated recommendations

---

## 🔐 Security Features

- ✅ **Password Security**: Django's built-in password hashing (PBKDF2)
- ✅ **Username Uniqueness**: Automatic suggestions for taken usernames
- ✅ **Farm Name Uniqueness**: Prevents duplicate farm identifiers
- ✅ **Session Management**: Secure session handling
- ✅ **CSRF Protection**: All forms protected against CSRF attacks
- ✅ **Input Validation**: Server-side validation for all inputs

---

## 📊 Weather Integration

- **Default Uganda Weather Data**: System includes regional weather profiles for all 16 districts
- **Optional OpenWeatherMap API**: Configure in `settings.py` to get real-time weather
- **Location-Based Forecasts**: Different weather profiles for each district
- **Rainfall Pattern Matching**: Recommendations consider current rainfall

---

## � Environment Variables
Set these in your environment before running the app:

```bash
set DJANGO_SECRET_KEY="your-production-secret"
set WEATHER_API_KEY="your-openweathermap-key"
```

- `DJANGO_SECRET_KEY`: must be set for production to avoid using the development fallback key
- `WEATHER_API_KEY`: optional; if not set, the app uses Uganda-specific weather defaults

## 🧪 Initial Setup
Run these commands once after cloning or resetting the database:

```bash
python manage.py migrate
python manage.py seed_crops
python manage.py createsuperuser
```

The `seed_crops` command populates the initial crop database used by the recommendation engine.

## 🚨 Deployment Checklist
Before deploying, ensure:

- `DEBUG = False`
- `ALLOWED_HOSTS` includes only trusted hostnames, not `['*']`
- `DJANGO_SECRET_KEY` is set in the environment
- `WEATHER_API_KEY` is configured if real weather data is desired

---

## �🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Django 4.2.7 |
| **Frontend** | HTML5, Bootstrap 5, JavaScript |
| **Database** | SQLite3 |
| **Authentication** | Django Auth |
| **API** | RESTful endpoints |
| **Mobile** | Responsive Bootstrap design |

---

## 📱 UI Highlights

- **Responsive Design**: Works on phones, tablets, desktops
- **Sidebar Navigation**: Quick access to main features
- **Mobile Bottom Navigation**: Easy navigation on small screens
- **Color-Coded Cards**: Green for success, blue for info, etc.
- **Icons & Visual Indicators**: Font Awesome icons throughout
- **Modal Dialogs**: Easy-to-read crop knowledge details
- **Progress Indicators**: Clear confidence levels for recommendations

---

## 🌍 Uganda-Specific Features

- **16 Ugandan Districts**: Kampala, Gulu, Entebbe, Jinja, Mbarara, Masaka, Mbale, Arua, Lira, Fort Portal, Mukono, Soroti, Hoima, Kitgum, Mubende, and other locations
- **Regional Weather Profiles**: Unique weather patterns for each region
- **Crop-Region Matching**: Recommendations consider regional suitability
- **Local Terminology**: Uses familiar local language for farmers
- **Uganda-Specific Yields**: Expected yields based on Ugandan production standards

---

## 📝 Example Workflows

### Workflow 1: New Farmer Registration & First Recommendation
```
1. Visit /signup/
2. Enter username "john_farmer"
3. Enter email and password
4. Select location "Kampala"
5. Enter first farm: "Green Valley Farm", 5 acres, loamy soil, rain-fed
6. Redirected to Dashboard
7. Click "AI Recommend"
8. See 8-10 recommendations like Maize, Beans, Tomatoes
9. Click "Read Farmer Knowledge" for each crop
10. Learn simple explanations for each crop
```

### Workflow 2: Manager Updates Crop Knowledge
```
1. Login as manager
2. Click "Manager Area"
3. Find Matooke (Bananas) in crop list
4. Click Edit
5. Update "Layman Knowledge" section
6. Add tips about manure and spacing
7. Save changes
8. All future farmer recommendations show updated knowledge
```

### Workflow 3: Multi-Farm Management
```
1. Farmer has 3 farms with different soils
2. "Farm 1": Sandy soil, Cassava, Groundnuts
3. "Farm 2": Loamy soil, Maize, Beans
4. "Farm 3": Clayey soil, Rice, Matooke
5. Each farm gets unique recommendations
6. Farmer can optimize crop choices per farm
```

---

## 🎓 For Layman Farmers

### What makes this system special for YOU:

1. **No Technical Knowledge Needed**
   - Simple "Sign Up" and "Login"
   - Clear buttons and instructions
   - No complex menus

2. **Recommendations You Can Understand**
   - Not just crop names
   - Explanations about WHY each crop suits your farm
   - Tips written in simple English

3. **Based on YOUR Farm**
   - Not generic advice
   - Uses your soil type, water source, location
   - Real weather for your area

4. **Learn While Farming**
   - Read farmer knowledge for each crop
   - Understand soil requirements
   - Learn best practices

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Username already exists | System suggests alternatives like `username12` |
| Can't login | Use farm name instead of username |
| No recommendations | Add a farm first, then click "AI Recommend" |
| Weather not updating | Check if farm location is correct in profile |
| Crops not showing knowledge | Manager needs to update crop details |

---

## 📞 Support & Admin Commands

### Create Admin/Manager Account:
```bash
python manage.py createsuperuser
```

### Seed Crops with AI Knowledge:
```bash
python manage.py seed_crops
```

### Run Development Server:
```bash
python manage.py runserver 0.0.0.0:8000
```

### Apply Database Changes:
```bash
python manage.py migrate
```

---

## ✅ System Status

- ✅ Database: SQLite (db.sqlite3)
- ✅ 18 Ugandan Crops: Pre-loaded with AI knowledge
- ✅ 16 Districts: Configured with weather data
- ✅ Development Server: Running on port 8000
- ✅ All Features: Fully operational

---

## 📚 Key Crop Knowledge Examples

### Maize
**Factors Favoring**: Uganda's tropical climate, 18-30°C, 600-1200mm rainfall
**Farmer Tips**: Plant early in morning, dig holes thumb-size, put 2 seeds, weed in first 4 weeks

### Matooke
**Factors Favoring**: Deep fertile soils, high rainfall (1500mm+), shelter from wind
**Farmer Tips**: Apply plenty of manure, use dry grass mulch, space 3m apart

### Coffee
**Factors Favoring**: Below 1500m altitude, volcanic soils, 2000-3000mm rainfall
**Farmer Tips**: Long-term investment (3-4 years), prune old branches, use shade trees

---

**System Version**: 1.0  
**Last Updated**: June 7, 2026  
**Developed For**: Ugandan Smallholder Farmers  
**Technology**: Django + AI-Powered Recommendations
