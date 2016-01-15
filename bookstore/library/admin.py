from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Topic)
admin.site.register(Author)
admin.site.register(Reservation)
admin.site.register(Customer)
admin.site.register(CustomerType)
admin.site.register(BookCopy)
