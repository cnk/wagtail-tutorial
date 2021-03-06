from django.apps import AppConfig


class WagtailPatchesConfig(AppConfig):
    name = 'wagtail_patches'
    verbose_name = 'Wagtail Patches'
    ready_is_done = False

    def ready(self):
        """
        This function runs as soon as the app is loaded. to apply our monkey patches
        """
        # As suggested by the Django docs, we need to make absolutely certain that this code runs only once.
        if not self.ready_is_done:
            # The act of performing this import executes all the code in monkey_patches.
            from . import monkey_patches  # noqa
            # # Unlike monkey_patches, the code of wagtail_hook_patches is in the function patch_hooks().
            # from .wagtail_hook_patches import patch_hooks
            # patch_hooks()

            self.ready_is_done = True
        else:
            print("{}.ready() executed more than once! This method's code is skipped on subsequent runs.".format(
                self.__class__.__name__
            ))
