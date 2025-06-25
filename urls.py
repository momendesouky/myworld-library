from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin views
    path('admin/books/', views.admin_book_list, name='admin_book_list'),
    path('admin/books/add/', views.add_book, name='add_book'),
    path('admin/books/edit/<str:book_id>/', views.edit_book, name='edit_book'),
    path('admin/books/delete/<str:book_id>/', views.delete_book, name='delete_book'),
    
    # User views
    path('books/', views.browse_books, name='browse_books'),
    path('books/<str:book_id>/', views.book_detail, name='book_detail'),
    path('books/<str:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/<str:book_id>/return/', views.return_book, name='return_book'),
    path('my-books/', views.borrowed_books, name='borrowed_books'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)