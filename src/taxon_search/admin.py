from django.contrib import admin
from .models import EnsemblMetadata, NCBITaxonFlat


# Registering the models
admin.site.register(EnsemblMetadata)
admin.site.register(NCBITaxonFlat)
