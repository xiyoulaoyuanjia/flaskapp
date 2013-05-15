DROP TABLE IF EXISTS `blog_entries`;
CREATE TABLE `blog_entries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) NOT NULL,
  `text` text,
  `href` varchar(500) NOT NULL,
  `oriId` varchar(500) DEFAULT NULL,
  `des` text,
  `datetime` datetime,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

