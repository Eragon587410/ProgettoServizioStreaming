# Usa Python 3.12 come base
FROM python:3.12

# Cartella di lavoro nel container
WORKDIR /app

# Copia i file del progetto nel container
COPY . /app

# Installa le librerie necessarie
RUN pip install --no-cache-dir flask cryptography sqlalchemy pymysql requests

# Rendi eseguibile lo script

RUN chmod +x /app/streamdash.sh

# Copia in /usr/local/bin per renderlo globale
RUN cp /app/streamdash.sh /usr/local/bin/streamdash



# Comando di default quando parte il container
CMD ["bash"]
