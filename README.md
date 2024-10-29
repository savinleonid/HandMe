
HandMe
HandMe is a second-hand marketplace web application inspired by platforms like Avito, designed to facilitate the buying and selling of used items. Built with Django and PostgreSQL, the app allows users to create, manage, and edit listings, explore products by category, and view details, along with full user account functionality.

Features
User Authentication: Registration, login, logout, profile management
Product Listings: Create, edit, delete, and browse listings
Filtering: Simultaneous filtering by category, search, and location
Image Uploads: Profile and product image uploads with automatic save functionality
Tech Stack
Backend: Django, PostgreSQL
Frontend: HTML, CSS, JavaScript, Bootstrap
Styling: Custom-styled popups, interactive navigation, and form controls
Setup
Clone the repository:

bash
Kodu kopyala
git clone https://github.com/savinleonid/HandMe.git
Install dependencies:

bash
Kodu kopyala
pip install -r requirements.txt
Setup Database:

Configure PostgreSQL in your Django settings.py.
Run migrations:
bash
Kodu kopyala
python manage.py migrate
Run server:

bash
Kodu kopyala
python manage.py runserver
Usage
Access the homepage to browse available items.
Register or log in to add or manage your own listings.
Use search, category filters, and location options for targeted browsing.
Contributing
Fork the project.
Create a new branch (git checkout -b feature/YourFeature).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature/YourFeature).
Open a pull request.
License
Distributed under the MIT License.

