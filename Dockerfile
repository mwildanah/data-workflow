FROM python:3.9.1

RUN apt-get install wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt install ./google-chrome-stable_current_amd64.deb
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip
RUN mv chromedriver-linux64/chromedriver /usr/bin/chromedriver

# # RUN pip install pandas sqlalchemy psycopg2
 
WORKDIR /tokped_scrape

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "crawl_paint.py"]

# COPY ingest_data.py ingest_data.py 

# ENTRYPOINT [ "python"]
# # ENTRYPOINT [ "python", "ingest_data.py" ]