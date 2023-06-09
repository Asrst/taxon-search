from django.contrib import admin
from .models import NCBITaxaNode, NCBITaxaName


# Registering the models
admin.site.register(NCBITaxaNode)
admin.site.register(NCBITaxaName)

