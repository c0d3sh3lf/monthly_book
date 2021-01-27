# Monthly Book

This application can be used to track your expenses on multiple categories. This also shows the trends and graphs on your spends. Currently, the app supports following functionalities.

- Register User
- Change Own Password
- Login / Logout
- Add Stores
- Edit Stores
- View Stores
- Delete Stores
- Add Products
- Edit Products
- View Products
- Delete Products
- Add Transactions
- Edit Transactions
- View Transactions
- Delete Transactions
- Generate Monthly Lists PDF
- Generate Current Month Transactions PDF
- Generate Monthly Transactions PDF
- Generate Quarterly Transactions PDF
- Generate Half Yearly Transactions PDF
- Generate Transactions for a given range PDF
- View Trends and Charts
- Dashboard

## Installation

To install this applciation, you will need docker and docker-compose installed on your system.

#### Step 1:

Download the application from git using below command

```
bash$ git clone https://github.com/c0d3sh3lf/monthly_book.git
```

#### Step 2:

Navigate to the build directory and run the first_run.sh file

```
bash$ cd monthly_book
bash$ ./first_run.sh
```

#### Step 3:

In this step, we shall setup the database

```
bash$ docker-compose run web python manage.py makemigrations
bash$ docker-compose run web python manage.py migrate
bash$ docker-compose run web python manage.py createsuperuser
```

Enter the information to create a superuser.

#### Step 4:

Once all the above is done, use rebuild.sh to rebuild the application images.

```
bash$ ./rebuild.sh
```

This shall clean up all the resources and run your application. You can access your application using the below address.

[https://127.0.0.1:8000](https://127.0.0.1:8000) OR https://<YOUR_SERVER_IP_ADDR>:8000

#### Step 5:

Cleaning up unused images by running the below command.

```
bash$ docker rmi $(docker images | grep "^<none>" | awk "{print $3}")
```

## Updating Code

Once in a while, we update our code to fix certain bugs, or provide a new feature. You can update the code with following command.

```
bash$ .\code_update.sh
```

## Backing up your database

It is good to backup your database once in a while or before running the code_update.sh. You can use the below command to backup your database.

```
bash$ docker-compose run web python manage.py dumpdata > db.json
```

## Restoring your database

For some unforseen reasons, if your database crashes or your applciation crashes and your to build your database once again, you can do so if you have taken the backup of your database previously by running these commands.

```
bash$ docker-compose run web python manage.py makemigrations
bash$ docker-compose run web python manage.py migrate
bash$ docker-compose run web python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> exit()
bash$ docker-compose run web python manage.py loaddata db.json
```

## Contributers:

1. Sumit Shrivastava [@invad3rsam](https://twitter.com/invad3rsam) - Author
