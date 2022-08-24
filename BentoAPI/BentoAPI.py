# Packages imported using "import"
import bentoml
import cloudpickle
import pickle
import io

# Packages imported using "from-import"
from fastapi import FastAPI
from fastapi import UploadFile, Form, File

# import customized library functions
from BentoModel import *
from BentoGlobal import *
from BentoBody import *


api = FastAPI(
    title='BentoML_API',
    description=f'BentoML API Set 🍱'
)

TAGS = []


@api.post("/pkl-to-bento")
async def pkl_to_bento(
        model_file: bytes = File(...),
        model_name: str = Form(...),
):
    file_stream = io.BytesIO(model_file)
    input_model = pickle.loads(file_stream.read())

    # TBD: Add metadata
    saved_model = bentoml.picklable_model.save_model(
        name=model_name,
        model=input_model,
        metadata={}
    )

    model_to_bento(str(saved_model.tag).split(':')[0])

    res = dict()
    res['model_tag'] = saved_model.tag
    return res
