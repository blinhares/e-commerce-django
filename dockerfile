FROM python:3.12.3-alpine3.19
LABEL mantainer="https://github.com/blinhares"

# Essa variável de ambiente é usada para controlar se o Python deve 
# gravar arquivos de bytecode (.pyc) no disco. 1 = Não, 0 = Sim
ENV PYTHONDONTWRITEBYTECODE 1

# Define que a saída do Python será exibida imediatamente no console ou em 
# outros dispositivos de saída, sem ser armazenada em buffer.
# Em resumo, você verá os outputs do Python em tempo real.
ENV PYTHONUNBUFFERED 1

# Copia a pasta "djangoapp" e "scripts" para dentro do container.
COPY djangoapp /djangoapp
COPY scripts /scripts

#Copiando Arquivos do Poetry para o conteiner
COPY poetry.lock poetry.lock 
COPY pyproject.toml pyproject.toml


# Entra na pasta djangoapp no container
WORKDIR /djangoapp

# A porta 8000 estará disponível para conexões externas ao container
# É a porta que vamos usar para o Django.
EXPOSE 8000

# RUN executa comandos em um shell dentro do container para construir a imagem. 
# O resultado da execução do comando é armazenado no sistema de arquivos da 
# imagem como uma nova camada.
# Agrupar os comandos em um único RUN pode reduzir a quantidade de camadas da 
# imagem e torná-la mais eficiente.
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  echo 'INSTALANDO POETRY' && \
  /venv/bin/pip install poetry && \
  echo 'ATIVANDO AMBIENTE VIRTUAL' && \
  source /venv/bin/activate && \
  echo 'INSTALANDO DEPENDENCIAS ...' && \
  poetry install && \
  echo 'DESATIVANDO AMBIENTE VIRTUAL' && \
  deactivate && \
  #instala dependencia atraves do requirements
  # /venv/bin/pip install -r /djangoapp/requirements.txt && \
  echo 'CRIANDO USUARIO' && \
  adduser --disabled-password --no-create-home duser && \
  echo 'CRIANDO PASTA STATIC' && \
  mkdir -p /data/web/static && \
  echo 'CRIANDO PASTA MEDIA' && \
  mkdir -p /data/web/media && \
  echo 'MUDANDO PERMICOES DE USUARIO' && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts && \
  su duser

# Adiciona a pasta scripts e venv/bin 
# no $PATH do container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Muda o usuário para duser
#no linux isso pode dar erro nas permissoes do arquivo. 
# Entao no nosso caso seguiremos no usuario root da imagem
#mudamos o usuario com o comando `su duser`
# USER duser 

# Executa o arquivo scripts/commands.sh
CMD ["commands.sh"]