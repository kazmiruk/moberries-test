from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Moberries Pizza Shop API",
        default_version='v1',
        description="Moberries home assignment api",
    ),
    public=True,
)
