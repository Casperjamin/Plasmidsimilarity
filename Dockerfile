FROM ubuntu:focal

# For easy upgrade later. ARG varibles only persist during docker image build time
ARG ABRICATE_VER="1.0.1"

LABEL base.image="ubuntu:focal"
LABEL dockerfile.version="2"
LABEL software="Plasmidsimilarity"
LABEL description="Comparing sequence and gene content of plasmids"
LABEL website="https://github.com/casperjamin/plasmidsimilarity"
LABEL license="https://github.com/Casperjamin/Plasmidsimilarity/blob/master/LICENSE"
LABEL maintainer="Casper Jamin"
LABEL maintainer.email="casperjamin@gmail.com"

# install dependencies
# removed: emboss
# ncbi-blast+ version in apt for ubuntu:focal = v2.9.0
RUN apt-get update && apt-get install -y --no-install-recommends \
  bioperl \
  gzip \
  unzip \
  liblist-moreutils-perl \
  libjson-perl \
  libtext-csv-perl \
  libfile-slurp-perl \
  liblwp-protocol-https-perl \
  libwww-perl \
  libpath-tiny-perl \
  git \
  ncbi-blast+ \
  wget \
  python3-pip && \
  apt-get autoclean && rm -rf /var/lib/apt/lists/*

# get any2fasta
RUN cd /usr/local/bin && \
  wget https://raw.githubusercontent.com/tseemann/any2fasta/master/any2fasta && \
  chmod +x any2fasta

# download abricate
RUN wget https://github.com/tseemann/abricate/archive/v${ABRICATE_VER}.tar.gz && \
    tar -zxvf v${ABRICATE_VER}.tar.gz && \
    rm -rf v${ABRICATE_VER}.tar.gz

# set $PATH
# set perl locale settings for singularity compatibility
ENV PATH="/abricate-${ABRICATE_VER}/bin:\
$PATH"\
    LC_ALL=C

# check dependencies, setup db's, make working directory /data
RUN abricate --check && \
    abricate --setupdb && \
    mkdir /data

# install plasmidsimilarity
RUN git clone https://github.com/casperjamin/Plasmidsimilarity.git
WORKDIR Plasmidsimilarity
RUN pip3 install .

WORKDIR /data
