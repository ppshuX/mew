# UserZone 类别筛选功能

## 功能概述

为userzone页面的右边大卡片动态帖子添加了类别筛选功能，用户可以根据不同类别查看动态内容。

## 新增功能

### 1. 动态类别
- **日常** (daily) - 日常生活相关
- **学习** (study) - 学习、考试、课程相关
- **工作** (work) - 工作、实习相关
- **旅行** (travel) - 旅行、出游相关
- **美食** (food) - 美食、餐饮相关
- **运动** (sports) - 运动、健身相关
- **娱乐** (entertainment) - 娱乐、休闲相关
- **其他** (other) - 其他类别

### 2. 筛选功能
- **动态类型筛选**: 朋友圈动态、广场动态、私密动态
- **类别筛选**: 全部类别、日常、学习、工作、旅行、美食、运动、娱乐、其他
- **组合筛选**: 可以同时按类型和类别进行筛选

### 3. 界面更新
- 在筛选按钮区域添加了类别下拉选择器
- 每个动态卡片显示对应的类别标签
- 不同类别使用不同的渐变色标签
- 响应式设计，支持移动端

## 技术实现

### 数据库变更
- 为 `moments.Post` 和 `plaza.Post` 模型添加了 `category` 字段
- 创建了相应的数据库迁移文件

### 后端更新
- 更新了 `userzone/views.py` 支持类别筛选
- 更新了 `moments/forms.py` 和 `plaza/forms.py` 添加类别选择
- 支持URL参数筛选：`?type=moments&category=daily`

### 前端更新
- 更新了 `userzone/templates/userzone/userzone.html` 模板
- 添加了类别筛选器和类别标签显示
- 更新了 `userzone/static/userzone/js/userzone.js` 处理筛选逻辑
- 添加了 `userzone/static/userzone/css/userzone.css` 样式

## 使用方法

1. 访问用户空间页面：`/userzone/用户名/`
2. 在右侧筛选区域选择动态类型（朋友圈/广场/私密）
3. 使用类别下拉菜单选择特定类别
4. 页面会自动刷新显示筛选结果

## 示例URL
- 查看所有朋友圈动态：`/userzone/用户名/?type=moments&category=all`
- 查看学习类朋友圈动态：`/userzone/用户名/?type=moments&category=study`
- 查看工作类广场动态：`/userzone/用户名/?type=plaza&category=work`

## 测试数据
已创建测试用户 `testuser` 包含各种类别的动态，可以访问 `/userzone/testuser/` 查看效果。 