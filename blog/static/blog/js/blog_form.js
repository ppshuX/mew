// blog_form.js
// 只保留高级博客编辑页面相关逻辑

document.addEventListener('DOMContentLoaded', function () {
    // 字数统计
    const textarea = document.querySelector('.mew-form-textarea');
    const maxLen = 5000;
    if (textarea) {
        const counter = document.createElement('div');
        counter.style.textAlign = 'right';
        counter.style.fontSize = '0.98rem';
        counter.style.marginTop = '4px';
        counter.style.color = '#aaa';
        counter.innerHTML = `0 / ${maxLen}`;
        textarea.parentNode.appendChild(counter);

        const warning = document.createElement('div');
        warning.style.color = '#ff4d4f';
        warning.style.fontSize = '0.98rem';
        warning.style.marginTop = '2px';
        warning.style.display = 'none';
        warning.textContent = '字数已超出最大限制！';
        textarea.parentNode.appendChild(warning);

        textarea.addEventListener('input', function () {
            const len = textarea.value.length;
            counter.innerHTML = `${len} / ${maxLen}`;
            if (len > maxLen) {
                warning.style.display = 'block';
                counter.style.color = '#ff4d4f';
            } else {
                warning.style.display = 'none';
                counter.style.color = '#aaa';
            }
        });
    }
});

function switchToMarkdown() {
    tabMarkdown.classList.add('active');
    tabEdit.classList.remove('active');
    tabPreview.classList.remove('active');
    editorArea.style.display = 'none';
    markdownArea.style.display = '';
    previewArea.style.display = 'none';
    currentMode = 'markdown';

    // 显式设置容器高度，防止高度为0
    document.getElementById('toastui-editor').style.minHeight = '400px';

    // 初始化 ToastUI Editor
    if (!toastEditor) {
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
            ],
            placeholder: '请在此输入Markdown内容...',
        });
        // 如果有富文本内容，尝试转换
        if (editorInstance) {
            const richContent = editorInstance.getData();
            const markdownText = convertHtmlToMarkdown(richContent);
            toastEditor.setMarkdown(markdownText);
        }
    }
}
