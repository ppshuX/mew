// blog_form.js
// 只保留高级博客编辑页面相关逻辑

// 在文件顶部声明全局 toastEditor
window.toastEditor = null;

let textarea;
document.addEventListener('DOMContentLoaded', function () {
    // 字数统计
    textarea = document.querySelector('.mew-form-textarea');
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

    // 表单提交校验
    var blogForm = document.getElementById('blog-form');
    if (blogForm) {
        blogForm.addEventListener('submit', function (e) {
            var content = '';
            var markdownArea = document.getElementById('markdown-area');
            var editorArea = document.getElementById('editor-area');
            if (window.toastEditor) {
                content = window.toastEditor.getMarkdown().trim();
            }
            // 同步内容到隐藏 textarea
            var hiddenTextarea = document.getElementById('blog-content-hidden');
            if (hiddenTextarea) {
                hiddenTextarea.value = content;
            }
            if (!content) {
                e.preventDefault();
                alert('博客内容不能为空！');
                return false;
            }
        });
    }

    // 初始化 ToastUI Editor
    window.toastEditor = new window.toastui.Editor({
        el: document.querySelector('#toastui-editor'),
        height: '400px',
        initialEditType: 'markdown',
        previewStyle: 'vertical',
        language: 'zh-CN',
        hooks: {
            addImageBlobHook: function (blob, callback) {
                const formData = new FormData();
                formData.append('image', blob);
                fetch('/blog/api/upload_blog_image/', {
                    method: 'POST',
                    body: formData,
                    credentials: 'include'
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.url) {
                            callback(data.url, blob.name);
                        } else {
                            alert('图片上传失败');
                        }
                    })
                    .catch(() => alert('图片上传失败'));
                return false;
            }
        }
    });
});
