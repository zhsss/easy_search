FROM python:3.8

RUN mkdir /program

WORKDIR /program

ADD *.py /program/
ADD *.txt /program/
ADD templates/* /program/templates/
ADD dao/* /program/dao/
ADD views/* /program/views/

RUN pip3 install -r /program/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN mkdir output

CMD ["python3","/program/app.py"]

EXPOSE 8000
