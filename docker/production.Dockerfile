# This docker file is used for production


# Creating image based on official python3 image
FROM python:3.10

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/production.txt

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/


# ---------- Build Stage ----------
# FROM python:3.12.9 AS builder

# WORKDIR /app

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# COPY requirements /app/requirements

# RUN pip install --upgrade pip
# RUN pip install --user -r requirements/production.txt


# # ---------- Final Stage ----------
# FROM python:3.12.9-slim

# WORKDIR /app

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV PATH="/root/.local/bin:$PATH"

# COPY --from=builder /root/.local /root/.local
# COPY . /app

