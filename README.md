

# Mew 项目介绍
```
```
## Mew 是一个全栈开发的社交博客系统，融合了博客创作、情绪记录、好友互动等功能。它不仅是技术成长的练习场，更是情感与生活的记录平台。
```

```
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
* 个人博客地址（开发中）：[Mew 个人空间](http://yourwebsite.com)
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
