FROM python:3.11.8-bookworm

WORKDIR /power_user_optimism

COPY . .

RUN pip install -r requirements.txt

workdir ../

CMD ["python3", "-m", "power_user_optimism"]