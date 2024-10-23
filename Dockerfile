FROM python:3.9-slim

# Install GnuPG and SOPS
RUN apt-get update && \
    apt-get install -y gnupg && \
    wget -O /usr/local/bin/sops https://github.com/mozilla/sops/releases/latest/download/sops-3.7.1.linux && \
    chmod +x /usr/local/bin/sops

# Set the working directory
WORKDIR /app

# Copy your application code
COPY ./my_login_app .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the encrypted secrets file
COPY secrets.yaml .

# Copy your PGP private key (make sure this is done securely)
COPY your_pgp_key.asc /root/.gnupg/private-key.asc

# Set the entrypoint to decrypt the secrets before starting the application
ENTRYPOINT ["sh", "-c", "gpg --import /root/.gnupg/private-key.asc && sops -d secrets.yaml > decrypted_secrets.yaml && exec python app.py"]
