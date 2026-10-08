-- Public initialization: schema only, no original users or business records.

-- Create and select your database before import.

SET NAMES utf8mb4;

SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE IF NOT EXISTS `buying`  (
  `pid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '产品id',
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '产品标题',
  `descInfo` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '产品介绍',
  `score` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '产品评分',
  `travel` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '售卖人数',
  `comment` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '点评人数',
  `retail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '供应商',
  `price` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '价格',
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'image',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'link',
  `feature` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '特色',
  PRIMARY KEY (`pid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

CREATE TABLE IF NOT EXISTS `comment`  (
  `commentId` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论id',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '评论内容',
  `ipLocatedName` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '来自哪里',
  `publishTypeTag` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '评论的时间',
  `score` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '得分',
  `scores` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '得分详细信息',
  `touristTypeDisplay` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '类型',
  `userNick` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '用户昵称',
  `userMember` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '用户类型',
  `att_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关联景点',
  PRIMARY KEY (`commentId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

CREATE TABLE IF NOT EXISTS `djy_att`  (
  `cargetId` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '唯一的id',
  `name` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '景区的名字',
  `commentScoreNum` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '景区的评分',
  `titleTips` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '景区的类型',
  `heatView` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '热度',
  `address` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '地址',
  `baseInfoItem` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '开放时间',
  `img` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT 'image',
  `url` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'link',
  `preferential` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '优惠政策',
  `service` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '服务设施',
  `hotTags` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '景区关键词',
  `descInfo` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '介绍',
  `poiId` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '评论获取的id',
  PRIMARY KEY (`cargetId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

CREATE TABLE IF NOT EXISTS `user`  (
  `id` int NOT NULL COMMENT '用户表主键',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录账号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录密码',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS=1;
