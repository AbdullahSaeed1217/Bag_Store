from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.HomePage,name='store/home/'),
    path('view-product/<int:product_id>',views.view_product, name='view_product'),
    path('about-us',views.AboutUs,name='store/about_us'),
    path('blog',views.Blog,name='store/blog'),
    path('contact_us',views.Contact,name='store/contact_us'),

    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)