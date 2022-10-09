FROM php:7.0-cli
COPY flag /flag
COPY src/ /home
RUN chmod 777 /home/test.html
RUN chmod 777 /home/test.pdf
RUN chmod 777 /flag

RUN apt-get update
RUN apt-get install xvfb -y
RUN apt-get install wkhtmltopdf -y
WORKDIR /home
CMD ["/bin/bash","/home/run.sh"]
EXPOSE  5023 
               
