**Installation**

**Clone the repository:**
$ git clone https://github.com/shaikhnabil/vendor_management.git

**Activate virtual environment**
cd myenv
Scripts\activate

**move to project folder to run project**
cd ../
cd vendor_management
python manage.py runserver
http://127.0.0.1:8000/

**Use thunder client extension to test api endpoint**
set header as header:Authorization value:token 3b74d3d0f5465f69b81534d06ed510dca3a228ce
request api using http://127.0.0.1:8000/vendors/ 
change urls to request other api endpoints
