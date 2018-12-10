-- MySQL dump 10.13  Distrib 8.0.12, for macos10.13 (x86_64)
--
-- Host: localhost    Database: iis_proj
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('ee542665fc4c');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cinnost`
--

DROP TABLE IF EXISTS `cinnost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `cinnost` (
  `id_cinnosti` int(11) NOT NULL AUTO_INCREMENT,
  `typ_cinnosti` varchar(30) NOT NULL,
  `odmena` int(11) NOT NULL,
  PRIMARY KEY (`id_cinnosti`),
  KEY `odmena` (`odmena`),
  CONSTRAINT `cinnost_ibfk_1` FOREIGN KEY (`odmena`) REFERENCES `sazba` (`id_sazby`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cinnost`
--

LOCK TABLES `cinnost` WRITE;
/*!40000 ALTER TABLE `cinnost` DISABLE KEYS */;
/*!40000 ALTER TABLE `cinnost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `denni_evidence`
--

DROP TABLE IF EXISTS `denni_evidence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `denni_evidence` (
  `id_cinnosti` int(11) NOT NULL,
  `id_zam` int(11) NOT NULL,
  `den_uskut` date DEFAULT NULL,
  `cas_uloz` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cas_zmeny` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_cinnosti`,`id_zam`),
  KEY `id_zam` (`id_zam`),
  CONSTRAINT `denni_evidence_ibfk_1` FOREIGN KEY (`id_cinnosti`) REFERENCES `cinnost` (`id_cinnosti`) ON DELETE CASCADE,
  CONSTRAINT `denni_evidence_ibfk_2` FOREIGN KEY (`id_zam`) REFERENCES `zamestnanec` (`id_zam`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `denni_evidence`
--

LOCK TABLES `denni_evidence` WRITE;
/*!40000 ALTER TABLE `denni_evidence` DISABLE KEYS */;
/*!40000 ALTER TABLE `denni_evidence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dokument`
--

DROP TABLE IF EXISTS `dokument`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `dokument` (
  `id_dokumentu` int(11) NOT NULL AUTO_INCREMENT,
  `id_zam` int(11) DEFAULT NULL,
  `id_voz` int(11) NOT NULL,
  `typ_dokumentu` int(11) DEFAULT NULL,
  `adresa_uloziste` varchar(30) NOT NULL,
  `platnost_do` date DEFAULT NULL,
  `zalozen_cas` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `posl_editace` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_dokumentu`),
  KEY `id_zam` (`id_zam`),
  KEY `typ_dokumentu` (`typ_dokumentu`),
  KEY `fk_vozidlo_dokument` (`id_voz`),
  CONSTRAINT `dokument_ibfk_2` FOREIGN KEY (`id_zam`) REFERENCES `zamestnanec` (`id_zam`) ON DELETE CASCADE,
  CONSTRAINT `dokument_ibfk_3` FOREIGN KEY (`typ_dokumentu`) REFERENCES `typ_dokumentu` (`id_typu`) ON DELETE CASCADE,
  CONSTRAINT `fk_vozidlo_dokument` FOREIGN KEY (`id_voz`) REFERENCES `vozidlo` (`id_voz`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dokument`
--

LOCK TABLES `dokument` WRITE;
/*!40000 ALTER TABLE `dokument` DISABLE KEYS */;
/*!40000 ALTER TABLE `dokument` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dovolena_zam`
--

DROP TABLE IF EXISTS `dovolena_zam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `dovolena_zam` (
  `id_naroku` int(11) NOT NULL AUTO_INCREMENT,
  `id_zam` int(11) NOT NULL,
  `rok` int(11) DEFAULT NULL,
  `narok` int(11) DEFAULT NULL,
  `vycerpano` int(11) DEFAULT NULL,
  `posl_aktual` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_naroku`),
  KEY `id_zam` (`id_zam`),
  CONSTRAINT `dovolena_zam_ibfk_1` FOREIGN KEY (`id_zam`) REFERENCES `zamestnanec` (`id_zam`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dovolena_zam`
--

LOCK TABLES `dovolena_zam` WRITE;
/*!40000 ALTER TABLE `dovolena_zam` DISABLE KEYS */;
/*!40000 ALTER TABLE `dovolena_zam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dovolena_zam_hist`
--

DROP TABLE IF EXISTS `dovolena_zam_hist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `dovolena_zam_hist` (
  `id_zaznamu` int(11) NOT NULL AUTO_INCREMENT,
  `id_zam` int(11) NOT NULL,
  `rok` int(11) DEFAULT NULL,
  `od` date DEFAULT NULL,
  `do` date DEFAULT NULL,
  `celkem` int(11) DEFAULT NULL,
  `potvrzeni` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_zaznamu`),
  KEY `id_zam` (`id_zam`),
  CONSTRAINT `dovolena_zam_hist_ibfk_1` FOREIGN KEY (`id_zam`) REFERENCES `zamestnanec` (`id_zam`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dovolena_zam_hist`
--

LOCK TABLES `dovolena_zam_hist` WRITE;
/*!40000 ALTER TABLE `dovolena_zam_hist` DISABLE KEYS */;
INSERT INTO `dovolena_zam_hist` VALUES (12,32,NULL,'2018-12-14','2018-12-17',4,0),(15,32,NULL,'2018-12-19','2018-12-21',3,1),(16,2,NULL,'2018-12-27','2018-12-31',5,1),(17,32,NULL,'2018-12-28','2018-12-29',2,0);
/*!40000 ALTER TABLE `dovolena_zam_hist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lekarska_prohl`
--

DROP TABLE IF EXISTS `lekarska_prohl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `lekarska_prohl` (
  `id_prohl` int(11) NOT NULL AUTO_INCREMENT,
  `id_zam` int(11) NOT NULL,
  `absolvovano_dne` date DEFAULT NULL,
  `platnost_do` date DEFAULT NULL,
  `posl_aktual` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_prohl`),
  KEY `id_zam` (`id_zam`),
  CONSTRAINT `lekarska_prohl_ibfk_1` FOREIGN KEY (`id_zam`) REFERENCES `zamestnanec` (`id_zam`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lekarska_prohl`
--

LOCK TABLES `lekarska_prohl` WRITE;
/*!40000 ALTER TABLE `lekarska_prohl` DISABLE KEYS */;
/*!40000 ALTER TABLE `lekarska_prohl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pracovni_sml`
--

DROP TABLE IF EXISTS `pracovni_sml`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `pracovni_sml` (
  `id_sml` int(11) NOT NULL AUTO_INCREMENT,
  `id_zam` int(11) NOT NULL,
  `typ_sml` varchar(15) DEFAULT NULL,
  `role_zam` varchar(15) DEFAULT NULL,
  `sjednana_dne` date DEFAULT NULL,
  `platnost_do` date DEFAULT NULL,
  `posl_aktual` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_sml`),
  KEY `id_zam` (`id_zam`),
  CONSTRAINT `pracovni_sml_ibfk_1` FOREIGN KEY (`id_zam`) REFERENCES `zamestnanec` (`id_zam`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pracovni_sml`
--

LOCK TABLES `pracovni_sml` WRITE;
/*!40000 ALTER TABLE `pracovni_sml` DISABLE KEYS */;
/*!40000 ALTER TABLE `pracovni_sml` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sazba`
--

DROP TABLE IF EXISTS `sazba`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sazba` (
  `id_sazby` int(11) NOT NULL AUTO_INCREMENT,
  `popis_sazby` varchar(30) DEFAULT NULL,
  `vyse_sazby` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_sazby`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sazba`
--

LOCK TABLES `sazba` WRITE;
/*!40000 ALTER TABLE `sazba` DISABLE KEYS */;
/*!40000 ALTER TABLE `sazba` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skoleni_ridicu`
--

DROP TABLE IF EXISTS `skoleni_ridicu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `skoleni_ridicu` (
  `id_skol` int(11) NOT NULL AUTO_INCREMENT,
  `id_zam` int(11) NOT NULL,
  `absolvovano_dne` date DEFAULT NULL,
  `platnost_do` date DEFAULT NULL,
  `posl_aktual` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_skol`),
  KEY `id_zam` (`id_zam`),
  CONSTRAINT `skoleni_ridicu_ibfk_1` FOREIGN KEY (`id_zam`) REFERENCES `zamestnanec` (`id_zam`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skoleni_ridicu`
--

LOCK TABLES `skoleni_ridicu` WRITE;
/*!40000 ALTER TABLE `skoleni_ridicu` DISABLE KEYS */;
/*!40000 ALTER TABLE `skoleni_ridicu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typ_dokumentu`
--

DROP TABLE IF EXISTS `typ_dokumentu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `typ_dokumentu` (
  `id_typu` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_typu`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typ_dokumentu`
--

LOCK TABLES `typ_dokumentu` WRITE;
/*!40000 ALTER TABLE `typ_dokumentu` DISABLE KEYS */;
/*!40000 ALTER TABLE `typ_dokumentu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uzivatel`
--

DROP TABLE IF EXISTS `uzivatel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `uzivatel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(30) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `poc_prihl` int(11) DEFAULT NULL,
  `posl_prihl` timestamp NULL DEFAULT NULL,
  `cas_posl_zmeny` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `role` varchar(10) DEFAULT 'user',
  `id_zam` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uzivatel_zamestnanec` (`id_zam`),
  CONSTRAINT `uzivatel_zamestnanec` FOREIGN KEY (`id_zam`) REFERENCES `zamestnanec` (`id_zam`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uzivatel`
--

LOCK TABLES `uzivatel` WRITE;
/*!40000 ALTER TABLE `uzivatel` DISABLE KEYS */;
INSERT INTO `uzivatel` VALUES (28,'madaos','pbkdf2:sha256:50000$WqPRV3f4$d05f56c5d828d95ab5a54d3c171589310f7e5e1e25e0692960948af1d48beac6',40,'2018-12-05 07:07:14','2018-12-03 09:55:39','admin',31),(31,'user1','pbkdf2:sha256:50000$5yn6U1hb$e95c91196fb13d079f915c7bd769e279019b74387ac22ff7e9a480b540e15a2a',15,'2018-12-05 07:09:28','2018-12-03 10:42:35','user',32),(32,'user2','pbkdf2:sha256:50000$STXWlID0$0062760c34a73daf5c15f4a16af6b9e6451e95f97aadcc4215e49984fdc4f0ad',4,'2018-12-05 06:14:13','2018-12-03 16:56:59','user',2);
/*!40000 ALTER TABLE `uzivatel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vozidlo`
--

DROP TABLE IF EXISTS `vozidlo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `vozidlo` (
  `spz` varchar(10) NOT NULL,
  `znacka` varchar(20) DEFAULT NULL,
  `model` varchar(20) DEFAULT NULL,
  `rok_vyroby` int(11) DEFAULT NULL,
  `vykon` int(11) DEFAULT NULL,
  `nosnost` int(11) DEFAULT NULL,
  `pocet_naprav` int(11) DEFAULT NULL,
  `emisni_trida` varchar(10) DEFAULT NULL,
  `zalozeno_cas` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `posl_aktual_cas` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_voz` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_voz`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vozidlo`
--

LOCK TABLES `vozidlo` WRITE;
/*!40000 ALTER TABLE `vozidlo` DISABLE KEYS */;
INSERT INTO `vozidlo` VALUES ('6B0 3678','Mercedes','Actros',2008,440,24000,10,'EURO V','2018-12-03 16:44:54','2018-12-03 16:44:54',1),('7B7 4223','Mercedes','Sprinter',2008,110,1100,2,'EURO IV','2018-12-03 16:46:02','2018-12-03 16:46:02',2),('3B6 0263','Mercedes','Vito',2004,80,900,2,'EURO III','2018-12-03 16:47:05','2018-12-03 16:47:05',3);
/*!40000 ALTER TABLE `vozidlo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zamestnanec`
--

DROP TABLE IF EXISTS `zamestnanec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `zamestnanec` (
  `id_zam` int(11) NOT NULL AUTO_INCREMENT,
  `kr_jmeno` varchar(20) DEFAULT NULL,
  `prijmeni` varchar(20) DEFAULT NULL,
  `dat_nar` date DEFAULT NULL,
  `trv_bydliste` varchar(50) DEFAULT NULL,
  `prech_bydliste` varchar(50) DEFAULT NULL,
  `telefon` varchar(15) DEFAULT NULL,
  `prac_sml` varchar(15) DEFAULT NULL,
  `akt_skol_id` int(11) DEFAULT NULL,
  `akt_prohlidka` int(11) DEFAULT NULL,
  `aktivni` int(11) DEFAULT NULL,
  `zalozen_cas` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `posl_aktual_cas` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `email` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id_zam`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zamestnanec`
--

LOCK TABLES `zamestnanec` WRITE;
/*!40000 ALTER TABLE `zamestnanec` DISABLE KEYS */;
INSERT INTO `zamestnanec` VALUES (2,'Jana','Horáčková','1991-07-19','V Újezdech 1, 621 00, Brno','Kořenského 20, 621 00 Brno','58','2',NULL,NULL,1,'2018-10-27 17:29:08','2018-10-27 17:29:08','barbara.lanickova@gmail.com'),(31,'Jakub','Křtitel','1988-06-11','Kainarova 28, 616 00 Brno','','','',NULL,NULL,1,'2018-12-02 21:06:08','2018-12-02 21:06:08','adam@lanicektransport.cz'),(32,'Petr','Novotný','1962-12-26','','','','',NULL,NULL,1,'2018-12-03 10:42:22','2018-12-03 10:42:22','petr@lanicektransport.cz');
/*!40000 ALTER TABLE `zamestnanec` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-05  8:17:34
