-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 17, 2023 at 01:41 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `itmajor`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_admin_acc`
--

CREATE TABLE `tbl_admin_acc` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_admin_acc`
--

INSERT INTO `tbl_admin_acc` (`admin_id`, `username`, `password`) VALUES
(1, 'admin123', 'admin123123');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_approved`
--

CREATE TABLE `tbl_approved` (
  `approved_id` int(11) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `user_type` enum('Applicant','Employer') NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_name2` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_approved`
--

INSERT INTO `tbl_approved` (`approved_id`, `firstname`, `lastname`, `email`, `user_type`, `file_name`, `file_name2`, `username`, `password`) VALUES
(1, 'Aljieo', 'Tolibas', 'jieotolibas19@gmail.com', 'Applicant', '5.png', 'FORM-01-_SCC-Statement-of-Claim.pdf', 'jieo', '123'),
(2, 'Carlo', 'Maneja', 'mafia.boss@gmail.com', 'Employer', 'DBMSerd.png', 'IOS image and Licensing.pdf', 'carlo', '123'),
(3, 'jords', 'pelago', 'jords.pelago@email.com', 'Applicant', '12.png', 'FORM-01-_SCC-Statement-of-Claim.pdf', 'jords', '123'),
(4, 'Jerson', 'Butawan', 'jerson.butawan@gmail.com', 'Applicant', '5.png', 'IOS image and Licensing.pdf', 'test1', '123'),
(5, 'Carlo', 'Maneja', 'mafia.boss@gmail.com', 'Employer', '12.png', 'FORM-01-_SCC-Statement-of-Claim.pdf', 'carlo', '123');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_job`
--

CREATE TABLE `tbl_job` (
  `job_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `position` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `work_hour` varchar(255) NOT NULL,
  `salary` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_job`
--

INSERT INTO `tbl_job` (`job_id`, `username`, `company_name`, `position`, `description`, `work_hour`, `salary`) VALUES
(1, 'carlo', 'Washington Wizards', 'Janitor', 'Tig map', '7-8 hours', '250'),
(2, 'carlo', 'Blackcat', 'Waiter', 'Serve people', '7-8 hours', '50');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_job_interested`
--

CREATE TABLE `tbl_job_interested` (
  `job_int_id` int(11) NOT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `lastname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `file_name` varchar(255) DEFAULT NULL,
  `file_name2` varchar(255) DEFAULT NULL,
  `job_id` int(11) DEFAULT NULL,
  `status` enum('pending','approved','rejected') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_job_interested`
--

INSERT INTO `tbl_job_interested` (`job_int_id`, `firstname`, `lastname`, `email`, `file_name`, `file_name2`, `job_id`, `status`) VALUES
(1, 'Carlo', 'Maneja', 'mafia.boss@gmail.com', 'DBMSerd.png', 'IOS image and Licensing.pdf', 1, 'pending'),
(2, 'jords', 'pelago', 'jords.pelago@email.com', '12.png', 'FORM-01-_SCC-Statement-of-Claim.pdf', 1, 'pending'),
(3, 'Carlo', 'Maneja', 'mafia.boss@gmail.com', 'DBMSerd.png', 'IOS image and Licensing.pdf', 2, 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_registration`
--

CREATE TABLE `tbl_registration` (
  `reg_id` int(11) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `birthdate` date NOT NULL,
  `gender` enum('male','female','other') NOT NULL,
  `address` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `user_type` enum('Applicant','Employer') NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_name2` varchar(255) NOT NULL,
  `status` enum('pending','approve','reject') NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_admin_acc`
--
ALTER TABLE `tbl_admin_acc`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `tbl_approved`
--
ALTER TABLE `tbl_approved`
  ADD PRIMARY KEY (`approved_id`);

--
-- Indexes for table `tbl_job`
--
ALTER TABLE `tbl_job`
  ADD PRIMARY KEY (`job_id`);

--
-- Indexes for table `tbl_job_interested`
--
ALTER TABLE `tbl_job_interested`
  ADD PRIMARY KEY (`job_int_id`),
  ADD KEY `job_id` (`job_id`);

--
-- Indexes for table `tbl_registration`
--
ALTER TABLE `tbl_registration`
  ADD PRIMARY KEY (`reg_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_admin_acc`
--
ALTER TABLE `tbl_admin_acc`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tbl_approved`
--
ALTER TABLE `tbl_approved`
  MODIFY `approved_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `tbl_job`
--
ALTER TABLE `tbl_job`
  MODIFY `job_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tbl_job_interested`
--
ALTER TABLE `tbl_job_interested`
  MODIFY `job_int_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbl_registration`
--
ALTER TABLE `tbl_registration`
  MODIFY `reg_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_job_interested`
--
ALTER TABLE `tbl_job_interested`
  ADD CONSTRAINT `tbl_job_interested_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `tbl_job` (`job_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
