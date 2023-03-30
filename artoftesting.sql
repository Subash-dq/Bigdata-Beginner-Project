-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: artoftesting
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
-- Table structure for table `employeedetails`
--

DROP TABLE IF EXISTS `employeedetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employeedetails` (
  `empid` int DEFAULT NULL,
  `fullname` varchar(40) DEFAULT NULL,
  `ManagerId` int DEFAULT NULL,
  `DateOfJoining` date DEFAULT NULL,
  `city` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employeedetails`
--

LOCK TABLES `employeedetails` WRITE;
/*!40000 ALTER TABLE `employeedetails` DISABLE KEYS */;
INSERT INTO `employeedetails` VALUES (121,'John Snow',321,'2019-01-31','Toronto'),(321,'Walter White',986,'2020-01-30','California'),(421,'Kuldeep Rana',876,'2021-11-27','New Delhi');
/*!40000 ALTER TABLE `employeedetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employeesalary`
--

DROP TABLE IF EXISTS `employeesalary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employeesalary` (
  `empid` int DEFAULT NULL,
  `project` varchar(40) DEFAULT NULL,
  `salary` int DEFAULT NULL,
  `variable` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employeesalary`
--

LOCK TABLES `employeesalary` WRITE;
/*!40000 ALTER TABLE `employeesalary` DISABLE KEYS */;
INSERT INTO `employeesalary` VALUES (121,'P1',8000,500),(321,'P2',10000,1000),(421,'P1',12000,0);
/*!40000 ALTER TABLE `employeesalary` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-29 18:44:39
