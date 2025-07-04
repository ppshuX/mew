// 以下为广场plaza页面js，仿照moments
window.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.like-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            const postId = this.dataset.postId;
            const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
            fetch(`/plaza/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    const icon = document.getElementById(`like-icon-${postId}`);
                    const count = document.getElementById(`like-count-${postId}`);
                    icon.textContent = data.liked ? '❤️' : '🤍';
                    count.textContent = data.like_count;
                })
                .catch(error => {
                    console.error('点赞失败:', error);
                });
        });
    });
}); 