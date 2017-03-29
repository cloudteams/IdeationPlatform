import json

from django.db import models
from django.db.models import Count

from bm_canvas.lists import BUSINESS_MODEL_SECTIONS

DEFAULT_PALETTE_CONFIG = {
    'FFFFFF': 'No tag',
    'FFF': 'No tag',
    'EF4836': 'Danger',
    '7D3C8C': 'Main action',
    '4183D7': 'Ongoing',
    'E9D460': 'Blocking',
    '67809F': 'Pending approval',
    '1BBC9B': 'Complete',
    'F89406': 'Idea',
    '65C6BB': 'Innovation',
    '6C7A89': 'Design',
    'BDC3C7': 'Testing',
    '333333': 'Competitive advantage',
    '333': 'Competitive advantage',
}


class BusinessModel(models.Model):
    """
    The Business Model for a Customer Platform Project
    """
    id = models.AutoField(primary_key=True)
    project_id = models.IntegerField()
    project_name = models.CharField(max_length=1023)
    title = models.TextField(default='Business Model #1')
    palette_config = models.TextField(default=json.dumps(DEFAULT_PALETTE_CONFIG))

    def __str__(self):
        return 'Business Model <%s> for Project #%d' % (self.title, self.project_id)

    @property
    def groups(self):
        result = self.entries.values('group_color').annotate(cnt=Count('id')).order_by('-cnt')
        for group in result:
            try:
                label = json.loads(self.palette_config)[group['group_color'][1:].upper()]
            except KeyError:
                label = ''

            if not label:
                label = 'No tag'

            group['label'] = label

        return result

    @property
    def tags(self):
        result = []
        colors = json.loads(self.palette_config)
        for color in colors:
            result.append({
                'label': colors[color],
                'color': '#' + color,
            })

        return result


class BusinessModelEntry(models.Model):
    """
    An entry under some section of the Business Model of a project
    """
    business_model = models.ForeignKey(BusinessModel, related_name='entries')
    author = models.CharField(max_length=255)
    section = models.CharField(max_length=255, choices=BUSINESS_MODEL_SECTIONS)
    text = models.TextField(blank=False)
    order = models.IntegerField()
    group_color = models.CharField(max_length=7, default='#FFFFFF')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return 'Entry #%d (%s) under <%d>' % (self.pk, self.section, self.business_model_id)

    def can_access(self, request):
        for p in request.session['projects']:
            if int(p['pid']) == self.business_model.project_id:
                return True

        return False

    def can_update(self, request):
        return self.can_access(request)

    @property
    def group(self):
        try:
            result = json.loads(self.business_model.palette_config)[self.group_color[1].upper()]
        except KeyError:
            result = ''

        if not result:
            result = 'No tag'

        return result