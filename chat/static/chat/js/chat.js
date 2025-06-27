// 聊天室页面独立JS
// 聊天自动滚动到底部
const chatBox = document.getElementById('chat-box');
if (chatBox) {
    chatBox.scrollTop = chatBox.scrollHeight;
}
// 移动端切换逻辑
function isMobile() {
    return window.innerWidth <= 700;
}
function mobileBackToList() {
    document.getElementById('chat-container').classList.remove('mobile-chat-active');
}
document.querySelectorAll('.chat-user-item').forEach(function (item) {
    item.addEventListener('click', function () {
        if (isMobile()) {
            document.getElementById('chat-container').classList.add('mobile-chat-active');
        }
        // 跳转到对应聊天（原有逻辑）
        const userId = this.getAttribute('data-user-id');
        if (userId) {
            window.location.href = '?user=' + userId;
        }
    });
}); 