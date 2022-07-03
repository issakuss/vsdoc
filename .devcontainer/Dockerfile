FROM issakuss/pandoc:2.18
ARG DEBIAN_FRONTEND=noninteractive
COPY requirements.txt /tmp/requirements.txt
ENV USER_ID=22398 \
    GROUP_ID=16003 \
    USER_NAME=issakuss \
    GROUP_NAME=abi

RUN apt update \
&&  apt install -y curl make tree vim \
#
# User / Group ID
&&  useradd -s /bin/bash -m ${USER_NAME} \
&&  export HOME=/home/${USER_NAME} \
&&  usermod -u ${USER_ID} ${USER_NAME} \
&&  groupadd -g ${GROUP_ID} ${GROUP_NAME} \
&&  usermod -g ${GROUP_NAME} ${USER_NAME} \
&&  chown -R ${USER_ID}:${GROUP_ID} /home/${USER_NAME} \
#
# Git
&&  apt install -y git git-lfs \
&&  git config --global user.email issakuss@gmail.com \
&&  git config --global user.name issakuss \
&&  git lfs install \ 
#
# Python
&&  apt install -y python3 python3-pip \
&&  pip3 install -U pip \
&&  pip install -r /tmp/requirements.txt \
&&  ln -s /usr/bin/python3 /usr/bin/python \
#
# dotfiles
&&  cd /home/${USER_NAME} \
&&  git clone https://github.com/issakuss/dotfiles \
&&  bash dotfiles/setup.sh || true \
&&  chown -R ${USER_ID}:${GROUP_ID} /home/${USER_NAME}/dotfiles \
#
# Cleaning
&&  apt autoremove -y \
&&  apt clean -y \
#
&&  echo "FIN"
ENV HOME /home/${USER_NAME}