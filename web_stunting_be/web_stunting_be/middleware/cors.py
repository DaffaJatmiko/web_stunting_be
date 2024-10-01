def cors_tween_factory(handler, registry):
    def cors_tween(request):
        # Menangani preflight request
        if request.method == 'OPTIONS':
            response = request.response
            # Atur origin yang sesuai
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Max-Age'] = '3600'
            return response

        # Menangani actual request
        response = handler(request)

        # Set header Content-Type ke application/json jika belum diatur
        if 'Content-Type' not in response.headers:
            response.headers['Content-Type'] = 'application/json'

        # Atur origin yang sesuai
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        return response

    return cors_tween
