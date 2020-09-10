————————————————————————— FINAL —————————————

CREATE TABLE Account (
account_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
user_name VARCHAR(255),
password TEXT,
first_name NVARCHAR(255),
last_name NVARCHAR(255),
role_id INT(2),
last_login_time DATETIME
);

CREATE TABLE Role (
role_id INT(2) UNSIGNED  PRIMARY KEY,
role_name NVARCHAR(255)
);


CREATE TABLE Vehicle (
vehicle_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
vehicle_name TEXT,
manufacturer_name TEXT,
year_of_manufacturer INT(6)
);

CREATE TABLE Device (
device_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
bluetooth_mac_address VARCHAR(18),
type_name  NVARCHAR(255),
group_name VARCHAR(255)
);

CREATE TABLE Rent (
rent_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
account_id INT(6),
vehicle_id INT(6),
status NVARCHAR(255)
);

// Insert Rent Table
INSERT INTO Rent(account_id, vehicle_id, status) VALUES(1, 1, "thuê" );
INSERT INTO Rent(account_id, vehicle_id, status) VALUES(3, 1, "thuê" );
INSERT INTO Rent(account_id, vehicle_id, status) VALUES(2, 2, "thuê" );

// Insert Role table
 INSERT INTO Role(role_id,role_name) VALUES(1, "Admin");
 INSERT INTO Role(role_id,role_name) VALUES(2, "Staff");
 INSERT INTO Role(role_id,role_name) VALUES(3, "User");

// Insert Device table
 INSERT INTO Device(bluetooth_mac_address, type_name, group_name) VALUES("DC:A6:32:49:00:D5", "server", "khu_vuc_01" );
 INSERT INTO Device(bluetooth_mac_address, type_name, group_name) VALUES("A4:5E:60:D7:4D:32", "client", "khu_vuc_01" );

INSERT INTO Device(bluetooth_mac_address, type_name, group_name) VALUES('6C:94:F8:BF:2A:9E', "client", "khu_vuc_01" );

// Insert Vehicle Table
INSERT INTO Vehicle(vehicle_name, manufacturer_name, year_of_manufacturer) VALUES("Xe Ford", "Toyota", 2010 );
INSERT INTO Vehicle(vehicle_name, manufacturer_name, year_of_manufacturer) VALUES("Xe Honda Civic", "Honda", 2020 );
INSERT INTO Vehicle(vehicle_name, manufacturer_name, year_of_manufacturer) VALUES("Xe La Dalat", "Nam Viet Nam", 1960 );
INSERT INTO Vehicle(vehicle_name, manufacturer_name, year_of_manufacturer) VALUES("Xe Huyndai X", "Huyndai", 2010 );
INSERT INTO Vehicle(vehicle_name, manufacturer_name, year_of_manufacturer) VALUES("Xe Morning X", "Morning", 2010 );

// Insert Admin- Account Table
INSERT INTO Account(user_name, password, role_id) VALUES("root", "rootroot", 1 );
INSERT INTO Account(user_name, password, role_id, first_name, last_name) VALUES("hockey", "password", 2, "Nhan vien", "Nguyen" );
INSERT INTO Account(user_name, password, role_id, first_name, last_name) VALUES("test_user01", "password", 3, "User 01", "Nguyen" );
INSERT INTO Account(user_name, password, role_id, first_name, last_name) VALUES("test_user02", "password", 3, "User 02", "Nguyen" );
INSERT INTO Account(user_name, password, role_id, first_name, last_name) VALUES("test_user03", "password", 3, "User 03", "Nguyen" );
