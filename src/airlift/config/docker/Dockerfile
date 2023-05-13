FROM {{ base_image }}
{% if requirements_path != None  %}
COPY ./requirements.txt /requirements/requirements.txt
RUN pip install -r /requirements/requirements.txt
{% endif %} 
