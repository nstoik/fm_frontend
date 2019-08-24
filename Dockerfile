# Build the node components
FROM node:10 as nodebuild
COPY package* webpack.config.js /workspaces/
COPY assets  /workspaces/assets/
RUN mkdir -p /workspaces/fm_frontend/webpack
WORKDIR /workspaces
RUN npm ci --silent
ENV NODE_ENV=production
RUN npm run-script build
#
#
# Add the pyton parts
FROM python:3.6-buster
# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG USERNAME=fm
ARG USER_UID=1000
ARG USER_GID=$USER_UID
#
# Install pipenv
RUN pip --disable-pip-version-check --no-cache-dir install pipenv && \
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

# Change to the newly created user
USER $USER_UID:$USER_GID
COPY fm_frontend /workspaces/fm_frontend/fm_frontend
COPY Pipfile* setup.py /workspaces/fm_frontend/
WORKDIR /workspaces/fm_frontend
#
# Production deploy steps below
RUN pipenv install --deploy --ignore-pipfile
# Copy over the stuff from the nodebuild
COPY --from=nodebuild /workspaces/fm_frontend/static/build/ /workspaces/fm_frontend/fm_frontend/static/build/
COPY --from=nodebuild /workspaces/fm_frontend/webpack/manifest.json /workspaces/fm_frontend/fm_frontend/webpack/manifest.json
# Install the package so the commands work
RUN pipenv run pip install -e .

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

EXPOSE 5000

CMD ["pipenv", "run", "fm_frontend", "run", "--host=0.0.0.0"]