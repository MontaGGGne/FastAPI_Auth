FROM python:3.10


WORKDIR /workdir

COPY ./fastapi_service /workdir
COPY ./requirements.in /workdir/
COPY for_pip_install/* /workdir/

RUN apt-get update
RUN apt-get upgrade -y

RUN python -m pip install pip-tools
RUN pip-compile
RUN pip-sync

RUN pip install ./train_and_valid_model-0.2.15-py3-none-any.whl
RUN pip install ./preprocess_data-0.1.10-py3-none-any.whl

RUN export MLFLOW_TRACKING_USERNAME=$DAGSHUB_USER
RUN export MLFLOW_TRACKING_PASSWORD=$DAGSHUB_PASSWORD

# RUN ls
# RUN alembic -c ./fastapi_service/app/alembic.ini revision --autogenerate
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "80"]