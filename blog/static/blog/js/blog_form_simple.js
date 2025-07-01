// blog_form_simple.js
// 只保留普通动态页面相关逻辑

document.addEventListener('DOMContentLoaded', function () {
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