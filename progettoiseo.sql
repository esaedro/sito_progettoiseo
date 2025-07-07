/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.11-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: progettoiseo
-- ------------------------------------------------------
-- Server version	10.11.11-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_profiloutente`
--

DROP TABLE IF EXISTS `accounts_profiloutente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profiloutente` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `numero_tessera` varchar(20) DEFAULT NULL,
  `immagine_profilo` varchar(100) DEFAULT NULL,
  `data_tesseramento` date DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `numero_tessera` (`numero_tessera`),
  CONSTRAINT `accounts_profiloutente_user_id_40d4a398_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profiloutente`
--

LOCK TABLES `accounts_profiloutente` WRITE;
/*!40000 ALTER TABLE `accounts_profiloutente` DISABLE KEYS */;
INSERT INTO `accounts_profiloutente` VALUES
(1,'20250613121022','','2025-06-13',1),
(13,'20250704183454','immagini_di_profilo/hanzo.png','2025-07-04',13),
(14,'20250704183519','immagini_di_profilo/ana.png','2025-07-04',14),
(15,'20250704183535','immagini_di_profilo/baptiste.png','2025-07-04',15),
(16,'20250704183551','immagini_di_profilo/mcree.png','2025-07-04',16),
(17,'20250704183604','immagini_di_profilo/mei.png','2025-07-04',17),
(18,'20250704183630','immagini_di_profilo/reinhardt.png','2025-07-04',18),
(19,'20250704183646','immagini_di_profilo/ashe.png','2025-07-04',19),
(20,'20250704183704','','2025-07-04',20),
(21,'20250704183717','','2025-07-04',21),
(22,'20250704183729','','2025-07-04',22),
(23,'20250704183806','immagini_di_profilo/mercy.png','2025-07-04',23),
(24,'20250704183819','immagini_di_profilo/sigma.png','2025-07-04',24),
(25,'20250704183837','immagini_di_profilo/illari.png','2025-07-04',25),
(26,'20250704183850','','2025-07-04',26),
(27,'20250704183859','','2025-07-04',27);
/*!40000 ALTER TABLE `accounts_profiloutente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articoli`
--

DROP TABLE IF EXISTS `articoli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `articoli` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(50) DEFAULT NULL,
  `titolo` varchar(200) NOT NULL,
  `testo` longtext NOT NULL,
  `data_pubblicazione` datetime(6) NOT NULL,
  `immagine` varchar(100) DEFAULT NULL,
  `autori_eliminati` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articoli`
--

LOCK TABLES `articoli` WRITE;
/*!40000 ALTER TABLE `articoli` DISABLE KEYS */;
INSERT INTO `articoli` VALUES
(26,'#Festa #Evento','ISEO TORNA DiPINTA','Sabato 10 e domenica 11 maggio 2025 in Piazza Garibaldi a Iseo torna “IseodiPinta”, il Festival della Birra Artigianale. \r\nUn weekend dedicato alla cultura del bere consapevole, con degustazioni e proposte da birrifici italiani e internazionali selezionati per qualità e stile. \r\nUn’occasione aperta a curiosi, appassionati e operatori per scoprire la ricchezza del panorama brassicolo, tra eccellenze locali e sperimentazioni da tutto il mondo.\r\n\r\n11 BIRRIFICI ITALIANI + 5 PUBLICAN con ETICHETTE anche ESTERE\r\nDomenica 11 ci saranno alcuni laboratori / workshop:\r\n• Ore 11:00 – “Le materie prime della birra”. Degustazione guidata con Gabriele Fontana del Birrificio Pagus\r\n• Ore 15:00 – “Sogno Lucido”. Un viaggio tra aromi, suggestioni e ricordi. Con Federico Cesetti Unionbirrai Beer Taster.\r\n• Ore 16:30 – “Pinte consapevoli”. Degustazione birre no alcol e low alcol. Con Valentina Pe’ della Associazione Le Donne della Birra e Unionbirrai Beer Taster\r\nSOLO SU PRENOTAZIONE tramite messaggio Whatsapp al numero 350 5212690.\r\n10€ cadauno, con 3 birre in degustazione.\r\nPagamento in cassa il giorno dell’evento.\r\nDove: Iseo Piazza Garibaldi\r\nOrari:\r\nSabato dalle 17:00 alle 24:00\r\nDomenica 11:00-22:00','2025-07-04 19:16:58.121403','immagini_articoli/immagine_articolo_1.jpg',''),
(27,'#Evento','FESTIVAL DEI LAGHI EUROPEI – Manca solo 1 settimana!','Si riparte con una nuova edizione ricca di emozioni!\r\n\r\nVenerdì 30 maggio alle 18:30 in Piazza Garibaldi: cerimonia di inaugurazione per dare ufficialmente il via al Festival.\r\nCultura, sapori, tradizioni e tanta bellezza da vivere insieme.\r\n\r\nScopri il programma completo sul sito ufficiale: https://visitlakeiseo.info/festival-dei-laghi-europei/\r\n\r\nNon mancare!','2025-07-04 19:18:36.414032','immagini_articoli/immagine_articolo_3.jpg',''),
(28,'#Intrattenimento','SUONI DI LUCE | VENERDÌ 30 MAGGIO – ORE 21:30','Porto Gabriele Rosa, Iseo\r\n“Suoni di luce. Musiche da film che illuminano la memoria”\r\nUn viaggio emozionante tra jazz, colonne sonore e grandi successi reinterpretati, avvolti dalla calda luce delle candele.\r\nSul palco, il gruppo “Soggetti Ritrovati 5th”:\r\n- Lara Iacovini – voce\r\n- Fabrizio Zappamiglio – chitarra\r\n- Giuseppe Chirico – tromba\r\n- Marco Mottola – contrabbasso\r\n- Marco Marini – ritmica\r\nScopri il programma completo del festival su: https://visitlakeiseo.info/festival-dei-laghi-europei/','2025-07-04 19:21:30.317075','immagini_articoli/immagine_articolo_5.jpg',''),
(29,'','BREVE STOP ALLA CIRCOLAZIONE PER LA MEZZA MARATONA','In occasione della manifestazione sportiva Half Marathon, si informa che il giorno 2 giugno 2025 sarà istituito il divieto di transito nei seguenti orari e tratti stradali:\r\n•	Dalle ore 8:00 alle ore 9:00:\r\no	Via Roma, dall’intersezione con via Martiri della Libertà fino a via Covelo (Comune di Iseo)\r\n•	Dalle ore 8:30 alle ore 9:00:\r\no	Tratto di strada da via Covelo fino al confine con il comune di Sulzano (tratto interessato dalla manifestazione)\r\nSi invita la cittadinanza alla massima collaborazione e si ringrazia per la comprensione.','2025-07-04 19:24:16.648973','immagini_articoli/immagine_articolo_7.jpg','');
/*!40000 ALTER TABLE `articoli` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articolo_autori`
--

DROP TABLE IF EXISTS `articolo_autori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `articolo_autori` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `articolo_id` int(11) NOT NULL,
  `profiloutente_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `articolo_autori_articolo_id_profiloutente_id_78ce1dfc_uniq` (`articolo_id`,`profiloutente_id`),
  KEY `articolo_autori_profiloutente_id_dc20f7bc_fk_accounts_` (`profiloutente_id`),
  CONSTRAINT `articolo_autori_articolo_id_0ee28b38_fk_articoli_id` FOREIGN KEY (`articolo_id`) REFERENCES `articoli` (`id`),
  CONSTRAINT `articolo_autori_profiloutente_id_dc20f7bc_fk_accounts_` FOREIGN KEY (`profiloutente_id`) REFERENCES `accounts_profiloutente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articolo_autori`
--

LOCK TABLES `articolo_autori` WRITE;
/*!40000 ALTER TABLE `articolo_autori` DISABLE KEYS */;
INSERT INTO `articolo_autori` VALUES
(11,26,13),
(12,26,14),
(13,27,13),
(14,28,23),
(15,29,15);
/*!40000 ALTER TABLE `articolo_autori` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES
(2,'Direttivo'),
(1,'Tesserato');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES
(40,1,14),
(41,1,16),
(42,1,28),
(37,1,32),
(38,1,34),
(39,1,36),
(1,2,1),
(2,2,2),
(3,2,3),
(4,2,4),
(5,2,5),
(6,2,6),
(7,2,7),
(8,2,8),
(9,2,9),
(10,2,10),
(11,2,11),
(12,2,12),
(13,2,13),
(14,2,14),
(15,2,15),
(16,2,16),
(17,2,17),
(18,2,18),
(19,2,19),
(20,2,20),
(21,2,21),
(22,2,22),
(23,2,23),
(24,2,24),
(25,2,25),
(26,2,26),
(27,2,27),
(28,2,28),
(29,2,29),
(30,2,30),
(31,2,31),
(32,2,32),
(33,2,33),
(34,2,34),
(35,2,35),
(36,2,36);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add articolo',7,'add_articolo'),
(26,'Can change articolo',7,'change_articolo'),
(27,'Can delete articolo',7,'delete_articolo'),
(28,'Can view articolo',7,'view_articolo'),
(29,'Can add evento',8,'add_evento'),
(30,'Can change evento',8,'change_evento'),
(31,'Can delete evento',8,'delete_evento'),
(32,'Can view evento',8,'view_evento'),
(33,'Can add profilo utente',9,'add_profiloutente'),
(34,'Can change profilo utente',9,'change_profiloutente'),
(35,'Can delete profilo utente',9,'delete_profiloutente'),
(36,'Can view profilo utente',9,'view_profiloutente');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES
(1,'pbkdf2_sha256$870000$HkteUcQD2YogysM1eDN4qo$Eo4jgHmIx/fznOvpb5SoOvuOe7aDNsPCnPA2y0+gxjc=','2025-07-04 19:11:42.900599',1,'admin','','','',1,1,'2025-06-13 12:10:22.093316'),
(13,'pbkdf2_sha256$870000$qyZKvG4yiIe7jFyN6wLCed$sVhtbXHCHy9Uwp7K+0OJ07egpqAxoq7uQk9sBOOwL88=','2025-07-04 19:15:11.994193',0,'luca.lucchi@gmail.com','Luca','Lucchi','luca.lucchi@gmail.com',0,1,'2025-07-04 18:34:53.000000'),
(14,'pbkdf2_sha256$870000$XmhmpcxiEG92Yk45liMA7F$B1CSCZCwJS6HtbNZI8ReTxeB/mKSDw3oBU2Rz0XlR4w=','2025-07-04 18:43:05.966889',0,'alessia.alessiani@yahoo.it','Alessia','Alessiani','alessia.alessiani@yahoo.it',0,1,'2025-07-04 18:35:18.000000'),
(15,'pbkdf2_sha256$870000$UaLqrD4obIj6k8DTm3Do7Z$yL3moFp716jOnQCJ0b+fiy8OBDmvfrcjhHzDd4JYgHw=','2025-07-04 19:23:06.531336',0,'marco.marchesi@libero.it','Marco','Marchesi','marco.marchesi@libero.it',0,1,'2025-07-04 18:35:35.000000'),
(16,'pbkdf2_sha256$870000$O0ulreuHgTa07hWYLyJUEG$WqOt1yaxkHBpqMMdRvKY4RRip6RwwgzOQKWdBkf/GM8=','2025-07-04 18:55:03.321200',0,'francesco.franceschetti@alice.it','Francesco','Franceschetti','francesco.franceschetti@alice.it',0,1,'2025-07-04 18:35:51.000000'),
(17,'pbkdf2_sha256$870000$QuIjTQvCtbuMGXjL6g4ja9$R9dcysSGIKs9jBns7QTJyzCQaOn9D61+V8WHv57dC+w=','2025-07-04 18:56:10.871793',0,'giulia.giulianini@gmail.com','Giulia','Giulianini','giulia.giulianini@gmail.com',0,1,'2025-07-04 18:36:04.000000'),
(18,'pbkdf2_sha256$870000$ugPMtpYMXUSwpIBelGHp50$FJryLL7qRc7sAjoNgVSpWynutw36u1OAWOWXdwweFt8=','2025-07-04 19:48:25.899253',0,'roberto','Roberto','Roberti','roberto.roberti@tin.it',0,1,'2025-07-04 18:36:30.000000'),
(19,'pbkdf2_sha256$870000$dOfmN6p734KQGE8W7O9Ggp$BqgOr2Wp/7jcWP0eHeo38x+BtfKqrT8M/PZpnShY7GI=','2025-07-04 19:53:35.203083',0,'stefania','Stefania','Stefanini','stefania.stefanini@virgilio.it',0,1,'2025-07-04 18:36:46.000000'),
(20,'pbkdf2_sha256$870000$DAdvcKspkKHN8ZnVkHITFo$7LWN4U4gFVbrfNRuAlM705MXOVNamOydm+6pMkwHuus=','2025-07-04 19:02:23.569965',0,'maurizio','Maurizio','Mauriziani','maurizio.mauriziani@live.it',0,1,'2025-07-04 18:37:03.495489'),
(21,'pbkdf2_sha256$870000$t400VEPyKYPcRfuGvaaDMN$Lblju/HhJCG/lT/zQAu5cdJYdg1TDnCpivzm9UON3Vo=','2025-07-04 19:03:08.733988',0,'daniele','Daniele','Danieli','daniele.danieli@inwind.it',0,1,'2025-07-04 18:37:16.000000'),
(22,'pbkdf2_sha256$870000$rI6w29YTYTDSGe0wY53KBj$dAcSId6ndSOZ5hCK9vM8IjSK7vJzeKViswiOhkZMCqk=','2025-07-04 19:03:49.655381',0,'andrea','Andrea','Andreani','andrea.andreani@iol.it',0,1,'2025-07-04 18:37:29.000000'),
(23,'pbkdf2_sha256$870000$u1L84Nj60uVmFYRQHJKKFf$8zVBlCcYw4MpMN64ArC/l9PN/mrzKJKQUVbzOWqfXQs=','2025-07-04 19:44:55.820346',0,'sofia','Sofia','Sofiani','sofia.sofiani@tiscali.it',0,1,'2025-07-04 18:38:05.000000'),
(24,'pbkdf2_sha256$870000$oKlthaCIt4BSyvibSmbeUz$ODtftAbWedX75DueyKbeOdoLxb+wQoz8Kef78gzkNIo=','2025-07-04 19:05:23.893419',0,'lorenzo','Lorenzo','Lorenzini','lorenzo.lorenzini@telecom.it',0,1,'2025-07-04 18:38:18.000000'),
(25,'pbkdf2_sha256$870000$tX1RL89bQVlOHKd7rjvwOp$kRQVioDk/CH90TLK+LnHcD1KO/4HND6u63mlRdgORng=','2025-07-04 19:39:49.379554',0,'gabriella','Gabriella','Gabrielli','gabriella.gabrielli@fastweb.it',0,1,'2025-07-04 18:38:37.000000'),
(26,'pbkdf2_sha256$870000$kHo9Ov7fjnxB7iBhcbTez8$xhuuzC6SrtD19Knc/bsT8vERIKnb77IcT2y/k+RIscU=','2025-07-04 19:36:20.451387',0,'riccardo','Riccardo','Riccardi','riccardo.riccardi@libero.it',0,1,'2025-07-04 18:38:49.684201'),
(27,'pbkdf2_sha256$870000$UAcpGXYT7uMizHZy2lyDWS$fR8+nsNBwpwc0wBk2uYDO9l+DvqgdwNmhF9ceOWCmt8=','2025-07-04 19:52:30.697788',0,'davide','Davide','Daviddi','davide.daviddi@gmail.com',0,1,'2025-07-04 18:38:59.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES
(1,1,1),
(16,13,1),
(39,13,2),
(17,14,1),
(31,14,2),
(18,15,1),
(40,15,2),
(19,16,1),
(35,16,2),
(20,17,1),
(37,17,2),
(21,18,1),
(41,18,2),
(22,19,1),
(42,19,2),
(23,20,1),
(24,21,1),
(25,22,1),
(26,23,1),
(43,23,2),
(27,24,1),
(38,24,2),
(28,25,1),
(36,25,2),
(29,26,1),
(30,27,1);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES
(1,'2025-06-13 12:52:32.474928','2','Direttivo',1,'[{\"added\": {}}]',3,1),
(2,'2025-06-13 12:52:38.798223','2','Direttivo',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),
(3,'2025-06-13 12:53:32.744059','1','Tesserato',2,'[{\"changed\": {\"fields\": [\"Permissions\"]}}]',3,1),
(4,'2025-06-13 12:53:45.716294','2','uno@example.com',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(5,'2025-06-13 23:06:29.592649','3','Amministratore',3,'',3,1),
(6,'2025-06-13 23:07:01.830849','3','due@example.com',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(7,'2025-06-30 16:09:10.315528','6','cinque',3,'',4,1),
(8,'2025-06-30 16:09:10.315594','5','quattro',3,'',4,1),
(9,'2025-06-30 16:09:10.315626','4','tre',3,'',4,1),
(10,'2025-07-01 15:20:07.937729','10','sei',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(11,'2025-07-04 18:28:52.137061','9','cinque',3,'',4,1),
(12,'2025-07-04 18:28:52.137102','3','due',3,'',4,1),
(13,'2025-07-04 18:28:52.137119','8','quattro',3,'',4,1),
(14,'2025-07-04 18:28:52.137134','10','sei',3,'',4,1),
(15,'2025-07-04 18:28:52.137148','11','sette',3,'',4,1),
(16,'2025-07-04 18:28:52.137162','7','tre',3,'',4,1),
(17,'2025-07-04 18:28:52.137175','2','uno',3,'',4,1),
(18,'2025-07-04 18:33:55.071112','12','luca.lucchi@gmail.com',3,'',4,1),
(19,'2025-07-04 18:40:12.807731','14','alessia.alessiani@yahoo.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(20,'2025-07-04 18:40:18.940868','22','andrea.andreani@iol.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(21,'2025-07-04 18:40:24.338612','21','daniele.danieli@inwind.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(22,'2025-07-04 18:40:29.583136','27','davide.daviddi@gmail.com',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(23,'2025-07-04 18:40:34.618997','16','francesco.franceschetti@alice.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(24,'2025-07-04 18:40:44.864134','25','gabriele.gabrielli@fastweb.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(25,'2025-07-04 18:40:49.585356','17','giulia.giulianini@gmail.com',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(26,'2025-07-04 18:40:57.167559','24','lorenzo.lorenzini@telecom.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(27,'2025-07-04 18:41:01.215190','13','luca.lucchi@gmail.com',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(28,'2025-07-04 18:41:05.340619','15','marco.marchesi@libero.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(29,'2025-07-04 19:00:18.192756','18','roberto',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(30,'2025-07-04 19:00:24.451648','19','stefania',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(31,'2025-07-04 19:00:37.934764','23','sofia.sofiani@tiscali.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(32,'2025-07-04 19:00:52.446102','22','andrea.andreani@iol.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(33,'2025-07-04 19:01:00.229066','21','daniele.danieli@inwind.it',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1),
(34,'2025-07-04 19:01:06.154364','27','davide.daviddi@gmail.com',2,'[{\"changed\": {\"fields\": [\"Groups\"]}}]',4,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES
(9,'accounts','profiloutente'),
(1,'admin','logentry'),
(7,'articoli','articolo'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(5,'contenttypes','contenttype'),
(8,'eventi','evento'),
(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES
(1,'contenttypes','0001_initial','2025-06-13 12:09:13.579668'),
(2,'auth','0001_initial','2025-06-13 12:09:14.179886'),
(3,'accounts','0001_initial','2025-06-13 12:09:14.310246'),
(4,'accounts','0002_remove_profiloutente_email','2025-06-13 12:09:14.363901'),
(5,'admin','0001_initial','2025-06-13 12:09:14.513820'),
(6,'admin','0002_logentry_remove_auto_add','2025-06-13 12:09:14.530482'),
(7,'admin','0003_logentry_add_action_flag_choices','2025-06-13 12:09:14.548509'),
(8,'articoli','0001_initial','2025-06-13 12:09:14.762729'),
(9,'articoli','0002_articolo_autori_eliminati','2025-06-13 12:09:14.810596'),
(10,'contenttypes','0002_remove_content_type_name','2025-06-13 12:09:14.930309'),
(11,'auth','0002_alter_permission_name_max_length','2025-06-13 12:09:14.985001'),
(12,'auth','0003_alter_user_email_max_length','2025-06-13 12:09:15.039863'),
(13,'auth','0004_alter_user_username_opts','2025-06-13 12:09:15.059850'),
(14,'auth','0005_alter_user_last_login_null','2025-06-13 12:09:15.126667'),
(15,'auth','0006_require_contenttypes_0002','2025-06-13 12:09:15.130697'),
(16,'auth','0007_alter_validators_add_error_messages','2025-06-13 12:09:15.149242'),
(17,'auth','0008_alter_user_username_max_length','2025-06-13 12:09:15.203650'),
(18,'auth','0009_alter_user_last_name_max_length','2025-06-13 12:09:15.255201'),
(19,'auth','0010_alter_group_name_max_length','2025-06-13 12:09:15.307887'),
(20,'auth','0011_update_proxy_permissions','2025-06-13 12:09:15.327574'),
(21,'auth','0012_alter_user_first_name_max_length','2025-06-13 12:09:15.378962'),
(22,'eventi','0001_initial','2025-06-13 12:09:15.634077'),
(23,'sessions','0001_initial','2025-06-13 12:09:15.704224'),
(24,'eventi','0002_evento_posti_massimi','2025-07-01 14:34:18.614457'),
(25,'eventi','0003_alter_evento_options_remove_evento_date_evento_and_more','2025-07-01 14:34:18.721990');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES
('4ofhndy59rokput1ba6uyuxajnzqj012','.eJxVjD0LwjAUAP9LZinkO89RcBQn55CXl5Jim0LTTOJ_N0IHXe-OezEf2p59q2nzE7Ezk-z0yzDEZypfEWJcW9nrcKA6XJcwzfft0bsSlnRbKc2Xo_-b5FBzP3AUznFQhGhRAulRorFgJPV31NYBCIGIXBmjknHCggQ1WkMESWjN3h8AWTlG:1uQDUe:JGrg1RR0f7hD6m06iWXyYCQ600UwRKWyba__ZePKk04','2025-06-27 23:07:28.181645');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventi`
--

DROP TABLE IF EXISTS `eventi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titolo` varchar(200) NOT NULL,
  `descrizione` longtext NOT NULL,
  `luogo` varchar(255) NOT NULL,
  `immagine` varchar(100) DEFAULT NULL,
  `numero_partecipanti` int(10) unsigned DEFAULT NULL CHECK (`numero_partecipanti` >= 0),
  `stato` varchar(50) NOT NULL,
  `organizzatore_id` bigint(20) DEFAULT NULL,
  `posti_massimi` int(10) unsigned DEFAULT NULL CHECK (`posti_massimi` >= 0),
  `fine_evento` datetime(6) DEFAULT NULL,
  `inizio_evento` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `eventi_organizzatore_id_960575c8_fk_accounts_profiloutente_id` (`organizzatore_id`),
  CONSTRAINT `eventi_organizzatore_id_960575c8_fk_accounts_profiloutente_id` FOREIGN KEY (`organizzatore_id`) REFERENCES `accounts_profiloutente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventi`
--

LOCK TABLES `eventi` WRITE;
/*!40000 ALTER TABLE `eventi` DISABLE KEYS */;
INSERT INTO `eventi` VALUES
(27,'sBANDAndo sul Lago','Nel cuore di Iseo, gli allievi dell’Accademia Musicale “Aureliano Bettoni” si esibiranno in un saggio itinerante aperto al pubblico: un momento speciale per condividere il loro percorso e il loro amore per la musica.\r\nScopri il programma completo del festival su: https://visitlakeiseo.info/festival-dei-laghi-europei/','Centro storico di Iseo','immagini_eventi/immagine_evento_1_RBVhdzl.jpg',0,'IN_ATTESA',13,30,'2025-07-31 16:00:00.000000','2025-07-31 14:30:00.000000'),
(28,'ARIE SUL LAGO','Lirica e operetta sul Lago d’Iseo!\r\nNell’ambito del progetto Onde Musicali, un concerto dedicato alle arie ambientate sui laghi europei.\r\nCon Elena d’Angelo (soubrette soprano), Matteo Mazzoli (comico baritono) e cantanti lirici vincitori di concorsi internazionali. Al pianoforte Sem Ceritelli.\r\n\r\nUna serata elegante tra emozioni, bel canto e atmosfere da sogno.\r\nScopri il programma completo del festival su: https://visitlakeiseo.info/festival-dei-laghi-europei/','Sagrato della Pieve, Iseo','immagini_eventi/immagine_evento_2.jpg',0,'CONCLUSO',17,25,'2025-06-01 21:00:00.000000','2025-06-01 19:00:00.000000'),
(29,'SANREMO STORY','Fabry Valli & The Red Dolphins Big Band portano sul lago la magia del Festival di Sanremo!\r\nUn viaggio musicale dagli anni ’50 a oggi, tra hit indimenticabili e arrangiamenti in stile big band, per raccontare oltre 70 anni di storia italiana attraverso le canzoni che ci hanno fatto sognare.\r\nScopri il programma completo del festival su: https://visitlakeiseo.info/festival-dei-laghi-europei/','Porto Gabriele Rosa, Iseo','immagini_eventi/immagine_evento_3_OSyyusd.jpg',0,'CONCLUSO',14,20,'2025-05-25 18:30:00.000000','2025-05-25 16:30:00.000000'),
(30,'A ISEO IL JAZZ È UNA FIABA','Le fiabe del Jazz: John Coltrane raccontato ai bambini\r\nSpettacolo-laboratorio di narrazione e musica \r\nClaudio Comini, voce narrante\r\nGuido Bombardieri, sax alto e soprano\r\n\r\nTratto dalla serie di audiolibri “le Fiabe del Jazz” di Roberto Piumini e Claudio Comini, edizioni Curci Yung\r\nIllustrazioni di Fabio Magnasciutti','Sala civica Castello Oldofredi, Iseo','immagini_eventi/immagine_evento_5.jpg',0,'IN_ATTESA',18,40,'2025-07-18 10:00:00.000000','2025-07-17 08:00:00.000000');
/*!40000 ALTER TABLE `eventi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evento_iscritti`
--

DROP TABLE IF EXISTS `evento_iscritti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `evento_iscritti` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `evento_id` int(11) NOT NULL,
  `profiloutente_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `evento_iscritti_evento_id_profiloutente_id_a9b1b663_uniq` (`evento_id`,`profiloutente_id`),
  KEY `evento_iscritti_profiloutente_id_058cb414_fk_accounts_` (`profiloutente_id`),
  CONSTRAINT `evento_iscritti_evento_id_b3262084_fk_eventi_id` FOREIGN KEY (`evento_id`) REFERENCES `eventi` (`id`),
  CONSTRAINT `evento_iscritti_profiloutente_id_058cb414_fk_accounts_` FOREIGN KEY (`profiloutente_id`) REFERENCES `accounts_profiloutente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento_iscritti`
--

LOCK TABLES `evento_iscritti` WRITE;
/*!40000 ALTER TABLE `evento_iscritti` DISABLE KEYS */;
/*!40000 ALTER TABLE `evento_iscritti` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-07 15:46:01
