from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50, blank=True)
    writer = models.CharField(max_length=50)
    date_time = models.DateField(auto_now_add=True)
    content = models.TextField(blank = True, null = True)

    class Meta:
        db_table = "article"

    def __str__(self):
        return self.title

    # class Meta:  #按时间下降排序
    #     ordering = ['-created_date']