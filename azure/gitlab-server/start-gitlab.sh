#!/bin/bash
sudo docker run --detach \
    --hostname $GITLAB_HOSTNAME \
    --publish 443:443 \
    --publish 80:80 \
    --publish 222:22 \
    --name gitlab \
    --restart always \
    --volume /srv/gitlab/config:/etc/gitlab \
    --volume /srv/gitlab/logs:/var/log/gitlab \
    --volume /srv/gitlab/data:/var/opt/gitlab \
    --log-driver json-file \
    --log-opt max-size=10m \
    --log-opt max-file=3 \
    gitlab/gitlab-ce:latest
