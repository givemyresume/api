FROM python:3.8-slim

EXPOSE 8001 80

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY ./api/requirements.txt .
RUN python -m pip install -r requirements.txt

# Uncomment the below commands only if you want server-side pdf generation
# Note: enabling these will download chrome and consume approx 800 MB of storage.
## RUN apt-get update -y && \
##     apt-get install -y git gnupg wget curl unzip --no-install-recommends && \
##     wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
##     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
##     apt-get update -y && \
##     apt-get install -y google-chrome-stable && \
##     CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
##     DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
##     CHROMEDRIVER_DIR=/usr/local/bin\
##     wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
##     unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR $$ \
##     CHROME_ENABLED=yes && \ 
##     rm $CHROMEDRIVER_DIR/chromedriver_linux64.zip

RUN apt-get update -y && \
    apt-get install -y git --no-install-recommends

WORKDIR /api
COPY ./api /api

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /api
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8001", ]