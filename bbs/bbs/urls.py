import os.path
from django.conf.urls.defaults import *
from bbsapp.views import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

site_media = os.path.join(
                          os.path.dirname(__file__),'../site_media'
                          )

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bbs.views.home', name='home'),
    # url(r'^bbs/', include('bbs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),

    #page view
    (r'^bbs/$',list_page),
    (r'^bbs/write/$',write_page),
    (r'^bbs/(\d+)/$',view_page),
    (r'^bbs/(\d+)/delete/$',delete_page),
    (r'^bbs/(\d+)/modify/$',modify_page),
    (r'^bbs/(\d+)/comment/$',comment_page),
#    (r'^delete/(\d+)/$',  'moderation.delete', name='comments-delete'),
    
    #sseion
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':site_media}),
    (r'^$', 'django.contrib.auth.views.login'),
    (r'^logout/$',logout_page),
    (r'^register/$',register_page),
    (r'^register/success/$',direct_to_template,{'template':'registration/register_success.html'}),
    
#    (r'^comments/$',include('django.contrib.comments.urls')),
)

#urlpatterns += patterns('',
#                        url(r'^comments/$',include('django.contrib.comments.urls')),
#                        )
