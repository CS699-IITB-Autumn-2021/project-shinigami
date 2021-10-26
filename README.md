## Motivation
Throughout a person's career, whenever he/she joins (or even applies to) a new Institute or Company, they have to go through the process of **Document Verification**. This is a cumbersome process and usually takes up a lot of time and resources.
**DocuFile** aims to provide easy access to a User's documents to the Institute/Company which will help in seamless and smooth verification of documents. It will also decrease the amount of time a person spends uploading the documents each time they apply to different Institutions. 

Users can store their documents safely in DocuFile and share them with a registered Institute or Company as per his/her need.

## List of features
1. The Users will have their documents stored **encrypted** in our servers.
2. Institute or Company can request a User to view their documents.
3. Users can grant access to an Institute's request and can revoke it later after the completion of document verification.
4. Users can request Institute or Company for Certificates.
5. Institute or Company can issue Certificate to Users.
6. A User's documents cannot be viewed by the admins. The private key used for encryption and decryption will not be stored in our servers. 

## Technology Stack
- **HTML**
- **CSS**
- **Bootstrap**
- **Python**
- **SQLite**
- Django


## List of deliverables:
- :heavy_check_mark: Create a sign-up page for Users
- :heavy_check_mark: Create a sign-up page for Institutes and Companies
- :heavy_check_mark: Create a common log-in page
- :heavy_check_mark: In User home-page, they're able to view their current documents.
- :heavy_check_mark: User able to grant or revoke view-permissions to Institute or Company and also see pending view-permissions.
- :heavy_check_mark: User able to see which Institutes or Companies can currently view his/her documents.
- :heavy_check_mark: Institute or Company (I/C) able to view an User's documents after receiving view permission from the User.
- :heavy_check_mark: I/C able to issue Certificates to Users.
- :heavy_check_mark: I/C able to request Users for view-permission of their documents.
- :heavy_check_mark: User able to request for certificates from an I/C.
- :heavy_check_mark: I/C able to view pending Certificate requests from User.
- :heavy_check_mark: Add encryption to Certificates

## Dependencies:
- Python3
- Django
- fpdf 
- PyPDF2

## How to use the app:
1. Install the dependencies first:
    * Python3 can be installed using the following documentation: https://docs.python.org/3/using/index.html
    * Next, open the terminal and type the following commands:
    * pip install Django
    * pip install fpdf
    * pip install PyPDF2
2. Next clone the app:
    * git clone https://github.com/CS699-IITB-Autumn-2021/project-shinigami
3. Finally, run the app:
    * cd project-shinigami/docuFile/
    * python manage.py makemigrations
    * python manage.py migrate
    * python manage.py runserver
4. Then open the url "localhost:8000" in your favourite browser to run the app
5. Once you log-in, you will be redirected to your respective homepage:
    * If you are a User, you can view your documents on the homepage.
    * If you are a Institute/Company, you can view pending Certificate requests on the homepage and also search for User's documents whose access you already have.

## Primary stakeholders of DocuFile:
- Institute/Companies in India: They will be the main customers/buyers of this app
- Student/Professionals: They will be the Users whose documents the Institute/Companies will check.

## Team Shinigami and its Contibutors:
- Vinayak Bhartia (213050041): User homepage and Institute homepage, Uploading Certificates and View-Access, Database integration, Documentation <br />
- Sagar Biswas (213050079): User homepage and Institute homepage, Login and Signup, Database integration, Documentation <br />
- Jaimin Chauhan (213059005): User homepage, Login and Signup, Encryption of documents, Database integration, Documentation <br />

## Path to Code Documentation:


## References:
- https://docs.djangoproject.com/en/3.2/
- https://bootstrapious.com/p/bootstrap-sidebar
- https://www.youtube.com/playlist?list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO
- https://stackoverflow.com/questions/48606087/getting-values-of-queryset-in-django
- https://www.digitalflapjack.com/blog/2021/4/27/bytes-not-bytearrays-with-django-please
- https://docs.djangoproject.com/en/3.2/ref/request-response/
- https://www.delftstack.com/howto/django/django-reset-database/
- https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/
- https://stackoverflow.com/questions/33218629/attaching-pdfs-to-emails-in-django
- https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
- https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
- https://www.geeksforgeeks.org/convert-text-and-text-file-to-pdf-using-python/
- https://www.geeksforgeeks.org/encrypt-and-decrypt-pdf-using-pypdf2/
