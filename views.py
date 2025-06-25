from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from .models import Book, BorrowRecord, User
from .forms import BookForm, UserRegistrationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'auth/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Replace with your desired redirect
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/signup.html', {'form': form})
@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_book_list')
    return redirect('browse_books')

@staff_member_required
def admin_book_list(request):
    books = Book.objects.all()
    return render(request, 'admin/book_list.html', {'books': books})

@staff_member_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('admin_book_list')
    else:
        form = BookForm()
    return render(request, 'admin/add_book.html', {'form': form})

@staff_member_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('admin_book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'admin/edit_book.html', {'form': form})

@staff_member_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('admin_book_list')
    return render(request, 'admin/delete_book.html', {'book': book})

@login_required
def browse_books(request):
    books = Book.objects.all()
    return render(request, 'user/browse.html', {'books': books})

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'user/book_detail.html', {'book': book})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.status == 'available':
        book.status = 'borrowed'
        book.borrowed_by = request.user
        book.due_date = timezone.now() + timezone.timedelta(days=14)
        book.save()
        
        BorrowRecord.objects.create(
            book=book,
            user=request.user,
            due_date=book.due_date
        )
        messages.success(request, 'Book borrowed successfully!')
    return redirect('book_detail', book_id=book.id)

@login_required
def return_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.status == 'borrowed' and book.borrowed_by == request.user:
        book.status = 'available'
        book.borrowed_by = None
        book.due_date = None
        book.save()
        
        record = BorrowRecord.objects.filter(book=book, user=request.user, returned=False).first()
        if record:
            record.returned = True
            record.save()
        messages.success(request, 'Book returned successfully!')
    return redirect('borrowed_books')

@login_required
def borrowed_books(request):
    borrowed_books = BorrowRecord.objects.filter(user=request.user, returned=False)
    return render(request, 'user/borrowed.html', {'borrowed_books': borrowed_books})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')