from django.db import models
from accounts.models import User # accounts 앱의 models.py에 있는 User 모델을 불러오겠다는 의미. 왜 불러오느냐? 게시물 작성할 때 writer에 유저 정보가 필요하기 때문에!
from main.models import Cinema # main 앱의 models.py에 있는 Cinema 모델을 불러오겠다는 의미. 커뮤니티 영화관 후기에서 '영화관 선택'이 있으므로 Cinema와 연결

# Create your models here.
def community_image_upload_path(instance, filename):
    return f'community/{instance.community.id}/{filename}'

class Community(models.Model):
    id = models.AutoField(primary_key=True)
    cinema = models.ForeignKey(Cinema, blank=False, null=True, on_delete=models.CASCADE, related_name='community_cinema')
    CATEGORY_LIST = (
        ('common', 'common'),
        ('cinema_tip', 'cinema_tip'),
        ('suggestion', 'suggestion'),
    )
    category = models.CharField(max_length=10, choices=CATEGORY_LIST, blank=False, null=False)
    writer = models.CharField(max_length=10, blank=False, null=False) # User 모델과 ForeignKey로 연결해야 하지만 지금은 일단 외래키 연결 안 하고 사용
    title = models.CharField(max_length=30)
    content = models.TextField(null=False, max_length=5000)
    view_cnt = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommunityComment(models.Model):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, blank=False, null=False, on_delete=models.CASCADE, related_name='comments_community')
    writer = models.CharField(max_length=10, blank=False, null=False)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommunityImage(models.Model):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='images_community')
    image = models.ImageField(upload_to=community_image_upload_path)

class CommunityLike(models.Model):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, blank=False, null=False, on_delete=models.CASCADE, related_name='likes_community')
    user = models.CharField(max_length=10, blank=False, null=False)