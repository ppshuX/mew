# 全屏编辑功能测试指南

## 测试环境准备

1. **启动开发服务器**
   ```bash
   cd /path/to/mew
   python manage.py runserver
   ```

2. **访问测试页面**
   - 博客编辑器：http://localhost:8000/blog/create/
   - 普通动态编辑器：http://localhost:8000/blog/simple_create/

## 功能测试清单

### ✅ 博客编辑器全屏功能测试

#### 1. 基本功能测试
- [ ] 页面正常加载，ToastUI Editor显示正常
- [ ] "全屏编辑"按钮显示在Tab按钮区域右侧
- [ ] 按钮图标为展开图标（fas fa-expand）
- [ ] 按钮文字显示"全屏编辑"

#### 2. 进入全屏模式测试
- [ ] 点击"全屏编辑"按钮
- [ ] 编辑器占满整个浏览器窗口
- [ ] 背景变为纯白色
- [ ] 按钮图标变为收缩图标（fas fa-compress）
- [ ] 按钮文字变为"退出全屏"
- [ ] 编辑器高度自动调整为窗口高度减去内边距
- [ ] ToastUI Editor工具栏和编辑区域正常显示

#### 3. 全屏模式编辑测试
- [ ] 在全屏模式下可以正常输入文字
- [ ] Markdown语法高亮正常
- [ ] 工具栏功能正常（加粗、斜体、标题等）
- [ ] 图片上传功能正常
- [ ] 预览功能正常

#### 4. 退出全屏模式测试
- [ ] 点击"退出全屏"按钮
- [ ] 编辑器恢复到原始大小
- [ ] 背景恢复正常
- [ ] 按钮图标和文字恢复
- [ ] 编辑内容保持不变

#### 5. ESC键退出测试
- [ ] 在全屏模式下按ESC键
- [ ] 编辑器自动退出全屏模式
- [ ] 所有状态恢复正常

### ✅ 普通动态编辑器全屏功能测试

#### 1. 基本功能测试
- [ ] 页面正常加载，textarea显示正常
- [ ] "全屏编辑"按钮显示在内容输入框右侧
- [ ] 按钮图标为展开图标（fas fa-expand）
- [ ] 按钮文字显示"全屏编辑"

#### 2. 进入全屏模式测试
- [ ] 点击"全屏编辑"按钮
- [ ] 文本框占满整个浏览器窗口
- [ ] 背景变为纯白色
- [ ] 按钮图标变为收缩图标（fas fa-compress）
- [ ] 按钮文字变为"退出全屏"
- [ ] 文本框高度自动调整
- [ ] 文本框自动获得焦点

#### 3. 全屏模式编辑测试
- [ ] 在全屏模式下可以正常输入文字
- [ ] 字数统计功能正常
- [ ] 超出字数限制时显示警告
- [ ] 图片上传功能正常

#### 4. 退出全屏模式测试
- [ ] 点击"退出全屏"按钮
- [ ] 文本框恢复到原始大小
- [ ] 背景恢复正常
- [ ] 按钮图标和文字恢复
- [ ] 编辑内容保持不变

#### 5. ESC键退出测试
- [ ] 在全屏模式下按ESC键
- [ ] 文本框自动退出全屏模式
- [ ] 所有状态恢复正常

## 兼容性测试

### 浏览器兼容性测试
- [ ] Chrome (推荐版本：90+)
- [ ] Firefox (推荐版本：88+)
- [ ] Safari (推荐版本：14+)
- [ ] Edge (推荐版本：90+)

### 设备兼容性测试
- [ ] 桌面端（1920x1080及以上分辨率）
- [ ] 桌面端（1366x768分辨率）
- [ ] 平板设备（横屏和竖屏）
- [ ] 手机设备（横屏和竖屏）

### 屏幕尺寸测试
- [ ] 大屏幕（27寸及以上）
- [ ] 中等屏幕（15-24寸）
- [ ] 小屏幕（13寸及以下）

## 性能测试

### 响应速度测试
- [ ] 全屏切换动画流畅（无明显卡顿）
- [ ] 编辑器刷新时间合理（< 200ms）
- [ ] 页面加载时间正常

### 内存使用测试
- [ ] 全屏模式下内存使用稳定
- [ ] 多次切换全屏模式无内存泄漏
- [ ] 长时间使用无性能下降

## 用户体验测试

### 视觉体验测试
- [ ] 全屏切换动画平滑自然
- [ ] 按钮状态变化清晰可见
- [ ] 全屏模式下界面简洁美观
- [ ] 文字和图标清晰可读

### 交互体验测试
- [ ] 按钮点击响应及时
- [ ] 键盘快捷键响应正常
- [ ] 焦点管理合理
- [ ] 错误处理友好

## 边界情况测试

### 异常情况测试
- [ ] 在编辑器加载过程中点击全屏按钮
- [ ] 在网络较慢的情况下切换全屏
- [ ] 在浏览器窗口调整大小时的全屏表现
- [ ] 在移动端横竖屏切换时的表现

### 内容安全测试
- [ ] 全屏模式下XSS防护正常
- [ ] 特殊字符输入正常
- [ ] 长文本编辑正常
- [ ] 图片上传安全

## 测试结果记录

### 测试环境
- 操作系统：
- 浏览器版本：
- 屏幕分辨率：
- 测试时间：

### 测试结果
- 通过测试项：
- 失败测试项：
- 需要改进的地方：

### 问题记录
1. **问题描述**：
   - 复现步骤：
   - 期望结果：
   - 实际结果：

2. **问题描述**：
   - 复现步骤：
   - 期望结果：
   - 实际结果：

## 测试完成标准

✅ **功能完整性**：所有核心功能正常工作
✅ **兼容性良好**：主流浏览器和设备兼容
✅ **性能达标**：响应速度和内存使用合理
✅ **用户体验**：界面美观，交互流畅
✅ **安全性**：无安全漏洞和风险

## 测试建议

1. **自动化测试**：建议编写自动化测试脚本
2. **用户反馈**：收集真实用户的使用反馈
3. **持续监控**：在生产环境中监控功能稳定性
4. **性能优化**：根据测试结果进行性能优化 