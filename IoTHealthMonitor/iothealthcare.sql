-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: cmpe295b.cgje8hjr4ff1.us-west-2.rds.amazonaws.com    Database: iothealth1
-- ------------------------------------------------------
-- Server version	5.6.27-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `iothealth1`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `iothealth1` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `iothealth1`;

--
-- Table structure for table `Allergy`
--

DROP TABLE IF EXISTS `Allergy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Allergy` (
  `UserId` int(11) DEFAULT NULL,
  `allergy_date` varchar(50) DEFAULT NULL,
  `allergy_name` varchar(100) DEFAULT NULL,
  `reaction` varchar(100) DEFAULT NULL,
  `severity` varchar(100) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `UserId` (`UserId`),
  CONSTRAINT `Allergy_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Allergy`
--

LOCK TABLES `Allergy` WRITE;
/*!40000 ALTER TABLE `Allergy` DISABLE KEYS */;
INSERT INTO `Allergy` VALUES (20,'04/20/2015','High Cholestrol','High','High',2);
/*!40000 ALTER TABLE `Allergy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CqmEvents`
--

DROP TABLE IF EXISTS `CqmEvents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CqmEvents` (
  `UserId` int(11) DEFAULT NULL,
  `Type` varchar(50) DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  KEY `UserId` (`UserId`),
  CONSTRAINT `CqmEvents_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CqmEvents`
--

LOCK TABLES `CqmEvents` WRITE;
/*!40000 ALTER TABLE `CqmEvents` DISABLE KEYS */;
INSERT INTO `CqmEvents` VALUES (20,'Encounter','Office Visit','2016-12-31','2016-01-01');
/*!40000 ALTER TABLE `CqmEvents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CqmOccurence`
--

DROP TABLE IF EXISTS `CqmOccurence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CqmOccurence` (
  `UserId` int(11) DEFAULT NULL,
  `Type` varchar(50) DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  KEY `UserId` (`UserId`),
  CONSTRAINT `CqmOccurence_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CqmOccurence`
--

LOCK TABLES `CqmOccurence` WRITE;
/*!40000 ALTER TABLE `CqmOccurence` DISABLE KEYS */;
INSERT INTO `CqmOccurence` VALUES (20,'Essential Hypertension','2016-12-31','2016-01-01');
/*!40000 ALTER TABLE `CqmOccurence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DeviceCredentials`
--

DROP TABLE IF EXISTS `DeviceCredentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DeviceCredentials` (
  `UserId` int(11) DEFAULT NULL,
  `clientId` varchar(255) DEFAULT NULL,
  `secretKey` varchar(255) DEFAULT NULL,
  `redirectUri` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DeviceCredentials`
--

LOCK TABLES `DeviceCredentials` WRITE;
/*!40000 ALTER TABLE `DeviceCredentials` DISABLE KEYS */;
INSERT INTO `DeviceCredentials` VALUES (20,'','',''),(21,'','',''),(23,'','','');
/*!40000 ALTER TABLE `DeviceCredentials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EmergencyContacts`
--

DROP TABLE IF EXISTS `EmergencyContacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EmergencyContacts` (
  `UserId` int(11) DEFAULT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Relation` varchar(50) DEFAULT NULL,
  `Phone` varchar(50) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Address` varchar(50) DEFAULT NULL,
  `Phone2` varchar(50) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `UserId` (`UserId`),
  CONSTRAINT `EmergencyContacts_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmergencyContacts`
--

LOCK TABLES `EmergencyContacts` WRITE;
/*!40000 ALTER TABLE `EmergencyContacts` DISABLE KEYS */;
INSERT INTO `EmergencyContacts` VALUES (20,'','Cousin','1234567890','','56 S','1234567890',1),(20,'Singhal','Cousin','1234567890','','56 S','1234567890',2);
/*!40000 ALTER TABLE `EmergencyContacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FoodEntry`
--

DROP TABLE IF EXISTS `FoodEntry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FoodEntry` (
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Item` varchar(255) NOT NULL,
  `Quantity` varchar(255) NOT NULL,
  `UserId` int(11) NOT NULL,
  `calorieEst` int(11) DEFAULT NULL,
  KEY `UserId` (`UserId`),
  CONSTRAINT `foodentry_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FoodEntry`
--

LOCK TABLES `FoodEntry` WRITE;
/*!40000 ALTER TABLE `FoodEntry` DISABLE KEYS */;
/*!40000 ALTER TABLE `FoodEntry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MeasurementPeriod`
--

DROP TABLE IF EXISTS `MeasurementPeriod`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MeasurementPeriod` (
  `EndDate` date DEFAULT NULL,
  `StartDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MeasurementPeriod`
--

LOCK TABLES `MeasurementPeriod` WRITE;
/*!40000 ALTER TABLE `MeasurementPeriod` DISABLE KEYS */;
INSERT INTO `MeasurementPeriod` VALUES ('2017-12-31','2016-01-01');
/*!40000 ALTER TABLE `MeasurementPeriod` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MedicalHistoryRecord`
--

DROP TABLE IF EXISTS `MedicalHistoryRecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MedicalHistoryRecord` (
  `UserId` int(11) DEFAULT NULL,
  `doc_visit_date` varchar(50) DEFAULT NULL,
  `doc_name` varchar(50) DEFAULT NULL,
  `primary_doc` varchar(3) DEFAULT NULL,
  `mode_of_visit` varchar(50) DEFAULT NULL,
  `body_weight` varchar(50) DEFAULT NULL,
  `blood_presure_systolic` varchar(50) DEFAULT NULL,
  `blood_presure_diastolic` varchar(50) DEFAULT NULL,
  `temperature` varchar(50) DEFAULT NULL,
  `prescribed_medicaltest_drugs` varchar(100) DEFAULT NULL,
  `comments_from_doc` varchar(1024) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `UserId` (`UserId`),
  CONSTRAINT `MedicalHistoryRecord_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MedicalHistoryRecord`
--

LOCK TABLES `MedicalHistoryRecord` WRITE;
/*!40000 ALTER TABLE `MedicalHistoryRecord` DISABLE KEYS */;
INSERT INTO `MedicalHistoryRecord` VALUES (20,'11/21/2016','Rustom','Yes','Person','78','120','80','98.6','None','None',2),(20,'10/22/2016','tr','yes','in person','10','80','120','98.6','x ','ok',3);
/*!40000 ALTER TABLE `MedicalHistoryRecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MedicalTestResults`
--

DROP TABLE IF EXISTS `MedicalTestResults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MedicalTestResults` (
  `UserId` int(11) DEFAULT NULL,
  `date_of_test` varchar(50) DEFAULT NULL,
  `test_results` varchar(100) DEFAULT NULL,
  `diagnostic_center_name` varchar(50) DEFAULT NULL,
  `scan_upload_results` varchar(50) DEFAULT NULL,
  KEY `UserId` (`UserId`),
  CONSTRAINT `MedicalTestResults_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MedicalTestResults`
--

LOCK TABLES `MedicalTestResults` WRITE;
/*!40000 ALTER TABLE `MedicalTestResults` DISABLE KEYS */;
/*!40000 ALTER TABLE `MedicalTestResults` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Medications`
--

DROP TABLE IF EXISTS `Medications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Medications` (
  `UserId` int(11) DEFAULT NULL,
  `date_of_medication` varchar(50) DEFAULT NULL,
  `type_of_medication` varchar(50) DEFAULT NULL,
  `name_of_mediaction` varchar(50) DEFAULT NULL,
  `instructions` varchar(100) DEFAULT NULL,
  `dose_qantity` double(7,2) DEFAULT NULL,
  `rate_quantity` double(7,2) DEFAULT NULL,
  `prescriber_name` varchar(50) DEFAULT NULL,
  `scan_upload_prescription` blob,
  KEY `UserId` (`UserId`),
  CONSTRAINT `Medications_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Medications`
--

LOCK TABLES `Medications` WRITE;
/*!40000 ALTER TABLE `Medications` DISABLE KEYS */;
/*!40000 ALTER TABLE `Medications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserProfile`
--

DROP TABLE IF EXISTS `UserProfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserProfile` (
  `Weight` varchar(255) NOT NULL,
  `Height` varchar(255) NOT NULL,
  `Goal` varchar(255) NOT NULL,
  `Gender` varchar(15) NOT NULL,
  `BMI` float NOT NULL,
  `Age` int(11) NOT NULL,
  `UserId` int(11) NOT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Phone` varchar(10) DEFAULT NULL,
  `Blood_type` varchar(5) DEFAULT NULL,
  `Birthday` varchar(12) DEFAULT NULL,
  KEY `UserId` (`UserId`),
  CONSTRAINT `userprofile_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserProfile`
--

LOCK TABLES `UserProfile` WRITE;
/*!40000 ALTER TABLE `UserProfile` DISABLE KEYS */;
INSERT INTO `UserProfile` VALUES ('78','72','132','male',10,26,20,'56 S Second Street','1234567890','A+','09/14/1990'),('170','70','150','male',24,26,21,'56 S Second Street','1234567890','A+','09/14/1990'),('123','70','132','male',511,25,23,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `UserProfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VaccinationImmunization`
--

DROP TABLE IF EXISTS `VaccinationImmunization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `VaccinationImmunization` (
  `UserId` int(11) DEFAULT NULL,
  `VaccinationImmunization_date` varchar(50) DEFAULT NULL,
  `VaccinationImmunization_name` varchar(50) DEFAULT NULL,
  `VaccinationImmunization_type` varchar(50) DEFAULT NULL,
  `VaccinationImmunization_dose_qantity` varchar(50) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `UserId` (`UserId`),
  CONSTRAINT `VaccinationImmunization_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VaccinationImmunization`
--

LOCK TABLES `VaccinationImmunization` WRITE;
/*!40000 ALTER TABLE `VaccinationImmunization` DISABLE KEYS */;
INSERT INTO `VaccinationImmunization` VALUES (20,'21/20/2016','Tetanus Shot','Normal','0.25',2),(20,'10/22/2016','Flu shot','Flu','.25',3);
/*!40000 ALTER TABLE `VaccinationImmunization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `UserId` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `EmailId` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (20,'','','','Doctor'),(21,'','','','Patient'),(22,'FirstProj','','',NULL),(23,'Yash','','','Patient');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-06 23:38:54
