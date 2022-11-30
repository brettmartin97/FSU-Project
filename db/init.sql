CREATE DATABASE if not exists fsu;

use fsu;

-- Updating tables in database.
CREATE TABLE if not exists `Role` (
  `roleId` int unsigned NOT NULL AUTO_INCREMENT,
  `roleName` varchar(50) NOT NULL,
  `commission` varchar(30),
  `hourlyRate` double,
  `hasGoal` boolean NOT NULL,
  `hasBooth` boolean NOT NULL,
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `RoleGoal` (
  `goalId` int unsigned NOT NULL AUTO_INCREMENT,
  `roleId` int unsigned NOT NULL,
  `goalName` varchar(80) NOT NULL,
  `value` double,
  PRIMARY KEY (`goalId`),
  FOREIGN KEY (`roleId`) REFERENCES `Role` (`roleId`) ON DELETE CASCADE
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
  `management` boolean NOT NULL,
  PRIMARY KEY (`userId`),
  FOREIGN KEY (`roleId`) REFERENCES `Role` (`roleId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `Schedule` (
  `scheduleId` int unsigned NOT NULL AUTO_INCREMENT,
  `dayId` int unsigned NOT NULL,
  `userId` int unsigned NOT NULL,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  PRIMARY KEY (`scheduleId`),
  FOREIGN KEY (`userId`) REFERENCES `User` (`userId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `AppointmentType` (
  `appointTypeId` int unsigned NOT NULL AUTO_INCREMENT,
  `typeName` varchar(100) NOT NULL,
  `description` varchar(250) NOT NULL,
  `duration` int NOT NULL,
  `hasHourlyRate` boolean NOT NULL,
  PRIMARY KEY (`appointTypeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE if not exists `Pricing` (
  `totalPriceId` int unsigned NOT NULL AUTO_INCREMENT,
  `appointTypeId` int unsigned NOT NULL,
  `roleId` int unsigned NOT NULL,
  `price` double NOT NULL,
  PRIMARY KEY (`totalPriceId`),
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
insert  into `Role`(`roleId`,`roleName`, `commission`, `hourlyRate`, `hasGoal`, `hasBooth`) values
(1, 'Level 1 Stylist', '45%', 0, TRUE, FALSE),
(2, 'Level 2 Stylist', '45%', 0, TRUE, FALSE),
(3, 'Level 3 Stylist', '45%', 0, TRUE, FALSE),
(4, 'Level 4 Stylist', '45%', 0, TRUE, FALSE),
(5, 'Level 5 Stylist', '50%', 0, TRUE, FALSE),
(6, 'Level 6 Stylist', '50%', 0, TRUE, FALSE),
(7, 'Level 7 Stylist', '55%', 0, TRUE, FALSE),
(8, 'Level 8 Stylist', '60%', 0, TRUE, FALSE),
(9, 'Level 9 Stylist', '60%', 0, TRUE, FALSE),
(10, 'Level 10 Stylist', '60%', 0, TRUE, FALSE),
(11, 'Booth Stylist', '60%', 0, FALSE, TRUE),
(12, 'Deskworker', 'N\A', 0, FALSE, FALSE),
(13, 'Admin', 'N\A', 0, FALSE, FALSE);


-- Insert data into the RoleGoal table.
insert  into `RoleGoal`(`goalId`, `roleId`,`goalName`, `value`) values
(1, 1, 'Total money made per day:', 300.00),
(2, 1, 'Percentage time booked:', 70.00),
(3, 1, 'Percentage of clients that rebooked:', 60.00),
(4, 2, 'Total money made per day:', 500.00),
(5, 2, 'Percentage time booked:', 70.00),
(6, 2, 'Percentage of clients that rebooked:', 60.00),
(7, 3, 'Total money made per day:', 600.00),
(8, 3, 'Percentage time booked:', 70.00),
(9, 3, 'Percentage of clients that rebooked:', 60.00),
(10, 4, 'Total money made per day:', 700.00),
(11, 4, 'Percentage time booked:', 75.00),
(12, 4, 'Percentage of clients that rebooked:', 65.00),
(13, 5, 'Total money made per day:', 800.00),
(14, 5, 'Percentage time booked:', 75.00),
(15, 5, 'Percentage of clients that rebooked:', 65.00),
(16, 6, 'Total money made per day:', 900.00),
(17, 6, 'Percentage time booked:', 75.00),
(18, 6, 'Percentage of clients that rebooked:', 65.00),
(19, 7, 'Total money made per day:', 1000.00),
(20, 7, 'Percentage time booked:', 80.00),
(21, 7, 'Percentage of clients that rebooked:', 70.00),
(22, 8, 'Total money made per day:', 1100.00),
(23, 8, 'Percentage time booked:', 80.00),
(24, 8, 'Percentage of clients that rebooked:', 70.00),
(25, 9, 'Total money made per day:', 1200.00),
(26, 9, 'Percentage time booked:', 80.00),
(27, 9, 'Percentage of clients that rebooked:', 70.00),
(28, 10, 'Total money made per day:', 1350.00),
(29, 10, 'Percentage time booked:', 85.00),
(30, 10, 'Percentage of clients that rebooked:', 75.00);


-- Insert data into the User table.
insert  into `User`(`userId`,`firstName`,`lastName`,`email`,`phone`,`username`,`password`,`roleId`, `management`) values
(1,'Admin', 'User','brettdrew@gmail.com',2147483647,'admin','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C',13, TRUE),
(2,'Alex', 'Temp1','temp1@gmail.com',111222333,'alex','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 1, FALSE),
(3,'Bella', 'Temp2','temp2@gmail.com',444555666,'bella','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 2, FALSE),
(4,'Carla', 'Temp3','temp3@gmail.com',777888999,'carla','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 3, FALSE),
(5,'Diane', 'Temp4','temp4@gmail.com',222111333,'diane','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 4, FALSE),
(6,'Elise', 'Temp5','temp5@gmail.com',333111222,'elise','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 5, FALSE),
(7,'Faith', 'Temp6','temp6@gmail.com',222333111,'faith','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 6, FALSE),
(8,'Grace', 'Temp7','temp7@gmail.com',444555444,'grace','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 7, FALSE),
(9,'Holly', 'Temp8','temp8@gmail.com',555444555,'holly','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 8, FALSE),
(10,'Isla', 'Temp9','temp9@gmail.com',111555222,'isla','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 9, FALSE),
(11,'Jolyne', 'Temp10','temp10@gmail.com',222444555,'jolyne','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 10, FALSE),
(12,'Katherine', 'Temp11','temp11@gmail.com',777222555,'katherine','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 11, FALSE),
(13,'Lily', 'Temp12','temp12@gmail.com',999777111,'lily','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 12, FALSE),
(14,'Max', 'Temp13','temp13@gmail.com',999111777,'max','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 12, TRUE),
(15,'Nick', 'Temp14','temp14@gmail.com',999888111,'nick','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C', 12, False);

-- Insert data into the Schedule table.
insert  into `Schedule`(`scheduleId`,`dayId`,`userId`, `startTime`, `endTime`) values
(1,1,2, '09:00:00', '17:00:00'),
(2,2,2, '09:00:00', '17:00:00'),
(3,3,2, '09:00:00', '17:00:00'),
(4,1,3, '09:00:00', '17:00:00'),
(5,2,3, '09:00:00', '17:00:00'),
(6,3,3, '09:00:00', '17:00:00'),
(7,4,4, '09:00:00', '17:00:00'),
(8,5,4, '09:00:00', '17:00:00'),
(9,6,4, '10:00:00', '17:00:00'),
(10,3,5, '09:00:00', '17:00:00'),
(11,4,5, '09:00:00', '17:00:00'),
(12,5,5, '09:00:00', '17:00:00'),
(13,6,5, '10:00:00', '17:00:00'),
(14,7,5, '10:00:00', '17:00:00'),
(15,1,6, '09:00:00', '17:00:00'),
(16,2,6, '09:00:00', '17:00:00'),
(17,3,6, '09:00:00', '17:00:00'),
(18,4,6, '09:00:00', '17:00:00'),
(19,5,6, '09:00:00', '17:00:00'),
(20,4,7, '09:00:00', '17:00:00'),
(21,5,7, '09:00:00', '17:00:00'),
(22,6,7, '10:00:00', '17:00:00'),
(23,7,7, '09:00:00', '17:00:00'),
(24,1,8, '12:00:00', '20:00:00'),
(25,2,8, '12:00:00', '20:00:00'),
(26,3,8, '12:00:00', '20:00:00'),
(27,4,8, '12:00:00', '20:00:00'),
(28,5,8, '12:00:00', '20:00:00'),
(29,1,9, '09:00:00', '17:00:00'),
(30,2,9, '12:00:00', '20:00:00'),
(31,3,9, '12:00:00', '20:00:00'),
(32,4,9, '12:00:00', '20:00:00'),
(33,5,9, '12:00:00', '20:00:00'),
(34,1,10, '12:00:00', '20:00:00'),
(35,2,10, '12:00:00', '20:00:00'),
(36,5,10, '09:00:00', '17:00:00'),
(37,6,10, '09:00:00', '17:00:00'),
(38,7,10, '09:00:00', '17:00:00'),
(39,1,11, '12:00:00', '20:00:00'),
(40,2,11, '12:00:00', '20:00:00'),
(41,3,11, '12:00:00', '20:00:00'),
(42,4,11, '12:00:00', '20:00:00'),
(43,5,11, '12:00:00', '20:00:00'),
(44,2,12, '09:00:00', '18:00:00'),
(45,3,12, '09:00:00', '18:00:00'),
(46,4,12, '09:00:00', '18:00:00'),
(47,5,12, '09:00:00', '18:00:00'),
(48,6,12, '10:00:00', '17:00:00'),
(49,1,13, '09:00:00', '17:00:00'),
(50,2,13, '09:00:00', '17:00:00'),
(51,3,13, '09:00:00', '17:00:00'),
(52,4,13, '09:00:00', '17:00:00'),
(53,5,13, '09:00:00', '17:00:00'),
(54,6,14, '10:00:00', '17:00:00'),
(55,7,14, '10:00:00', '17:00:00'),
(56,1,15, '12:00:00', '20:00:00'),
(57,2,15, '12:00:00', '20:00:00'),
(58,3,15, '12:00:00', '20:00:00'),
(59,4,15, '12:00:00', '20:00:00'),
(60,5,15, '12:00:00', '20:00:00');

-- Insert data into the AppointmentType table.
insert  into `AppointmentType`(`appointTypeId`,`typeName`, `description`, `duration`, `hasHourlyRate`) values
(1, 'Barber Cut', 'A basic haircut. Includes fades but does not include Skin Fades or Pixies. All haircuts include a shampoo and blow-dry', 30, FALSE),
(2, 'Shag', 'DescTemp2', 30, FALSE),
(3, 'Long Cut', 'DescTemp3', 40, FALSE),
(4, 'Precision Cut', 'DescTemp4', 40, FALSE),
(5, 'Balayage', 'DescTemp5', 120, FALSE),
(6, 'Bleach and Tone', 'DescTemp6', 180, FALSE),
(7, 'Partial Highlight', 'DescTemp7', 90, FALSE),
(8, 'Full Highlight', 'DescTemp8', 120, FALSE),
(9, 'Corrective color', 'DescTemp9', 360, FALSE),
(10, 'Wax', 'DescTemp10', 30, FALSE),
(11, 'Root retouch', 'DescTemp11', 60, FALSE),
(12, 'Conditioning Treatment', 'DescTemp12', 30, FALSE),
(13, 'Undercut', 'DescTemp13', 30, FALSE),
(14, 'Bang Trim ', 'DescTemp14', 15, FALSE),
(15, 'All over color', 'DescTemp15', 180, FALSE),
(16, 'Toner', 'DescTemp16', 20, FALSE);


-- Insert data into the Pricing table.
insert  into `Pricing`(`totalPriceId`,`appointTypeId`, `roleId`, `price`) values
(1, 1, 1, 40.00),
(2, 1, 2, 40.00),
(3, 1, 3, 40.00),
(4, 1, 4, 40.00),
(5, 1, 5, 50.00),
(6, 1, 6, 50.00),
(7, 1, 7, 55.00),
(8, 1, 8, 60.00),
(9, 1, 9, 60.00),
(10, 1, 10, 60.00),
(11, 1, 11, 60.00),
(12, 2, 1, 55.00),
(13, 2, 2, 55.00),
(14, 2, 3, 55.00),
(15, 2, 4, 55.00),
(16, 2, 5, 60.00),
(17, 2, 6, 60.00),
(18, 2, 7, 65.00),
(19, 2, 8, 70.00),
(20, 2, 9, 70.00),
(21, 2, 10, 70.00),
(22, 2, 11, 70.00),
(23, 3, 1, 55.00),
(24, 3, 2, 55.00),
(25, 3, 3, 55.00),
(26, 3, 4, 55.00),
(27, 3, 5, 60.00),
(28, 3, 6, 60.00),
(29, 3, 7, 65.00),
(30, 3, 8, 70.00),
(31, 3, 9, 70.00),
(32, 3, 10, 70.00),
(33, 3, 11, 70.00),
(34, 4, 1, 45.00),
(35, 4, 2, 45.00),
(36, 4, 3, 45.00),
(37, 4, 4, 45.00),
(38, 4, 5, 50.00),
(39, 4, 6, 50.00),
(40, 4, 7, 55.00),
(41, 4, 8, 60.00),
(42, 4, 9, 60.00),
(43, 4, 10, 60.00),
(44, 4, 11, 60.00),
(45, 5, 1, 185.00),
(46, 5, 2, 185.00),
(47, 5, 3, 185.00),
(48, 5, 4, 185.00),
(49, 5, 5, 195.00),
(50, 5, 6, 195.00),
(51, 5, 7, 200.00),
(52, 5, 8, 205.00),
(53, 5, 9, 205.00),
(54, 5, 10, 205.00),
(55, 5, 11, 205.00),
(56, 6, 1, 195.00),
(57, 6, 2, 195.00),
(58, 6, 3, 195.00),
(59, 6, 4, 195.00),
(60, 6, 5, 205.00),
(61, 6, 6, 205.00),
(62, 6, 7, 210.00),
(63, 6, 8, 220.00),
(64, 6, 9, 220.00),
(65, 6, 10, 220.00),
(66, 6, 11, 220.00),
(67, 7, 1, 145.00),
(68, 7, 2, 145.00),
(69, 7, 3, 145.00),
(70, 7, 4, 145.00),
(71, 7, 5, 155.00),
(72, 7, 6, 155.00),
(73, 7, 7, 160.00),
(74, 7, 8, 165.00),
(75, 7, 9, 165.00),
(76, 7, 10, 165.00),
(77, 7, 11, 165.00),
(78, 8, 1, 165.00),
(79, 8, 2, 165.00),
(80, 8, 3, 165.00),
(81, 8, 4, 165.00),
(82, 8, 5, 175.00),
(83, 8, 6, 175.00),
(84, 8, 7, 180.00),
(85, 8, 8, 185.00),
(86, 8, 9, 185.00),
(87, 8, 10, 185.00),
(88, 8, 11, 185.00),
(89, 9, 1, 100.00),
(90, 9, 2, 100.00),
(91, 9, 3, 100.00),
(92, 9, 4, 100.00),
(93, 9, 5, 105.00),
(94, 9, 6, 105.00),
(95, 9, 7, 110.00),
(96, 9, 8, 115.00),
(97, 9, 9, 115.00),
(98, 9, 10, 115.00),
(99, 9, 11, 115.00),
(100, 10, 1, 15.00),
(101, 10, 2, 15.00),
(102, 10, 3, 15.00),
(103, 10, 4, 15.00),
(104, 10, 5, 20.00),
(105, 10, 6, 20.00),
(106, 10, 7, 25.00),
(107, 10, 8, 30.00),
(108, 10, 9, 30.00),
(109, 10, 10, 30.00),
(110, 10, 11, 30.00),
(111, 11, 1, 65.00),
(112, 11, 2, 65.00),
(113, 11, 3, 65.00),
(114, 11, 4, 65.00),
(115, 11, 5, 70.00),
(116, 11, 6, 70.00),
(117, 11, 7, 75.00),
(118, 11, 8, 80.00),
(119, 11, 9, 80.00),
(120, 11, 10, 80.00),
(121, 11, 11, 80.00),
(122, 12, 1, 30.00),
(123, 12, 2, 30.00),
(124, 12, 3, 30.00),
(125, 12, 4, 30.00),
(126, 12, 5, 35.00),
(127, 12, 6, 35.00),
(128, 12, 7, 40.00),
(129, 12, 8, 45.00),
(130, 12, 9, 45.00),
(131, 12, 10, 45.00),
(132, 12, 11, 45.00),
(133, 13, 1, 25.00),
(134, 13, 2, 25.00),
(135, 13, 3, 25.00),
(136, 13, 4, 25.00),
(137, 13, 5, 30.00),
(138, 13, 6, 30.00),
(139, 13, 7, 35.00),
(140, 13, 8, 40.00),
(141, 13, 9, 40.00),
(142, 13, 10, 40.00),
(143, 13, 11, 40.00),
(144, 14, 1, 10.00),
(145, 14, 2, 10.00),
(146, 14, 3, 10.00),
(147, 14, 4, 10.00),
(148, 14, 5, 15.00),
(149, 14, 6, 15.00),
(150, 14, 7, 20.00),
(151, 14, 8, 25.00),
(152, 14, 9, 25.00),
(153, 14, 10, 25.00),
(154, 14, 11, 25.00),
(155, 15, 1, 85.00),
(156, 15, 2, 85.00),
(157, 15, 3, 85.00),
(158, 15, 4, 85.00),
(159, 15, 5, 90.00),
(160, 15, 6, 90.00),
(161, 15, 7, 95.00),
(162, 15, 8, 100.00),
(163, 15, 9, 100.00),
(164, 15, 10, 100.00),
(165, 15, 11, 100.00),
(166, 16, 1, 30.00),
(167, 16, 2, 30.00),
(168, 16, 3, 30.00),
(169, 16, 4, 30.00),
(170, 16, 5, 35.00),
(171, 16, 6, 35.00),
(172, 16, 7, 40.00),
(173, 16, 8, 45.00),
(174, 16, 9, 45.00),
(175, 16, 10, 45.00),
(176, 16, 11, 45.00);


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


-- Insert date into the Appointment table.
insert  into `Appointment`(`appointId`,`userId`,`appointTypeId`,`customerId`,`totalPriceId`, `notes`, `startTime`) values
(1, 2, 1, 1, 1, 'Baked in Temp Appointment1', '2022-11-28 09:00:00'),
(2, 2, 1, 2, 1, 'Baked in Temp Appointment2', '2022-11-28 09:30:00'),
(3, 2, 6, 6, 56, 'Baked in Temp Appointment3', '2022-11-28 10:00:00'),
(4, 2, 2, 3, 12, 'Baked in Temp Appointment4', '2022-11-28 13:00:00'),
(5, 2, 7, 15, 67, 'Baked in Temp Appointment5', '2022-11-28 13:30:00'),
(6, 2, 2, 3, 12, 'Baked in Temp Appointment6', '2022-11-28 15:00:00'),
(7, 2, 3, 13, 23, 'Baked in Temp Appointment7', '2022-11-28 15:50:00'),
(8, 3, 9, 10, 90, 'Baked in Temp Appointment8', '2022-11-29 10:00:00'),
(9, 3, 1, 11, 2, 'Baked in Temp Appointment9', '2022-11-29 16:00:00'),
(10, 4, 5, 15, 47, 'Baked in Temp Appointment10', '2022-12-01 09:00:00'),
(11, 4, 5, 6, 47, 'Baked in Temp Appointment11', '2022-12-01 11:30:00'),
(12, 5, 8, 12, 81, 'Baked in Temp Appointment12', '2022-12-01 10:00:00'),
(13, 5, 8, 13, 81, 'Baked in Temp Appointment13', '2022-12-01 13:00:00'),
(14, 6, 16, 14, 170, 'Baked in Temp Appointment14', '2022-11-30 09:30:00'),
(15, 6, 11, 9, 115, 'Baked in Temp Appointment15', '2022-11-30 10:30:00'),
(16, 6, 10, 8, 104, 'Baked in Temp Appointment16', '2022-11-30 12:25:00'),
(17, 6, 4, 7, 104, 'Baked in Temp Appointment17', '2022-11-30 14:45:00'),
(18, 7, 5, 11, 50, 'Baked in Temp Appointment18', '2022-12-02 11:00:00'),
(19, 7, 12, 9, 127, 'Baked in Temp Appointment19', '2022-12-02 14:00:00'),
(20, 8, 1, 5, 7, 'Baked in Temp Appointment20', '2022-11-28 12:00:00'),
(21, 8, 3, 12, 29, 'Baked in Temp Appointment21', '2022-11-28 15:00:00'),
(22, 9, 5, 11, 52, 'Baked in Temp Appointment22', '2022-12-02 15:00:00'),
(23, 9, 16, 14, 173, 'Baked in Temp Appointment23', '2022-12-02 18:00:00'),
(24, 9, 1, 7, 8, 'Baked in Temp Appointment24', '2022-12-02 19:00:00'),
(25, 10, 9, 7, 97, 'Baked in Temp Appointment25', '2022-12-03 09:00:00'),
(26, 10, 16, 1, 174, 'Baked in Temp Appointment26', '2022-12-03 15:00:00'),
(27, 10, 10, 12, 108, 'Baked in Temp Appointment27', '2022-12-03 16:15:00'),
(28, 11, 11, 4, 120, 'Baked in Temp Appointment28', '2022-12-01 12:00:00'),
(29, 11, 10, 9, 109, 'Baked in Temp Appointment29', '2022-12-01 15:00:00'),
(30, 11, 4, 8, 43, 'Baked in Temp Appointment30', '2022-12-01 12:00:00'),
(31, 12, 15, 3, 165, 'Baked in Temp Appointment31', '2022-12-02 10:00:00'),
(32, 12, 7, 1, 77, 'Baked in Temp Appointment32', '2022-12-02 14:00:00'),
(33, 12, 3, 15, 33, 'Baked in Temp Appointment33', '2022-12-02 16:00:00'),
(34, 6, 16, 14, 170, 'Baked in Temp Appointment14', '2022-11-28 09:30:00'),
(35, 6, 11, 9, 115, 'Baked in Temp Appointment15', '2022-11-29 10:30:00'),
(36, 6, 10, 8, 104, 'Baked in Temp Appointment16', '2022-11-30 12:25:00'),
(37, 6, 4, 7, 104, 'Baked in Temp Appointment17', '2022-12-01 14:45:00'),
(38, 6, 16, 14, 170, 'Baked in Temp Appointment14', '2022-11-28 09:30:00'),
(39, 6, 11, 9, 115, 'Baked in Temp Appointment15', '2022-11-29 10:30:00'),
(40, 6, 10, 8, 104, 'Baked in Temp Appointment16', '2022-11-30 12:25:00'),
(41, 6, 4, 7, 104, 'Baked in Temp Appointment17', '2022-12-01 14:45:00');