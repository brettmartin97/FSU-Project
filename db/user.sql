CREATE DATABASE fsu;

CREATE TABLE `user` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` int unsigned NOT NULL
  PRIMARY KEY (`id`)
);

insert  into `user`(`id`,`name`,`email`,`phone`,`address`) values
(1,'Brett Martin','brettdrew@gmail.com',2147483647);
