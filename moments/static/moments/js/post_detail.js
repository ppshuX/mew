// 点赞功能
window.addEventListener('DOMContentLoaded', function () {
    const likeBtn = document.querySelector('.like-btn, .detail-like-btn');
    if (likeBtn) {
        likeBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            const likeCountSpan = document.querySelector('.like-count, .detail-like-count');
            const likeIcon = this.querySelector('.like-icon');
            fetch(`/moments/${postId}/like/`, {
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

    // 正文展开/收起逻辑（动态插入按钮）
    var content = document.getElementById('detail-content');
    if (content) {
        // 计算一行高度
        var lineHeight = parseFloat(getComputedStyle(content).lineHeight) || 24;
        var maxLines = 20;
        var maxHeight = lineHeight * maxLines;
        // 判断是否超出20行
        if (content.scrollHeight > maxHeight + 2) {
            // 初始折叠
            content.style.maxHeight = maxHeight + 'px';
            content.style.overflow = 'hidden';
            // 创建按钮
            var btnWrap = document.createElement('div');
            btnWrap.style.width = '100%';
            btnWrap.style.textAlign = 'center';
            var btn = document.createElement('button');
            btn.id = 'expand-btn';
            btn.className = 'expand-btn';
            btn.title = '展开/收起正文';
            btn.innerHTML = '<span id="expand-text">展开剩余部分</span> <span id="expand-icon">▼</span>';
            btnWrap.appendChild(btn);
            content.parentNode.insertBefore(btnWrap, content.nextSibling);
            var expanded = false;
            btn.onclick = function () {
                expanded = !expanded;
                if (expanded) {
                    content.classList.add('expanded');
                    content.style.maxHeight = 'none';
                    content.style.overflow = 'visible';
                    document.getElementById('expand-icon').textContent = '▲';
                    document.getElementById('expand-text').textContent = '收起';
                } else {
                    content.classList.remove('expanded');
                    content.style.maxHeight = maxHeight + 'px';
                    content.style.overflow = 'hidden';
                    document.getElementById('expand-icon').textContent = '▼';
                    document.getElementById('expand-text').textContent = '展开剩余部分';
                }
            };
        } else {
            // 内容未超出，不显示按钮，且确保内容全部展示
            content.style.maxHeight = 'none';
            content.style.overflow = 'visible';
        }
    }

    // 评论区展开/收起竖排按钮
    var toggleCommentsBtn = document.getElementById('toggle-comments-btn');
    var commentsFooter = document.getElementById('comments-footer');
    var commentsInner = document.getElementById('comments-inner');
    if (toggleCommentsBtn && commentsFooter && commentsInner) {
        var commentsVisible = true;
        commentsFooter.style.display = 'block';
        toggleCommentsBtn.innerHTML = '<span>收起评论区</span>';
        toggleCommentsBtn.title = '收起评论区';
        toggleCommentsBtn.onclick = function () {
            commentsVisible = !commentsVisible;
            if (commentsVisible) {
                commentsFooter.style.display = 'block';
                commentsInner.classList.remove('fadeout');
                commentsInner.classList.add('fadein');
                toggleCommentsBtn.innerHTML = '<span>收起评论区</span>';
                toggleCommentsBtn.title = '收起评论区';
            } else {
                commentsInner.classList.remove('fadein');
                commentsInner.classList.add('fadeout');
                setTimeout(function () {
                    commentsFooter.style.display = 'none';
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
            // 如果评论数小于3，隐藏按钮
            if (commentBoxes.length <= 2) {
                showMoreBtn.style.display = 'none';
                hideMoreBtn.style.display = 'none';
            } else {
                showMoreBtn.style.display = 'block';
                hideMoreBtn.style.display = 'none';
            }
            commentsInner.classList.remove('expanded');
        };
        // 自动展开全部评论（如URL带参数）
        if (window.location.search.indexOf('show_all_comments=1') !== -1) {
            setTimeout(function () { showMoreBtn.click(); }, 100);
        }
    }

    // 正文滑到底部自动滚到评论区
    if (content) {
        content.addEventListener('wheel', function (e) {
            if (!content.classList.contains('expanded')) {
                // 只在未展开时生效
                var isBottom = (content.scrollHeight - content.scrollTop - content.clientHeight) < 2;
                if (isBottom && e.deltaY > 0) {
                    // 平滑滚动到评论区
                    var footer = document.getElementById('comments-footer');
                    if (footer) {
                        window.scrollTo({
                            top: footer.offsetTop - window.innerHeight / 2,
                            behavior: 'smooth'
                        });
                    }
                }
            }
        });
    }

    // 评论点赞交互
    document.querySelectorAll('.comment-like-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            var commentId = this.dataset.commentId;
            var liked = this.dataset.liked === 'true';
            var textSpan = document.getElementById('comment-like-text-' + commentId);
            var countSpan = document.getElementById('comment-like-count-' + commentId);
            var iconSpan = document.getElementById('comment-like-icon-' + commentId);
            // 假设后端有接口 /moments/comment/<id>/like/，返回 {liked:bool, like_count:int}
            fetch(`/moments/comment/${commentId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.dataset.liked = data.liked ? 'true' : 'false';
                    textSpan.textContent = data.liked ? '取消点赞' : '点赞';
                    countSpan.textContent = data.like_count;
                    // 动画效果
                    this.classList.add('like-anim');
                    setTimeout(() => this.classList.remove('like-anim'), 300);
                });
        });
    });

    // 评论删除AJAX
    document.querySelectorAll('.trash-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            if (!confirm('确定删除这条评论吗？')) return;
            var form = this.closest('form');
            var commentBox = this.closest('.detail-comment-box');
            var formData = new FormData(form);
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            }).then(res => {
                if (res.ok) {
                    commentBox.classList.add('hide');
                    setTimeout(() => commentBox.remove(), 400);
                }
            });
        });
    });
}); 