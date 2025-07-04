console.log('userzone.js loaded');

// 目前无需JS，预留

// UserZone 页面交互效果
document.addEventListener('DOMContentLoaded', function () {

    // 编辑动态按钮点击事件
    const editPostBtn = document.querySelector('.uz-edit-post-btn');
    if (editPostBtn) {
        editPostBtn.addEventListener('click', function () {
            // 跳转到blog创建页面
            window.location.href = '/blog/create/';
        });

        // 添加悬停效果
        editPostBtn.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });

        editPostBtn.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) scale(1)';
        });
    }

    // 卡片进入动画
    const cards = document.querySelectorAll('.uz-card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;
        cardObserver.observe(card);
    });

    // 头像悬停效果
    const avatars = document.querySelectorAll('.uz-avatar, .uz-visitor-avatar');
    avatars.forEach(avatar => {
        avatar.addEventListener('mouseenter', function () {
            this.style.transform = 'scale(1.1) rotate(5deg)';
        });

        avatar.addEventListener('mouseleave', function () {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });

    // 图片预览功能
    const postImages = document.querySelectorAll('.uz-post-img');
    postImages.forEach(img => {
        img.addEventListener('click', function (e) {
            e.stopPropagation(); // 阻止事件冒泡，避免触发卡片点击
            showImagePreview(this.src, this.alt);
        });

        // 添加点击提示
        img.style.cursor = 'pointer';
        img.title = '点击查看大图';
    });

    // 点赞按钮动画
    const likeButtons = document.querySelectorAll('.uz-post-action');
    likeButtons.forEach(button => {
        if (button.textContent.includes('👍')) {
            button.addEventListener('click', function (e) {
                e.stopPropagation(); // 阻止事件冒泡，避免触发卡片点击
                e.preventDefault();
                animateLike(this);
            });
        }
    });

    // 动态卡片点击跳转
    const postCards = document.querySelectorAll('.uz-post-card');
    postCards.forEach(card => {
        // 检查是否有data-url属性
        const url = card.getAttribute('data-url');
        if (url) {
            card.style.cursor = 'pointer';

            card.addEventListener('click', function (e) {
                // 如果点击的是图片或按钮，不跳转
                if (e.target.closest('.uz-post-img') || e.target.closest('.uz-post-action')) {
                    return;
                }

                // 添加点击反馈
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    window.location.href = url;
                }, 150);
            });

            // 悬停效果
            card.addEventListener('mouseenter', function () {
                this.style.transform = 'translateY(-4px) scale(1.01)';
            });

            card.addEventListener('mouseleave', function () {
                this.style.transform = 'translateY(0) scale(1)';
            });
        }
    });

    // 统计数字动画
    animateNumbers();

    // 在线状态脉冲动画
    const onlineDots = document.querySelectorAll('.uz-dot.online');
    onlineDots.forEach(dot => {
        dot.addEventListener('mouseenter', function () {
            this.style.animation = 'pulse 0.5s infinite';
        });

        dot.addEventListener('mouseleave', function () {
            this.style.animation = 'pulse 2s infinite';
        });
    });

    // 按钮悬停效果
    const buttons = document.querySelectorAll('.uz-btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-3px) scale(1.02)';
        });

        button.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    const btns = document.querySelectorAll('.uz-filter-btn');
    const lists = {
        moments: document.getElementById('moments-list'),
        plaza: document.getElementById('plaza-list'),
        private: document.getElementById('private-list')
    };
    const categoryFilter = document.getElementById('category-filter');

    // 初始化：确保当前选中的类型正确显示
    function initializeDisplay() {
        const activeBtn = document.querySelector('.uz-filter-btn.active');
        if (activeBtn) {
            const activeType = activeBtn.getAttribute('data-type');
            Object.keys(lists).forEach(key => {
                if (lists[key]) {
                    if (key === activeType) {
                        lists[key].style.display = 'block';
                        lists[key].style.opacity = '1';
                    } else {
                        lists[key].style.display = 'none';
                        lists[key].style.opacity = '0';
                    }
                }
            });
        }
    }

    // 页面加载时初始化显示
    initializeDisplay();

    // 动态类型筛选
    btns.forEach(btn => {
        btn.addEventListener('click', function () {
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const type = btn.getAttribute('data-type');

            // 显示对应的内容区域
            Object.keys(lists).forEach(key => {
                if (lists[key]) {
                    if (key === type) {
                        lists[key].style.display = 'block';
                        lists[key].style.opacity = '1';
                    } else {
                        lists[key].style.display = 'none';
                        lists[key].style.opacity = '0';
                    }
                }
            });

            // 重新应用当前类别筛选
            const currentCategory = categoryFilter ? categoryFilter.value : 'all';
            filterPostsByCategory(currentCategory);

            // 更新URL参数但不刷新页面
            updateURLParams(type, currentCategory, false);
        });
    });

    // 类别筛选
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function () {
            const currentType = document.querySelector('.uz-filter-btn.active').getAttribute('data-type');
            const selectedCategory = this.value;

            // 客户端筛选：隐藏/显示对应类别的帖子
            filterPostsByCategory(selectedCategory);

            // 更新URL参数但不刷新页面
            updateURLParams(currentType, selectedCategory, false);
        });
    }

    // 客户端筛选帖子
    function filterPostsByCategory(category) {
        const currentType = document.querySelector('.uz-filter-btn.active').getAttribute('data-type');
        const currentList = lists[currentType];

        if (!currentList) return;

        const posts = currentList.querySelectorAll('.uz-post-card');

        posts.forEach(post => {
            const categoryBadge = post.querySelector('.uz-category-badge');
            if (categoryBadge) {
                const postCategory = categoryBadge.getAttribute('data-category');
                if (category === 'all' || postCategory === category) {
                    post.style.display = '';
                    post.style.opacity = '1';
                } else {
                    post.style.display = 'none';
                    post.style.opacity = '0';
                }
            }
        });
    }

    // 更新URL参数
    function updateURLParams(type, category, reload = false) {
        const url = new URL(window.location);
        url.searchParams.set('type', type);
        url.searchParams.set('category', category);

        if (reload) {
            window.location.href = url.toString();
        } else {
            // 使用history API更新URL而不刷新页面
            window.history.pushState({}, '', url.toString());
        }
    }

    // 关注/取关按钮AJAX
    const followForm = document.getElementById('follow-form');
    if (followForm) {
        console.log('fetching', followForm.action);
        followForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const btn = document.getElementById('follow-btn');
            btn.disabled = true;
            fetch(followForm.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': followForm.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        btn.textContent = data.followed ? '已关注' : '关注';
                        // 刷新粉丝数
                        const followerNum = document.querySelector('.uz-follower-num');
                        if (followerNum) followerNum.textContent = data.follower_count;
                    } else {
                        alert(data.msg || '操作失败');
                    }
                })
                .catch(() => alert('网络错误'))
                .finally(() => { btn.disabled = false; });
        });
    }

    // 私信按钮点击跳转到聊天室
    const messageBtn = document.querySelector('.uz-btn-message');
    if (messageBtn) {
        messageBtn.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = '/chat/';
        });
    }
});

// 图片预览功能
function showImagePreview(src, alt) {
    // 创建遮罩层
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        cursor: pointer;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;

    // 创建图片容器
    const imgContainer = document.createElement('div');
    imgContainer.style.cssText = `
        max-width: 90%;
        max-height: 90%;
        position: relative;
    `;

    // 创建图片
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt;
    img.style.cssText = `
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 12px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    `;

    // 创建关闭按钮
    const closeBtn = document.createElement('div');
    closeBtn.innerHTML = '×';
    closeBtn.style.cssText = `
        position: absolute;
        top: -40px;
        right: 0;
        width: 30px;
        height: 30px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 20px;
        cursor: pointer;
        transition: background 0.3s ease;
    `;

    closeBtn.addEventListener('mouseenter', function () {
        this.style.background = 'rgba(255, 255, 255, 0.3)';
    });

    closeBtn.addEventListener('mouseleave', function () {
        this.style.background = 'rgba(255, 255, 255, 0.2)';
    });

    // 组装并添加到页面
    imgContainer.appendChild(img);
    imgContainer.appendChild(closeBtn);
    overlay.appendChild(imgContainer);
    document.body.appendChild(overlay);

    // 显示动画
    setTimeout(() => {
        overlay.style.opacity = '1';
    }, 10);

    // 关闭事件
    const closePreview = () => {
        overlay.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(overlay);
        }, 300);
    };

    overlay.addEventListener('click', closePreview);
    closeBtn.addEventListener('click', closePreview);

    // ESC键关闭
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            closePreview();
        }
    });
}

// 点赞动画
function animateLike(button) {
    const icon = button.querySelector('.uz-post-action-icon');
    const originalText = icon.textContent;

    // 创建心形动画
    icon.textContent = '❤️';
    icon.style.transform = 'scale(1.5)';
    icon.style.transition = 'transform 0.3s ease';

    // 添加粒子效果
    createHeartParticles(button);

    setTimeout(() => {
        icon.style.transform = 'scale(1)';
        setTimeout(() => {
            icon.textContent = originalText;
        }, 150);
    }, 300);
}

// 创建心形粒子效果
function createHeartParticles(container) {
    for (let i = 0; i < 6; i++) {
        const particle = document.createElement('span');
        particle.textContent = '❤️';
        particle.style.cssText = `
            position: absolute;
            font-size: 12px;
            pointer-events: none;
            animation: floatUp 1s ease-out forwards;
            z-index: 1000;
        `;

        const rect = container.getBoundingClientRect();
        particle.style.left = rect.left + Math.random() * rect.width + 'px';
        particle.style.top = rect.top + Math.random() * rect.height + 'px';

        document.body.appendChild(particle);

        setTimeout(() => {
            document.body.removeChild(particle);
        }, 1000);
    }
}

// 数字动画
function animateNumbers() {
    const numbers = document.querySelectorAll('.uz-stat-number');

    numbers.forEach(number => {
        const finalValue = parseInt(number.textContent);
        const duration = 2000;
        const startTime = Date.now();

        function updateNumber() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = Math.floor(finalValue * progress);

            number.textContent = currentValue;

            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        }

        updateNumber();
    });
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes floatUp {
        0% {
            transform: translateY(0) scale(1);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) scale(0);
            opacity: 0;
        }
    }
    
    @keyframes slideInUp {
        from {
            transform: translateY(30px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .uz-card {
        animation: slideInUp 0.6s ease-out;
    }
`;
document.head.appendChild(style);

