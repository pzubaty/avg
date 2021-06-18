# FROM rocker/r-base:latest
FROM quay.io/pzubaty/rocker-r-base:latest

RUN apt-get update \
  && apt-get install -y \
       libpoppler-cpp-dev \
       ffmpeg \
       libavfilter-dev \
       libtesseract-dev \
       libleptonica-dev \
       tesseract-ocr-eng \
       libwebp-dev \
       libgdal-dev \
       imagemagick \
       r-cran-httr \
       libssl-dev \
       libmagick++-dev \
       libfontconfig-dev \
       libxml2-dev \
       libsodium-dev \
       cargo \
       default-jre \
       libreoffice-java-common \
       libreoffice \
       wget && \
       rm -rf /var/lib/apt/lists/*

RUN install2.r --error --deps TRUE \
       magick googledrive tuber pdftools aws.polly usethis docxtractr

RUN installGithub.r --deps TRUE \
       jhudsl/ariExtra jhudsl/ari jhudsl/text2speech jhudsl/didactr

RUN echo "/usr/lib/libreoffice/program/" > /etc/ld.so.conf.d/openoffice.conf && \
       ldconfig && \
       apt-get update && apt-get install -y python3-pip \
       procps net-tools openssh-client && \
       pip3 install requests && \
       pip3 install flask && \
       pip3 install gunicorn && \
       pip3 install webvtt && \
       rm -rf /tmp/downloaded_packages/ /tmp/*.rds && \
       rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/usr/local/lib
COPY pptx2ari.sh /opt
COPY gs2ari.sh /opt
COPY run.sh /opt
COPY handle_requests.py /opt
COPY run_command.py /opt
COPY soffice /usr/lib/libreoffice/program/soffice

RUN wget https://github.com/RedHatOfficial/RedHatFont/archive/4.0.2.tar.gz -O /root/font.tar.gz && \
       mkdir -pv /root/font && \
       tar zxvf /root/font.tar.gz --directory /root/font && \
       ls -al /root/font* && \
       cp -v /root/font/*/*/*/*.ttf /usr/share/fonts && \
       fc-cache -f -v && \
       rm -fr /root/font.tar.gz /root/font*

RUN chmod +x /opt/pptx2ari.sh && \
    chmod +x /opt/gs2ari.sh && \
    chmod +x /opt/run.sh && \
    chmod +x /usr/lib/libreoffice/program/soffice && \
    chmod -R og+rwx /opt

ENV HOME "/tmp"
WORKDIR "/opt"

# CMD ["/opt/run.sh"]
# CMD ["/opt/handle_requests.py"]
# EXPOSE 8000
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "handle_requests:app"]

