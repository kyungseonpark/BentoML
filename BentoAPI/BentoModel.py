import bentoml
import typing as t
from datetime import datetime


def make_label():
    now = datetime.now()
    time_tag = now.strftime("%y%m%d%H%M")
    return time_tag


def model_to_bento(
        service_name: str,
        build_ctx: t.Optional[str] = None,
):
    service_py_path = f'{service_name}'
    with open('/app/BentoML_service.py', 'r', encoding='utf-8') as f:
        bento_service = f.read()
        prev_glo_val = ["MODEL_NAME = ''"]
        new_glo_val = [f"MODEL_NAME = '{service_name}'"]

        for pgv, ngv in zip(prev_glo_val, new_glo_val):
            bento_service = bento_service.replace(pgv, ngv)

        with open(service_py_path, 'w', encoding='UTF8') as nf:
            nf.write(bento_service)

    built_model = bentoml.bentos.build(service=f'{service_name}:svc', build_ctx=build_ctx)

    docker_img_tag = f'{built_model.tag}'
    success_containerize = bentoml.bentos.containerize(tag=built_model.tag, docker_image_tag=docker_img_tag)
    if not success_containerize:
        print("Containerize Failed.")
    return docker_img_tag
