#!-*- coding: utf-8 -*-
# python3.7
# CreateTime: 2023/3/16 15:10
# FileName:

import sys

sys.path.append('..')

import constant
from dao import mysqlDB


def user_table_sql():
    init_sql_1 = 'SET NAMES utf8mb4;'
    init_sql_2 = 'SET FOREIGN_KEY_CHECKS = 0;'
    drop_sql = f'DROP TABLE IF EXISTS `{constant.UserTable}`;'
    create_sql = f"""CREATE TABLE `{constant.UserTable}`  (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户ID',
                  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `email` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `salt` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '盐',
                  `bcrypt_str` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `is_ban` tinyint(1) UNSIGNED ZEROFILL NOT NULL DEFAULT 0 COMMENT '是否封禁',
                  `create_at` timestamp NOT NULL COMMENT '创建时间',
                  `update_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                  `update_by` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新人的邮箱',
                  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
                  PRIMARY KEY (`id`) USING BTREE,
                  UNIQUE INDEX ```uid```(`uid`) USING BTREE,
                  UNIQUE INDEX `email`(`email`) USING BTREE
                ) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
                """
    set_key_sql = 'SET FOREIGN_KEY_CHECKS = 1;'
    return init_sql_1, init_sql_2, drop_sql, create_sql, set_key_sql


def role_table_sql():
    init_sql_1 = 'SET NAMES utf8mb4;'
    init_sql_2 = 'SET FOREIGN_KEY_CHECKS = 0;'
    drop_sql = f'DROP TABLE IF EXISTS `{constant.RoleTable}`;'
    create_sql = f"""CREATE TABLE `{constant.RoleTable}`  (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `role_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色ID',
                  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色名称',
                  `parent` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '父角色',
                  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
                  `create_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
                  `update_at` timestamp NULL DEFAULT NULL,
                  `create_by` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `update_by` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
                  PRIMARY KEY (`id`) USING BTREE,
                  UNIQUE INDEX `name`(`name`) USING BTREE,
                  UNIQUE INDEX ```role_id```(`role_id`) USING BTREE
                ) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
                """
    set_key_sql = 'SET FOREIGN_KEY_CHECKS = 1;'
    return init_sql_1, init_sql_2, drop_sql, create_sql, set_key_sql


def user_role_table_sql():
    init_sql_1 = 'SET NAMES utf8mb4;'
    init_sql_2 = 'SET FOREIGN_KEY_CHECKS = 0;'
    drop_sql = f'DROP TABLE IF EXISTS `{constant.UserRoleTable}`;'
    create_sql = f"""CREATE TABLE `{constant.UserRoleTable}`  (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `role_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `update_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
                  `update_by` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  PRIMARY KEY (`id`) USING BTREE,
                  INDEX ```uid```(`uid`) USING BTREE,
                  UNIQUE INDEX `unique`(`uid`, `role_id`) USING BTREE,
                  INDEX ```role_id```(`role_id`) USING BTREE
                ) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
                """
    set_key_sql = 'SET FOREIGN_KEY_CHECKS = 1;'
    return init_sql_1, init_sql_2, drop_sql, create_sql, set_key_sql


def role_permission_table_sql():
    init_sql_1 = 'SET NAMES utf8mb4;'
    init_sql_2 = 'SET FOREIGN_KEY_CHECKS = 0;'
    drop_sql = f'DROP TABLE IF EXISTS `{constant.RolePermissionTable}`;'
    create_sql = f"""CREATE TABLE `{constant.RolePermissionTable}`  (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `role_id` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `permission` varchar(5000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '权限',
                  `update_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
                  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '更新人邮箱',
                  PRIMARY KEY (`id`) USING BTREE,
                  UNIQUE INDEX `role_id`(`role_id`) USING BTREE
                ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
                """
    set_key_sql = 'SET FOREIGN_KEY_CHECKS = 1;'
    return init_sql_1, init_sql_2, drop_sql, create_sql, set_key_sql


def demo_table_sql():
    init_sql_1 = 'SET NAMES utf8mb4;'
    init_sql_2 = 'SET FOREIGN_KEY_CHECKS = 0;'
    drop_sql = f'DROP TABLE IF EXISTS `{constant.DemoTable}`;'
    create_sql = f"""CREATE TABLE `{constant.DemoTable}`  (
                  `id` int NOT NULL AUTO_INCREMENT,
                  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
                  `auth` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户',
                  `update_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
                  PRIMARY KEY (`id`) USING BTREE,
                  INDEX ```title```(`title`) USING BTREE,
                  INDEX `auth`(`auth`) USING BTREE
                ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;
                """
    set_key_sql = 'SET FOREIGN_KEY_CHECKS = 1;'
    return init_sql_1, init_sql_2, drop_sql, create_sql, set_key_sql


def create_table(table, table_sql_list):
    for sql in table_sql_list:
        res = mysqlDB.execute(sql)
    print(f'{table} 创建成功')


def main():
    tables = {
        'user': user_table_sql(),
        'role': role_table_sql(),
        'user_role': user_role_table_sql(),
        'role_permission': role_permission_table_sql(),
        'demo': demo_table_sql(),
    }
    for table, table_sql_list in tables.items():
        create_table(table, table_sql_list)


if __name__ == '__main__':
    main()
