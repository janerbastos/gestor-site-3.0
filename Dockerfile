FROM registry.ufopa.edu.br/library/django5_python3-11:2.0.2

WORKDIR /apps

COPY . /apps/mamba

# configurações do supervisor
COPY ./docker/supervision/supervisord.conf /etc/supervisord.conf

# # Configurações do nginx
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/enabled/default.conf /etc/nginx/http.d/default.conf
COPY ./docker/nginx/enabled/rss.conf /etc/nginx/http.d/rss.conf

EXPOSE 8000

ENV PATH='/apps/venv/bin:$PATH'

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
