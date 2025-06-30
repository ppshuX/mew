// blog_form.js
// 预留页面交互脚本

document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.querySelector('.mew-form-textarea');
    if (!textarea) return;
    const maxLen = 5000;

    // 创建字数统计和提示元素
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
});
