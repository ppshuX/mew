from django.db import models
from django.contrib.auth.models import User
from user_profile.models import UserProfile

# Create your models here.

class UserZoneVisitor(models.Model):
    userzone_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='visited_userzone')  # 被访问者
    visitor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='userzone_visited')  # 访客
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visited_at']
        unique_together = ('userzone_owner', 'visitor')

    def __str__(self):
        return f"{self.visitor.user.username} 访问了 {self.userzone_owner.user.username} 的空间"
