# -*- coding: utf-8 -*-
import django
import pytest

from .resource_app.models import TestModel


def test_django_version():
    assert django.VERSION == (1, 9, 13, 'final', 0)


@pytest.mark.django_db
def test_filter():
    tm = TestModel.objects.create(case_char='char', case_slug='slug')
    result1 = TestModel.objects.filter(case_char__contains='ha')
    result2 = TestModel.objects.filter(case_slug__icontains='LU')
    result3 = TestModel.objects.filter(case_char__contains='x')
    assert tm in list(result1)
    assert tm in list(result2)
    assert tm not in list(result3)


@pytest.mark.django_db
def test_int_array_filters():
    tm = TestModel.objects.create(int_array=[1, 2, 3])
    result1 = TestModel.objects.filter(int_array__array_contains=[1])
    result2 = TestModel.objects.filter(int_array__array_contained=[2, 3])
    result3 = TestModel.objects.filter(int_array__array_contains=[4])
    result4 = TestModel.objects.filter(int_array__array_overlaps=[1, 4])
    assert tm in list(result1)
    assert tm in list(result2)
    assert tm not in list(result3)
    assert tm in list(result4)


@pytest.mark.django_db
def test_txt_array_filters():
    tm = TestModel.objects.create(txt_array=['1', '2', '3'])
    result1 = TestModel.objects.filter(txt_array__array_contains=['1'])
    result2 = TestModel.objects.filter(txt_array__array_contained=['2', '3'])
    result3 = TestModel.objects.filter(txt_array__array_contains=['4'])
    result4 = TestModel.objects.filter(txt_array__array_overlaps=['1', '4'])
    assert tm in list(result1)
    assert tm in list(result2)
    assert tm not in list(result3)
    assert tm in list(result4)
