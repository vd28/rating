from django import template
from django.conf import settings

register = template.Library()


@register.filter
def reorder_app_list(app_list):
    conf = getattr(settings, 'ADMIN_APP_LIST', None)

    if conf is None:
        return app_list

    app_mapping = {}
    for app in app_list:
        app_mapping[app['app_label']] = (
            app,
            {model['object_name'].lower(): model for model in app['models']}
        )

    new_app_list = []

    for app_conf in conf:

        if isinstance(app_conf, str):
            app_label = app_conf
            models_conf = None
        else:
            app_label = app_conf['app']
            models_conf = app_conf['models']

        if app_label not in app_mapping:
            continue

        app, model_mapping = app_mapping[app_label]

        if models_conf is None:
            new_app_list.append(app)

        else:
            new_model_list = []

            for model_name in models_conf:
                model_name = model_name.lower()
                if model_name in model_mapping:
                    new_model_list.append(model_mapping[model_name])

            app['models'] = new_model_list
            new_app_list.append(app)

    return new_app_list
