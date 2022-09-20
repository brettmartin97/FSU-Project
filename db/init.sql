CREATE DATABASE if not exists fsu;

use fsu;

CREATE TABLE if not exists `user` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` int unsigned NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` INT unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

insert  into `user`(`id`,`name`,`email`,`phone`,`username`,`password`,`role`) values
(1,'Brett Martin','brettdrew@gmail.com',2147483647,'bmartin','$2b$12$nWfHVJ/lyS8HxtL6Q6953.EoV79MMjQn4hegWhxEXka6lWb9CJF0C',13);


-- Testing comment.