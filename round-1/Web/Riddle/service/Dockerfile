FROM node:6
COPY flag /flag
RUN chmod a=r /flag
COPY src/ /home
RUN npm install
RUN /home/requirements.sh
WORKDIR /home
CMD ["/bin/sh","/home/run.sh"]
EXPOSE 5069
