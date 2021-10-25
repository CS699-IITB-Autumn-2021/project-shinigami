Problem Statement or Motivation


Sell your product/service (One sentence)


List of features


Technology Stack (highlight ones learnt in CS699)
- HTML
- CSS
- Bootstrap
- Python
- SQLite
- Django


List of deliverables:
:heavy_check_mark: Create a sign-up page for Users
:heavy_check_mark: Create a sign-up page for Institutes and Companies
:heavy_check_mark: Create a common log-in page
:heavy_check_mark: In User home-page, they're able to view their current documents.
:heavy_check_mark: User able to grant or revoke view-permissions to Institute or Company and also see pending view-permissions.
:heavy_check_mark: User able to see which Institutes or Companies can currently view his/her documents.
:heavy_check_mark: Institute or Company (I/C) able to view an User's documents after receiving view permission from the User.
:heavy_check_mark: I/C able to issue Certificates to Users.
:heavy_check_mark: I/C able to request Users for view-permission of their documents.
:heavy_check_mark: User able to request for certificates from an I/C.
:heavy_check_mark: I/C able to view pending Certificate requests from User.
:heavy_check_mark: Add encryption to Certificates

Dependencies:
- Python3
- Django
- fpdf 
- PyPDF2

Installing the dependencies:
- Python3 can be installed using the following documentation: https://docs.python.org/3/using/index.html
- pip install Django
- pip install fpdf
- pip install PyPDF2

Running the app:
- git clone https://github.com/CS699-IITB-Autumn-2021/project-shinigami
- cd project-shinigami/docuFile/
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver
- Then go to "localhost:8000" to open the app.

Primary stakeholders of DocuFile:
- Every person who is a student or a professional can be a User
- Every Institute or Company which verifies their student's or worker's documents

Team Shinigami and its Contibutors:
- Vinayak Bhartia (213050041): User homepage, Uploading of image by Institute and view by User <br />
- Sagar Biswas (213050079): User homepage and Institute homepage, Login and Signup <br />
- Jaimin Chauhan (213059005): User homepage and Institute homepage, Login and Signup <br />

Path to Code Documentation (index.html):


References:
- https://docs.djangoproject.com/en/3.2/
- https://bootstrapious.com/p/bootstrap-sidebar
- https://www.youtube.com/playlist?list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO
