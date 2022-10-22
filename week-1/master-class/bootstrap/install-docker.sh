
#!/usr/bin/env bash

# set docker install home
export DOCKER_INSTALL="/tmp/docker-install"
echo "INFO: downloading temporary docker install files to ${DOCKER_INSTALL}"

# Create install directory
(mkdir ${DOCKER_INSTALL} && cd ${DOCKER_INSTALL} ) ||
	(echo "Failed to create ${DOCKER_INSTALL}" && exit 1)

# Download DMG install
curl -o ${DOCKER_INSTALL}/dmginstall.sh https://gist.githubusercontent.com/afgomez/4172338/raw/0c242cc069287f1f5289e1be28c98e9c372e8073/dmginstall.sh
chmod +x ${DOCKER_INSTALL}/dmginstall.sh

# Download and install Docker engine for Mac
${DOCKER_INSTALL}/dmginstall.sh https://download.docker.com/mac/stable/Docker.dmg

# Install VirtualBox, vagrant and vagrant-manager
brew cask install virtualbox
brew cask install vagrant
brew cask install vagrant-manager

# Install minikube - https://github.com/kubernetes/minikube/releases
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.15.0/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/

# Install minikube & K8 - https://kubernetes.github.io/docs/getting-started-guides/minikube/
curl -Lo kubectl http://storage.googleapis.com/kubernetes-release/release/v1.5.1/bin/darwin/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
