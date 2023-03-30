-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: edureka
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `employeeinfo`
--

DROP TABLE IF EXISTS `employeeinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employeeinfo` (
  `EmpID` int NOT NULL,
  `EmpFname` varchar(45) DEFAULT NULL,
  `EmpLname` varchar(45) DEFAULT NULL,
  `Department` varchar(45) DEFAULT NULL,
  `Project` varchar(10) DEFAULT NULL,
  `Address` varchar(45) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` char(1) DEFAULT NULL,
  PRIMARY KEY (`EmpID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employeeinfo`
--

LOCK TABLES `employeeinfo` WRITE;
/*!40000 ALTER TABLE `employeeinfo` DISABLE KEYS */;
INSERT INTO `employeeinfo` VALUES (1,'Sanjay','Mehra','HR','P1','Hyderabad(HYD)','1976-12-01','M'),(2,'Ananya','Mishra','Admin','P2','Delhi(DEL)','1968-05-02','F'),(3,'Rohan','Diwan','Account','P3','Mumbai(BOM)','1980-01-01','M'),(4,'Sonia','Kulkarni','HR','P1','Hyderabad(HYD)','1992-05-02','F'),(5,'Ankit','Kapoor','Admin','P2','Delhi(DEL)','1994-07-03','M');
/*!40000 ALTER TABLE `employeeinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employeeposition`
--

DROP TABLE IF EXISTS `employeeposition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employeeposition` (
  `EmpID` int NOT NULL,
  `EmpPosition` varchar(45) DEFAULT NULL,
  `DateOfJoining` date DEFAULT NULL,
  `SALARY` int DEFAULT NULL,
  PRIMARY KEY (`EmpID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employeeposition`
--

LOCK TABLES `employeeposition` WRITE;
/*!40000 ALTER TABLE `employeeposition` DISABLE KEYS */;
INSERT INTO `employeeposition` VALUES (1,'Manager','2022-05-01',500000),(2,'Executive','2022-05-02',75000),(3,'Manager','2022-05-01',90000),(4,'Lead','2022-05-02',85000),(5,'Executive','2022-05-01',300000);
/*!40000 ALTER TABLE `employeeposition` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-27 17:28:37
