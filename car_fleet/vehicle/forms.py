from django.forms import ModelForm, ModelChoiceField
from enterprise.models import Enterprise
from vehicle.models import Vehicle



class VehicleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        manager_id = kwargs.pop('manager_id')
        super(VehicleForm, self).__init__(*args, **kwargs)
        companies = Enterprise.objects.filter(manager__id=manager_id)
        self.fields['enterprise'] = ModelChoiceField(queryset=companies)

    class Meta:
        model = Vehicle
        fields = "__all__"
