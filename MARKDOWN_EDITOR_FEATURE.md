# Markdown 编辑器功能实现说明

## 功能概述

为博客编辑器添加了 ToastUI Editor 支持，提供类似 Typora 的所见即所得 Markdown 编辑体验。用户可以选择使用富文本编辑器或 ToastUI Editor 来编写博客内容，享受现代化的 Markdown 编辑体验。

## 实现的功能

### 1. 三种编辑模式

#### 富文本编辑模式
- 使用 CKEditor 5 富文本编辑器
- 支持工具栏操作（加粗、斜体、链接、列表、表格等）
- 所见即所得的编辑体验

#### Markdown 编辑模式（ToastUI Editor）
- 使用 ToastUI Editor 提供类似 Typora 的体验
- 支持完整的 Markdown 语法
- 实时预览功能
- 丰富的工具栏（加粗、斜体、标题、列表、表格、图片、链接、代码块等）
- 支持垂直分屏和标签页模式
- 从富文本模式自动转换内容

#### 预览模式
- 实时预览 Markdown 或富文本内容
- 完整的 HTML 渲染
- 支持所有 Markdown 语法元素

### 2. ToastUI Editor 特性

#### 工具栏功能
- **文本格式**：标题、加粗、斜体、删除线
- **列表**：无序列表、有序列表、任务列表
- **引用**：引用块
- **代码**：行内代码、代码块
- **表格**：插入和编辑表格
- **媒体**：图片插入、链接
- **其他**：分割线、缩进、全屏、预览

#### 编辑模式
- **Markdown 模式**：纯 Markdown 编辑
- **WYSIWYG 模式**：所见即所得编辑
- **垂直分屏**：左侧编辑，右侧预览
- **标签页模式**：编辑和预览切换

#### 高级功能
- 实时预览
- 语法高亮
- 自动保存
- 图片拖拽上传
- 表格编辑器
- 代码块语法高亮

### 3. Markdown 语法支持

#### 基础语法
- **标题**：`# 一级标题` 到 `###### 六级标题`
- **粗体**：`**粗体文字**` 或 `__粗体文字__`
- **斜体**：`*斜体文字*` 或 `_斜体文字_`
- **删除线**：`~~删除文字~~`
- **链接**：`[链接文字](URL)`
- **图片**：`![图片描述](图片URL)`

#### 列表
- **无序列表**：
  ```markdown
  - 列表项1
  - 列表项2
  ```
- **有序列表**：
  ```markdown
  1. 第一项
  2. 第二项
  ```
- **任务列表**：
  ```markdown
  - [x] 已完成任务
  - [ ] 未完成任务
  ```

#### 引用和代码
- **引用**：`> 引用文字`
- **行内代码**：`` `代码` ``
- **代码块**：
  ```markdown
  ```javascript
  function hello() {
      console.log("Hello World!");
  }
  ```
  ```

#### 表格
```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
```

#### 其他
- **分割线**：`---` 或 `***`
- **脚注**：`[^1]` 和 `[^1]: 脚注内容`

### 4. 技术实现

#### 前端技术栈
- **ToastUI Editor**：主要的 Markdown 编辑器
- **CKEditor 5**：富文本编辑器
- **内容转换**：JavaScript 实现富文本到 Markdown 的转换

#### 核心功能
1. **模式切换**：在富文本、Markdown、预览三种模式间切换
2. **内容转换**：富文本到 Markdown 的自动转换
3. **实时预览**：Markdown 内容的实时 HTML 渲染
4. **工具栏集成**：完整的 Markdown 编辑工具栏

#### 样式设计
- **ToastUI Editor**：现代化的编辑器界面
- **自定义主题**：与项目设计风格一致
- **响应式设计**：适配移动端和桌面端

### 5. 使用方法

#### 创建博客
1. 访问博客创建页面
2. 选择编辑模式：
   - **富文本编辑**：使用 CKEditor 5
   - **Markdown编辑**：使用 ToastUI Editor
   - **预览**：查看最终效果
3. 在 Markdown 模式下：
   - 使用工具栏按钮快速插入格式
   - 直接输入 Markdown 语法
   - 实时查看预览效果
4. 填写博客标题、标签、摘要等信息
5. 选择发布位置（朋友圈/广场/私密）
6. 点击"发布博客"或"保存草稿"

#### 编辑现有博客
1. 在博客详情页点击"编辑博客"
2. 使用相同的三种模式进行编辑
3. 保存修改

### 6. ToastUI Editor 配置

#### 编辑器配置
```javascript
toastEditor = new toastui.Editor({
    el: document.querySelector('#toastui-editor'),
    height: '400px',
    initialEditType: 'markdown',
    previewStyle: 'vertical',
    language: 'zh-CN',
    toolbarItems: [
        'heading', 'bold', 'italic', 'strike',
        'divider', 'hr', 'quote',
        'ul', 'ol', 'task', 'indent', 'outdent',
        'table', 'image', 'link',
        'code', 'codeblock',
        'scrollSync', 'fullScreen', 'preview'
    ]
});
```

#### 自定义功能
- 图片上传处理
- 自定义工具栏
- 主题定制
- 响应式适配

### 7. 用户体验优化

#### 界面设计
- 清晰的模式切换按钮
- 直观的工具栏布局
- 美观的编辑器界面
- 流畅的切换动画

#### 功能增强
- 自动保存草稿
- 快捷键支持
- 语法提示
- 错误检查

#### 响应式支持
- 移动端友好的界面
- 触摸设备优化
- 自适应布局
- 移动端工具栏优化

### 8. 技术细节

#### 文件修改
- `blog/templates/blog/blog_form.html`：集成 ToastUI Editor
- `blog/static/blog/css/blog_form.css`：自定义 ToastUI Editor 样式
- 引入 ToastUI Editor CDN 资源

#### JavaScript 功能
```javascript
// 初始化 ToastUI Editor
function initToastEditor() {
    toastEditor = new toastui.Editor({...});
}

// 模式切换
function switchToMarkdown() {
    initToastEditor();
    // 内容转换逻辑
}

// 表单提交处理
document.querySelector('form').addEventListener('submit', function(e) {
    if (currentMode === 'markdown' && toastEditor) {
        const htmlContent = toastEditor.getHTML();
        // 设置到表单字段
    }
});
```

### 9. 优势特点

#### 相比纯文本框的优势
1. **工具栏支持**：快速插入常用格式
2. **实时预览**：所见即所得的编辑体验
3. **语法高亮**：更好的代码显示
4. **表格编辑器**：可视化表格编辑
5. **图片处理**：拖拽上传和预览
6. **多种模式**：Markdown、WYSIWYG、分屏预览

#### 相比其他编辑器的优势
1. **轻量级**：加载速度快
2. **现代化**：界面美观
3. **功能完整**：支持所有常用功能
4. **易于定制**：主题和功能可定制
5. **移动端友好**：响应式设计

### 10. 未来扩展

#### 功能增强
1. **插件系统**：支持第三方插件
2. **协作编辑**：多人实时协作
3. **版本历史**：编辑历史记录
4. **导入导出**：支持多种格式

#### 编辑器增强
1. **更多主题**：多种编辑器主题
2. **自定义工具栏**：用户可配置工具栏
3. **快捷键**：更多快捷键支持
4. **拼写检查**：内置拼写检查

#### 内容增强
1. **数学公式**：LaTeX 数学公式支持
2. **图表支持**：Mermaid 图表渲染
3. **脚注**：Markdown 脚注功能
4. **目录生成**：自动生成文章目录

## 注意事项

1. **浏览器兼容性**：需要现代浏览器支持
2. **网络依赖**：需要加载 ToastUI Editor CDN
3. **内容安全**：所有用户输入都会经过安全处理
4. **性能考虑**：大文档的实时预览可能需要优化

## 测试建议

1. **功能测试**：测试所有 Markdown 语法和工具栏功能
2. **模式切换**：测试三种模式间的切换
3. **内容转换**：测试富文本到 Markdown 的转换
4. **响应式测试**：测试不同设备上的显示效果
5. **性能测试**：测试大文档的编辑性能 