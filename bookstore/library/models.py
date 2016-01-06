from django.db import models


# Create your models here.

class Publisher(models.Model):
    '''
        Définit la table Publisher
        '''

    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)


    def __str__(self):
        return self.name


class Topic(models.Model):
    topic_name = models.CharField(max_length=20)

    def __str__(self):
        return self.topic_name


class Book(models.Model):
    '''
        Définit la table Book
        '''
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    topic = models.ManyToManyField(Topic)
    editor = models.ForeignKey(Publisher)

    def __str__(self):
        return self.title
