CREATE DATABASE if not exists fsu;

use fsu;

-- Updating tables in database.
CREATE TABLE if not exists `Role` (
  `roleId` int unsigned NOT NULL AUTO_INCREMENT,
  `roleName` varchar(50) NOT NULL,
  `commission` varchar(30),
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `User` (
  `userId` int unsigned NOT NULL AUTO_INCREMENT,
  `firstName` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` int unsigned NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `roleId` INT unsigned NOT NULL,
  PRIMARY KEY (`userId`),
  FOREIGN KEY (`roleId`) REFERENCES `Role` (`roleId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `Schedule` (
  `dayId` int unsigned NOT NULL,
  `userId` int unsigned NOT NULL,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  PRIMARY KEY (`dayId`, `userId`),
  FOREIGN KEY (`userId`) REFERENCES `User` (`userId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `AppointmentType` (
  `appointTypeId` int unsigned NOT NULL AUTO_INCREMENT,
  `typeName` varchar(100) NOT NULL,
  `description` varchar(250) NOT NULL,
  `duration` int NOT NULL,
  PRIMARY KEY (`appointTypeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `Pricing` (
  `totalPriceId` int unsigned NOT NULL AUTO_INCREMENT,
  `appointTypeId` int unsigned NOT NULL,
  `roleId` int unsigned NOT NULL,
  `price` varchar(100) NOT NULL,
  PRIMARY KEY (`totalPriceId`, `appointTypeId`, `roleId`),
  FOREIGN KEY (`appointTypeId`) REFERENCES `AppointmentType` (`appointTypeId`) ON DELETE CASCADE,
  FOREIGN KEY (`roleId`) REFERENCES `Role` (`roleId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `Customer` (
  `customerId` int unsigned NOT NULL AUTO_INCREMENT,
  `firstName` varchar(50) NOT NULL,
  `lastName` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phoneNumber` int unsigned NOT NULL,
  PRIMARY KEY (`customerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `Appointment` (
  `appointId` int unsigned NOT NULL AUTO_INCREMENT,
  `userId` int unsigned NOT NULL,
  `appointTypeId` int unsigned NOT NULL,
  `customerId` int unsigned,
  `totalPriceId` int unsigned,
  `notes` varchar(250),
  `startTime` datetime NOT NULL,
  PRIMARY KEY (`appointId`),
  FOREIGN KEY (`userId`) REFERENCES `User` (`userId`) ON DELETE CASCADE,
  FOREIGN KEY (`appointTypeId`) REFERENCES `AppointmentType` (`appointTypeId`) ON DELETE CASCADE,
  FOREIGN KEY (`customerId`) REFERENCES `Customer` (`customerId`) ON DELETE CASCADE,
  FOREIGN KEY (`totalPriceId`) REFERENCES `Pricing` (`totalPriceId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserting dummy test data:

-- Insert data into the Role table.
insert  into `Role`(`roleId`,`roleName`, `commission`) values
(1, 'Level 1 Stylist', '5%'),
(2, 'Level 2 Stylist', '10%'),
(3, 'Level 3 Stylist', '15%'),
(4, 'Level 4 Stylist', '20%'),
(5, 'Level 5 Stylist', '25%'),
(6, 'Level 6 Stylist', '30%'),
(7, 'Level 7 Stylist', '30%'),
(8, 'Level 8 Stylist', '30%'),
(9, 'Level 9 Stylist', '30%'),
(10, 'Level 10 Stylist', '30%'),
(11, 'Booth Stylist', '35%'),
(12, 'Deskworker', 'N\A'),
(13, 'Admin', 'N\A');


-- Insert data into the User table.
insert  into `User`(`userId`,`firstName`,`lastName`,`email`,`phone`,`username`,`password`,`roleId`) values
(1,'Admin', 'User','brettdrew@gmail.com',2147483647,'admin','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C',13),
(2,'Alex', 'Temp1','temp1@gmail.com',111222333,'alex','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 1),
(3,'Bella', 'Temp2','temp2@gmail.com',444555666,'bella','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 2),
(4,'Carla', 'Temp3','temp3@gmail.com',777888999,'carla','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 3),
(5,'Diane', 'Temp4','temp4@gmail.com',222111333,'diane','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 4),
(6,'Elise', 'Temp5','temp5@gmail.com',333111222,'elise','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 5),
(7,'Faith', 'Temp6','temp6@gmail.com',222333111,'faith','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 6),
(8,'Grace', 'Temp7','temp7@gmail.com',444555444,'grace','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 7),
(9,'Holly', 'Temp8','temp8@gmail.com',555444555,'holly','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 8),
(10,'Isla', 'Temp9','temp9@gmail.com',111555222,'isla','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 9),
(11,'Jolyne', 'Temp10','temp10@gmail.com',222444555,'jolyne','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 10),
(12,'Katherine', 'Temp11','temp11@gmail.com',777222555,'katherine','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 11),
(13,'Lily', 'Temp12','temp12@gmail.com',999777111,'lily','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 12);



-- Insert data into the Customer table.
insert  into `Customer`(`customerId`,`firstName`,`lastName`,`email`,`phoneNumber`) values
(1,'Austin', 'Custemp1','custemp1@gmail.com', 850111222),
(2,'Brian', 'Custemp2','custemp2@gmail.com', 850222111),
(3,'Clark', 'Custemp3','custemp3@gmail.com', 850111333),
(4,'Dustin', 'Custemp4','custemp4@gmail.com', 850333111),
(5,'Ethan', 'Custemp5','custemp5@gmail.com', 850111444),
(6,'Fiona', 'Custemp6','custemp6@gmail.com', 850444111),
(7,'George', 'Custemp7','custemp7@gmail.com', 850111555),
(8,'Henry', 'Custemp8','custemp8@gmail.com', 850555111),
(9,'Issac', 'Custemp9','custemp9@gmail.com', 850111777),
(10,'John', 'Custemp10','custemp10@gmail.com', 850777111),
(11,'Ken', 'Custemp11','custemp11@gmail.com', 850111888),
(12,'Larry', 'Custemp12','custemp12@gmail.com', 850888111),
(13,'Mark', 'Custemp13','custemp13@gmail.com', 850111999),
(14,'Nathan', 'Custemp14','custemp14@gmail.com', 850999111),
(15,'Olivia', 'Custemp15','custemp15@gmail.com', 850222333);