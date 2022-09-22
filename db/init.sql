CREATE DATABASE if not exists fsu;

use fsu;

CREATE TABLE if not exists `user` (
  `userId` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` int unsigned NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` INT unsigned NOT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert  into `user`(`userId`,`name`,`email`,`phone`,`username`,`password`,`role`) values
(1,'Brett Martin','brettdrew@gmail.com',2147483647,'bmartin','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C',13);


-- New Tables:

CREATE TABLE if not exists `StylistLevel` (
  `levelId` int unsigned NOT NULL AUTO_INCREMENT,
  `levelName` varchar(50) NOT NULL,
  PRIMARY KEY (`levelId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `Stylist` (
  `stylistId` int unsigned NOT NULL AUTO_INCREMENT,
  `userId` int unsigned NOT NULL,
  `levelId` int unsigned NOT NULL,
  `booth` varchar(20) NOT NULL,
  PRIMARY KEY (`stylistId`),
  FOREIGN KEY (`userId`) REFERENCES `user` (`userId`),
  FOREIGN KEY (`levelId`) REFERENCES `StylistLevel` (`levelId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `AppointmentType` (
  `appointTypeId` int unsigned NOT NULL AUTO_INCREMENT,
  `typeName` varchar(100) NOT NULL,
  `description` varchar(250) NOT NULL,
  `duration` int NOT NULL,
  PRIMARY KEY (`appointTypeId`)
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
  `stylistId` int unsigned NOT NULL,
  `appointTypeId` int unsigned NOT NULL,
  `customerId` int unsigned NOT NULL,
  `startTime` datetime NOT NULL,
  `price` varchar(20) NOT NULL,
  `notes` varchar(250) NOT NULL,
  PRIMARY KEY (`appointId`),
  FOREIGN KEY (`stylistId`) REFERENCES `Stylist` (`stylistId`),
  FOREIGN KEY (`appointTypeId`) REFERENCES `AppointmentType` (`appointTypeId`),
  FOREIGN KEY (`customerId`) REFERENCES `Customer` (`customerId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
