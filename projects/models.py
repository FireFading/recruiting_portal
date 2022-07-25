from django.db import models
from django.utils.text import slugify
import uuid

from users.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default='default.jpg', upload_to='project_images')
    tags = models.ManyToManyField(Tag, blank=True)
    total_votes = models.IntegerField(default=0, null=True, blank=True)
    votes_ratio = models.IntegerField(default=0, null=True, blank=True)
    demo_link = models.CharField(max_length=500, null=True, blank=True)
    source_link = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    
class Review(models.Model):
    owner = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    review_text = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
        unique_together = [['owner', 'project']]
    
    def __str__(self):
        return self.value
    
    

