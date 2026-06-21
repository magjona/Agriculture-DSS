# Uganda Farm Decision Support System

A Django-based agricultural recommendation system for Ugandan farmers, powered by AI and local knowledge.

## Features

### For Farmers
- 🔐 **Dual Login** - Sign in with username or unique farm name
- 🌱 **AI Crop Recommendations** - Tailored to your soil, water source, and location
- 🐓 **Livestock Recommendations** - Chickens, goats, pigs, cattle, and beekeeping
- 🌦️ **Local Weather Defaults** - Per Ugandan region weather data
- 📊 **Soil Analysis** - Recommendations based on your soil type
- 💰 **Market Insights** - Price and demand information for Ugandan crops
- 🐛 **Pest & Disease Management** - Local control methods
- 📝 **Planting Guides** - Step-by-step instructions
- 📱 **Responsive Design** - Works on mobile phones

### For Managers/Admins
- 👥 **User Management** - View all farmers and their farms
- 🌾 **Crop Management** - Add, edit, remove crops
- 🐓 **Livestock Management** - Manage livestock information
- 📈 **Recommendations Overview** - See all recommendations
- 🗺️ **Location-based Filtering** - Group data by Ugandan region
- 📊 **Quick Statistics** - Overview of system usage

## Ugandan Locations Included
Kampala, Entebbe, Jinja, Masaka, Mbale, Mbarara, Gulu, Lira, Soroti, Arua, Kitgum, Mubende, Kabale, Kasese, Iganga, Fort Portal, Hoima

## Crops Supported
Maize (Longe 5), Matooke (Plantain Bananas), Robusta Coffee, Beans, Cassava, Groundnuts, Sorghum, Millet, Potatoes, Sweet Potatoes, Irish Potatoes, Tomatoes, Cabbage, Onions, Pumpkins, Sunflower, Sesame, Rice

## Quick Start

### 1. Set Up (Run these commands manually!)
Open a fresh Command Prompt or PowerShell in `C:\Users\MAGADA\Desktop\MJR\vscode`:

```powershell
# Activate virtual environment
venv\Scripts\activate

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Load Uganda-specific data
python manage.py seed_crops

# Create admin user (optional but recommended)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

### 2. Access the System
- **Farmer Dashboard**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## Documentation
- [Farmer User Guide](./docs/FARMER_GUIDE.md)
- [Admin/Manager Guide](./docs/ADMIN_GUIDE.md)
- [Migration Instructions](./MIGRATION_INSTRUCTIONS.txt)

## System Requirements
- Python 3.8+
- Django 6.0+
- SQLite3 (built-in)

## Contributing
This system is designed specifically for the Ugandan agricultural context. Local knowledge and feedback are highly valued!
