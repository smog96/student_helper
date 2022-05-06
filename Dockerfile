# ------- Global vars
ARG APP_USER=appuser
ARG APP_NAME=bot

FROM python:3.10.2 as base

ARG APP_USER
ARG APP_NAME

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create a group and user to run our app
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Create project directory and cd
WORKDIR /${APP_NAME}
# Install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN python -m poetry install

# Copy project files
COPY . .
# Switch to non-root
USER ${APP_USER}:${APP_USER}


ENTRYPOINT ["watchgod"]

# --- telegram bot
FROM base as telegram_bot
# Run app
CMD ["python -m src.telegram.main"]

# --- vk bot --- feature
# Run app
#CMD ["src.main.main"]

