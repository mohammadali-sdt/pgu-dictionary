from django.shortcuts import render


def handle_not_found_page(request, exception):
    return render(request, 'dictionary/not_found_page.html')
