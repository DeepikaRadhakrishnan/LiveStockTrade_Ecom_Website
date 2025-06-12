-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 17, 2025 at 07:39 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `livecommerce`
--

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(50) NOT NULL,
  `vetcategory` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `age` int(30) NOT NULL,
  `price` int(50) NOT NULL,
  `quantity` int(30) NOT NULL,
  `description` varchar(50) NOT NULL,
  `images` text NOT NULL,
  `username` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `vetcategory`, `name`, `age`, `price`, `quantity`, `description`, `images`, `username`) VALUES
(1, 'coat', 'Rock', 2, 12000, 2, 'Its a good condition ', 'div2.jpg', 'Kali'),
(2, 'sheep', 'gir', 2, 8000, 5, 'good', 'gallery-11.jpg', 'Kali'),
(3, 'cattle', 'gir', 3, 18000, 3, 'High quality', 'gallery-2.jpg', 'Kali'),
(4, 'dog', 'tenna', 2, 3000, 2, 'Hygine', 'hrn.jpg', 'raj');

-- --------------------------------------------------------

--
-- Table structure for table `requests1`
--

CREATE TABLE `requests1` (
  `id` int(11) NOT NULL,
  `buyer_name` varchar(30) NOT NULL,
  `buyer_username` varchar(30) NOT NULL,
  `buyer_mobile` varchar(20) NOT NULL,
  `buyer_id` int(11) NOT NULL,
  `price` varchar(30) NOT NULL,
  `product_id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `category` varchar(100) NOT NULL,
  `seller_username` varchar(30) NOT NULL,
  `link` varchar(255) default NULL,
  `meeting_date` date default NULL,
  `meeting_time` time default NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `requests1`
--

INSERT INTO `requests1` (`id`, `buyer_name`, `buyer_username`, `buyer_mobile`, `buyer_id`, `price`, `product_id`, `image`, `category`, `seller_username`, `link`, `meeting_date`, `meeting_time`) VALUES
(1, 'Samsi', 'sam', '9876453478', 1, '12000', 1, 'div2.jpg', 'coat', 'Kali', '7878', NULL, NULL),
(2, 'Samsi', 'sam', '9876453478', 1, '8000', 2, 'gallery-11.jpg', 'sheep', 'Kali', 'https://yoom-zoom-clone.vercel.app/meeting/863f99e8-64c1-4ba4-b0bf-7f4e4454fbcc', '2025-05-24', '11:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `tb_admin`
--

CREATE TABLE `tb_admin` (
  `id` int(50) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_admin`
--

INSERT INTO `tb_admin` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `tb_booking`
--

CREATE TABLE `tb_booking` (
  `id` int(50) NOT NULL,
  `vetcategory` varchar(10) NOT NULL,
  `uname` varchar(50) NOT NULL,
  `price` int(10) NOT NULL,
  `total` int(10) NOT NULL,
  `username` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobileno` bigint(20) NOT NULL,
  `address` varchar(30) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `submission_datetime` datetime NOT NULL,
  `orderstatus` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_booking`
--

INSERT INTO `tb_booking` (`id`, `vetcategory`, `uname`, `price`, `total`, `username`, `name`, `mobileno`, `address`, `payment_method`, `submission_datetime`, `orderstatus`) VALUES
(5, 'dog', 'raj', 3000, 3000, 'logo', 'Lokesh', 8989675645, '67,Ramnad', 'Cash on Delivery', '2023-12-26 14:06:19', ''),
(6, 'coat', 'Kali', 12000, 12000, 'sam', 'Samsi', 9876453478, '27,theni', 'Direct Bank Transfer', '2023-12-28 14:57:49', 'delivered'),
(7, 'sheep', 'Kali', 8000, 8000, 'sam', 'Samsi', 9876453478, '27,theni', '', '2024-02-18 18:23:46', ''),
(8, 'sheep', 'Kali', 8000, 8000, 'sam', 'Samsi', 9876453478, '27,theni', 'Cash on Delivery', '2024-04-13 15:00:25', ''),
(9, 'cattle', 'Kali', 18000, 18000, 'sam', 'Samsi', 9876453478, '27,theni', 'Direct Bank Transfer', '2025-02-27 12:14:46', 'processing'),
(10, 'coat', 'Kali', 12000, 12000, 'sam', 'Samsi', 9876453478, '27,theni', 'UPI', '2025-03-23 10:36:29', '');

-- --------------------------------------------------------

--
-- Table structure for table `tb_buyer`
--

CREATE TABLE `tb_buyer` (
  `id` int(50) NOT NULL,
  `name` varchar(15) NOT NULL,
  `username` varchar(10) NOT NULL,
  `address` varchar(50) NOT NULL,
  `mobileno` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(20) NOT NULL,
  `action` int(5) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_buyer`
--

INSERT INTO `tb_buyer` (`id`, `name`, `username`, `address`, `mobileno`, `email`, `password`, `action`) VALUES
(1, 'Samsi', 'sam', '27,theni', 9876453478, 'sa@gmail.com', '123098', 0),
(2, 'Lokesh', 'Logo', '67,Ramnad', 8989675645, 'lo@gmail.com', '11223344', 0),
(3, 'abu', 'abu', 'pudukottai', 1234567899, 'abu@gmail.com', '123345', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tb_seller`
--

CREATE TABLE `tb_seller` (
  `id` int(50) NOT NULL,
  `name` varchar(20) NOT NULL,
  `username` varchar(10) NOT NULL,
  `address` varchar(50) NOT NULL,
  `mobileno` bigint(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `proof` text NOT NULL,
  `password` varchar(20) NOT NULL,
  `action` int(5) NOT NULL,
  `token` varchar(10) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_seller`
--

INSERT INTO `tb_seller` (`id`, `name`, `username`, `address`, `mobileno`, `email`, `proof`, `password`, `action`, `token`) VALUES
(1, 'Kalirajan', 'kali', '45,thoothukudi', 8987987867, 'ka@gmail.com', '', '101010', 1, '#834502'),
(2, 'Raja', 'raj', '45,Trichy', 8987675678, 'so@gmail.com', '', '000000', 1, '');

-- --------------------------------------------------------

--
-- Table structure for table `tb_total`
--

CREATE TABLE `tb_total` (
  `id` int(50) NOT NULL,
  `username` varchar(20) NOT NULL,
  `vetcategory` varchar(10) NOT NULL,
  `quantity` int(20) NOT NULL,
  `price` int(20) NOT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_total`
--

INSERT INTO `tb_total` (`id`, `username`, `vetcategory`, `quantity`, `price`) VALUES
(1, 'Kali', 'sheep', 2, 8000),
(2, 'Kali', 'sheep', 1, 8000),
(3, 'Kali', 'sheep', 2, 8000),
(4, 'Kali', 'sheep', 2, 8000),
(5, 'Kali', 'sheep', 1, 8000),
(6, 'Kali', 'sheep', 1, 8000),
(7, 'Kali', 'sheep', 1, 8000),
(8, 'Kali', 'sheep', 1, 8000),
(9, 'Kali', 'sheep', 3, 8000),
(10, 'Kali', 'sheep', 1, 8000),
(11, 'Kali', 'sheep', 3, 8000),
(12, 'Kali', 'coat', 2, 12000),
(13, 'Kali', 'coat', 2, 12000),
(14, 'Kali', 'coat', 4, 12000),
(15, 'Kali', 'coat', 4, 12000),
(16, 'Kali', 'sheep', 3, 8000),
(17, 'Kali', 'sheep', 2, 8000),
(18, 'Kali', 'sheep', 2, 8000),
(19, 'Kali', 'sheep', 2, 8000),
(20, 'Kali', 'sheep', 5, 8000),
(21, 'Kali', 'sheep', 4, 8000),
(22, 'Kali', 'sheep', 4, 8000),
(23, 'Kali', 'coat', 2, 12000),
(24, 'Kali', 'sheep', 4, 8000),
(25, 'Kali', 'sheep', 4, 8000),
(26, 'Kali', 'sheep', 6, 8000),
(27, 'Kali', 'sheep', 2, 8000),
(28, 'Kali', 'sheep', 2, 8000),
(29, 'Kali', 'sheep', 4, 8000),
(30, 'Kali', 'sheep', 5, 8000),
(31, 'Kali', 'sheep', 3, 8000),
(32, 'Kali', 'sheep', 5, 8000),
(33, 'Kali', 'sheep', 5, 8000),
(34, 'Kali', 'sheep', 5, 8000),
(35, 'Kali', 'coat', 2, 12000),
(36, 'Kali', 'sheep', 2, 8000),
(37, 'Kali', 'cattle', 3, 18000),
(38, 'Kali', 'cattle', 3, 18000),
(39, 'Kali', 'cattle', 3, 18000),
(40, 'Kali', 'coat', 1, 12000),
(41, 'Kali', 'coat', 1, 12000),
(42, 'Kali', 'sheep', 2, 8000),
(43, 'Kali', 'sheep', 3, 8000),
(44, 'Kali', 'sheep', 6, 8000),
(45, 'Kali', 'coat', 1, 12000),
(46, 'Kali', 'cattle', 2, 18000),
(47, 'Kali', 'cattle', 1, 18000),
(48, 'Kali', 'cattle', 2, 18000),
(49, 'Kali', 'cattle', 1, 18000),
(50, 'Kali', 'coat', 2, 12000),
(51, 'Kali', 'cattle', 2, 18000),
(52, 'Kali', 'cattle', 1, 18000),
(53, 'Kali', 'cattle', 3, 18000),
(54, 'Kali', 'cattle', 2, 18000),
(55, 'Kali', 'sheep', 2, 8000),
(56, 'Kali', 'coat', 1, 12000),
(57, 'Kali', 'sheep', 3, 8000),
(58, 'raj', 'dog', 2, 3000),
(59, 'Kali', 'sheep', 2, 8000),
(60, 'Kali', 'sheep', 2, 8000),
(61, 'Kali', 'sheep', 2, 8000),
(62, 'Kali', 'cattle', 2, 18000),
(63, 'Kali', 'coat', 2, 12000),
(64, 'raj', 'dog', 2, 3000),
(65, 'raj', 'dog', 3, 3000),
(66, 'Kali', 'coat', 1, 12000),
(67, 'Kali', 'sheep', 1, 8000),
(68, 'Kali', 'coat', 1, 12000),
(69, 'Kali', 'coat', 1, 12000),
(70, 'Kali', 'coat', 1, 12000),
(71, 'Kali', 'coat', 1, 12000),
(72, 'Kali', 'sheep', 2, 8000),
(73, 'Kali', 'cattle', 1, 18000),
(74, 'Kali', 'coat', 1, 12000),
(75, 'Kali', 'coat', 1, 12000),
(76, 'Kali', 'coat', 1, 12000);

-- --------------------------------------------------------

--
-- Table structure for table `tb_view`
--

CREATE TABLE `tb_view` (
  `id` int(11) NOT NULL,
  `susername` varchar(20) NOT NULL,
  `vetcategory` varchar(20) NOT NULL,
  `price` varchar(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `pid` varchar(11) NOT NULL,
  `status` int(11) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `date` varchar(20) NOT NULL,
  `time` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `room_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tb_view`
--

INSERT INTO `tb_view` (`id`, `susername`, `vetcategory`, `price`, `username`, `pid`, `status`, `rdate`, `date`, `time`, `email`, `room_id`) VALUES
(2, 'Kali', 'coat', '12000', 'sam', '1', 1, '07-03-2024', '12-03-2024', '10 pm', '', '1234'),
(3, 'Kali', 'coat', '12000', 'sam', '1', 1, '07-03-2024', '12-03-2024', '10 pm', 'exsample74@gmail.com', ''),
(4, 'Kali', 'coat', '12000', 'sam', '1', 0, '07-03-2024', '', '', 'sa@gmail.com', '');
