from django import template
from django.conf import settings

register = template.Library()


@register.filter
def reorder_app_list(app_list):
    if len(app_list) == 0:
        return app_list

    conf = getattr(settings, 'ADMIN_APP_LIST', None)

    if conf is None:
        return app_list

    app_mapping = {app['app_label']: app for app in app_list}
    new_app_list = []

    for app_conf in conf:

        if isinstance(app_conf, str):
            app_label = app_conf
            models_conf = None
        else:
            app_label = app_conf['app']
            models_conf = app_conf['models']

        app = app_mapping.get(app_label)

        if app is None:
            continue

        if models_conf is None:
            new_app_list.append(app)

        elif len(models_conf) > 0:
            model_mapping = {model['object_name'].lower(): model for model in app['models']}
            new_model_list = []

            for model_name in models_conf:
                model = model_mapping.get(model_name.lower())
                if model is not None:
                    new_model_list.append(model)

            app['models'] = new_model_list
            new_app_list.append(app)

    return new_app_list
