# 初始化
* 创建表：
  ```cmd
  cd init
  python create_table.py
  ```
* 初始化数据：
  ```cmd
  cd init
  python init_data.py
  ```
* 将生成的角色ID填充至 `constant.py`

# 启动
``python app.py``

# 用户
* 新用户为`默认角色`

# 角色
* 初始化角色： `超管`、`管理员`、`默认角色`
* 角色可继承，但不可继承至`初始化角色`

# 权限
* 涉及到`管理员`的变更，均须`超管`权限
* 功能权限：用户所有角色的权限集合。（`超管`及`管理员`拥有所有权限）
* 数据权限：TODO
