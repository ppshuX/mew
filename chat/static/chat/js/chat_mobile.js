// 微信风格移动端聊天JS
window.addEventListener('DOMContentLoaded', function () {
    var msgBox = document.getElementById('wxchat-messages');
    var inputForm = document.querySelector('.wxchat-inputbar');

    // 页面加载时滚动到底部
    if (msgBox) {
        scrollToBottom();
    }

    // 监听表单提交，发送消息后滚动到底部
    if (inputForm) {
        inputForm.addEventListener('submit', function () {
            // 延迟执行，确保新消息已添加到DOM
            setTimeout(function () {
                scrollToBottom();
            }, 100);
        });
    }

    // 滚动到底部的函数
    function scrollToBottom() {
        if (msgBox) {
            msgBox.scrollTop = msgBox.scrollHeight;
        }
    }

    // 监听窗口大小变化，重新滚动到底部
    window.addEventListener('resize', function () {
        setTimeout(scrollToBottom, 50);
    });

    // 监听消息区域滚动，确保新消息可见
    if (msgBox) {
        msgBox.addEventListener('scroll', function () {
            // 如果用户手动滚动，可以在这里添加逻辑
        });
    }
}); 