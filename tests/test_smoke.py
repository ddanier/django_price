def test_smoke():
    """Just some basic smoke tests (syntax, app loading)"""
    import django_price
    import django_price.currency
    import django_price.fields
    import django_price.models
    import django_price.price
    import django_price.tax
    import django_price.utils


def test_system_checks():
    import django

    if django.VERSION >= (1, 7, 0):
        from django.core import checks

        if django.VERSION >= (1, 8, 0):
            assert not checks.run_checks(include_deployment_checks=False), "Some Django system checks failed"
        else:
            assert not checks.run_checks(), "Some Django system checks failed"
