from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from tendenci.core.categories.forms import CategoryField
from tendenci.core.categories.models import CategoryItem
from tendenci.core.files.models import File
from tendenci.core.perms.forms import TendenciBaseForm
from tendenci.apps.user_groups.models import Group


class FileForm(TendenciBaseForm):

    group = forms.ModelChoiceField(required=True, queryset=Group.objects.filter(status=True, status_detail='active'), empty_label=None)

    class Meta:
        model = File

        fields = (
            'file',
            'name',
            'group',
            'tags',
            'allow_anonymous_view',
            'user_perms',
            'member_perms',
            'group_perms',
            'status',
        )

        fieldsets = [('', {
                      'fields': [
                        'file',
                        'name',
                        'group',
                        'tags',
                      ],
                      'legend': ''
                      }),

                      ('Permissions', {
                      'fields': ['allow_anonymous_view',
                                 'user_perms',
                                 'member_perms',
                                 'group_perms',
                                 ],
                      'classes': ['permissions'],
                      }),

                     ('Administrator Only', {
                      'fields': ['status',
                                 'status_detail'],
                      'classes': ['admin-only'],
                    })]

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user', None)
        else:
            self.user = None

        super(FileForm, self).__init__(*args, **kwargs)


class SwfFileForm(TendenciBaseForm):

    class Meta:
        model = File

        fields = (
            'file',
            'name',
            'allow_anonymous_view',
            'user_perms',
            'member_perms',
            'group_perms',
            'status',
        )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user', None)
        else:
            self.user = None

        super(SwfFileForm, self).__init__(*args, **kwargs)


class MostViewedForm(forms.Form):
    """
    Takes in the date range and files type you're
    searching for and returns back a result list.
    """

    TYPES = (
      ('all', 'All File Types'),
      ('pdf', 'PDF Documents'),
      ('slides', 'Slides'),
      ('spreadsheet', 'Spreadsheets'),
      ('text', 'Text Documents'),
      ('zip', 'Zip Files'),
    )

    start_dt = forms.DateField(label='Start')
    end_dt = forms.DateField(label='End')
    file_type = forms.ChoiceField(label='File Type', choices=TYPES)

    def __init__(self, *args, **kwargs):
        super(MostViewedForm, self).__init__(*args, **kwargs)
        self.fields['file_type'].widget.attrs['class'] = 'btn'


class FileSearchForm(forms.Form):
    q = forms.CharField(label=_("Search"), required=False, max_length=200,)
    category = CategoryField(label=_('Category'), choices=[], required=False)
    sub_category = CategoryField(label=_('Sub Category'), choices=[], required=False)
    group = forms.ChoiceField(label=_('Group'), choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(FileSearchForm, self).__init__(*args, **kwargs)

        groups = Group.objects.filter(status=True, status_detail='active')
        groups = [[g.id, g.name] for g in groups]
        groups.insert(0, ['', '------------'])
        self.fields['group'].choices = tuple(groups)

        content_type = ContentType.objects.get(app_label='files', model='file')
        categories = CategoryItem.objects.filter(content_type=content_type,
                                                 parent__exact=None)
        categories = list(set([cat.category.name for cat in categories]))
        categories = [[cat, cat] for cat in categories]
        categories.insert(0, ['', '------------'])
        self.fields['category'].choices = tuple(categories)

        # set up the sub category choices
        sub_categories = CategoryItem.objects.filter(content_type=content_type,
                                                     category__exact=None)
        sub_categories = list(set([cat.parent.name for cat in sub_categories]))
        sub_categories = [[cat, cat] for cat in sub_categories]
        sub_categories.insert(0, ['', '------------'])
        self.fields['sub_category'].choices = tuple(sub_categories)
