// blog_form_simple.js
// 只保留普通动态页面相关逻辑

document.addEventListener('DOMContentLoaded', function () {
    // 多图上传、预览、删除
    const input = document.getElementById('id_images');
    const preview = document.getElementById('image-preview-container');
    const addBtn = document.getElementById('add-image-btn');
    if (input && preview && addBtn) {
        let filesArr = [];

        if (addBtn && input) {
            addBtn.onclick = () => input.click();
        }

        if (input) {
            input.onchange = function (e) {
                let newFiles = Array.from(e.target.files);
                if (filesArr.length + newFiles.length > 9) {
                    alert('最多只能上传9张图片');
                    return;
                }
                filesArr = filesArr.concat(newFiles);
                renderPreview();
            };
        }

        function renderPreview() {
            if (!preview) return;
            preview.innerHTML = '';
            filesArr.forEach((file, idx) => {
                let reader = new FileReader();
                reader.onload = function (e) {
                    let div = document.createElement('div');
                    div.style.position = 'relative';
                    div.innerHTML = `
                        <img src="${e.target.result}" style="width:80px;height:80px;object-fit:cover;border-radius:6px;">
                        <span data-idx="${idx}" style="position:absolute;top:0;right:0;cursor:pointer;color:red;font-weight:bold;font-size:20px;background:#fff;border-radius:50%;padding:0 6px;">×</span>
                    `;
                    preview.appendChild(div);
                    let spans = document.querySelectorAll('span');
                    spans.forEach(function (span) {
                        if (span) {
                            span.onclick = function () {
                                filesArr.splice(idx, 1);
                                renderPreview();
                            };
                        }
                    });
                };
                reader.readAsDataURL(file);
            });
            // 更新input的files
            if (input) {
                let dataTransfer = new DataTransfer();
                filesArr.forEach(f => dataTransfer.items.add(f));
                input.files = dataTransfer.files;
            }
        }
    }

    // 全屏编辑功能
    var fullscreenBtn = document.getElementById('fullscreen-btn');
    var editorWrapper = document.getElementById('editor-wrapper');
    var textarea = document.querySelector('.mew-form-textarea');

    if (fullscreenBtn && editorWrapper && textarea) {
        fullscreenBtn.addEventListener('click', function () {
            editorWrapper.classList.toggle('fullscreen');
            fullscreenBtn.classList.toggle('fullscreen-active');

            // 更新按钮图标和文本
            if (editorWrapper.classList.contains('fullscreen')) {
                fullscreenBtn.innerHTML = '<i class="fas fa-compress"></i> 退出全屏';
                // 全屏时聚焦到文本框
                setTimeout(function () {
                    textarea.focus();
                }, 100);
            } else {
                fullscreenBtn.innerHTML = '<i class="fas fa-expand"></i> 全屏编辑';
            }
        });
    }

    // 支持 ESC 键退出全屏
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && editorWrapper && editorWrapper.classList.contains('fullscreen')) {
            editorWrapper.classList.remove('fullscreen');
            fullscreenBtn.classList.remove('fullscreen-active');
            fullscreenBtn.innerHTML = '<i class="fas fa-expand"></i> 全屏编辑';
        }
    });

    // 字数统计功能
    if (textarea) {
        const maxLen = 5000;
        const counter = document.createElement('div');
        counter.style.textAlign = 'right';
        counter.style.fontSize = '0.9rem';
        counter.style.marginTop = '4px';
        counter.style.color = '#aaa';
        counter.innerHTML = `0 / ${maxLen}`;
        textarea.parentNode.appendChild(counter);

        const warning = document.createElement('div');
        warning.style.color = '#ff4d4f';
        warning.style.fontSize = '0.9rem';
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

    // 图片预览功能
    const imageInput = document.querySelector('input[name="images"]');
    if (imageInput) {
        imageInput.addEventListener('change', function (e) {
            const files = e.target.files;
            if (files.length > 9) {
                alert('最多只能选择9张图片');
                e.target.value = '';
                return;
            }

            // 这里可以添加图片预览功能
            console.log(`选择了 ${files.length} 张图片`);
        });
    }
}); 