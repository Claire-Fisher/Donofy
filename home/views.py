from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def contact(request):
    """ A view to return the Contact Us page """

    return render(request, 'home/contact_us.html')


def contact_send(request):
    """ A view for contact us form functionality"""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        send_mail(
            f'Contact Form Submission from {name}',
            message,
            email,
            ['donofy.uk@gmail.com'],
            fail_silently=False,
        )
        return redirect('contact_success')
    else:
        messages.error(
            request,
            "Please check your form is valid and try again."
        )

    return render(request, 'home/contact.html')


def contact_success(request):
    """ A view to render contact_success page"""
    return render(request, 'home/contact_success.html')


def custom_404(request, exception=None):
    """
    Render custom 404 error template
    """
    return render(request, '404.html', status=404)
