FROM python:3.9-slim

# Install virtualenv and create a virtual environment
RUN pip install --no-cache-dir -U virtualenv>=20.13.1 && virtualenv /env --python=python3.9
ENV PATH /env/bin:$PATH

# Install pip requirements
WORKDIR /app
COPY . .
RUN /env/bin/pip install --no-cache-dir . && \
    rm nginx.conf

# Install nginx and copy configuration
RUN apt-get update && apt-get install -y --no-install-recommends nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm /etc/nginx/sites-enabled/default \
    && mkdir -p /var/log/django \
    && touch /var/log/django/api_dados_rio.log \
    && chown www-data:www-data /var/log/django/api_dados_rio.log
COPY nginx.conf /etc/nginx/nginx.conf

# Copy app, generate static and set permissions
RUN /env/bin/python manage.py collectstatic --no-input --settings=api_dados_rio.settings.base && \
    chown -R www-data:www-data /app

# Expose and run app
EXPOSE 80
STOPSIGNAL SIGKILL
CMD ["/app/start-server.sh"]
