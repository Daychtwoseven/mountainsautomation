/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : mountainsautomation

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 25/12/2022 23:40:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for app_urlresults
-- ----------------------------
DROP TABLE IF EXISTS `app_urlresults`;
CREATE TABLE `app_urlresults`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `url_id` bigint NOT NULL,
  `address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `applicant` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `city` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `date` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `existing_solar_system` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `job_value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `kw` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `name` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `panel_upgrade` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `state` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `status` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `total_cost` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `utility_information` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `zip` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `record_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `owner` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `contractor` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `app_urlresults_url_id_915b1b51_fk_app_urls_id`(`url_id`) USING BTREE,
  CONSTRAINT `app_urlresults_url_id_915b1b51_fk_app_urls_id` FOREIGN KEY (`url_id`) REFERENCES `app_urls` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8221 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of app_urlresults
-- ----------------------------
INSERT INTO `app_urlresults` VALUES (8299, '2022-12-25 15:11:37.131182', 69, '424 SEBASTIAN SQ', NULL, 'SAINT AUGUSTINE', '2022-12-22', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32095', '12219466', NULL, 'MCKINNEY, CHRISTOPHER R');
INSERT INTO `app_urlresults` VALUES (8300, '2022-12-25 15:11:38.029136', 69, '3304 WOODBURY CT', NULL, 'SAINT AUGUSTINE', '2022-12-22', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12214880', NULL, 'MCKINNEY, CHRISTOPHER R');
INSERT INTO `app_urlresults` VALUES (8301, '2022-12-25 15:11:38.879960', 69, '76 ELIANA AVE', NULL, 'Saint Johns', '2022-12-22', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12219493', NULL, 'GWINN, WILLIAM B');
INSERT INTO `app_urlresults` VALUES (8302, '2022-12-25 15:11:39.738480', 69, '213 OLETA WAY', NULL, 'SAINT AUGUSTINE', '2022-12-22', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32095', '12219516', NULL, 'PHILLIPS, WAYNE A');
INSERT INTO `app_urlresults` VALUES (8303, '2022-12-25 15:11:40.651311', 69, '2716 N SCREECH OWL AVE', NULL, 'SAINT AUGUSTINE', '2022-12-22', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32084', '12219490', NULL, 'PADGETT II, RONNIE FREEMAN');
INSERT INTO `app_urlresults` VALUES (8304, '2022-12-25 15:11:41.528778', 69, '219 FLORA LAKE CIR', NULL, 'SAINT AUGUSTINE', '2022-12-22', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32095', '12219485', NULL, 'NEWMAN, MICHAEL DAVID');
INSERT INTO `app_urlresults` VALUES (8305, '2022-12-25 15:11:42.359120', 69, '196 E NEW ENGLAND DR', NULL, 'ELKTON', '2022-12-22', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32033', '12219467', NULL, 'GAYDOU, ROGER W');
INSERT INTO `app_urlresults` VALUES (8306, '2022-12-25 15:11:43.222284', 69, '378 ATLANTA DR', NULL, 'SAINT AUGUSTINE', '2022-12-21', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12219460', NULL, 'CIRILLO, JOSEPH');
INSERT INTO `app_urlresults` VALUES (8307, '2022-12-25 15:11:44.072420', 69, '267 STONEWELL DR', NULL, 'SAINT JOHNS', '2022-12-21', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12218754', NULL, 'HALL, ANDREW');
INSERT INTO `app_urlresults` VALUES (8308, '2022-12-25 15:11:44.938777', 69, '745 PORTO CRISTO AVE', NULL, 'SAINT AUGUSTINE', '2022-12-21', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12219444', NULL, 'ALBRIGHT, GREG');
INSERT INTO `app_urlresults` VALUES (8309, '2022-12-25 15:11:45.765916', 69, '219 MYRTLE BROOK BND', NULL, 'PONTE VEDRA', '2022-12-21', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32081', '12219447', NULL, 'PASTERNAK, MICHAEL C');
INSERT INTO `app_urlresults` VALUES (8310, '2022-12-25 15:11:46.633495', 69, '141 SMITH ST', NULL, 'SAINT AUGUSTINE', '2022-12-21', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32084', '12219439', NULL, 'JEFFS, BRYSON');
INSERT INTO `app_urlresults` VALUES (8311, '2022-12-25 15:11:47.468677', 69, '581 N LEGACY TRL', NULL, 'SAINT AUGUSTINE', '2022-12-21', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12219369', NULL, 'PADGETT II, RONNIE FREEMAN');
INSERT INTO `app_urlresults` VALUES (8312, '2022-12-25 15:11:48.329620', 69, '51 ONYX CT', NULL, 'SAINT AUGUSTINE', '2022-12-21', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12219367', NULL, 'PADGETT II, RONNIE FREEMAN');
INSERT INTO `app_urlresults` VALUES (8313, '2022-12-25 15:11:49.170302', 69, '48 ATLAS DR', NULL, 'SAINT AUGUSTINE', '2022-12-21', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12216838', NULL, 'EMES, BRETT L');
INSERT INTO `app_urlresults` VALUES (8314, '2022-12-25 15:11:50.043350', 69, '3160 TROUT CREEK CT', NULL, 'SAINT AUGUSTINE', '2022-12-19', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12219150', NULL, 'MCKINNEY, CHRISTOPHER R');
INSERT INTO `app_urlresults` VALUES (8315, '2022-12-25 15:11:50.909512', 69, '113 TOTTEN WAY', NULL, 'SAINT AUGUSTINE', '2022-12-19', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12219149', NULL, 'MCKINNEY, CHRISTOPHER R');
INSERT INTO `app_urlresults` VALUES (8316, '2022-12-25 15:11:51.774147', 69, '162 WINDERMERE WAY', NULL, 'SAINT AUGUSTINE', '2022-12-19', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32095', '12218976', NULL, 'VERNER, CHRISTOPHER LOWE');
INSERT INTO `app_urlresults` VALUES (8317, '2022-12-25 15:11:52.686059', 69, '449 GLORIETA DR', NULL, 'SAINT AUGUSTINE', '2022-12-19', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32095', '12217279', NULL, 'VERGONA, MICHAEL R');
INSERT INTO `app_urlresults` VALUES (8318, '2022-12-25 15:11:53.540829', 69, '115 FIDDLEWOOD DR', NULL, 'SAINT JOHNS', '2022-12-16', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12219249', NULL, 'PEEBLES, STEVEN W');
INSERT INTO `app_urlresults` VALUES (8319, '2022-12-25 15:11:54.428249', 69, '576 N LEGACY TRL', NULL, 'SAINT AUGUSTINE', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12219233', NULL, 'PADGETT II, RONNIE FREEMAN');
INSERT INTO `app_urlresults` VALUES (8320, '2022-12-25 15:11:55.285409', 69, '126 MOSAIC PARK AVE', NULL, 'SAINT AUGUSTINE', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218218', NULL, 'PASTERNAK, MICHAEL C');
INSERT INTO `app_urlresults` VALUES (8321, '2022-12-25 15:11:56.135023', 69, '338 PORTA ROSA CIR', NULL, 'SAINT AUGUSTINE', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12219201', NULL, 'PEEBLES, STEVEN W');
INSERT INTO `app_urlresults` VALUES (8322, '2022-12-25 15:11:56.985079', 69, '197 ANTILA WAY', NULL, 'SAINT JOHNS', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12219179', NULL, 'CUSICK, THOMAS STEPHEN JR');
INSERT INTO `app_urlresults` VALUES (8323, '2022-12-25 15:11:57.878019', 69, '123 BRYSON DR', NULL, 'SAINT JOHNS', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12218997', NULL, 'HALL, ANDREW');
INSERT INTO `app_urlresults` VALUES (8324, '2022-12-25 15:11:58.737180', 69, '2050 OAK HAMMOCK DR', NULL, 'PONTE VEDRA BEACH', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32082', '12218881', NULL, 'HALL, ANDREW');
INSERT INTO `app_urlresults` VALUES (8325, '2022-12-25 15:11:59.605945', 69, '54 WILLOW CREEK CT', NULL, 'Saint Augustine', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12217866', NULL, 'HALL, ANDREW');
INSERT INTO `app_urlresults` VALUES (8326, '2022-12-25 15:12:00.461606', 69, '218 HUTCHINSON LN', NULL, 'SAINT AUGUSTINE', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32095', '12217865', NULL, 'HALL, ANDREW');
INSERT INTO `app_urlresults` VALUES (8327, '2022-12-25 15:12:01.358569', 69, '181 BRYBAR DR', NULL, 'SAINT AUGUSTINE', '2022-12-15', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32095', '12219198', NULL, 'BOOTH, ALBERT ERIC');
INSERT INTO `app_urlresults` VALUES (8328, '2022-12-25 15:12:02.222257', 69, '2766 HILLTOP RD', NULL, 'SAINT AUGUSTINE', '2022-12-14', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12218965', NULL, 'SHAFFER, MICHAEL JOHN');
INSERT INTO `app_urlresults` VALUES (8329, '2022-12-25 15:12:03.065436', 69, '551 WINDLEY DR', NULL, 'SAINT AUGUSTINE', '2022-12-14', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218459', NULL, 'SHAFFER, MICHAEL JOHN');
INSERT INTO `app_urlresults` VALUES (8330, '2022-12-25 15:12:03.939106', 69, '3013 1ST ST', NULL, 'SAINT AUGUSTINE', '2022-12-14', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32084', '12219165', NULL, 'UPCHURCH, GLEN DANIEL JR');
INSERT INTO `app_urlresults` VALUES (8331, '2022-12-25 15:12:04.766803', 69, '2836 SHEEPHEAD CT', NULL, 'SAINT AUGUSTINE', '2022-12-14', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12219166', NULL, 'UPCHURCH, GLEN DANIEL JR');
INSERT INTO `app_urlresults` VALUES (8332, '2022-12-25 15:12:05.648540', 69, '83 PICKETT DR', NULL, 'SAINT AUGUSTINE', '2022-12-14', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32084', '12214009', NULL, 'YATES, DANIEL THOMAS');
INSERT INTO `app_urlresults` VALUES (8333, '2022-12-25 15:12:06.522655', 69, '152 GREENWAY LN', NULL, 'SAINT AUGUSTINE', '2022-12-14', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218849', NULL, 'PADGETT II, RONNIE FREEMAN');
INSERT INTO `app_urlresults` VALUES (8334, '2022-12-25 15:12:07.375002', 69, '2790 JOE ASHTON RD', NULL, 'SAINT AUGUSTINE', '2022-12-14', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218753', NULL, 'JOHNSON, CHRISTOPHER S');
INSERT INTO `app_urlresults` VALUES (8335, '2022-12-25 15:12:08.236008', 69, '1042 GARRISON DR', NULL, 'SAINT AUGUSTINE', '2022-12-13', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218978', NULL, 'ALBRIGHT, GREG');
INSERT INTO `app_urlresults` VALUES (8336, '2022-12-25 15:12:09.107094', 69, '165 AUSTIN PARK AVE', NULL, 'PONTE VEDRA', '2022-12-12', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32081', '12218982', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8337, '2022-12-25 15:12:10.399975', 69, '101 VILLAGE DEL LAGO LN', NULL, 'SAINT AUGUSTINE', '2022-12-12', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32080', '12218958', NULL, 'JOYCE, PAUL');
INSERT INTO `app_urlresults` VALUES (8338, '2022-12-25 15:12:11.224598', 69, '403 CROSS RIDGE DR', NULL, 'PONTE VEDRA', '2022-12-12', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32081', '12218920', NULL, 'PEEBLES, STEVEN W');
INSERT INTO `app_urlresults` VALUES (8339, '2022-12-25 15:12:12.089576', 69, '531 ESPACIO LN', NULL, 'SAINT AUGUSTINE', '2022-12-09', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12218972', NULL, 'CIRILLO, JOSEPH');
INSERT INTO `app_urlresults` VALUES (8340, '2022-12-25 15:12:12.937268', 69, '263 MYRTLE OAK CT', NULL, 'SAINT AUGUSTINE', '2022-12-09', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218074', NULL, 'GWINN, WILLIAM B');
INSERT INTO `app_urlresults` VALUES (8341, '2022-12-25 15:12:13.777965', 69, '285 JARAMA CIR', NULL, 'SAINT AUGUSTINE', '2022-12-08', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32084', '12218843', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8342, '2022-12-25 15:12:14.646896', 69, '1145 W KESLEY LN', NULL, 'SAINT JOHNS', '2022-12-08', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12218587', NULL, 'VAUGHT, JARED');
INSERT INTO `app_urlresults` VALUES (8343, '2022-12-25 15:12:15.493082', 69, '707 MONTIANO CIR', NULL, 'SAINT AUGUSTINE', '2022-12-07', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32084', '12218456', NULL, 'PASTERNAK, MICHAEL C');
INSERT INTO `app_urlresults` VALUES (8344, '2022-12-25 15:12:16.413214', 69, '116 CAPTAINS POINTE CIR', NULL, 'SAINT AUGUSTINE', '2022-12-07', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12217657', NULL, 'CHEVALIER, JOSEPH BRYAN');
INSERT INTO `app_urlresults` VALUES (8345, '2022-12-25 15:12:17.271692', 69, '2413 PARK RIDGE DR', NULL, 'SAINT AUGUSTINE', '2022-12-07', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218826', NULL, 'MCKINNEY, CHRISTOPHER R');
INSERT INTO `app_urlresults` VALUES (8346, '2022-12-25 15:12:18.145858', 69, '133 KINGS TRACE DR', NULL, 'SAINT AUGUSTINE', '2022-12-07', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12218824', NULL, 'MCKINNEY, CHRISTOPHER R');
INSERT INTO `app_urlresults` VALUES (8347, '2022-12-25 15:12:19.013393', 69, '208 ARGONAUT RD', NULL, 'SAINT AUGUSTINE', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12218759', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8348, '2022-12-25 15:12:19.863780', 69, '128 BILBAO DR', NULL, 'SAINT AUGUSTINE', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12218757', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8349, '2022-12-25 15:12:20.735724', 69, '102 WINDWALKER DR', NULL, 'SAINT AUGUSTINE', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218756', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8350, '2022-12-25 15:12:21.603194', 69, '119 GREEN TURTLE LN', NULL, 'SAINT AUGUSTINE', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12218452', NULL, 'PADGETT II, RONNIE FREEMAN');
INSERT INTO `app_urlresults` VALUES (8351, '2022-12-25 15:12:22.459832', 69, '1122 LINWOOD LOOP', NULL, 'SAINT JOHNS', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12218235', NULL, 'PADGETT II, RONNIE FREEMAN');
INSERT INTO `app_urlresults` VALUES (8352, '2022-12-25 15:12:23.335250', 69, '64 SEASCAPE CIR', NULL, 'SAINT AUGUSTINE', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32080', '12218762', NULL, 'GALLAGHER, WILLIAM HENRY');
INSERT INTO `app_urlresults` VALUES (8353, '2022-12-25 15:12:24.293392', 69, '137 CALLISTO WAY', NULL, 'Saint Johns', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12218712', NULL, 'BOOTH, ALBERT ERIC');
INSERT INTO `app_urlresults` VALUES (8354, '2022-12-25 15:12:25.218011', 69, '241 HAWTHORNE RD', NULL, 'SAINT AUGUSTINE', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12218429', NULL, 'BOOTH, ALBERT ERIC');
INSERT INTO `app_urlresults` VALUES (8355, '2022-12-25 15:12:26.076026', 69, '126 LIPIZZAN TRL', NULL, 'SAINT AUGUSTINE', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32095', '12218431', NULL, 'BOOTH, ALBERT ERIC');
INSERT INTO `app_urlresults` VALUES (8356, '2022-12-25 15:12:26.940481', 69, '292 S FIELD CREST DR', NULL, 'SAINT AUGUSTINE', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218713', NULL, 'BOOTH, ALBERT ERIC');
INSERT INTO `app_urlresults` VALUES (8357, '2022-12-25 15:12:27.807012', 69, '116 SAND HARBOR DR', NULL, 'PONTE VEDRA', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32081', '12217818', NULL, 'JOHNSON, CHRISTOPHER S');
INSERT INTO `app_urlresults` VALUES (8358, '2022-12-25 15:12:28.659645', 69, '169 GLEN VALLEY DR', NULL, 'PONTE VEDRA', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32081', '12218073', NULL, 'JOHNSON, CHRISTOPHER S');
INSERT INTO `app_urlresults` VALUES (8359, '2022-12-25 15:12:29.545338', 69, '26 ANTILA WAY', NULL, 'SAINT JOHNS', '2022-12-06', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12212822', NULL, 'JOHNSON, CHRISTOPHER S');
INSERT INTO `app_urlresults` VALUES (8360, '2022-12-25 15:12:30.418274', 69, '105 MEADOW CREEK DR', NULL, 'SAINT JOHNS', '2022-12-02', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12218585', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8361, '2022-12-25 15:12:31.360284', 69, '373 GRANT LOGAN DR', NULL, 'Saint Johns', '2022-12-02', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12218529', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8362, '2022-12-25 15:12:32.204469', 69, '308 N LAKE CUNNINGHAM AVE', NULL, 'SAINT JOHNS', '2022-12-02', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12218493', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8363, '2022-12-25 15:12:33.089606', 69, '309 WHITE HORSE WAY', NULL, 'SAINT JOHNS', '2022-12-02', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32259', '12217999', NULL, 'CHRISTENSEN, CAMERON');
INSERT INTO `app_urlresults` VALUES (8364, '2022-12-25 15:12:33.935047', 69, '239 LA MANCHA DR', NULL, 'SAINT AUGUSTINE', '2022-12-02', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12218584', NULL, 'WHITE, GARY YOUNG');
INSERT INTO `app_urlresults` VALUES (8365, '2022-12-25 15:12:34.812286', 69, '802 HUFFNER HILL CIR', NULL, 'SAINT AUGUSTINE', '2022-12-01', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12216229', NULL, 'BERRY, EDWARD SCOTT');
INSERT INTO `app_urlresults` VALUES (8366, '2022-12-25 15:12:35.651679', 69, '270 SAWMILL LANDING DR', NULL, 'SAINT AUGUSTINE', '2022-12-01', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12216222', NULL, 'BERRY, EDWARD SCOTT');
INSERT INTO `app_urlresults` VALUES (8367, '2022-12-25 15:12:36.517893', 69, '496 OCEAN JASPER DR', NULL, 'SAINT AUGUSTINE', '2022-12-01', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12216223', NULL, 'BERRY, EDWARD SCOTT');
INSERT INTO `app_urlresults` VALUES (8368, '2022-12-25 15:12:37.409366', 69, '108 BARBAROSA ST', NULL, 'SAINT AUGUSTINE', '2022-12-01', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32086', '12216703', NULL, 'BERRY, EDWARD SCOTT');
INSERT INTO `app_urlresults` VALUES (8369, '2022-12-25 15:12:38.253508', 69, '3000 FORT CAROLINE CT', NULL, 'SAINT AUGUSTINE', '2022-12-01', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218217', NULL, 'PASTERNAK, MICHAEL C');
INSERT INTO `app_urlresults` VALUES (8370, '2022-12-25 15:12:39.114722', 69, '522 WILLOW LAKE DR', NULL, 'SAINT AUGUSTINE', '2022-12-01', NULL, NULL, NULL, NULL, NULL, NULL, 'FL', NULL, NULL, NULL, '32092', '12218215', NULL, 'PASTERNAK, MICHAEL C');
INSERT INTO `app_urlresults` VALUES (8371, '2022-12-25 15:16:12.249357', 70, '2038 ANGELICO CI', NULL, NULL, '2022-12-23', NULL, NULL, NULL, NULL, '', NULL, NULL, 'Applied', NULL, NULL, NULL, 'BP22-10014.REV01', NULL, NULL);
INSERT INTO `app_urlresults` VALUES (8372, '2022-12-25 15:16:52.070568', 70, '3419 W SWAIN RD', NULL, NULL, '2022-12-22', NULL, NULL, NULL, NULL, '', NULL, NULL, 'Applied', NULL, NULL, NULL, 'BP22-11861', NULL, NULL);
INSERT INTO `app_urlresults` VALUES (8373, '2022-12-25 15:17:06.461527', 70, '2808 SEA BIRD WY', NULL, NULL, '2022-12-22', NULL, NULL, NULL, NULL, '', NULL, NULL, 'Applied', NULL, NULL, NULL, 'BP22-10289.REV01', NULL, NULL);
INSERT INTO `app_urlresults` VALUES (8374, '2022-12-25 15:17:39.594437', 70, '10308 CREEK TRAIL CI', NULL, NULL, '2022-12-22', NULL, NULL, NULL, NULL, '', NULL, NULL, 'Issued', NULL, NULL, NULL, 'BP22-11851', NULL, NULL);
INSERT INTO `app_urlresults` VALUES (8375, '2022-12-25 15:19:53.155032', 71, '1400 Bear Gulch RD *\nWoodside', NULL, NULL, '2022-12-22', 'Application for 30 panel PV system to be installed at two roof locations on existing Dwelling. Total system AC rating is 9.75kW. System is using microinverters. Attached is one PDF with all documentation including manufacturer specifications “It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.”', NULL, NULL, NULL, NULL, NULL, NULL, 'In Review', NULL, NULL, NULL, 'BLD2022-03005', NULL, 'Richard Halvorsen');
INSERT INTO `app_urlresults` VALUES (8376, '2022-12-25 15:20:01.694948', 71, '544 Sunset WAY *\nEmerald Hills', NULL, NULL, '2022-12-21', '3.1KW PV(8)MODULE ROOFTOP MOUNT INSTALLATION, REPLACE EXISTING 200A MAIN PANEL WITH NEW 200A MAIN PANEL WITH 175A MAIN BREAKER WITH 225A BUSBAR. EXISTING SOLAR SYSTEM INSTALLED. “It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.”', NULL, NULL, NULL, NULL, NULL, NULL, 'In Review', NULL, NULL, NULL, 'BLD2022-02994', NULL, 'GILBERT CORREIA');
INSERT INTO `app_urlresults` VALUES (8377, '2022-12-25 15:20:10.877049', 71, '3852 Jefferson AVE *\nEmerald Hills', NULL, NULL, '2022-12-20', '10.1KW PV(26)MODULE ROOFTOP MOUNT INSTALLATION “It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.”', NULL, NULL, NULL, NULL, NULL, NULL, 'In Review', NULL, NULL, NULL, 'BLD2022-02988', NULL, 'GILBERT CORREIA');
INSERT INTO `app_urlresults` VALUES (8378, '2022-12-25 15:20:21.195122', 71, '2737 BLENHEIM AVE *\nREDWOOD CITY', NULL, NULL, '2022-12-19', 'Installing roof mount solar PV 4.74 kW 12 mods “It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.”', NULL, NULL, NULL, NULL, NULL, NULL, 'In Review', NULL, NULL, NULL, 'BLD2022-02970', NULL, 'Nexus Energy Systems');
INSERT INTO `app_urlresults` VALUES (8379, '2022-12-25 15:20:27.920871', 71, '2111 QUEENS LN *\nSAN MATEO HIGHLANDS', NULL, NULL, '2022-12-19', 'Installation of 12.71kW Solar system with 31 REC410 panels and IQ8A micro inverters *It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.*', NULL, NULL, NULL, NULL, NULL, NULL, 'In Review', NULL, NULL, NULL, 'BLD2022-02966', NULL, 'Jeff Long');
INSERT INTO `app_urlresults` VALUES (8380, '2022-12-25 15:20:45.829322', 71, '60 INYO PL *\nREDWOOD CITY', NULL, NULL, '2022-12-19', 'SYSTEM SIZE: 10530W DC, 7600W AC • MODULES: (27) JA SOLAR: JAM54S31-390/MR • INVERTERS: (1) SOLAREDGE TECHNOLOGIES: SE7600H-USSN • RACKING: ULTRA RAIL SPEEDSEAL FOOT, SEE DRAWING SNR-DC-00438 • ENERGY STORAGE SYSTEM: (2) TESLA: POWERWALL, 13.5KWh, 5KW INVERTER OUTPUT, LITHIUM-ION BATTERY (WEIGHT: 251.3LB EACH) • MAIN PANEL UPGRADE: EXISTING 100 AMP MAIN PANEL WITH 100 AMP MAIN BREAKER TO BE REPLACED WITH NEW 200 AMP MAIN PANEL WITH 225 AMP BUSBAR AND 200 AMP MAIN BREAKER. • BACKUP GATEWAY: (1) 200A TESLA POWERWALL CONTROL PANEL *It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.*', NULL, NULL, NULL, NULL, NULL, NULL, 'In Review', NULL, NULL, NULL, 'BLD2022-02971', NULL, 'daniel strobel');
INSERT INTO `app_urlresults` VALUES (8381, '2022-12-25 15:21:02.432037', 71, '524 SUNSET WAY *\nEMERALD LAKE HILLS', NULL, NULL, '2022-12-16', 'New MSP 200 amps', NULL, NULL, NULL, NULL, NULL, NULL, 'Issued', NULL, NULL, NULL, 'BLD2022-02956', NULL, 'Maria Harb');
INSERT INTO `app_urlresults` VALUES (8382, '2022-12-25 15:21:57.820085', 71, '471 CORTEZ AVE *\nMIRAMAR', NULL, NULL, '2022-12-14', '(2) AC COUPLED BATTERY INSTALLATION 5.0 kW (MAX CONTINUOUS), 7.0kW (PEAK), 13.5 kWH *It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.*', NULL, NULL, NULL, NULL, NULL, NULL, 'Incomplete', NULL, NULL, NULL, 'BLD2022-02934', NULL, 'Josue Gutierrez');
INSERT INTO `app_urlresults` VALUES (8383, '2022-12-25 15:22:09.016983', 71, '196 NOTTINGHAM AVE *\nREDWOOD CITY', NULL, NULL, '2022-12-14', 'Rooftop PV Solar installation, 4550W DC (3.8 kW), *It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.*', NULL, NULL, NULL, NULL, NULL, NULL, 'In Review', NULL, NULL, NULL, 'BLD2022-02938', NULL, 'brandy hunter');
INSERT INTO `app_urlresults` VALUES (8384, '2022-12-25 15:22:14.960790', 71, '621 HILLCREST WAY *\nEMERALD LAKE HILLS', NULL, NULL, '2022-12-14', 'Residential ESS System 10kW Tesla battery system including Gateway, 2 PowerWalls and backup loads subpanel. *It is the permittee’s obligation and responsibility to ensure that all work associated with this Permit complies with all current Orders of the Health Officer of the County of San Mateo related to the Novel Coronavirus Disease 2019 (COVID-19). The County of San Mateo assumes no responsibility for work performed by permittee that is not in compliance with all current Orders.*', NULL, NULL, NULL, NULL, NULL, NULL, 'In Review', NULL, NULL, NULL, 'BLD2022-02941', NULL, 'Marina Zierk');

-- ----------------------------
-- Table structure for app_urls
-- ----------------------------
DROP TABLE IF EXISTS `app_urls`;
CREATE TABLE `app_urls`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `url` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `date_created` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of app_urls
-- ----------------------------
INSERT INTO `app_urls` VALUES (1, 'https://aca-prod.accela.com/ONE/Cap/CapHome.aspx?module=Building&TabName=Building', 'Reno NV', '2022-12-03 09:27:11.072991', 1);
INSERT INTO `app_urls` VALUES (2, 'https://aca-prod.accela.com/SANDIEGO/Cap/CapHome.aspx?module=DSD&TabName=DSD&TabList=Home', 'San Diego', '2022-12-03 13:27:30.602765', 1);
INSERT INTO `app_urls` VALUES (3, 'https://aca-prod.accela.com/PASCO/Cap/CapHome.aspx?module=Building&TabName=Building', 'Pasco County', '2022-12-03 14:44:00.022988', 1);
INSERT INTO `app_urls` VALUES (4, 'https://aca-prod.accela.com/LEXKY/Cap/CapHome.aspx?module=Building&TabName=Building', 'Lexington Ky', '2022-12-03 19:48:22.119323', 1);
INSERT INTO `app_urls` VALUES (5, 'https://aca-prod.accela.com/LJCMG/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Louisville Ky', '2022-12-05 06:10:59.060214', 1);
INSERT INTO `app_urls` VALUES (6, 'https://aca-prod.accela.com/CHESTERFIELD/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Chesterfield County', '2022-12-05 06:39:13.588805', 1);
INSERT INTO `app_urls` VALUES (7, 'https://aca-prod.accela.com/CHESAPEAKE/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Jacksonville County', '2022-12-05 06:45:29.930573', 1);
INSERT INTO `app_urls` VALUES (8, 'https://aca-prod.accela.com/LEONCO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Tallahassee', '2022-12-05 06:47:47.152163', 1);
INSERT INTO `app_urls` VALUES (9, 'https://aca-prod.accela.com/FTL/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Fort Lauderdale', '2022-12-05 06:57:19.943218', 1);
INSERT INTO `app_urls` VALUES (10, 'https://aca.plantation.org/CitizenAccess/default.aspx', 'Plantation FL', '2022-12-05 07:01:32.788296', 0);
INSERT INTO `app_urls` VALUES (11, 'https://aca-prod.accela.com/PINELLAS/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Pinellas County', '2022-12-05 07:16:16.510099', 1);
INSERT INTO `app_urls` VALUES (12, 'https://accela-aca.fcgov.com/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'FT Collins', '2022-12-05 07:33:15.939945', 1);
INSERT INTO `app_urls` VALUES (13, 'https://aca-prod.accela.com/PALOALTO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Palo Alto', '2022-12-06 02:37:22.004744', 1);
INSERT INTO `app_urls` VALUES (14, 'https://citizenportal.slcgov.com/Citizen/Cap/CapHome.aspx?module=Building&TabName=Building', 'SLC', '2022-12-06 08:29:05.871919', 1);
INSERT INTO `app_urls` VALUES (15, 'https://lmsaca.fresno.gov/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building', 'Fresno', '2022-12-06 12:58:42.968408', 1);
INSERT INTO `app_urls` VALUES (16, 'https://aca-prod.accela.com/CLARKCO/Cap/CapHome.aspx?module=Building&TabName=Building', 'Las Vegas', '2022-12-07 06:41:02.090743', 1);
INSERT INTO `app_urls` VALUES (17, 'https://aca-prod.accela.com/MONTEREY/Cap/CapHome.aspx?module=Building&TabName=Building', 'Monterey', '2022-12-07 11:34:16.279431', 1);
INSERT INTO `app_urls` VALUES (18, 'https://aca-prod.accela.com/ALAMEDA/Cap/CapHome.aspx?module=Building&TabName=Building', 'Alameda', '2022-12-08 11:03:19.605679', 1);
INSERT INTO `app_urls` VALUES (19, 'https://ca.columbus.gov/ca/Cap/CapHome.aspx?module=Building&TabName=Building', 'Columbus', '2022-12-08 14:56:40.075105', 1);
INSERT INTO `app_urls` VALUES (20, 'https://aca-prod.accela.com/MENIFEE/Cap/CapHome.aspx?module=Permits&TabName=Permits&TabList=Home', 'Menifee', '2022-12-09 04:00:08.441204', 1);
INSERT INTO `app_urls` VALUES (21, 'https://aca-prod.accela.com/SACRAMENTO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Sacramento', '2022-12-09 08:01:40.301805', 1);
INSERT INTO `app_urls` VALUES (22, 'https://epermits.cccounty.us/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building', 'Contra Costa County', '2022-12-09 08:20:18.621643', 1);
INSERT INTO `app_urls` VALUES (23, 'https://aca.cityofberkeley.info/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Berkley CA', '2022-12-09 11:35:18.161247', 0);
INSERT INTO `app_urls` VALUES (24, 'https://epermit.myclearwater.com/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Clearwater FL', '2022-12-09 11:48:02.314568', 1);
INSERT INTO `app_urls` VALUES (25, 'https://aca-prod.accela.com/BERNCO/Cap/CapHome.aspx?module=Building&TabName=Building&TabList=Home', 'Bernalillo County NM', '2022-12-09 11:54:59.920019', 1);
INSERT INTO `app_urls` VALUES (26, 'https://citizenportal.meridiancity.org/CitizenAccess/Cap/CapHome.aspx?module=Dev-Services&TabName=Dev-Services', 'Meridian', '2022-12-11 04:02:36.630470', 1);
INSERT INTO `app_urls` VALUES (27, 'https://aca-prod.accela.com/TOS/Cap/CapHome.aspx?module=Building&TabName=Building', 'Sahuarita AZ', '2022-12-11 17:23:08.000000', 1);
INSERT INTO `app_urls` VALUES (28, 'https://aca-prod.accela.com/QC/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Queen Creek AZ', '2022-12-11 17:40:24.000000', 1);
INSERT INTO `app_urls` VALUES (29, 'https://permits.cityofboise.org/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Boise ID', '2022-12-11 22:05:54.000000', 1);
INSERT INTO `app_urls` VALUES (30, 'https://citizenaccess.arapahoegov.com/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Arapahoe County CO', '2022-12-11 23:03:04.000000', 1);
INSERT INTO `app_urls` VALUES (31, 'https://accela.maricopa.gov/CitizenAccessMCOSS/Cap/CapHome.aspx?module=PnD&TabName=PnD', 'Maricopa County', '2022-12-13 11:41:35.000000', 1);
INSERT INTO `app_urls` VALUES (32, 'https://aca-prod.accela.com/OAKLAND/Cap/CapHome.aspx?module=Building&TabName=Home', 'Oakland CA', '2022-12-13 13:28:40.000000', 1);
INSERT INTO `app_urls` VALUES (33, 'https://permits.adcogov.org/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building&TabList=HOME%7C0%7CBuilding%7C1%7CPlanning%7C2%7CPermits%7C3%7CEnforcement%7C4%7CContractors%7C5%7CCurrentTabIndex%7C1', 'Denver CO', '2022-12-13 13:54:57.000000', 1);
INSERT INTO `app_urls` VALUES (34, 'https://eportal.galvestontx.gov/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'GALVESTION TX', '2022-12-13 15:18:59.000000', 1);
INSERT INTO `app_urls` VALUES (35, 'https://aca.cityofchino.org/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building', 'Chino CA', '2022-12-15 16:32:35.000000', 1);
INSERT INTO `app_urls` VALUES (36, 'https://aca-prod.accela.com/MANATEE/Cap/CapHome.aspx?module=Building&TabName=Building', 'Manatee', '2022-12-15 21:44:34.000000', 1);
INSERT INTO `app_urls` VALUES (37, 'https://plus.fairfaxcounty.gov/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building&TabList=Home', 'Fairfax County', '2022-12-15 23:28:42.000000', 1);
INSERT INTO `app_urls` VALUES (38, 'https://aca.sanantonio.gov/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building&TabList=Home%7C0%7CLandDevelopment%7C1%7CBuilding%7C2%7CFire%7C3%7CCurrentTabIndex%7C2', 'San Antonio', '2022-12-16 23:00:48.000000', 1);
INSERT INTO `app_urls` VALUES (39, 'https://aca-prod.accela.com/ATLANTA_GA/Cap/CapHome.aspx?module=Building&TabName=Building', 'Atlanta GA', '2022-12-16 23:52:46.000000', 1);
INSERT INTO `app_urls` VALUES (40, 'https://aca-prod.accela.com/DELAND/Cap/CapHome.aspx?module=Building&TabName=Home', 'Deland FL', '2022-12-17 00:10:46.000000', 1);
INSERT INTO `app_urls` VALUES (41, 'https://aca-prod.accela.com/TAMPA/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Tampa FL', '2022-12-17 00:44:37.000000', 1);
INSERT INTO `app_urls` VALUES (42, 'https://cd.visalia.city/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Vicelia', '2022-12-17 07:27:27.000000', 1);
INSERT INTO `app_urls` VALUES (43, 'https://aca-prod.accela.com/ONE/Cap/CapHome.aspx?module=Building&TabName=Building', 'Washoe NV', '2022-12-17 17:48:51.000000', 1);
INSERT INTO `app_urls` VALUES (44, 'https://aca-prod.accela.com//Lancaster/Cap/CapHome.aspx?module=Permits', 'Lancaster CA', '2022-12-17 20:04:16.000000', 1);
INSERT INTO `app_urls` VALUES (45, 'https://aca-prod.accela.com/POLKCO/Cap/CapHome.aspx?module=Building&TabName=Building', 'Polk County FL', '2022-12-17 20:33:59.000000', 1);
INSERT INTO `app_urls` VALUES (46, 'https://secureapps.charlottecountyfl.gov/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building', 'Charlotte County FL', '2022-12-17 21:44:49.000000', 1);
INSERT INTO `app_urls` VALUES (47, 'https://aca-prod.accela.com/HCFL/Cap/GlobalSearchResults.aspx?QueryText=solar#CAPList', 'Hillsborough County FL', '2022-12-17 22:04:15.000000', 1);
INSERT INTO `app_urls` VALUES (48, 'https://epermit.myclearwater.com/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Clearwater FL (2)', '2022-12-17 22:14:04.000000', 1);
INSERT INTO `app_urls` VALUES (49, 'https://aca-prod.accela.com/WESTON/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Weston FL', '2022-12-17 22:21:48.000000', 1);
INSERT INTO `app_urls` VALUES (50, 'https://aca-prod.accela.com/PHARR/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Pharr TX', '2022-12-17 22:28:31.000000', 1);
INSERT INTO `app_urls` VALUES (51, 'https://epicla.lacounty.gov/energov_prod/SelfService/#/search?m=1&fm=2&ps=100&pn=1&em=true&st=solar', 'Los Angeles County', '2022-12-20 16:54:45.000000', 1);
INSERT INTO `app_urls` VALUES (52, 'https://aca-prod.accela.com/CONCORD/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Concord CA', '2022-12-20 20:37:01.000000', 1);
INSERT INTO `app_urls` VALUES (53, 'https://citizen.srcity.org/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Santa Rosa CA', '2022-12-20 21:00:08.000000', 1);
INSERT INTO `app_urls` VALUES (54, 'https://aca-prod.accela.com/PIMA/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Pima County AZ', '2022-12-20 21:07:53.000000', 1);
INSERT INTO `app_urls` VALUES (55, 'https://aca-prod.accela.com/LAKECO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Lake County CA', '2022-12-20 21:36:57.000000', 1);
INSERT INTO `app_urls` VALUES (56, 'https://permitsonline.roseville.ca.us/OPS/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Roseville CA', '2022-12-20 21:56:10.000000', 1);
INSERT INTO `app_urls` VALUES (57, 'https://permits.mynevadacounty.com/CitizenAccess/Cap/CapHome.aspx?module=Building', 'Nevada County CA', '2022-12-20 22:24:20.000000', 0);
INSERT INTO `app_urls` VALUES (58, 'https://deltonafl-energovweb.tylerhost.net/apps/SelfService#/search?m=1&fm=2&ps=100&pn=1&em=true&st=solar', 'Deltona FL', '2022-12-21 21:14:17.000000', 1);
INSERT INTO `app_urls` VALUES (59, 'https://energovweb.sugarlandtx.gov/EnerGov_prod/SelfService#/search?m=1&fm=2&ps=100&pn=1&em=true&st=solar', 'Sugarland TX', '2022-12-21 21:41:18.000000', 1);
INSERT INTO `app_urls` VALUES (60, 'https://aca-prod.accela.com/CVB/Cap/GlobalSearchResults.aspx?QueryText=solar#', 'VA BEACH GENERAL', '2022-12-21 21:59:34.000000', 1);
INSERT INTO `app_urls` VALUES (61, 'https://accela.co.kern.ca.us/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Home', 'Kern County CA', '2022-12-21 23:08:38.000000', 1);
INSERT INTO `app_urls` VALUES (62, 'https://aca-prod.accela.com/SHELBYCO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Memphis TN', '2022-12-23 12:42:34.000000', 1);
INSERT INTO `app_urls` VALUES (63, 'https://stluciecountyfl-energovpub.tylerhost.net/Apps/SelfService#/search?m=1&fm=2&ps=100&pn=1&em=true&st=solar', 'Port st lucie FL', '2022-12-23 13:32:06.000000', 1);
INSERT INTO `app_urls` VALUES (64, 'https://aca.longmontcolorado.gov/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Longmont CO', '2022-12-23 14:34:25.000000', 1);
INSERT INTO `app_urls` VALUES (65, 'https://aca.longmontcolorado.gov/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building&TabList=Home%7C0%7CBuilding%7C1%7CEnforcement%7C2%7CLicenses%7C3%7CPlanning%7C4%7CPublicWorks%7C5%7CCurrentTabIndex%7C1', 'Longmont CO (2)', '2022-12-23 15:28:02.000000', 1);
INSERT INTO `app_urls` VALUES (66, 'https://cvportal.provo.org/CityViewPortal/Permit/Locator', 'Provo UT', '2022-12-23 22:00:57.000000', 1);
INSERT INTO `app_urls` VALUES (67, 'https://portal.iworq.net/LEHI/permits/602?search=solar&field=text5', 'Lehi UT', '2022-12-23 23:34:26.000000', 1);
INSERT INTO `app_urls` VALUES (68, 'https://energovweb.kissimmee.gov/EnerGov_Prod/SelfService#/search?m=1&fm=2&ps=100&pn=1&em=true&st=solar', 'Kissimmee FL ', '2022-12-23 23:53:32.000000', 1);
INSERT INTO `app_urls` VALUES (69, 'http://webapp.sjcfl.us/Applications/WATSWebX/Permit/SearchResults.aspx?PermitType=1&PermitNo=&Clrsht=&Parcel=&Addr=&ProjNm=&CLNm=&CLId=&SepticNo=&Lgl1=&Lgl2=&Lgl3=&PU=670&FromDt=&ToDt=&PP=False&Sort=&SortOrder=', 'Saint Augistine County', '2022-12-24 09:29:53.000000', 1);
INSERT INTO `app_urls` VALUES (70, 'https://aca-prod.accela.com/STOCKTON/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Stockton CA', '2022-12-25 21:36:51.000000', 1);
INSERT INTO `app_urls` VALUES (71, 'https://aca-prod.accela.com/SMCGOV/Cap/GlobalSearchResults.aspx?QueryText=solar', 'San Mateo CA', '2022-12-25 22:04:09.000000', 1);

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add urls', 7, 'add_urls');
INSERT INTO `auth_permission` VALUES (26, 'Can change urls', 7, 'change_urls');
INSERT INTO `auth_permission` VALUES (27, 'Can delete urls', 7, 'delete_urls');
INSERT INTO `auth_permission` VALUES (28, 'Can view urls', 7, 'view_urls');
INSERT INTO `auth_permission` VALUES (29, 'Can add url results', 8, 'add_urlresults');
INSERT INTO `auth_permission` VALUES (30, 'Can change url results', 8, 'change_urlresults');
INSERT INTO `auth_permission` VALUES (31, 'Can delete url results', 8, 'delete_urlresults');
INSERT INTO `auth_permission` VALUES (32, 'Can view url results', 8, 'view_urlresults');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (8, 'app', 'urlresults');
INSERT INTO `django_content_type` VALUES (7, 'app', 'urls');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2022-12-15 08:30:24.824244');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2022-12-15 08:30:25.070210');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2022-12-15 08:30:25.188906');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2022-12-15 08:30:25.194914');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2022-12-15 08:30:25.199455');
INSERT INTO `django_migrations` VALUES (6, 'app', '0001_initial', '2022-12-15 08:30:25.289617');
INSERT INTO `django_migrations` VALUES (7, 'app', '0002_urlresults_remove_results_date_created', '2022-12-15 08:30:25.305639');
INSERT INTO `django_migrations` VALUES (8, 'app', '0003_urlresultsvalue_urlresults_url_delete_results_and_more', '2022-12-15 08:30:25.389282');
INSERT INTO `django_migrations` VALUES (9, 'app', '0004_urlresults_address_urlresults_applicant_and_more', '2022-12-15 08:30:25.565361');
INSERT INTO `django_migrations` VALUES (10, 'app', '0005_remove_urlresultsvalue_attribute_and_more', '2022-12-15 08:30:25.630471');
INSERT INTO `django_migrations` VALUES (11, 'app', '0006_urlresults_record_id', '2022-12-15 08:30:25.640986');
INSERT INTO `django_migrations` VALUES (12, 'app', '0007_alter_urlresults_date', '2022-12-15 08:30:25.687080');
INSERT INTO `django_migrations` VALUES (13, 'app', '0008_urls_is_active', '2022-12-15 08:30:25.704620');
INSERT INTO `django_migrations` VALUES (14, 'app', '0009_alter_urlresults_address_alter_urlresults_applicant_and_more', '2022-12-15 08:30:26.056298');
INSERT INTO `django_migrations` VALUES (15, 'app', '0010_urlresults_owner', '2022-12-15 08:30:26.065834');
INSERT INTO `django_migrations` VALUES (16, 'contenttypes', '0002_remove_content_type_name', '2022-12-15 08:30:26.107429');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0002_alter_permission_name_max_length', '2022-12-15 08:30:26.136976');
INSERT INTO `django_migrations` VALUES (18, 'auth', '0003_alter_user_email_max_length', '2022-12-15 08:30:26.153004');
INSERT INTO `django_migrations` VALUES (19, 'auth', '0004_alter_user_username_opts', '2022-12-15 08:30:26.158509');
INSERT INTO `django_migrations` VALUES (20, 'auth', '0005_alter_user_last_login_null', '2022-12-15 08:30:26.190065');
INSERT INTO `django_migrations` VALUES (21, 'auth', '0006_require_contenttypes_0002', '2022-12-15 08:30:26.192068');
INSERT INTO `django_migrations` VALUES (22, 'auth', '0007_alter_validators_add_error_messages', '2022-12-15 08:30:26.197072');
INSERT INTO `django_migrations` VALUES (23, 'auth', '0008_alter_user_username_max_length', '2022-12-15 08:30:26.231641');
INSERT INTO `django_migrations` VALUES (24, 'auth', '0009_alter_user_last_name_max_length', '2022-12-15 08:30:26.263185');
INSERT INTO `django_migrations` VALUES (25, 'auth', '0010_alter_group_name_max_length', '2022-12-15 08:30:26.275706');
INSERT INTO `django_migrations` VALUES (26, 'auth', '0011_update_proxy_permissions', '2022-12-15 08:30:26.281214');
INSERT INTO `django_migrations` VALUES (27, 'auth', '0012_alter_user_first_name_max_length', '2022-12-15 08:30:26.313271');
INSERT INTO `django_migrations` VALUES (28, 'sessions', '0001_initial', '2022-12-15 08:30:26.333303');
INSERT INTO `django_migrations` VALUES (29, 'app', '0011_urlresults_contractor', '2022-12-23 15:17:05.232538');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_session
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
