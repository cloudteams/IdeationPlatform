from django.db import models

from bm_canvas.lists import BUSINESS_MODEL_SECTIONS


class BusinessModel(models.Model):
    """
    The Business Model for a Customer Platform Project
    """
    project_id = models.IntegerField(unique=True, primary_key=True)
    project_name = models.CharField(max_length=1023)

    def __str__(self):
        return 'Business Model <> for Project #%d' % self.project_id


class BusinessModelEntry(models.Model):
    """
    An entry under some section of the Business Model of a project
    """
    business_model = models.ForeignKey(BusinessModel, related_name='entries')
    author = models.CharField(max_length=255)
    section = models.CharField(max_length=255, choices=BUSINESS_MODEL_SECTIONS)
    text = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return 'Entry #%d (%s) under <%d>' % (self.pk, self.section, self.business_model_id)

    def can_access(self, request):
        for p in request.session['projects']:
            if int(p['pid']) == self.business_model_id:
                return True

        return False

    def can_update(self, request):
        return self.can_access(request)
