# Usamos uma imagem base leve com Python
FROM python:3.9-slim

# Instala o exiftool (a imagem do python é baseada em Debian, então usamos apt-get)
RUN apt-get update && apt-get install -y libimage-exiftool-perl

# Instala o Flask, que usaremos para criar o servidor web
RUN pip install Flask

# Copia nosso código para dentro do contêiner
WORKDIR /app
COPY . .

# Expõe a porta 5000 e inicia nosso aplicativo
EXPOSE 5000
CMD ["python", "app.py"]
