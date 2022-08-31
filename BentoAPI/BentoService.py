import bentoml
from bentoml.io import JSON


def bento_service(framework: str, model_name_tag: str):
    model_name = model_name_tag.split(':')[0]
    bento_runner = getattr(bentoml, framework).get(f'{model_name_tag}').to_runner()
    service = bentoml.Service(f'{model_name}', runners=[bento_runner])

    @service.api(input=JSON(), output=JSON())
    def predict(input_data: dict) -> dict:
        res = dict()
        res['y_pred'] = bento_runner.run(input_data)
        return res

    return service
