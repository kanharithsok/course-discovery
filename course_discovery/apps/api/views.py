from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from drf_yasg.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from django.db.models import Q


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        CoreJSONRenderer,
        OpenAPIRenderer,
        SwaggerUIRenderer,
    ]

    exclude_from_schema = True

    def get(self, request):
        generator = SchemaGenerator(title='Discovery API')
        schema = generator.get_schema(request=request)
        if not schema:
            # get_schema() uses the same permissions check as the API endpoints.
            # If we don't get a schema document back, it means the user is not
            # authenticated or doesn't have permission to access the API.
            # api_docs_permission_denied_handler() handles both of these cases.
            return api_docs_permission_denied_handler(request)
        elif schema and request.user and request.user.is_anonymous:
            return _redirect_to_login(request)

        return Response(schema)


def _redirect_to_login(request):
    login_url = '{path}?next={next}'.format(path=reverse('login'), next=request.path)
    return redirect(login_url, permanent=False)


def api_docs_permission_denied_handler(request):
    """
    Permission denied handler for calls to the API documentation.

    Args:
        request (Request): Original request to the view the documentation

    Raises:
        PermissionDenied: The user is not authorized to view the API documentation.

    Returns:
        HttpResponseRedirect: Redirect to the login page if the user is not logged in. After a
            successful login, the user will be redirected back to the original path.
    """
    if request.user and request.user.is_authenticated:
        raise PermissionDenied(_('You are not permitted to access the API documentation.'))
    return _redirect_to_login(request)


def get_queryset(self):
    """
    Get the list of courses for the view.
    """
    queryset = super().get_queryset()
    user = self.request.user

    # If user is not authenticated, return only public courses
    if not user.is_authenticated:
        return queryset.filter(public=True)

    # If user is staff, return all courses
    if user.is_staff:
        return queryset

    # Get user's email domain
    user_email_domain = user.email.split('@')[-1] if user.email else None

    # Filter courses based on organization and email domain
    return queryset.filter(
        Q(public=True) |  # Public courses are always accessible
        Q(organizations__key='CBC-Internal', organizations__isnull=False) &  # CBC-Internal courses
        Q(organizations__key='CBC-Internal', organizations__isnull=False, organizations__users__email__endswith='@yopmail.com') |  # Only yopmail.com users can access CBC-Internal courses
        Q(organizations__users=user)  # Courses from user's organizations
    ).distinct()
