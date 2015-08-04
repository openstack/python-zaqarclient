from zaqarclient.queues.v1 import api


class V2(api.V1_1):
    label = 'v2'
    schema = api.V1_1.schema.copy()
