# Packages imported using "import"
import os
import xgboost as xgb
import pandas as pd

# Packages imported using "from-import"
from io import BytesIO
from fastapi import FastAPI
from fastapi import UploadFile, File, Form

# import customized library functions
from BentoModel import *
from BentoGlobal import *
from BentoBody import *


bentoml = FastAPI(
    title='BentoML_API',
    description=f'BentoML API Set 🍱'
)

TAGS = []


@bentoml.post("/create-model")
async def CreateBentoModel(
        # Dataset Information
        dataset: UploadFile = Form(...),
        file_extension: str = Form(...),
        target_column: str = Form(...),
        # Training Information
        train_type: str = Form(...),
        algorithm: str = Form(...),
        # Customization Information
        model_name: str = Form(...)
):
    """
    :param dataset: Dataset to use for model learning
    :param file_extension: Dataset extension type (csv or parquet)
    :param target_column: Target Column name in dataset
    :param train_type: Model training type (Multi Classification: mul_clf, Binary Classification: bin_clf, Registrar: reg)
    :param algorithm: Algorithm to use for model training
    :param model_name: Model Name

    :return: Tag of Saved Model
    """
    # Load Dataset
    read_dataset = await dataset.read()
    if file_extension == 'csv':
        read_df = pd.read_csv(BytesIO(read_dataset))
    elif file_extension == 'parquet':
        read_df = pd.read_parquet(BytesIO(read_dataset))

    del read_dataset
    await dataset.close()

    # Divide X,y
    y_data = read_df[target_column].values
    if str(y_data.dtype) == 'object':
        raise Exception
    x_data = read_df.drop(target_column, axis=1).values

    if algorithm == 'xgb':
        saved_model_tag = XGBoost(x_data=x_data, y_data=y_data, model_name=model_name, train_type=train_type)

    return {"saved_model_tag": saved_model_tag}
