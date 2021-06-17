-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 10, 2019 at 01:49 AM
-- Server version: 10.1.34-MariaDB
-- PHP Version: 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `unjobbed`
--

-- --------------------------------------------------------

--
-- Table structure for table `cache_job_title`
--

CREATE TABLE `cache_job_title` (
  `job_id` int(11) NOT NULL,
  `job_title` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cache_job_title`
--

INSERT INTO `cache_job_title` (`job_id`, `job_title`) VALUES
(1, 'Bull Fighter'),
(2, 'Software Engineer'),
(3, 'Hula Dancer'),
(4, 'Systems Analyst'),
(5, 'Parking Attendant');

-- --------------------------------------------------------

--
-- Table structure for table `cache_location`
--

CREATE TABLE `cache_location` (
  `loc_id` int(11) NOT NULL,
  `location_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cache_location`
--

INSERT INTO `cache_location` (`loc_id`, `location_name`) VALUES
(1, 'Portland, Or'),
(2, 'San Diego, Ca'),
(3, 'Houston, Tx'),
(4, 'El Paso, Tx'),
(5, 'Plano, Tx'),
(6, 'San Francisco, Ca'),
(7, 'Maui, Hi'),
(8, 'Seattle, Wa'),
(9, 'Atlanta, Ga'),
(10, 'Denver, Co'),
(11, 'Memphis, Tn'),
(12, 'Dallas, Tx'),
(13, 'Tulsa, Ok'),
(14, 'Chicago, Il'),
(15, 'Austin, Tx');

-- --------------------------------------------------------

--
-- Table structure for table `unjobbed_access`
--

CREATE TABLE `unjobbed_access` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `forgot_login` tinyint(1) NOT NULL,
  `confirmed_login` tinyint(1) NOT NULL,
  `confirmed_login_string` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `unjobbed_access`
--

INSERT INTO `unjobbed_access` (`id`, `username`, `email`, `password`, `forgot_login`, `confirmed_login`, `confirmed_login_string`) VALUES
(1, 'noelman', 'noelman@hotmail.com', 'pbkdf2:sha256:50000$1UBywPof$9b06c3d3d99d52cb95413eb441e1f4e1cc41515b1b839085d6b5aa3dfa8a692f', 0, 0, '7LPP4261'),
(2, 'joeblow', 'joeblow@gmail.com', 'pbkdf2:sha256:50000$8mJKLCXh$fdecd1f20099bc490e84c4bc3f2e8f78443b5dafe422864892c02d80cd84df2c', 0, 0, '5HNCRDTI'),
(3, 'jjjj', 'jjjj@gmail.com', 'pbkdf2:sha256:50000$QRmylw3b$85a140be52c708edbbf41487a8d0a63228b7deacb22afa135f35f7adce6d6ea1', 0, 0, 'Q1L2GPKN'),
(4, 'somebody', 'peter.somebody@gmail.com', 'pbkdf2:sha256:50000$lcJicaAh$ce5fcaff85a50a3c08b1110bf73834f7f0af32493743fbe3c5a5a98152af1808', 0, 0, '5Q4LJWXI');

-- --------------------------------------------------------

--
-- Table structure for table `user_profile`
--

CREATE TABLE `user_profile` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `profile_id` int(11) NOT NULL,
  `fname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `zipcode` int(5) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `is_user_18` tinyint(1) DEFAULT NULL,
  `pref_comm` varchar(50) DEFAULT NULL,
  `desired_pay` int(6) DEFAULT NULL,
  `date_to_start` date DEFAULT NULL,
  `reason_for_leaving` varchar(255) DEFAULT NULL,
  `legally_eligible` tinyint(1) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `unjobbed_resume` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `job_title` varchar(72) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `employer` varchar(72) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `job_desc` text CHARACTER SET utf8 COLLATE utf8_general_ci,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `currently_employed` smallint(1) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

--
-- Dumping data for table `user_profile`
--

INSERT INTO `user_profile` (`profile_id`, `fname`, `lname`, `city`, `zipcode`, `state`, `phone`, `address`, `is_user_18`, `pref_comm`, `desired_pay`, `date_to_start`, `reason_for_leaving`, `legally_eligible`, `user_id`) VALUES
(1, 'Noel', 'Yunginger', 'Portland', 97206, 'OR', '5035551212', ' 123 Main St', 1, 'email', 1000000, '2019-03-10', ' I want to make the big bucks', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `xref_job_search`
--

CREATE TABLE `xref_job_search` (
  `search_id` int(11) NOT NULL,
  `search_date_time` datetime DEFAULT NULL,
  `job_id` int(11) NOT NULL,
  `loc_id` int(11) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `xref_job_search`
--

INSERT INTO `xref_job_search` (`search_id`, `search_date_time`, `job_id`, `loc_id`, `id`) VALUES
(36, '2019-03-09 15:11:55', 2, 11, 1),
(37, '2019-03-09 15:15:09', 1, 4, 1),
(38, '2019-03-09 15:17:36', 2, 10, 1),
(39, '2019-03-09 15:18:46', 2, 9, 1),
(40, '2019-03-09 15:20:39', 2, 6, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cache_job_title`
--
ALTER TABLE `cache_job_title`
  ADD PRIMARY KEY (`job_id`);

--
-- Indexes for table `cache_location`
--
ALTER TABLE `cache_location`
  ADD PRIMARY KEY (`loc_id`);

--
-- Indexes for table `unjobbed_access`
--
ALTER TABLE `unjobbed_access`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD PRIMARY KEY (`profile_id`),
  ADD KEY `user_profile_fk1` (`user_id`);

--
-- Indexes for table `xref_job_search`
--
ALTER TABLE `xref_job_search`
  ADD PRIMARY KEY (`search_id`),
  ADD KEY `job_id_unfk1` (`job_id`),
  ADD KEY `job_id_unfk2` (`loc_id`),
  ADD KEY `job_id_unfk3` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cache_job_title`
--
ALTER TABLE `cache_job_title`
  MODIFY `job_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `cache_location`
--
ALTER TABLE `cache_location`
  MODIFY `loc_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `unjobbed_access`
--
ALTER TABLE `unjobbed_access`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user_profile`
--
ALTER TABLE `user_profile`
  MODIFY `profile_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `xref_job_search`
--
ALTER TABLE `xref_job_search`
  MODIFY `search_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_profile`
--
ALTER TABLE `user_profile`
  ADD CONSTRAINT `user_profile_fk1` FOREIGN KEY (`user_id`) REFERENCES `unjobbed_access` (`id`);

--
-- Constraints for table `xref_job_search`
--
ALTER TABLE `xref_job_search`
  ADD CONSTRAINT `job_id_unfk1` FOREIGN KEY (`job_id`) REFERENCES `cache_job_title` (`job_id`),
  ADD CONSTRAINT `job_id_unfk2` FOREIGN KEY (`loc_id`) REFERENCES `cache_location` (`loc_id`),
  ADD CONSTRAINT `job_id_unfk3` FOREIGN KEY (`id`) REFERENCES `unjobbed_access` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
