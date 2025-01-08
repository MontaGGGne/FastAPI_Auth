FROM python:3.10


WORKDIR /workdir

COPY fastapi_service/* /workdir/
# COPY for_pip_install/* /workdir/

RUN apt-get update && apt-get upgrade
RUN python -m pip install pip-tools
RUN pip-compile
RUN pip-sync

# RUN pip install -U -e ./
# RUN pip install ./train_and_valid_model-0.2.15-py3-none-any.whl
# RUN pip install ./preprocess_data-0.1.10-py3-none-any.whl

# RUN export MLFLOW_TRACKING_USERNAME=$USER
# RUN export MLFLOW_TRACKING_PASSWORD=$PASSWORD

# Run the application
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]