// 博客详情页评论区交互，完全照抄moments
window.addEventListener('DOMContentLoaded', function () {
    // 评论区展开/收起竖排按钮
    var toggleCommentsBtn = document.getElementById('toggle-comments-btn');
    var commentsFooterWrapper = document.getElementById('comments-footer-wrapper');
    var commentsFooter = document.getElementById('comments-footer');
    var commentsInner = document.getElementById('comments-inner');
    if (toggleCommentsBtn && commentsFooterWrapper && commentsFooter && commentsInner) {
        var commentsVisible = true; // 默认展开
        commentsFooterWrapper.style.display = '';
        toggleCommentsBtn.innerHTML = '<span>收起评论区</span>';
        toggleCommentsBtn.title = '收起评论区';
        toggleCommentsBtn.onclick = function () {
            commentsVisible = !commentsVisible;
            if (commentsVisible) {
                commentsFooterWrapper.style.display = '';
                commentsInner.classList.remove('fadeout');
                commentsInner.classList.add('fadein');
                toggleCommentsBtn.innerHTML = '<span>收起评论区</span>';
                toggleCommentsBtn.title = '收起评论区';
            } else {
                commentsInner.classList.remove('fadein');
                commentsInner.classList.add('fadeout');
                setTimeout(function () {
                    commentsFooterWrapper.style.display = 'none';
                }, 400);
                toggleCommentsBtn.innerHTML = '<span>展开评论区</span>';
                toggleCommentsBtn.title = '展开评论区';
            }
        };
    }

    // 评论区前两条可见，其余默认隐藏（JS控制）
    var commentBoxes = document.querySelectorAll('.detail-comment-box');
    var showMoreBtn = document.getElementById('show-more-comments-btn');
    var hideMoreBtn = document.getElementById('hide-more-comments-btn');
    if (commentBoxes.length <= 2) {
        if (showMoreBtn) showMoreBtn.style.display = 'none';
        if (hideMoreBtn) hideMoreBtn.style.display = 'none';
    } else {
        commentBoxes.forEach(function (box, idx) {
            if (idx >= 2) box.style.display = 'none';
            else box.style.display = '';
        });
    }
    // 展示剩余评论按钮
    if (showMoreBtn && hideMoreBtn && commentsInner) {
        showMoreBtn.onclick = function () {
            commentBoxes.forEach(function (box) {
                box.style.display = '';
            });
            showMoreBtn.style.display = 'none';
            hideMoreBtn.style.display = 'block';
            commentsInner.classList.add('expanded');
        };
        hideMoreBtn.onclick = function () {
            // 始终显示前两条，其余隐藏
            commentBoxes.forEach(function (box, idx) {
                if (idx < 2) {
                    box.style.display = '';
                } else {
                    box.style.display = 'none';
                }
            });
            if (commentBoxes.length <= 2) {
                showMoreBtn.style.display = 'none';
                hideMoreBtn.style.display = 'none';
            } else {
                showMoreBtn.style.display = 'block';
                hideMoreBtn.style.display = 'none';
            }
            commentsInner.classList.remove('expanded');
        };
    }

    // 评论AJAX提交
    var form = document.getElementById('blog-comment-form');
    var input = document.getElementById('blog-comment-input');
    if (form && input && commentsInner) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var content = input.value.trim();
            if (!content) return;
            var csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
            var url = form.getAttribute('action') || window.location.pathname.replace(/\/$/, '') + '/add_comment/';
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'comment=' + encodeURIComponent(content)
            })
                .then(async res => {
                    let text = await res.text();
                    try {
                        let data = JSON.parse(text);
                        return data;
                    } catch (e) {
                        alert('服务器返回内容：' + text);
                        throw e;
                    }
                })
                .then(data => {
                    if (data.success) {
                        var temp = document.createElement('div');
                        temp.innerHTML = data.html;
                        var newComment = temp.firstElementChild;
                        if (newComment) {
                            var first = commentsInner.querySelector('.detail-comment-box');
                            if (first) commentsInner.insertBefore(newComment, first);
                            else commentsInner.insertBefore(newComment, form);
                            bindCommentActions(newComment);
                            // 只刷新新插入评论的删除表单token
                            var globalToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                            var delForm = newComment.querySelector('form[action*="delete"]');
                            if (delForm) {
                                var inputToken = delForm.querySelector('input[name="csrfmiddlewaretoken"]');
                                if (inputToken) inputToken.value = globalToken;
                            }
                        }
                    }
                    input.value = '';
                })
                .catch(() => alert('评论失败'));
        });
    }

    // 点赞/删除事件绑定
    function bindCommentActions(box) {
        // 点赞
        box.querySelectorAll('.comment-like-btn').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                const commentId = this.dataset.commentId;
                const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                const textSpan = document.getElementById('comment-like-text-' + commentId);
                const countSpan = document.getElementById('comment-like-count-' + commentId);
                const iconSpan = document.getElementById('comment-like-icon-' + commentId);
                fetch(`/blog/comment/${commentId}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        this.dataset.liked = data.liked ? 'true' : 'false';
                        countSpan.textContent = data.like_count;
                        if (data.liked) {
                            iconSpan.textContent = '👍';
                            textSpan.textContent = '取消点赞';
                            this.classList.add('liked');
                        } else {
                            iconSpan.textContent = '👍🏻';
                            textSpan.textContent = '点赞';
                            this.classList.remove('liked');
                        }
                    })
                    .catch(error => {
                        console.error('评论点赞失败:', error);
                    });
            });
        });
        // 删除事件委托已在下方实现
    }
    // 页面初始所有评论都绑定一次
    document.querySelectorAll('.detail-comment-box').forEach(bindCommentActions);

    // 新增：评论删除事件委托，保证所有评论都能删
    if (commentsInner) {
        commentsInner.addEventListener('click', function (e) {
            if (e.target.classList.contains('trash-btn')) {
                e.preventDefault();
                if (!confirm('确定删除这条评论吗？')) return;
                var form = e.target.closest('form');
                var commentBox = e.target.closest('.detail-comment-box');
                var formData = new FormData(form);
                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                }).then(res => {
                    if (res.ok) {
                        if (commentBox && commentBox.classList) {
                            commentBox.classList.add('hide');
                            setTimeout(() => commentBox.remove(), 400);
                        } else {
                            window.location.reload();
                        }
                    }
                });
            }
        });
    }

    // 博客点赞功能
    var likeBtn = document.getElementById('like-btn-' + (window.postId || (window.location.pathname.match(/\d+/) || [])[0]));
    if (likeBtn) {
        likeBtn.addEventListener('click', function (e) {
            e.preventDefault();
            var postId = this.dataset.postId;
            var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            var likeCountSpan = document.getElementById('like-count-' + postId);
            var likeIcon = document.getElementById('like-icon-' + postId);
            fetch(`/blog/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.dataset.liked = data.liked ? 'true' : 'false';
                    likeCountSpan.textContent = data.like_count;
                    if (data.liked) {
                        likeIcon.textContent = '❤️';
                        likeCountSpan.classList.remove('text-muted');
                        likeCountSpan.classList.add('text-danger');
                    } else {
                        likeIcon.textContent = '🤍';
                        likeCountSpan.classList.remove('text-danger');
                        likeCountSpan.classList.add('text-muted');
                    }
                })
                .catch(error => console.error('点赞失败:', error));
        });
    }
}); 