
# Patients

The essence of our project is an online organizer for doctors so that they can have a convenient database of patients and have a list of records for each date and hour.

## Technologies we used
### Python technologies
- for manipulating filesystem paths we used moduls **pathlib** and **os**
- for parsing commands from the console we used modul **sys**
- for get info about date and etc. we used modul **datetime**
- for create main part of backend of course we used **django**

### Database
For database we used **sqllite**.
It is an embedded, server-less relational database management system and does not require any installation.

### Frontend
For easier create a html and css part of project we use **boosttrap**

## Navigation in application

When you first hit the site, you see the main page:

![image](https://user-images.githubusercontent.com/116711001/231284846-1bf38294-e3cb-44af-b5c8-89d434078cbc.png)

For using all oportunities our site, you have to register or log in, if you already have account.

![image](https://user-images.githubusercontent.com/116711001/231284999-0e99b87a-d5fb-4b1c-b725-404ee9c909f0.png)
![image](https://user-images.githubusercontent.com/116711001/231285020-73c01b4e-3388-4bd1-9421-900ba8b67202.png)


After autentification you can move on site by side menu:

![image](https://user-images.githubusercontent.com/116711001/231285167-9c72401c-0d08-4378-8bb0-51c5f0b0c76b.png)

### 'Add patient' 
On this page you can add patient to your patients list.

![image](https://user-images.githubusercontent.com/116711001/231386356-1579986f-7a21-4818-8531-f7546ec8a4b3.png)

### 'View patients' 
you can to look on all your patients.

![image](https://user-images.githubusercontent.com/116711001/231285567-4a5077e7-0bd1-4e64-b569-47e8fb59e932.png)

You have to options, what can you do with your patient. Edit info about patient or delete him.

![image](https://user-images.githubusercontent.com/116711001/231285745-9a2e71f3-d63d-41d3-b639-56e6f077fa5b.png)

You can search patient in list also.

![image](https://user-images.githubusercontent.com/116711001/231285771-216c9142-b34d-49c9-b9a0-f7dd1066bd82.png)

### 'View calendar'
Here is your calendar to enroll patients and moderate their admission.

![image](https://user-images.githubusercontent.com/116711001/231285884-bb355e86-156a-4e5d-b076-6e9295f3bca2.png)

Tup to buttom **'New event'** for creating new visit.

![image](https://user-images.githubusercontent.com/116711001/231285956-46386269-6bf1-4188-a011-e209a83afa28.png)

![image](https://user-images.githubusercontent.com/116711001/231386703-5dbb2439-8a66-4e2e-8cc0-87252e4ddb5f.png)

## Local run

If you want to run local server, you have to open terminal in directory 'patients' and write next command:
```bash
python manage.py runserver

```

For creating new database in local host write next commands:

```bash
python manage.py makemigrations patients_ap

python manage.py migrate 
```

For creating superuser for admin panel:

```bash
python manage.py createsuperuser
```





