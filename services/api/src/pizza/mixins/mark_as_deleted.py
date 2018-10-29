from rest_framework import response


class MarkAsDeletedMixin(object):
    def destroy(self, *args, **kwargs):
        obj = self.get_object()
        obj.is_deleted = True
        obj.save()

        return response.Response(status=204)
