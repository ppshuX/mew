---
# Mew 项目介绍


## Mew 是一个全栈开发的社交博客系统，融合了博客创作、情绪记录、好友互动等功能。它不仅是技术成长的练习场，更是情感与生活的记录平台。


## 🚀 项目说明（简要）


### 1. 克隆项目

```bash
git clone https://github.com/yourusername/mew.git
cd mew
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库与迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建管理员账户（可选）

```bash
python manage.py createsuperuser
```

### 5. 运行项目

```bash
python manage.py runserver
```

### 6. 配置 Nginx（静态与媒体）

```nginx
nginx

location /static/ {
    alias /home/your_project_path/staticfiles/;
}

location /media/ {
    alias /home/your_project_path/media/;
}
```

🖼️ **项目预览** 🎨

* 首页展示
* 博客编辑页
* 用户空间

📌 **项目亮点** 🎯

* **全栈能力展示**：从后端逻辑到前端样式均由作者独立开发
* **安全性考虑**：完善的登录认证系统与权限判断
* **模块解耦**：每个功能模块可独立使用或扩展
* **情绪表达**：特别设计了“朋友圈”和“心情说说”模块，用于记录成长与情绪波动

👨‍💻 **作者信息**

* 昵称：J.Grigg（Json）
* 年龄：20岁 / 软件工程专业
* 学校：211大学（南昌大学）
* 个人博客地址（开发中）：[Mew 个人空间](https://app7534.acapp.acwing.com.cn)
* Email：[2064747320@qq.com](mailto:2064747320@qq.com)

⭐️ **TODO List（未来计划）**

* 添加博客草稿箱功能
* 升级前端为 Vue3 + Tailwind
* 添加通知系统（新评论提醒）
* 开发移动端适配页面
* 完成“宠物领养平台”长期计划（结合 Mew 登录系统）

🪐 **项目愿景**

“Mew 是一份关于自我记录的温柔抵达。它见证成长、表达真实，也承载心中的那一点光。”

欢迎关注、参与开发、提出建议或 fork 项目！

```

```
# 数据备份脚本说明

## 概述

本脚本用于定期备份 Mew 项目的数据库文件（`db.sqlite3`）和媒体文件（`media/` 文件夹）。它会将数据库和媒体文件备份到指定的 GitHub 仓库中，并推送到远程仓库进行保存。可以通过设置定时任务自动化执行。

## 功能

- **数据库备份**：将 `db.sqlite3` 文件进行备份，命名为 `db_<日期>.sqlite3`。
- **媒体文件备份**：将 `media/` 文件夹进行压缩，命名为 `media_<日期>.tar.gz`。
- **推送到 GitHub**：将备份文件推送到一个私有 GitHub 仓库，用于长期存储。
- **每日自动备份**：可以通过定时任务（例如 cron）每天自动执行备份操作。

## 脚本执行流程

1. **进入项目目录**：
   脚本会进入 Mew 项目的根目录。

2. **备份数据库文件**：
   脚本会将 `db.sqlite3` 文件复制到指定的备份目录，并给文件命名为 `db_<日期>.sqlite3`，其中 `<日期>` 格式为 `YYYYMMDD_HHMMSS`。

3. **备份媒体文件**：
   脚本会将 `media/` 文件夹打包成一个 `.tar.gz` 文件，命名为 `media_<日期>.tar.gz`。

4. **推送到 GitHub**：
   脚本会进入指定的 GitHub 仓库目录，并将备份文件提交到仓库。每次提交的日志中会包含备份的日期信息。

## 脚本代码

```bash
#!/bin/bash

# 1. 设置变量
PROJECT_DIR="/home/acs/mew"         # 项目根目录
BACKUP_REPO_DIR="/home/acs/myblog-backup" # 备份仓库目录
DATE=$(date +"%Y%m%d_%H%M%S")  # 当前时间，用于文件命名

# 2. 进入项目目录，备份数据库和media
cd "$PROJECT_DIR"
cp db.sqlite3 "$BACKUP_REPO_DIR/db_$DATE.sqlite3"
tar czf "$BACKUP_REPO_DIR/media_$DATE.tar.gz" media/

# 3. 进入备份仓库目录，推送到GitHub
cd "$BACKUP_REPO_DIR"
git add .
git commit -m "Backup on $DATE"
git push origin master

# 提示备份成功
echo "Backup completed successfully! Files pushed to GitHub."
```
