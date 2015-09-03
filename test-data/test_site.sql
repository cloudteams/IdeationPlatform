CREATE DATABASE IF NOT EXISTS test_database;
USE test_database;
CREATE TABLE `users` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
  `firstname` varchar(255) default NULL,
  `lastname` varchar(255) default NULL,
  `gender` TEXT default NULL,
  `age` mediumint default NULL,
  `address` varchar(255) default NULL
);
INSERT INTO `users` VALUES (1,'Joshua','Berg','Male',54,'117-9283 Placerat. St.');
INSERT INTO `users` VALUES (2,'Vielka','Douglas','Female',33,'8186 Massa. Rd.');
INSERT INTO `users` VALUES (3,'Xantha','Kramer','Male',19,'P.O. Box 470, 7598 Tempus Ave');
INSERT INTO `users` VALUES (4,'Galvin','Maxwell','Female',51,'Ap #789-1731 Eget St.');
INSERT INTO `users` VALUES (5,'Gage','Alvarez','Male',25,'8484 Ultrices. Street');
INSERT INTO `users` VALUES (6,'Rhona','Glass','Female',24,'958-5459 Arcu. St.');
INSERT INTO `users` VALUES (7,'Kirby','Skinner','Male',49,'P.O. Box 803, 858 Lobortis Road');
INSERT INTO `users` VALUES (8,'Cleo','Aguilar','Female',60,'3918 Euismod Road');
INSERT INTO `users` VALUES (9,'Kevyn','Washington','Male',32,'835-5966 Est. St.');
INSERT INTO `users` VALUES (10,'August','Shaw','Female',33,'P.O. Box 853, 7698 Euismod Rd.');
INSERT INTO `users` VALUES (11,'Pascale','Bell','Male',48,'Ap #941-1231 Dolor. Rd.');
INSERT INTO `users` VALUES (12,'Leigh','Freeman','Female',59,'134-7594 Eu Road');
INSERT INTO `users` VALUES (13,'Ocean','Woods','Male',20,'148-6617 Vitae Rd.');
INSERT INTO `users` VALUES (14,'Pamela','Fowler','Female',58,'8235 Erat. Rd.');
INSERT INTO `users` VALUES (15,'Nina','Lindsey','Male',45,'Ap #488-5582 Fusce Av.');
INSERT INTO `users` VALUES (16,'Illana','Glover','Female',60,'6702 At, Street');
INSERT INTO `users` VALUES (17,'Brenda','Garcia','Male',41,'996-9424 Vivamus Rd.');
INSERT INTO `users` VALUES (18,'Katelyn','Frye','Female',51,'P.O. Box 227, 2289 Eu Rd.');
INSERT INTO `users` VALUES (19,'Gray','Lester','Male',26,'Ap #338-158 Auctor. St.');
INSERT INTO `users` VALUES (20,'Melyssa','Glenn','Female',56,'504-660 Ridiculus St.');
INSERT INTO `users` VALUES (21,'August','Landry','Male',57,'2408 Vulputate St.');
INSERT INTO `users` VALUES (22,'Arthur','Francis','Female',42,'Ap #847-4148 Habitant Rd.');
INSERT INTO `users` VALUES (23,'Rooney','Rowland','Male',42,'563-652 Sem St.');
INSERT INTO `users` VALUES (24,'Sean','Daniels','Female',59,'6465 Volutpat. Road');
INSERT INTO `users` VALUES (25,'Tobias','Phelps','Male',43,'P.O. Box 374, 8588 Pharetra. Ave');
INSERT INTO `users` VALUES (26,'Quynn','Ruiz','Female',45,'P.O. Box 662, 4143 Lectus Road');
INSERT INTO `users` VALUES (27,'Rana','Briggs','Male',43,'820-7322 Elementum St.');
INSERT INTO `users` VALUES (28,'Keaton','Gill','Female',47,'204-2772 Nascetur Av.');
INSERT INTO `users` VALUES (29,'Darryl','Thompson','Male',37,'Ap #823-1847 Egestas Ave');
INSERT INTO `users` VALUES (30,'Armando','Evans','Female',54,'Ap #263-2767 Sed Street');
INSERT INTO `users` VALUES (31,'Samantha','Harrington','Male',29,'Ap #831-2854 Aliquet Av.');
INSERT INTO `users` VALUES (32,'Jesse','Finch','Female',52,'P.O. Box 415, 2431 Sociis Street');
INSERT INTO `users` VALUES (33,'Emery','Buchanan','Male',55,'P.O. Box 897, 7338 Pede. Rd.');
INSERT INTO `users` VALUES (34,'Ann','Woods','Female',27,'P.O. Box 675, 4284 In Ave');
INSERT INTO `users` VALUES (35,'Uma','Richard','Male',62,'Ap #789-4655 Odio. Av.');
INSERT INTO `users` VALUES (36,'Kelly','Mullins','Female',33,'590-8078 Enim. Avenue');
INSERT INTO `users` VALUES (37,'Magee','Frazier','Male',20,'9940 Magnis Avenue');
INSERT INTO `users` VALUES (38,'Knox','Workman','Female',20,'770-4661 A, Av.');
INSERT INTO `users` VALUES (39,'Dorothy','King','Male',54,'P.O. Box 201, 8043 Nisl. Ave');
INSERT INTO `users` VALUES (40,'William','Bernard','Female',29,'876-2745 Molestie Av.');
INSERT INTO `users` VALUES (41,'Mechelle','Cunningham','Male',48,'P.O. Box 826, 4029 Parturient St.');
INSERT INTO `users` VALUES (42,'Dean','Bray','Female',42,'P.O. Box 855, 8789 Lacus Avenue');
INSERT INTO `users` VALUES (43,'Rylee','Farrell','Male',65,'557-5913 Laoreet St.');
INSERT INTO `users` VALUES (44,'Leslie','Buckley','Female',53,'1754 Ipsum. Rd.');
INSERT INTO `users` VALUES (45,'Maryam','Levine','Male',58,'733-453 Risus Road');
INSERT INTO `users` VALUES (46,'Garrett','Palmer','Female',63,'4327 Et Rd.');
INSERT INTO `users` VALUES (47,'Whitney','Ratliff','Male',18,'P.O. Box 787, 2829 Amet, Ave');
INSERT INTO `users` VALUES (48,'Addison','Callahan','Female',56,'Ap #418-6028 Lobortis Ave');
INSERT INTO `users` VALUES (49,'Amanda','Clements','Male',49,'1762 Egestas Rd.');
INSERT INTO `users` VALUES (50,'Camille','Shaw','Female',24,'P.O. Box 888, 9235 Lacinia. St.');
INSERT INTO `users` VALUES (51,'Velma','Knowles','Male',40,'P.O. Box 840, 7473 Mollis Ave');
INSERT INTO `users` VALUES (52,'Kermit','Bullock','Female',64,'6426 Facilisi. Rd.');
INSERT INTO `users` VALUES (53,'Hall','Watkins','Male',63,'Ap #836-964 Augue Road');
INSERT INTO `users` VALUES (54,'Holmes','Cole','Female',40,'Ap #476-1418 Ante Rd.');
INSERT INTO `users` VALUES (55,'Emerson','Thornton','Male',55,'1043 Accumsan Street');
INSERT INTO `users` VALUES (56,'Charissa','Coffey','Female',52,'999-938 Nec Rd.');
INSERT INTO `users` VALUES (57,'Philip','Watts','Male',30,'396-2307 Rutrum Rd.');
INSERT INTO `users` VALUES (58,'Boris','Poole','Female',65,'3261 Ac Av.');
INSERT INTO `users` VALUES (59,'Grady','Morton','Male',50,'222-2940 Adipiscing St.');
INSERT INTO `users` VALUES (60,'Erica','Albert','Female',37,'262-5878 Nulla. Av.');
INSERT INTO `users` VALUES (61,'Tana','Galloway','Male',49,'P.O. Box 503, 7553 Mollis Rd.');
INSERT INTO `users` VALUES (62,'Riley','Cotton','Female',31,'P.O. Box 360, 7450 Euismod St.');
INSERT INTO `users` VALUES (63,'Zahir','Dejesus','Male',65,'Ap #391-7073 Duis St.');
INSERT INTO `users` VALUES (64,'Kaitlin','Harmon','Female',59,'2498 Dui, Avenue');
INSERT INTO `users` VALUES (65,'Vincent','Vance','Male',47,'Ap #205-5928 Dolor. St.');
INSERT INTO `users` VALUES (66,'Graham','Higgins','Female',57,'919 Nullam St.');
INSERT INTO `users` VALUES (67,'Charlotte','Good','Male',22,'P.O. Box 246, 1631 Molestie. Road');
INSERT INTO `users` VALUES (68,'Andrew','Fry','Female',45,'5885 Sem St.');
INSERT INTO `users` VALUES (69,'Eric','Sexton','Male',52,'475-5889 Nec, Road');
INSERT INTO `users` VALUES (70,'Axel','Arnold','Female',43,'P.O. Box 557, 3684 Velit Street');
INSERT INTO `users` VALUES (71,'Dexter','Potts','Male',34,'9970 Iaculis Ave');
INSERT INTO `users` VALUES (72,'Rudyard','Prince','Female',45,'Ap #360-1046 Vulputate, Road');
INSERT INTO `users` VALUES (73,'Teegan','Barnett','Male',29,'717-9172 Sollicitudin St.');
INSERT INTO `users` VALUES (74,'Cara','Love','Female',30,'Ap #169-7104 Aenean Ave');
INSERT INTO `users` VALUES (75,'Sierra','Wilkins','Male',21,'Ap #825-6621 Molestie Street');
INSERT INTO `users` VALUES (76,'Yardley','Roberts','Female',35,'245-5519 Blandit Rd.');
INSERT INTO `users` VALUES (77,'Lacota','Walton','Male',54,'576-9495 Mollis Road');
INSERT INTO `users` VALUES (78,'Nevada','Hendrix','Female',60,'521-6893 Suscipit Rd.');
INSERT INTO `users` VALUES (79,'Amir','Galloway','Male',49,'251 Elit. St.');
INSERT INTO `users` VALUES (80,'Meredith','Marquez','Female',63,'1303 Morbi Av.');
INSERT INTO `users` VALUES (81,'Jacqueline','Jenkins','Male',28,'Ap #653-959 Feugiat Avenue');
INSERT INTO `users` VALUES (82,'Dahlia','Estes','Female',39,'P.O. Box 953, 3422 Blandit St.');
INSERT INTO `users` VALUES (83,'Keely','Carson','Male',62,'Ap #721-5340 Aliquam Rd.');
INSERT INTO `users` VALUES (84,'Marny','Little','Female',21,'P.O. Box 588, 1025 Penatibus Street');
INSERT INTO `users` VALUES (85,'Valentine','Ortega','Male',46,'Ap #323-9422 Ut, Av.');
INSERT INTO `users` VALUES (86,'Aretha','Sandoval','Female',31,'366-8130 Rutrum Avenue');
INSERT INTO `users` VALUES (87,'Carly','Walls','Male',29,'P.O. Box 149, 5227 Ac Rd.');
INSERT INTO `users` VALUES (88,'Len','Stout','Female',46,'9438 Sociis Road');
INSERT INTO `users` VALUES (89,'Leslie','Cooley','Male',28,'Ap #575-2723 Curabitur Rd.');
INSERT INTO `users` VALUES (90,'Nerea','Langley','Female',56,'201-1732 Curabitur Avenue');
INSERT INTO `users` VALUES (91,'Urielle','Mccall','Male',52,'Ap #479-7723 Vestibulum Road');
INSERT INTO `users` VALUES (92,'Stacy','Frost','Female',63,'2528 Mauris St.');
INSERT INTO `users` VALUES (93,'Tanisha','Callahan','Male',49,'101 Nunc Ave');
INSERT INTO `users` VALUES (94,'Lewis','Mosley','Female',63,'128 Enim. Avenue');
INSERT INTO `users` VALUES (95,'Igor','Mueller','Male',33,'422-3037 Sit St.');
INSERT INTO `users` VALUES (96,'Indigo','George','Female',42,'P.O. Box 591, 866 Eu Street');
INSERT INTO `users` VALUES (97,'Ruby','Pruitt','Male',31,'1141 Vehicula. St.');
INSERT INTO `users` VALUES (98,'Chase','Combs','Female',31,'P.O. Box 555, 1699 Non, Road');
INSERT INTO `users` VALUES (99,'Leslie','Mcbride','Male',49,'Ap #770-9832 Dolor. Rd.');
INSERT INTO `users` VALUES (100,'Lynn','Cardenas','Female',33,'3723 Cursus Avenue');
CREATE TABLE `running` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`user`	INTEGER NOT NULL,
	`duration`	INTEGER,
	FOREIGN KEY (user) REFERENCES users(id)
);
INSERT INTO `running` VALUES (1,1,21);
INSERT INTO `running` VALUES (2,85,35);
INSERT INTO `running` VALUES (3,11,29);
INSERT INTO `running` VALUES (4,95,29);
INSERT INTO `running` VALUES (5,67,24);
INSERT INTO `running` VALUES (6,94,9);
INSERT INTO `running` VALUES (7,73,32);
INSERT INTO `running` VALUES (8,40,37);
INSERT INTO `running` VALUES (9,30,5);
INSERT INTO `running` VALUES (10,38,37);
INSERT INTO `running` VALUES (11,67,34);
INSERT INTO `running` VALUES (12,69,16);
INSERT INTO `running` VALUES (13,20,9);
INSERT INTO `running` VALUES (14,72,5);
INSERT INTO `running` VALUES (15,48,36);
INSERT INTO `running` VALUES (16,62,39);
INSERT INTO `running` VALUES (17,70,13);
INSERT INTO `running` VALUES (18,80,24);
INSERT INTO `running` VALUES (19,41,38);
INSERT INTO `running` VALUES (20,72,27);
INSERT INTO `running` VALUES (21,44,29);
INSERT INTO `running` VALUES (22,86,30);
INSERT INTO `running` VALUES (23,38,24);
INSERT INTO `running` VALUES (24,76,39);
INSERT INTO `running` VALUES (25,57,19);
INSERT INTO `running` VALUES (26,94,36);
INSERT INTO `running` VALUES (27,18,34);
INSERT INTO `running` VALUES (28,69,36);
INSERT INTO `running` VALUES (29,4,26);
INSERT INTO `running` VALUES (30,53,39);
INSERT INTO `running` VALUES (31,55,16);
INSERT INTO `running` VALUES (32,44,17);
INSERT INTO `running` VALUES (33,96,23);
INSERT INTO `running` VALUES (34,63,9);
INSERT INTO `running` VALUES (35,55,22);
INSERT INTO `running` VALUES (36,44,39);
INSERT INTO `running` VALUES (37,21,16);
INSERT INTO `running` VALUES (38,18,38);
INSERT INTO `running` VALUES (39,19,20);
INSERT INTO `running` VALUES (40,16,14);
INSERT INTO `running` VALUES (41,53,35);
INSERT INTO `running` VALUES (42,92,4);
INSERT INTO `running` VALUES (43,13,26);
INSERT INTO `running` VALUES (44,20,31);
INSERT INTO `running` VALUES (45,90,31);
INSERT INTO `running` VALUES (46,15,13);
INSERT INTO `running` VALUES (47,18,4);
INSERT INTO `running` VALUES (48,84,28);
INSERT INTO `running` VALUES (49,98,16);
INSERT INTO `running` VALUES (50,83,21);
INSERT INTO `running` VALUES (51,1,36);
INSERT INTO `running` VALUES (52,42,13);
INSERT INTO `running` VALUES (53,21,15);
INSERT INTO `running` VALUES (54,1,11);
INSERT INTO `running` VALUES (55,62,8);
INSERT INTO `running` VALUES (56,36,32);
INSERT INTO `running` VALUES (57,9,13);
INSERT INTO `running` VALUES (58,3,9);
INSERT INTO `running` VALUES (59,21,27);
INSERT INTO `running` VALUES (60,94,21);
INSERT INTO `running` VALUES (61,53,31);
INSERT INTO `running` VALUES (62,30,33);
INSERT INTO `running` VALUES (63,57,7);
INSERT INTO `running` VALUES (64,7,9);
INSERT INTO `running` VALUES (65,95,33);
INSERT INTO `running` VALUES (66,84,33);
INSERT INTO `running` VALUES (67,75,25);
INSERT INTO `running` VALUES (68,56,24);
INSERT INTO `running` VALUES (69,32,31);
INSERT INTO `running` VALUES (70,68,8);
INSERT INTO `running` VALUES (71,57,11);
INSERT INTO `running` VALUES (72,12,39);
INSERT INTO `running` VALUES (73,33,19);
INSERT INTO `running` VALUES (74,73,28);
INSERT INTO `running` VALUES (75,93,40);
INSERT INTO `running` VALUES (76,85,16);
INSERT INTO `running` VALUES (77,41,6);
INSERT INTO `running` VALUES (78,30,26);
INSERT INTO `running` VALUES (79,90,4);
INSERT INTO `running` VALUES (80,26,23);
INSERT INTO `running` VALUES (81,11,11);
INSERT INTO `running` VALUES (82,24,18);
INSERT INTO `running` VALUES (83,69,13);
INSERT INTO `running` VALUES (84,66,29);
INSERT INTO `running` VALUES (85,97,29);
INSERT INTO `running` VALUES (86,63,31);
INSERT INTO `running` VALUES (87,30,28);
INSERT INTO `running` VALUES (88,41,24);
INSERT INTO `running` VALUES (89,43,21);
INSERT INTO `running` VALUES (90,84,40);
INSERT INTO `running` VALUES (91,15,39);
INSERT INTO `running` VALUES (92,3,29);
INSERT INTO `running` VALUES (93,51,36);
INSERT INTO `running` VALUES (94,36,11);
INSERT INTO `running` VALUES (95,70,21);
INSERT INTO `running` VALUES (96,89,30);
INSERT INTO `running` VALUES (97,84,40);
INSERT INTO `running` VALUES (98,90,5);
INSERT INTO `running` VALUES (99,65,30);
INSERT INTO `running` VALUES (100,93,39);
INSERT INTO `running` VALUES (101,90,39);
INSERT INTO `running` VALUES (102,88,12);
INSERT INTO `running` VALUES (103,39,35);
INSERT INTO `running` VALUES (104,9,6);
INSERT INTO `running` VALUES (105,89,26);
INSERT INTO `running` VALUES (106,51,34);
INSERT INTO `running` VALUES (107,70,24);
INSERT INTO `running` VALUES (108,70,16);
INSERT INTO `running` VALUES (109,71,21);
INSERT INTO `running` VALUES (110,5,27);
INSERT INTO `running` VALUES (111,42,7);
INSERT INTO `running` VALUES (112,17,37);
INSERT INTO `running` VALUES (113,23,38);
INSERT INTO `running` VALUES (114,84,22);
INSERT INTO `running` VALUES (115,42,22);
INSERT INTO `running` VALUES (116,19,15);
INSERT INTO `running` VALUES (117,1,15);
INSERT INTO `running` VALUES (118,95,10);
INSERT INTO `running` VALUES (119,9,15);
INSERT INTO `running` VALUES (120,78,24);
INSERT INTO `running` VALUES (121,18,8);
INSERT INTO `running` VALUES (122,58,10);
INSERT INTO `running` VALUES (123,23,37);
INSERT INTO `running` VALUES (124,28,12);
INSERT INTO `running` VALUES (125,70,36);
INSERT INTO `running` VALUES (126,36,33);
INSERT INTO `running` VALUES (127,79,32);
INSERT INTO `running` VALUES (128,4,40);
INSERT INTO `running` VALUES (129,39,16);
INSERT INTO `running` VALUES (130,27,30);
INSERT INTO `running` VALUES (131,70,22);
INSERT INTO `running` VALUES (132,58,12);
INSERT INTO `running` VALUES (133,3,28);
INSERT INTO `running` VALUES (134,14,7);
INSERT INTO `running` VALUES (135,59,25);
INSERT INTO `running` VALUES (136,18,8);
INSERT INTO `running` VALUES (137,83,36);
INSERT INTO `running` VALUES (138,23,27);
INSERT INTO `running` VALUES (139,42,32);
INSERT INTO `running` VALUES (140,5,16);
INSERT INTO `running` VALUES (141,10,35);
INSERT INTO `running` VALUES (142,95,27);
INSERT INTO `running` VALUES (143,70,25);
INSERT INTO `running` VALUES (144,32,38);
INSERT INTO `running` VALUES (145,92,19);
INSERT INTO `running` VALUES (146,2,33);
INSERT INTO `running` VALUES (147,84,30);
INSERT INTO `running` VALUES (148,58,33);
INSERT INTO `running` VALUES (149,87,11);
INSERT INTO `running` VALUES (150,1,21);
INSERT INTO `running` VALUES (151,45,27);
INSERT INTO `running` VALUES (152,84,29);
INSERT INTO `running` VALUES (153,72,31);
INSERT INTO `running` VALUES (154,84,33);
INSERT INTO `running` VALUES (155,19,4);
INSERT INTO `running` VALUES (156,43,26);
INSERT INTO `running` VALUES (157,89,10);
INSERT INTO `running` VALUES (158,74,30);
INSERT INTO `running` VALUES (159,3,36);
INSERT INTO `running` VALUES (160,78,5);
INSERT INTO `running` VALUES (161,85,17);
INSERT INTO `running` VALUES (162,91,33);
INSERT INTO `running` VALUES (163,100,9);
INSERT INTO `running` VALUES (164,77,32);
INSERT INTO `running` VALUES (165,45,35);
INSERT INTO `running` VALUES (166,44,36);
INSERT INTO `running` VALUES (167,87,31);
INSERT INTO `running` VALUES (168,26,34);
INSERT INTO `running` VALUES (169,42,25);
INSERT INTO `running` VALUES (170,60,27);
INSERT INTO `running` VALUES (171,46,24);
INSERT INTO `running` VALUES (172,26,10);
INSERT INTO `running` VALUES (173,30,18);
INSERT INTO `running` VALUES (174,26,12);
INSERT INTO `running` VALUES (175,6,6);
INSERT INTO `running` VALUES (176,31,20);
INSERT INTO `running` VALUES (177,15,6);
INSERT INTO `running` VALUES (178,23,14);
INSERT INTO `running` VALUES (179,86,33);
INSERT INTO `running` VALUES (180,94,24);
INSERT INTO `running` VALUES (181,51,17);
INSERT INTO `running` VALUES (182,71,23);
INSERT INTO `running` VALUES (183,30,22);
INSERT INTO `running` VALUES (184,75,18);
INSERT INTO `running` VALUES (185,95,27);
INSERT INTO `running` VALUES (186,39,22);
INSERT INTO `running` VALUES (187,46,7);
INSERT INTO `running` VALUES (188,56,34);
INSERT INTO `running` VALUES (189,99,39);
INSERT INTO `running` VALUES (190,27,25);
INSERT INTO `running` VALUES (191,55,24);
INSERT INTO `running` VALUES (192,55,39);
INSERT INTO `running` VALUES (193,70,26);
INSERT INTO `running` VALUES (194,71,30);
INSERT INTO `running` VALUES (195,31,15);
INSERT INTO `running` VALUES (196,38,36);
INSERT INTO `running` VALUES (197,7,28);
INSERT INTO `running` VALUES (198,40,19);
INSERT INTO `running` VALUES (199,2,11);
INSERT INTO `running` VALUES (200,57,19);
INSERT INTO `running` VALUES (201,60,18);
INSERT INTO `running` VALUES (202,69,4);
INSERT INTO `running` VALUES (203,17,39);
INSERT INTO `running` VALUES (204,50,19);
INSERT INTO `running` VALUES (205,66,9);
INSERT INTO `running` VALUES (206,15,9);
INSERT INTO `running` VALUES (207,48,15);
INSERT INTO `running` VALUES (208,85,38);
INSERT INTO `running` VALUES (209,98,19);
INSERT INTO `running` VALUES (210,32,23);
INSERT INTO `running` VALUES (211,48,16);
INSERT INTO `running` VALUES (212,82,28);
INSERT INTO `running` VALUES (213,91,36);
INSERT INTO `running` VALUES (214,89,23);
INSERT INTO `running` VALUES (215,43,20);
INSERT INTO `running` VALUES (216,48,31);
INSERT INTO `running` VALUES (217,31,15);
INSERT INTO `running` VALUES (218,77,9);
INSERT INTO `running` VALUES (219,66,9);
INSERT INTO `running` VALUES (220,47,5);
INSERT INTO `running` VALUES (221,7,4);
INSERT INTO `running` VALUES (222,14,25);
INSERT INTO `running` VALUES (223,21,24);
INSERT INTO `running` VALUES (224,79,16);
INSERT INTO `running` VALUES (225,82,11);
INSERT INTO `running` VALUES (226,65,26);
INSERT INTO `running` VALUES (227,70,17);
INSERT INTO `running` VALUES (228,23,32);
INSERT INTO `running` VALUES (229,50,25);
INSERT INTO `running` VALUES (230,1,23);
INSERT INTO `running` VALUES (231,12,13);
INSERT INTO `running` VALUES (232,3,24);
INSERT INTO `running` VALUES (233,2,35);
INSERT INTO `running` VALUES (234,69,31);
INSERT INTO `running` VALUES (235,22,9);
INSERT INTO `running` VALUES (236,23,40);
INSERT INTO `running` VALUES (237,100,26);
INSERT INTO `running` VALUES (238,33,8);
INSERT INTO `running` VALUES (239,39,17);
INSERT INTO `running` VALUES (240,91,10);
INSERT INTO `running` VALUES (241,8,9);
INSERT INTO `running` VALUES (242,29,6);
INSERT INTO `running` VALUES (243,5,40);
INSERT INTO `running` VALUES (244,59,39);
INSERT INTO `running` VALUES (245,44,20);
INSERT INTO `running` VALUES (246,26,31);
INSERT INTO `running` VALUES (247,85,33);
INSERT INTO `running` VALUES (248,61,35);
INSERT INTO `running` VALUES (249,3,16);
INSERT INTO `running` VALUES (250,30,27);
INSERT INTO `running` VALUES (251,97,33);
INSERT INTO `running` VALUES (252,34,12);
INSERT INTO `running` VALUES (253,53,16);
INSERT INTO `running` VALUES (254,16,9);
INSERT INTO `running` VALUES (255,81,37);
INSERT INTO `running` VALUES (256,48,22);
INSERT INTO `running` VALUES (257,59,28);
INSERT INTO `running` VALUES (258,14,26);
INSERT INTO `running` VALUES (259,72,23);
INSERT INTO `running` VALUES (260,11,9);
INSERT INTO `running` VALUES (261,4,13);
INSERT INTO `running` VALUES (262,16,12);
INSERT INTO `running` VALUES (263,54,32);
INSERT INTO `running` VALUES (264,99,21);
INSERT INTO `running` VALUES (265,44,4);
INSERT INTO `running` VALUES (266,25,5);
INSERT INTO `running` VALUES (267,77,10);
INSERT INTO `running` VALUES (268,78,17);
INSERT INTO `running` VALUES (269,73,36);
INSERT INTO `running` VALUES (270,45,31);
INSERT INTO `running` VALUES (271,64,15);
INSERT INTO `running` VALUES (272,60,33);
INSERT INTO `running` VALUES (273,19,26);
INSERT INTO `running` VALUES (274,47,22);
INSERT INTO `running` VALUES (275,7,27);
INSERT INTO `running` VALUES (276,77,21);
INSERT INTO `running` VALUES (277,28,15);
INSERT INTO `running` VALUES (278,90,14);
INSERT INTO `running` VALUES (279,55,27);
INSERT INTO `running` VALUES (280,60,29);
INSERT INTO `running` VALUES (281,2,13);
INSERT INTO `running` VALUES (282,1,25);
INSERT INTO `running` VALUES (283,6,21);
INSERT INTO `running` VALUES (284,88,27);
INSERT INTO `running` VALUES (285,91,8);
INSERT INTO `running` VALUES (286,14,35);
INSERT INTO `running` VALUES (287,19,38);
INSERT INTO `running` VALUES (288,41,6);
INSERT INTO `running` VALUES (289,7,12);
INSERT INTO `running` VALUES (290,73,10);
INSERT INTO `running` VALUES (291,42,22);
INSERT INTO `running` VALUES (292,34,28);
INSERT INTO `running` VALUES (293,9,6);
INSERT INTO `running` VALUES (294,3,37);
INSERT INTO `running` VALUES (295,79,26);
INSERT INTO `running` VALUES (296,61,24);
INSERT INTO `running` VALUES (297,41,17);
INSERT INTO `running` VALUES (298,54,31);
INSERT INTO `running` VALUES (299,15,29);
INSERT INTO `running` VALUES (300,6,30);
INSERT INTO `running` VALUES (301,100,14);
INSERT INTO `running` VALUES (302,27,35);
INSERT INTO `running` VALUES (303,29,15);
INSERT INTO `running` VALUES (304,60,35);
INSERT INTO `running` VALUES (305,56,26);
INSERT INTO `running` VALUES (306,96,20);
INSERT INTO `running` VALUES (307,14,10);
INSERT INTO `running` VALUES (308,98,11);
INSERT INTO `running` VALUES (309,38,10);
INSERT INTO `running` VALUES (310,74,31);
INSERT INTO `running` VALUES (311,82,11);
INSERT INTO `running` VALUES (312,56,20);
INSERT INTO `running` VALUES (313,78,26);
INSERT INTO `running` VALUES (314,35,32);
INSERT INTO `running` VALUES (315,98,8);
INSERT INTO `running` VALUES (316,16,24);
INSERT INTO `running` VALUES (317,6,10);
INSERT INTO `running` VALUES (318,58,36);
INSERT INTO `running` VALUES (319,75,19);
INSERT INTO `running` VALUES (320,9,29);
INSERT INTO `running` VALUES (321,94,39);
INSERT INTO `running` VALUES (322,57,4);
INSERT INTO `running` VALUES (323,57,28);
INSERT INTO `running` VALUES (324,81,36);
INSERT INTO `running` VALUES (325,54,26);
INSERT INTO `running` VALUES (326,61,28);
INSERT INTO `running` VALUES (327,45,35);
INSERT INTO `running` VALUES (328,100,5);
INSERT INTO `running` VALUES (329,31,9);
INSERT INTO `running` VALUES (330,25,26);
INSERT INTO `running` VALUES (331,58,28);
INSERT INTO `running` VALUES (332,66,5);
INSERT INTO `running` VALUES (333,57,34);
INSERT INTO `running` VALUES (334,8,30);
INSERT INTO `running` VALUES (335,38,31);
INSERT INTO `running` VALUES (336,5,36);
INSERT INTO `running` VALUES (337,19,24);
INSERT INTO `running` VALUES (338,5,33);
INSERT INTO `running` VALUES (339,31,40);
INSERT INTO `running` VALUES (340,35,39);
INSERT INTO `running` VALUES (341,21,17);
INSERT INTO `running` VALUES (342,44,19);
INSERT INTO `running` VALUES (343,60,20);
INSERT INTO `running` VALUES (344,25,35);
INSERT INTO `running` VALUES (345,18,15);
INSERT INTO `running` VALUES (346,85,36);
INSERT INTO `running` VALUES (347,36,13);
INSERT INTO `running` VALUES (348,12,14);
INSERT INTO `running` VALUES (349,66,37);
INSERT INTO `running` VALUES (350,77,38);
INSERT INTO `running` VALUES (351,61,13);
INSERT INTO `running` VALUES (352,1,18);
INSERT INTO `running` VALUES (353,39,6);
INSERT INTO `running` VALUES (354,4,36);
INSERT INTO `running` VALUES (355,72,37);
INSERT INTO `running` VALUES (356,94,33);
INSERT INTO `running` VALUES (357,45,27);
INSERT INTO `running` VALUES (358,31,5);
INSERT INTO `running` VALUES (359,94,6);
INSERT INTO `running` VALUES (360,15,9);
INSERT INTO `running` VALUES (361,63,14);
INSERT INTO `running` VALUES (362,99,30);
INSERT INTO `running` VALUES (363,1,4);
INSERT INTO `running` VALUES (364,18,14);
INSERT INTO `running` VALUES (365,57,37);
INSERT INTO `running` VALUES (366,45,28);
INSERT INTO `running` VALUES (367,92,15);
INSERT INTO `running` VALUES (368,56,23);
INSERT INTO `running` VALUES (369,78,9);
INSERT INTO `running` VALUES (370,42,20);
INSERT INTO `running` VALUES (371,60,29);
INSERT INTO `running` VALUES (372,92,22);
INSERT INTO `running` VALUES (373,46,7);
INSERT INTO `running` VALUES (374,34,27);
INSERT INTO `running` VALUES (375,58,39);
INSERT INTO `running` VALUES (376,57,23);
INSERT INTO `running` VALUES (377,83,24);
INSERT INTO `running` VALUES (378,62,31);
INSERT INTO `running` VALUES (379,18,19);
INSERT INTO `running` VALUES (380,38,18);
INSERT INTO `running` VALUES (381,8,19);
INSERT INTO `running` VALUES (382,61,40);
INSERT INTO `running` VALUES (383,67,11);
INSERT INTO `running` VALUES (384,5,32);
INSERT INTO `running` VALUES (385,83,8);
INSERT INTO `running` VALUES (386,65,17);
INSERT INTO `running` VALUES (387,82,28);
INSERT INTO `running` VALUES (388,93,12);
INSERT INTO `running` VALUES (389,22,32);
INSERT INTO `running` VALUES (390,53,29);
INSERT INTO `running` VALUES (391,12,18);
INSERT INTO `running` VALUES (392,11,5);
INSERT INTO `running` VALUES (393,84,7);
INSERT INTO `running` VALUES (394,2,29);
INSERT INTO `running` VALUES (395,41,35);
INSERT INTO `running` VALUES (396,36,32);
INSERT INTO `running` VALUES (397,25,4);
INSERT INTO `running` VALUES (398,68,5);
INSERT INTO `running` VALUES (399,41,9);
INSERT INTO `running` VALUES (400,92,18);
INSERT INTO `running` VALUES (401,24,14);
