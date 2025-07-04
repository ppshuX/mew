// 聊天室页面独立JS
// 聊天自动滚动到底部
$(function () {
    var $chatBox = $('#chat-box');
    if ($chatBox.length) {
        $chatBox.scrollTop($chatBox[0].scrollHeight);
    }

    // 移动端切换逻辑
    function isMobile() {
        return window.innerWidth <= 700;
    }
    window.isMobile = isMobile; // 兼容外部调用
    window.mobileBackToList = function () {
        $('#chat-container').removeClass('mobile-chat-active');
    };

    // 用户点击跳转
    $('.chat-user-item').on('click', function () {
        if (isMobile()) {
            $('#chat-container').addClass('mobile-chat-active');
        }
        var userId = $(this).data('user-id');
        if (userId) {
            window.location.href = '?user=' + userId;
        }
    });

    // 聊天用户实时搜索
    $('#chat-user-search').on('input', function () {
        var kw = $(this).val().toLowerCase();
        $('#chat-user-list .chat-user-item').each(function () {
            var username = $(this).data('username');
            if (username && username.toLowerCase().indexOf(kw) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('chat-user-search');
    const userItems = document.querySelectorAll('.chat-user-item');
    const noUserFound = document.getElementById('no-user-found');

    searchInput.addEventListener('input', function () {
        const keyword = this.value.toLowerCase().trim();
        let hasMatch = false;

        userItems.forEach(item => {
            const username = item.getAttribute('data-username');
            if (username && username.includes(keyword)) {
                item.style.display = '';
                hasMatch = true;
            } else {
                item.style.display = 'none';
            }
        });

        // 是否显示"没有匹配项"
        if (noUserFound) {
            noUserFound.style.display = hasMatch ? 'none' : 'block';
        }
    });
});