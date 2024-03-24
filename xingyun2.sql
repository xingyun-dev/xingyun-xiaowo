-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: flaskvue
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `article`
--

DROP TABLE IF EXISTS `article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `article` (
  `articleid` int NOT NULL AUTO_INCREMENT,
  `userid` int DEFAULT NULL,
  `category` tinyint DEFAULT NULL,
  `headline` varchar(255) NOT NULL,
  `content` mediumtext NOT NULL,
  `thumbnail` varchar(40) DEFAULT NULL,
  `readcount` int DEFAULT '0',
  `replycount` int DEFAULT '0',
  `recommended` tinyint DEFAULT '0',
  `hide` tinyint DEFAULT '0',
  `drafted` tinyint DEFAULT '0',
  `checked` tinyint DEFAULT '1',
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  `is_markdown` tinyint NOT NULL DEFAULT '0',
  `article_introduce` text,
  PRIMARY KEY (`articleid`)
) ENGINE=InnoDB AUTO_INCREMENT=263 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `commentid` int NOT NULL AUTO_INCREMENT,
  `userid` int DEFAULT NULL,
  `articleid` int DEFAULT NULL,
  `content` text,
  `ipaddr` varchar(20) DEFAULT NULL,
  `replyid` int DEFAULT '0',
  `agreecount` int DEFAULT '0',
  `opposecount` int DEFAULT '0',
  `hide` tinyint DEFAULT '0',
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  PRIMARY KEY (`commentid`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `favorite`
--

DROP TABLE IF EXISTS `favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorite` (
  `favoriteid` int NOT NULL AUTO_INCREMENT,
  `articleid` int DEFAULT NULL,
  `userid` int DEFAULT NULL,
  `canceled` tinyint DEFAULT '0',
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  PRIMARY KEY (`favoriteid`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  `communicate_user` int DEFAULT NULL,
  PRIMARY KEY (`message_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_vip_follow`
--

DROP TABLE IF EXISTS `tb_vip_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_vip_follow` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vip_id` bigint DEFAULT '0' COMMENT '用户ID(粉丝ID)',
  `followed_vip_id` bigint DEFAULT '0' COMMENT '关tb_vip_follow注的用户ID',
  `status` tinyint(1) DEFAULT '0' COMMENT '关注状态(0关注 1取消)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `vip_followed_indx` (`vip_id`,`followed_vip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户关注关系表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tools`
--

DROP TABLE IF EXISTS `tools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tools` (
  `tools_id` int NOT NULL AUTO_INCREMENT,
  `tools_avatar` varchar(255) NOT NULL,
  `tools_name` varchar(255) NOT NULL,
  `tools_introduce` text,
  `tools_link` varchar(255) DEFAULT NULL,
  `tools_type` varchar(50) NOT NULL,
  `tools_jianjie` text,
  `tools_check` int DEFAULT '0',
  `tools_userid` int DEFAULT NULL,
  `tools_user_nickname` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`tools_id`),
  KEY `fk_tools_userid` (`tools_userid`),
  CONSTRAINT `fk_tools_userid` FOREIGN KEY (`tools_userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_shezhi`
--

DROP TABLE IF EXISTS `user_shezhi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_shezhi` (
  `shezhi_id` int NOT NULL AUTO_INCREMENT,
  `userid` int DEFAULT NULL,
  `wang_img` varchar(255) DEFAULT NULL,
  `wang_name` varchar(255) DEFAULT NULL,
  `wang_user_name` varchar(255) DEFAULT NULL,
  `wang_lian` varchar(255) DEFAULT NULL,
  `wang_user_avatar` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`shezhi_id`),
  KEY `userid` (`userid`),
  CONSTRAINT `user_shezhi_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(32) NOT NULL,
  `nickname` varchar(30) DEFAULT NULL,
  `avatar` varchar(20) DEFAULT NULL,
  `role` varchar(10) NOT NULL DEFAULT 'user',
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL,
  `introduce` varchar(250) DEFAULT '请用一句话介绍自己吧！',
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-24 11:32:23
