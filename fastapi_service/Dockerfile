FROM python:3.10


WORKDIR /workdir

COPY fastapi_service/* /workdir/
COPY for_pip_install/* /workdir/for_pip_install/

RUN apt-get update && apt-get upgrade

RUN pip install ./for_pip_install/train_and_valid_model-0.2.15-py3-none-any.whl
RUN pip install ./for_pip_install/preprocess_data-0.1.10-py3-none-any.whl

RUN python -m pip install pip-tools
RUN pip-compile
RUN pip-sync

# RUN pip install -U -e ./

RUN export MLFLOW_TRACKING_USERNAME=$USER
RUN export MLFLOW_TRACKING_PASSWORD=$PASSWORD

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]