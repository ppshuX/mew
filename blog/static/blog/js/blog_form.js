// blog_form.js
// 预留页面交互脚本

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

    // 多图上传、预览、删除
    const input = document.getElementById('id_images');
    const preview = document.getElementById('image-preview-container');
    const addBtn = document.getElementById('add-image-btn');
    if (input && preview && addBtn) {
        let filesArr = [];

        addBtn.onclick = () => input.click();

        input.onchange = function (e) {
            let newFiles = Array.from(e.target.files);
            if (filesArr.length + newFiles.length > 9) {
                alert('最多只能上传9张图片');
                return;
            }
            filesArr = filesArr.concat(newFiles);
            renderPreview();
        };

        function renderPreview() {
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
                    div.querySelector('span').onclick = function () {
                        filesArr.splice(idx, 1);
                        renderPreview();
                    };
                };
                reader.readAsDataURL(file);
            });
            // 更新input的files
            let dataTransfer = new DataTransfer();
            filesArr.forEach(f => dataTransfer.items.add(f));
            input.files = dataTransfer.files;
        }
    }
});
