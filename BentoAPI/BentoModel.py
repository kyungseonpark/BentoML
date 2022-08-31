import bentoml
import typing as t
from datetime import datetime
from BentoGlobal import *


def make_label():
    now = datetime.now()
    time_tag = now.strftime("%y%m%d%H%M")
    return time_tag


def model_to_bento(
        model_name_tag: str,
        build_ctx: t.Optional[str] = None,
):
    model_name = model_name_tag.split(':')[0]
    service_py_path = f'{model_name}.py'
    with open('/app/BentoML_service.py', 'r', encoding='utf-8') as f:
        bento_service = f.read()
        prev_glo_val = ["MODEL_NAME = ''"]
        new_glo_val = [f"MODEL_NAME = '{model_name_tag}'"]

        for pgv, ngv in zip(prev_glo_val, new_glo_val):
            bento_service = bento_service.replace(pgv, ngv)

        with open(service_py_path, 'w', encoding='UTF8') as nf:
            nf.write(bento_service)

    built_model = bentoml.bentos.build(service=f'{service_py_path}:svc', build_ctx=build_ctx)

    docker_img_tag = f'{built_model.tag}'
    success_containerize = bentoml.bentos.containerize(tag=built_model.tag, docker_image_tag=docker_img_tag)
    if not success_containerize:
        print("Containerize Failed.")
    return docker_img_tag
