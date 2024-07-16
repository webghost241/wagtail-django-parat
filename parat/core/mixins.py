class UUIDSlugMixin:
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(uuid=self.kwargs["uuid"])
        return context
