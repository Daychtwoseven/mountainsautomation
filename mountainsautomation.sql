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

 Date: 06/01/2023 01:20:58
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
) ENGINE = InnoDB AUTO_INCREMENT = 13677 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of app_urlresults
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 117 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
INSERT INTO `app_urls` VALUES (72, 'https://co-franklin-oh.smartgovcommunity.com/ApplicationPublic/ApplicationSearch?query=solar&__submitFormValidator__=a1671vih748761000t&_conv=1', 'Franklin County OH', '2022-12-26 10:30:10.000000', 1);
INSERT INTO `app_urls` VALUES (73, 'https://rivcoplus.org/EnerGov_Prod/SelfService#/search?m=1&fm=2&ps=100&pn=2&em=false&st=Solar%20Roof%20Mount', 'Riverside County CA', '2022-12-26 11:13:54.000000', 1);
INSERT INTO `app_urls` VALUES (74, 'https://palmscss.tularecounty.ca.gov/EnerGov_Prod/SelfService#/search?m=1&fm=2&ps=100&pn=2&em=true&st=solar', 'Tulare County CA', '2022-12-26 11:24:45.000000', 1);
INSERT INTO `app_urls` VALUES (75, 'https://build.henrico.us/henprod/pub/lms/Default.aspx?PossePresentation=PermitSearchByContractor', 'Henrico County VA', '2022-12-26 21:08:37.000000', 1);
INSERT INTO `app_urls` VALUES (76, 'https://aca-prod.accela.com/MOVAL/Cap/CapHome.aspx?module=Building&TabName=Building&TabList=Home%7C0%7CBuilding%7C1%7CCode%7C2%7CFire%7C3%7CLandDevelopment%7C4%7CPlanning%7C5%7CSpecialDist%7C6%7CTransportation%7C7%7CCurrentTabIndex%7C1', 'Moreno Vally CA', '2022-12-26 21:48:30.000000', 1);
INSERT INTO `app_urls` VALUES (77, 'https://aca-prod.accela.com/RICHMOND/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Richmond KY', '2022-12-26 23:01:56.000000', 1);
INSERT INTO `app_urls` VALUES (78, 'https://haywardca-energovpub.tylerhost.net/Apps/SelfService#/search?m=1&fm=2&ps=100&pn=1&em=true&st=solar', 'Hayward County CA', '2022-12-26 23:22:03.000000', 1);
INSERT INTO `app_urls` VALUES (79, 'https://energovcss.miamibeachfl.gov/energovprod/selfservice#/search?m=1&fm=2&ps=100&pn=1&em=true&st=solar', 'Miami Beach FL', '2022-12-26 23:41:36.000000', 1);
INSERT INTO `app_urls` VALUES (80, 'https://acaweb.brevardcounty.us/CitizenAccess/Cap/GlobalSearchResults.aspx?QueryText=solar#', 'Brevard County FL', '2022-12-27 21:48:40.000000', 1);
INSERT INTO `app_urls` VALUES (81, 'https://permits.daytonohio.gov/Permits/Cap/CapHome.aspx?module=Building&TabName=Building', 'Dayton OH', '2022-12-27 22:06:07.000000', 1);
INSERT INTO `app_urls` VALUES (82, 'https://c.lakecountyfl.gov/offices/building_services/permit_activity_reports/permits_issued_by_type.aspx?mylakefl=true', 'Lake County FL', '2022-12-27 22:41:56.000000', 1);
INSERT INTO `app_urls` VALUES (83, 'https://fasttrack.ocfl.net/OnlineServices/permit-building.aspx', 'Orange County FL', '2022-12-28 15:28:09.000000', 1);
INSERT INTO `app_urls` VALUES (84, 'https://dbiweb02.sfgov.org/dbipts/Default2.aspx?page=KeywordSearch', 'San Fran CA', '2022-12-28 19:53:55.000000', 1);
INSERT INTO `app_urls` VALUES (85, 'https://ims.palmbayflorida.org/ims/Find3/Results?cat=Permits', 'Palm Bay FL', '2022-12-28 22:52:40.000000', 0);
INSERT INTO `app_urls` VALUES (86, 'https://accela.fortworthtexas.gov/CitizenAccess/Cap/CapHome.aspx?module=Development&TabName=Development', 'Forth Worth TX', '2022-12-29 22:50:33.000000', 1);
INSERT INTO `app_urls` VALUES (87, 'https://aca-prod.accela.com/HUMBOLDT/Cap/GlobalSearchResults.aspx?QueryText=Photovoltaic', ' Humboldt County CA', '2022-12-31 15:09:16.000000', 1);
INSERT INTO `app_urls` VALUES (88, 'https://aca-prod.accela.com/ARLINGTONCO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Arlington VA ', '2022-12-31 23:16:24.000000', 1);
INSERT INTO `app_urls` VALUES (89, 'https://aca-prod.accela.com/CORTE/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Corte County CA', '2022-12-31 23:32:03.000000', 1);
INSERT INTO `app_urls` VALUES (90, 'https://aca-prod.accela.com/CRYSTALLAKE/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Crystal Lake IL', '2022-12-31 23:38:04.000000', 1);
INSERT INTO `app_urls` VALUES (91, 'https://aca-prod.accela.com/CUPERTINO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Cuoertino CA', '2022-12-31 23:53:42.000000', 1);
INSERT INTO `app_urls` VALUES (92, 'https://aca-prod.accela.com/DUBLINOH/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Dublin OH', '2023-01-01 00:33:05.000000', 1);
INSERT INTO `app_urls` VALUES (93, 'https://aca-prod.accela.com/EVANSTON/Cap/CapHome.aspx?module=Building&TabName=Building', 'Evanston IL', '2023-01-01 00:39:01.000000', 1);
INSERT INTO `app_urls` VALUES (94, 'https://aca-prod.accela.com/FAIRFAX/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Fairfax VA', '2023-01-01 02:04:12.000000', 1);
INSERT INTO `app_urls` VALUES (95, 'https://aca-prod.accela.com/GRASSVALLEY/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Grass Valley CA', '2023-01-01 11:48:41.000000', 1);
INSERT INTO `app_urls` VALUES (96, 'https://aca-prod.accela.com/JURUPA/Cap/CapHome.aspx?module=Building&TabName=Building', 'Jurupa Valley CA', '2023-01-01 12:03:59.000000', 1);
INSERT INTO `app_urls` VALUES (97, 'https://aca-prod.accela.com/KETTERING/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Kettering OH', '2023-01-01 12:09:46.000000', 1);
INSERT INTO `app_urls` VALUES (98, 'https://aca-prod.accela.com/LAKECO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Lake CA', '2023-01-01 12:19:57.000000', 1);
INSERT INTO `app_urls` VALUES (99, 'https://aca-oregon.accela.com/oregon/Cap/CapHome.aspx?module=Building&TabName=Building', 'Oregon', '2023-01-01 13:22:34.000000', 1);
INSERT INTO `app_urls` VALUES (100, 'https://aca-prod.accela.com/PARADISEVLY/Cap/GlobalSearchResults.aspx?QueryText=solar', 'PARADISE VALLEY AZ', '2023-01-01 13:36:29.000000', 1);
INSERT INTO `app_urls` VALUES (101, 'https://aca-prod.accela.com/PRCITY/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Paso CA', '2023-01-01 14:21:00.000000', 1);
INSERT INTO `app_urls` VALUES (102, 'https://aca-prod.accela.com/PHARR/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Pharr TX', '2023-01-01 14:49:38.000000', 1);
INSERT INTO `app_urls` VALUES (103, 'https://aca-prod.accela.com/SOMERTON/Cap/GlobalSearchResults.aspx?QueryText=solar#', 'Somerton AZ', '2023-01-01 17:59:55.000000', 1);
INSERT INTO `app_urls` VALUES (104, 'https://aca-prod.accela.com/WC/Cap/GlobalSearchResults.aspx?QueryText=solar#', 'Walnut Creek CA', '2023-01-01 18:23:51.000000', 1);
INSERT INTO `app_urls` VALUES (105, 'https://aca-prod.accela.com/YORBALINDA/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Yorba linda CA', '2023-01-01 23:31:12.000000', 1);
INSERT INTO `app_urls` VALUES (106, 'https://aca-prod.accela.com/YUBA/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Yuba City CA', '2023-01-01 23:37:28.000000', 1);
INSERT INTO `app_urls` VALUES (107, 'https://aca-prod.accela.com/TLG/Cap/CapHome.aspx?module=Building&TabName=Building', 'Los Gatos CA', '2023-01-02 16:36:11.000000', 1);
INSERT INTO `app_urls` VALUES (108, 'https://aca-prod.accela.com/SBCO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Santa Barbara CA', '2023-01-02 18:16:26.000000', 1);
INSERT INTO `app_urls` VALUES (109, 'https://aca-prod.accela.com/MENLOPARK/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Menla Park CA', '2023-01-04 08:54:31.000000', 1);
INSERT INTO `app_urls` VALUES (110, 'https://aca-prod.accela.com/LIVERMORE/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Livemore CA', '2023-01-04 09:46:48.000000', 1);
INSERT INTO `app_urls` VALUES (111, 'https://aca-prod.accela.com/LONETREE/Cap/GlobalSearchResults.aspx?QueryText=solar#', 'Lonetree CO', '2023-01-04 10:06:11.000000', 1);
INSERT INTO `app_urls` VALUES (112, 'https://aca-prod.accela.com/SHELBYCO/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Shelby county CA', '2023-01-04 12:07:30.000000', 1);
INSERT INTO `app_urls` VALUES (113, 'https://aca-prod.accela.com/CITYOFRC/Cap/CapHome.aspx?module=Building&TabName=Building', 'Rancho Cucamonga CA', '2023-01-04 14:12:29.000000', 1);
INSERT INTO `app_urls` VALUES (114, 'https://aca-prod.accela.com/SANBENITO/Cap/GlobalSearchResults.aspx?QueryText=solar#', 'San Benito County CA', '2023-01-04 15:28:22.000000', 1);
INSERT INTO `app_urls` VALUES (115, 'https://aca-prod.accela.com/TEHACHAPI/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Tehachapi CA', '2023-01-04 19:49:11.000000', 1);
INSERT INTO `app_urls` VALUES (116, 'https://aca-prod.accela.com/SCCGOV/Cap/GlobalSearchResults.aspx?QueryText=solar', 'Santa Clara CA', '2023-01-04 20:00:45.000000', 1);

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
