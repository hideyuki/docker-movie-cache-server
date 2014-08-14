FROM ubuntu:14.04
MAINTAINER Hideyuki Takei <takehide22@gmail.com>

# apt-get
RUN apt-get update
RUN apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install curl vim git mercurial openssh-server sudo daemontools daemontools-run

# Install python
RUN apt-get -y install python python-pip
RUN pip install boto

# Install youtube-dl
RUN curl https://yt-dl.org/latest/youtube-dl -o /usr/local/bin/youtube-dl
RUN chmod a+x /usr/local/bin/youtube-dl


# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 22
CMD ["/usr/bin/svscan", "/etc/service/"]

