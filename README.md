# ChaosServer
"Chaos Server" implementation in Python/Django

### Overview
The "Chaos server" has one endpoint - /response, and can operate in one of the following modes:
  1. normal - in this mode, 100% of /response requests will result in 200 http responses.
  2. degraded - in this mode, 50% of /response requests will result in 200 http responses,
                              25% of /response requests will result in 401 http responses,
                              25% of /response requests will result in 500 http responses.
  3. failure - in this mode, 5% of /response requests will result in 200 http responses,
                            95% of /response requests will result in 500 http responses.

The "Chaos server" has two interfaces - admin panel & test client, that will be explained in the following section.

### Setup & Run the Project
*** Assumptions:  Python is installed on user's computer. 
                  Python commands can be executed from any location on user's computer. 
- First, click "Clone or download"->"Download ZIP" in this git repository.
- Unzip the project to a required directory on your computer.
- Open "cmd" shell.
- Change the current working directory to the project's directory.
- Running the server: python manage.py runserver
- In order to set server's "chaos mode", open web browser and go to the admin panel: 127.0.0.1:8000/admin/
- Here, you will be required to provide Username & Password - use the following:
    Username: admin
    Password: adminadmin
- Now you can choose the required "chaos mode" using the related buttons.
- In order to probe the server's /response endpoint:
    - Open "cmd" shell.
    - Change the current working directory to the project's directory.
    - Run: python test.py
    - It will probe the server's /response endpoint for 100 times, and will output (to the console) the real percentage of the different http statuses from the server.
- Enjoy. :)

### Unit Tests
- The project includes unit tests for the two project's apps: admin_panel, response.
- In order to run them:
    - Open "cmd" shell.
    - Change the current working directory to the project's directory.
    - Run: python manage.py test admin_panel response
- admin_panel unit tests: Check that http requests from admin panel change the server's chaos_mode properly.
- response unit tests: Check that the required percentages of each http response are received in each server's chaos_mode.
