from flask import request, json, Response


def test_signal():
    title = request.args.get('title')
    print(f"Received title: {title}")

    response_data = {
        'result': 'success',
        'msg': '이 요청은 GET!',
        'title_received': title
    }

    response_json = json.dumps(response_data, ensure_ascii=False)
    return Response(response_json, content_type='application/json; charset=utf-8')
