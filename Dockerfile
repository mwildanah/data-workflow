FROM python:3.9.1

# # RUN pip install pandas sqlalchemy psycopg2
 
WORKDIR /tokped_scrape

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "crawl_paint.py"]

# COPY ingest_data.py ingest_data.py 

# ENTRYPOINT [ "python"]
# # ENTRYPOINT [ "python", "ingest_data.py" ]