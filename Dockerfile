FROM python:3.8.8
WORKDIR /fleetstudiotest
ADD . /fleetstudiotest
ENV STATIC_URL /static
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT [ "python" ]
CMD ["loginapi/app.py"]