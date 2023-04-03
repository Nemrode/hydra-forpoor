FROM ubuntu:latest

# Install SSH server and create a user
RUN apt-get update && \
    apt-get install -y openssh-server && \
    useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 ubuntu && \
    echo 'ubuntu:password' | chpasswd

# Configure SSH server
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication no/' /etc/ssh/sshd_config

RUN service ssh start

# Expose SSH port and start SSH server
EXPOSE 22

CMD ["/bin/bash"]
