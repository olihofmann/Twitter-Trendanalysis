FROM python:3.7-alpine

# install dependencies
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories ; \
    apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev ; \
    ln -s /usr/include/locale.h /usr/include/xlocale.h

# Install and configure python packages
ADD requirements.txt /build/
RUN pip install -r /build/requirements.txt

# Copy python app
COPY app.py .
COPY templates /templates
COPY static /static

EXPOSE 5000

# Start the Webserver
CMD ["python", "/app.py"]