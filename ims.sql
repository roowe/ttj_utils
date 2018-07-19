SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `fund`;
CREATE TABLE `fund` (
  `code` varchar(10) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `fund` (`code`, `name`) VALUES
('000051',	'沪深300'),
('000071',	'华夏恒生ETF'),
('000216',	'黄金'),
('000478',	'建信500'),
('000614',	'德国30(DAX)'),
('000968',	'广发养老'),
('001051',	'华夏上证50ETF'),
('001052',	'中证500'),
('001061',	'海外收益债'),
('001064',	'广发环保'),
('001180',	'广发医药'),
('001469',	'全指金融'),
('003376',	'7-10年国开债'),
('003765',	'广发创业板'),
('004752',	'中证传媒'),
('050027',	'博时信用债'),
('100032',	'中证红利'),
('100038',	'富国300增强'),
('110026',	'易方达创业板'),
('160416',	'石油指数'),
('160629',	'鹏华传媒'),
('162411',	'华宝油气'),
('270048',	'广发纯债'),
('340001',	'可转债'),
('501018',	'南方原油'),
('502010',	'证券公司');

DROP TABLE IF EXISTS `fund_history`;
CREATE TABLE `fund_history` (
  `timestamp` bigint(20) NOT NULL,
  `code` varchar(10) NOT NULL,
  `change_pct` decimal(10,6) NOT NULL,
  `unit_net_value` decimal(10,6) NOT NULL,
  `acc_net_value` decimal(10,6) NOT NULL,
  UNIQUE KEY `code_timestamp` (`code`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `fund_rate`;
CREATE TABLE `fund_rate` (
  `timestamp` bigint(20) NOT NULL,
  `code` varchar(10) NOT NULL,
  `rate` decimal(10,6) NOT NULL,
  `acc_rate` decimal(10,6) NOT NULL,
  UNIQUE KEY `code_timestamp` (`code`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

