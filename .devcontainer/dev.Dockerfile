#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

FROM python:3.9-buster

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG USERNAME=fm
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Configure apt and install packages
RUN apt-get update && \
    apt-get -yqq install --no-install-recommends apt-utils dialog apt-transport-https locales 2>&1 && \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    apt-get -yqq install git procps lsb-release && \
    # Install node prereqs, nodejs and yarn
    # Ref: https://deb.nodesource.com/setup_12.x
    # Ref: https://yarnpkg.com/en/docs/install
    echo "deb https://deb.nodesource.com/node_12.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
    wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
    wget -qO- https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    apt-get update && \
    apt-get install -yqq nodejs yarn && \
    npm i -g npm@^6 && \
    # Clean up
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*


RUN pip install -U pip && pip install pipenv && \
    # create new user
    groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    # [Optional] Uncomment the next three lines to add sudo support
    # apt-get install -y sudo && \
    # echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    # chmod 0440 /etc/sudoers.d/$USERNAME && \
    # make working directory and change owner
    mkdir -p /workspaces/fm_frontend/ && \
    chown $USER_UID:$USER_GID /workspaces/fm_frontend/

# add bash history. https://code.visualstudio.com/docs/remote/containers-advanced#_persist-bash-history-between-runs
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo $SNIPPET >> "/root/.bashrc" \
    # [Optional] If you have a non-root user
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory \
    && echo $SNIPPET >> "/home/$USERNAME/.bashrc"

# Change to the newly created user
USER $USER_UID:$USER_GID
COPY fm_frontend /workspaces/fm_frontend/fm_frontend
COPY Pipfile* package* setup.py /workspaces/fm_frontend/
WORKDIR /workspaces/fm_frontend

# Set up the dev environment
RUN pipenv install --dev && \
    npm install

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

EXPOSE 5000 2992

CMD ["/bin/bash"]