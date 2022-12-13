from django.db import models
import uuid
from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = [
            "title",
            "-created",  # -vote_ratio", "-vote_total"
        ]

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list(
            "owner__id", flat=True
        )  # flat= True converts this variable into a list
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value="UP").count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):

    VOTE_TYPE = (("UP", "UP VOTE"), ("DOWN", "DOWN VOTE"))
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = [["owner", "project"]]

    def __str__(self) -> str:
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self) -> str:
        return self.name


# one to many - use models.foreignKey in the child table
# many to many - link model that will be many to the other table that will be many using the models.ManyToManyField
