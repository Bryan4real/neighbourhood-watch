from django.contrib import admin
from .models import Profile,Neighbourhood,Post,Business,NeighbourhoodAdmin,SystemAdmin,Contact
# Register your models here.


admin.site.register(Neighbourhood)
admin.site.register(Profile)
admin.site.register(Business)
admin.site.register(Post)
admin.site.register(NeighbourhoodAdmin)
admin.site.register(SystemAdmin)
admin.site.register(Contact)
