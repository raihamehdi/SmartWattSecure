
from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse,NoReverseMatch
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin


class RestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is restricted
            if request.user.is_restricted:
                # Log out the user
                logout(request)
                # Redirect to the login page or any other page
                return redirect('login')  # Change 'login' to your login URL name

        response = self.get_response(request)
        return response


class SeparateSessionMiddleware(MiddlewareMixin):
    """
    Middleware to ensure separate sessions for staff (admin) users and regular users.
    """

    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                # Resolve the admin panel URL
                admin_url = reverse('adminview')  
            except NoReverseMatch:
                admin_url = '/adminpanel/'  # Fallback to the hardcoded URL if reverse fails

            # If the user is staff (admin), ensure they access only admin pages
            if request.user.is_staff:
                # If accessing a non-admin page, log them out
                if not request.path.startswith(admin_url) and not request.path.startswith('/admin/'):
                    logout(request)
                    return redirect(admin_url)  # Redirect to admin panel

            # If the user is not staff (regular user), ensure they access only user pages
            else:
                try:
                    user_dashboard_url = reverse('dashboard')  # Resolve the user dashboard URL
                except NoReverseMatch:
                    user_dashboard_url = '/'  # Fallback to the homepage

                # If accessing an admin page, log them out
                if request.path.startswith(admin_url) or request.path.startswith('/admin/'):
                    logout(request)
                    return redirect('/admin-login/')  # Redirect to admin login

        return None
