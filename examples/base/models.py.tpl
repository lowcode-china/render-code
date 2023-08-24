from django.db import models

class Person(models.Model):
    {%- for name, prop in data.properties.items() %}
    {%- if prop.type == 'string' %}
    {{ name }} = models.CharField(max_length={{ prop.maxLength }})
    {%- endif %}
    {%- endfor %}
