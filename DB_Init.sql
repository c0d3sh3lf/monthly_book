CREATE DATABASE monthly_book_data;
CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'Lol@1234';
GRANT ALL ON monthly_book_data.* TO 'djangouser'@'%';
FLUSH PRIVILEGES;