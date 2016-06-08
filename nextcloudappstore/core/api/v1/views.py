from nextcloudappstore.core.api.v1.serializers import AppSerializer
from nextcloudappstore.core.models import App
from nextcloudappstore.core.permissions import AllowedToEditApp
from nextcloudappstore.core.versioning import app_has_included_release
from rest_framework import authentication
from rest_framework.generics import GenericAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class Apps(DestroyAPIView):
    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, AllowedToEditApp)
    serializer_class = AppSerializer
    queryset = App.objects.all()

    def get(self, request, *args, **kwargs):
        apps = App.objects.prefetch_related('categories', 'authors',
                                            'releases', 'screenshots',
                                            'releases__databases',
                                            'releases__libs').all()

        def app_filter(app):
            return app_has_included_release(app, self.kwargs['version'])

        working_apps = list(filter(app_filter, apps))
        serializer = self.get_serializer(working_apps, many=True)
        return Response(serializer.data)


class AppReleases(GenericAPIView):
    pass