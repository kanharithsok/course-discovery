""" API v1 URLs. """
from django.urls import include, path, re_path
from rest_framework import routers

from course_discovery.apps.api.v1.views import search as search_views
from course_discovery.apps.api.v1.views.affiliates import AffiliateWindowViewSet, ProgramsAffiliateWindowViewSet
from course_discovery.apps.api.v1.views.bulk_operation_tasks import BulkOperationTaskViewSet
from course_discovery.apps.api.v1.views.catalog_queries import CatalogQueryContainsViewSet
from course_discovery.apps.api.v1.views.catalogs import CatalogViewSet
from course_discovery.apps.api.v1.views.collaborators import CollaboratorViewSet
from course_discovery.apps.api.v1.views.comments import CommentViewSet
from course_discovery.apps.api.v1.views.course_editors import CourseEditorViewSet
from course_discovery.apps.api.v1.views.course_review import CourseReviewViewSet
from course_discovery.apps.api.v1.views.course_runs import CourseRunViewSet
from course_discovery.apps.api.v1.views.courses import CourseRecommendationViewSet, CourseViewSet
from course_discovery.apps.api.v1.views.currency import CurrencyView
from course_discovery.apps.api.v1.views.level_types import LevelTypeViewSet
from course_discovery.apps.api.v1.views.organizations import OrganizationViewSet
from course_discovery.apps.api.v1.views.pathways import PathwayViewSet
from course_discovery.apps.api.v1.views.people import PersonViewSet
from course_discovery.apps.api.v1.views.program_types import ProgramTypeViewSet
from course_discovery.apps.api.v1.views.programs import ProgramViewSet
from course_discovery.apps.api.v1.views.sources import SourceViewSet
from course_discovery.apps.api.v1.views.subjects import SubjectViewSet
from course_discovery.apps.api.v1.views.topics import TopicViewSet
from course_discovery.apps.api.v1.views.user_management import UsernameReplacementView

app_name = 'v1'

partners_router = routers.SimpleRouter()
partners_router.register(r'affiliate_window/catalogs', AffiliateWindowViewSet, basename='affiliate_window')
partners_router.register(
    r'affiliate_window/programs/catalogs',
    ProgramsAffiliateWindowViewSet,
    basename='programs_affiliate_window'
)

urlpatterns = [
    path('partners/', include((partners_router.urls, 'partners'))),
    path('search/typeahead', search_views.TypeaheadSearchView.as_view(), name='search-typeahead'),
    path('search/person_typeahead/', search_views.PersonTypeaheadSearchView.as_view(), name='person-search-typeahead'),
    path('currency', CurrencyView.as_view(), name='currency'),
    re_path(r'^catalog/query_contains/?', CatalogQueryContainsViewSet.as_view(), name='catalog-query_contains'),
    path('replace_usernames/', UsernameReplacementView.as_view(), name="replace_usernames"),
]


router = routers.SimpleRouter()
router.register(r'catalogs', search_views.CourseSearchViewSet)
router.register(r'comments', search_views.CourseSearchViewSet, basename='comment')
router.register(r'courses', search_views.CourseSearchViewSet, basename='course')
router.register(r'course_recommendations', search_views.CourseSearchViewSet, basename='course_recommendations')
router.register(r'course_editors', search_views.CourseSearchViewSet, basename='course_editor')
router.register(r'course_review', search_views.CourseSearchViewSet, basename='course-review')
router.register(r'course_runs', search_views.CourseSearchViewSet, basename='course_run')
router.register(r'bulk_operation_tasks', search_views.CourseSearchViewSet, basename='bulkoperationtask')
router.register(r'collaborators', search_views.CourseSearchViewSet, basename='collaborator')
router.register(r'organizations', search_views.CourseSearchViewSet, basename='organization')
router.register(r'sources', search_views.CourseSearchViewSet, basename='source')
router.register(r'people', search_views.CourseSearchViewSet, basename='person')
router.register(r'subjects', search_views.CourseSearchViewSet, basename='subject')
router.register(r'topics', search_views.CourseSearchViewSet, basename='topic')
router.register(r'pathways', search_views.CourseSearchViewSet, basename='pathway')
router.register(r'programs', search_views.CourseSearchViewSet, basename='program')
router.register(r'level_types', search_views.CourseSearchViewSet, basename='level_type')
router.register(r'program_types', search_views.CourseSearchViewSet, basename='program_type')
router.register(r'search/limited', search_views.CourseSearchViewSet, basename='search-limited')
router.register(r'search/all', search_views.CourseSearchViewSet, basename='search-all')
router.register(r'search/courses', search_views.CourseSearchViewSet, basename='search-courses')
router.register(r'search/course_runs', search_views.CourseSearchViewSet, basename='search-course_runs')
router.register(r'search/programs', search_views.CourseSearchViewSet, basename='search-programs')
router.register(r'search/people', search_views.CourseSearchViewSet, basename='search-people')


urlpatterns += router.urls
