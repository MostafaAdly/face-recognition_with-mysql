# face-recognition_with-mysql
A simple face recognition made with python to recognize student faces from images saved in a MySQL Database.

Installation:
- Make sure you have at least python 3.10 or above.
- Make sure you have all libraries included installed.
- Make sure you have a database. (including the structure of it mentioned down below) (in summary just make sure you query the two mentioned queries down below in the needed database).

MySQL Database query to create the 2 needed tables as this is not coded:


-- Creating table attendance
CREATE TABLE `attendance` (
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `class` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `time_attended` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Creative table students
CREATE TABLE `students` (
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_url` varchar(2555) COLLATE utf8mb4_unicode_ci NOT NULL,
  `classes` varchar(2555) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
