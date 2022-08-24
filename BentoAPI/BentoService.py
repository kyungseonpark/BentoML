import bentoml
from bentoml.io import JSON


def bento_service(model_name: str):
    bento_runner = bentoml.picklable_model.get(f'{model_name}:latest').to_runner()
    service = bentoml.Service(f'{model_name}', runners=[bento_runner])

    @service.api(input=JSON(), output=JSON())
    def predict(input_data: dict) -> dict:
        res = dict()
        res['y_pred'] = bento_runner.run(input_data)
        return res

    return service
