# inventory-management
This is a inventory management system that is no longer being used. Able to convert user inputs into a unique label, barcode and qr code

# How to Setup
1. Clone Project
```
git clone https://github.com/soysushi/tribe_inventory.git
```

2. Go To Project Directory
```
cd inventory-management
```
3. Create Virtual Environment
```
python3 -m venv venv
```
4. Active Virtual Environment
```
source venv/bin/activate
```
5. Install Requirements File
```
pip install -r requirements.txt
```
6. Migrate Database
```
python manage.py migrate
```
7. Create Super User
```
python manage.py createsuperuser
```
8. Run Project
```
python manage.py runserver
```
