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

    // 初始化 ToastUI Editor
    var initContent = document.getElementById('init-content');
    var initialValue = '';
    if (initContent && initContent.value.trim()) {
        initialValue = initContent.value;
    }
    window.toastEditor = new window.toastui.Editor({
        el: document.querySelector('#toastui-editor'),
        height: '400px',
        initialEditType: 'markdown',
        previewStyle: 'vertical',
        language: 'zh-CN',
        initialValue: initialValue,
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

    // 实时同步编辑器内容到隐藏域
    window.toastEditor.on('change', function () {
        var hiddenTextarea = document.getElementById('blog-content-hidden');
        if (hiddenTextarea) {
            hiddenTextarea.value = window.toastEditor.getMarkdown();
        }
    });

    var saveDraftBtn = document.getElementById('save-draft-btn');
    if (saveDraftBtn) {
        saveDraftBtn.onclick = function (e) {
            e.preventDefault();
            // 设置草稿标志
            var form = document.getElementById('blog-form');
            let hidden = form.querySelector('input[name="is_draft"]');
            if (!hidden) {
                hidden = document.createElement('input');
                hidden.type = 'hidden';
                hidden.name = 'is_draft';
                form.appendChild(hidden);
            }
            hidden.value = 'true';
            form.requestSubmit();
        };
    }

    // 表单提交时再同步一次（双保险）
    var blogForm = document.getElementById('blog-form');
    if (blogForm) {
        blogForm.addEventListener('submit', function (e) {
            var hiddenTextarea = document.getElementById('blog-content-hidden');
            if (window.toastEditor && hiddenTextarea) {
                hiddenTextarea.value = window.toastEditor.getMarkdown().trim();
            }
            // 强制同步关键词字段
            var tagsInput = document.querySelector('input[name="blog_tags"]');
            if (tagsInput) {
                tagsInput.value = tagsInput.value.trim();
            }
        });
    }

    // 全屏编辑功能
    var fullscreenBtn = document.getElementById('fullscreen-btn');
    var editorWrapper = document.getElementById('editor-wrapper');
    var exitFullscreenBtn = document.getElementById('exit-fullscreen-btn');

    if (fullscreenBtn && editorWrapper) {
        fullscreenBtn.addEventListener('click', function () {
            editorWrapper.classList.toggle('fullscreen');
            fullscreenBtn.classList.toggle('fullscreen-active');

            // 更新按钮图标和文本
            var icon = fullscreenBtn.querySelector('i');
            var text = fullscreenBtn.textContent.trim();

            if (editorWrapper.classList.contains('fullscreen')) {
                icon.className = 'fas fa-compress';
                fullscreenBtn.innerHTML = '<i class="fas fa-compress"></i> 退出全屏';
                if (exitFullscreenBtn) exitFullscreenBtn.style.display = 'flex';
            } else {
                icon.className = 'fas fa-expand';
                fullscreenBtn.innerHTML = '<i class="fas fa-expand"></i> 全屏编辑';
                if (exitFullscreenBtn) exitFullscreenBtn.style.display = 'none';
            }
        });
    }

    // 新增：点击退出全屏按钮
    if (exitFullscreenBtn && editorWrapper) {
        exitFullscreenBtn.addEventListener('click', function () {
            if (editorWrapper.classList.contains('fullscreen')) {
                editorWrapper.classList.remove('fullscreen');
                if (fullscreenBtn) fullscreenBtn.classList.remove('fullscreen-active');
                if (fullscreenBtn) fullscreenBtn.innerHTML = '<i class="fas fa-expand"></i> 全屏编辑';
                exitFullscreenBtn.style.display = 'none';
            }
        });
    }

    // 支持 ESC 键退出全屏
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && editorWrapper && editorWrapper.classList.contains('fullscreen')) {
            editorWrapper.classList.remove('fullscreen');
            fullscreenBtn.classList.remove('fullscreen-active');

            var icon = fullscreenBtn.querySelector('i');
            icon.className = 'fas fa-expand';
            fullscreenBtn.innerHTML = '<i class="fas fa-expand"></i> 全屏编辑';
            if (exitFullscreenBtn) exitFullscreenBtn.style.display = 'none';

            // 刷新编辑器以适配新尺寸
            if (window.toastEditor) {
                setTimeout(function () {
                    window.toastEditor.resize();
                }, 100);
            }
        }
    });
});
