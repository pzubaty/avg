FROM rocker/r-base:latest

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
       libreoffice && \
       rm -rf /var/lib/apt/lists/*

RUN install2.r --error --deps TRUE \
       magick googledrive tuber pdftools aws.polly usethis docxtractr

RUN installGithub.r --deps TRUE \
       jhudsl/ariExtra jhudsl/ari jhudsl/text2speech jhudsl/didactr

RUN echo "/usr/lib/libreoffice/program/" > /etc/ld.so.conf.d/openoffice.conf && \
       ldconfig && \
       rm -rf /tmp/downloaded_packages/ /tmp/*.rds && \
       rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/usr/local/lib
COPY pptx2ari.sh /opt && \
     gs2ari.sh /opt && \
     run.sh /opt && \
     soffice /usr/lib/libreoffice/program/soffice && \
     --from=jrottenberg/ffmpeg /usr/local /usr/local/

RUN chmod +x /opt/pptx2ari.sh && \
    chmod +x /opt/gs2ari.sh && \
    chmod +x /opt/run.sh && \
    chmod +x /usr/lib/libreoffice/program/soffice && \
    chmod -R og+rwx /opt

ENV HOME "/tmp"
WORKDIR "/opt"

CMD ["/opt/run.sh"]
# RUN useradd avg \
#   && echo "avg:avg" | chpasswd \
#        && mkdir /home/avg \
#        && chown avg:avg /home/avg \
#        && addgroup avg staff
