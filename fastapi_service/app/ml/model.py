import traceback
import logging
import traceback
import os
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import numpy as np
from typing import List, Dict, Any

from train.train import Autoencoder_Model
from prepData.prepData import PrepData

from dotenv import load_dotenv

load_dotenv()

USER = os.environ.get('DAGSHUB_USER')
PASSWORD = os.environ.get('DAGSHUB_PASSWORD')
TOKEN = os.environ.get('DAGSHUB_TOKEN')
URI = os.environ.get('DAGSHUB_URI')
NAME_MODEL = os.environ.get('DAGSHUB_NAME_MODEL')
VERSION_MODEL = os.environ.get('DAGSHUB_VERSION_MODEL')


def load_autoencoder_model():
    """Load a pre-trained sentiment analysis model.
    Returns:
        model (function): A function that takes a text input and returns a
        SentimentPrediction object.
    """
    try:
        model_class = Autoencoder_Model()
        logging.info(f"Success get MODEL CLASS")
    except Exception:
        logging.error(f"Get MODEL CLASS error - {traceback.format_exc()}")
        raise
    try:
        logging.info(f"Waiting get model ...")
        model_hf = model_class.load_model_from_MlFlow(dagshub_toc_username=USER,
                                                      dagshub_toc_pass=TOKEN,
                                                      dagshub_toc_tocen=TOKEN)
        logging.info(f"Success get MODEL")
    except Exception:
        logging.error(f"Get MODEL error - {traceback.format_exc()}")
        raise

    def model(data_dict: List[Dict[str, Any]]) -> dict:

        prep_class = PrepData()

        units_list = []
        for dict_unit in data_dict:
            units_list.append(dict_unit['unit number'])
        units_uniq_list = sorted(list(set(units_list)))
        try:
            numpy_from_data = prep_class.json_to_numpy(data_dict)
            pipe_line_data = prep_class.employ_Pipline(numpy_from_data)
            predict_data = model_class.start_predict_model(model_hf,
                                                           pipe_line_data)
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Predict part error: {repr(e)}"
            )
        prep_res: np.array = model_class.get_class_from_object(model_hf,
                                                               predict_data)
        res_prep_dict = {}
        for unit, res in zip(units_uniq_list, prep_res.flatten().tolist()):
            res_prep_dict[unit] = bool(res)
        return res_prep_dict
    return model
