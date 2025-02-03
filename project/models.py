from django.db import models

class Languages(models.Model):
    lang_key= models.CharField(max_length=255, null=False)
    lang_name= models.CharField(max_length=255, null=False)
    def __str__(self):
        return self.lang_name
    
class Pages(models.Model):
    page_name = models.CharField(max_length=255)
    def __str__(self):
        return self.page_name
    
class CombinationLanguageAndPage(models.Model):
    lang = models.ForeignKey(Languages, on_delete=models.CASCADE)
    page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    key = models.CharField(max_length=5000)
    value = models.CharField(max_length=5000)

class AddImages(models.Model):
    page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    image_key = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return f"Image {self.id}"