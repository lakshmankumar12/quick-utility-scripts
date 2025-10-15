# Use the moss/xelatex base image
FROM moss/xelatex

# Set working directory
WORKDIR /data

# Install Noto fonts and clean up APT artifacts
RUN apt-get update && \
    apt-get install -y fonts-noto && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Default command
CMD ["/bin/bash"]

