# Admin/Manager Guide

Welcome to the Uganda Farm Decision Support System - Manager Dashboard! This guide helps administrators manage the system.

## Table of Contents
1. [Accessing the Manager Dashboard](#1-accessing-the-manager-dashboard)
2. [Managing Farmers](#2-managing-farmers)
3. [Managing Farms](#3-managing-farms)
4. [Managing Crops](#4-managing-crops)
5. [Managing Livestock](#5-managing-livestock)
6. [Managing Recommendations](#6-managing-recommendations)
7. [Creating a Manager Account](#7-creating-a-manager-account)

---

## 1. Accessing the Manager Dashboard

Only staff/administrator accounts can access the manager dashboard.

### Logging In
1. Go to http://127.0.0.1:8000
2. Log in with your staff account
3. You'll automatically be redirected to the Manager Dashboard

### If You Don't Have a Staff Account

Create one using the command line:
```powershell
cd C:\Users\MAGADA\Desktop\MJR\vscode
venv\Scripts\activate
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

---

## 2. Managing Farmers

The manager dashboard shows all registered farmers and:
- Username
- Location
- Phone number
- Number of farms

You can view farmer farms and recommendations.

---

## 3. Managing Farms

### Adding a Farm
1. On the manager dashboard, click "Add Farm"
2. Select the farmer who owns the farm
3. Enter farm details
4. Save

### Editing a Farm
1. Find the farm in the list
2. Click "Edit"
3. Update information
4. Save

### Deleting a Farm
1. Find the farm
2. Click "Delete"
3. Confirm deletion

---

## 4. Managing Crops

### Adding a Crop
1. On manager dashboard, find Crops section
2. Click "Add Crop"
3. Fill in all details:
   - Name
   - Ideal Soil Type
   - Planting Season
   - Expected Yield
   - Description
   - Factors Favouring
   - Layman Knowledge (simple explanation for farmers)
   - Preferred Regions (Ugandan districts/regions
   - Best for Farmer Type (smallholder/commercial
   - Market Potential (Uganda-specific)
   - Planting Instructions
   - Pest & Disease Management (local methods)
4. Save

### Editing a Crop
1. Find crop in list
2. Click Edit
3. Update fields
4. Save

### Deleting a Crop
1. Find crop
2. Delete
3. Confirm

---

## 5. Managing Livestock

### Adding Livestock
1. Manager Dashboard → Livestock
2. Click Add Livestock
3. Fill in details:
   - Name
   - Description
   - Best Regions
   - Expected Income
   - Housing Requirements
   - Feeding Guide
   - Health Tips
   - Market Info
   - Best for Farmer Type
4. Save

---

## 6. Managing Recommendations

Recommendations can be edited or deleted. You can also create manual recommendations.

---

## 7. Creating a Manager Account

To make a user into a manager:
1. Log in to Django Admin at http://127.0.0.1:8000/admin
2. Go to Users
3. Find user
4. Check "Staff status" and "Manager"
5. Save

---

## Uganda-Specific Tips

### Updating Crop Data
Ensure includes pre-loaded with common Ugandan, you can:
- Update market prices
- Add local pests
- Update planting seasons based on latest extension advice
- Add new crops/livestock relevant

### Regional Specific
- Add new regions to `UGANDAN_LOCATIONS` in `core/models.py`

---

## Best Practices

1. **Regularly update crop market info
2. **Keep planting guides simple and practical
3. **Use local language in knowledge
4. **Back database regularly
