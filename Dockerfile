FROM python:3.14-slim

# Run as a non-root user.
RUN useradd --create-home --uid 10001 appuser
WORKDIR /srv
COPY app/ ./app/
USER 10001

EXPOSE 8080
CMD ["python", "-m", "app.main"]
