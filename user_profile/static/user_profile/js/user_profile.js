// 头像上传预览
window.addEventListener('DOMContentLoaded', function () {
    var avatarInput = document.querySelector('input[type="file"][name$="avatar"]');
    var previewImg = document.querySelector('.user-profile-avatar-preview');
    if (avatarInput && previewImg) {
        avatarInput.addEventListener('change', function (e) {
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = function (ev) {
                    previewImg.src = ev.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
}); 