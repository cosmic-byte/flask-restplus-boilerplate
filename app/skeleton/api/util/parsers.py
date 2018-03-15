from flask_restplus import reqparse

search_parser = reqparse.RequestParser(bundle_errors=True)
search_parser.add_argument('type', type=str, required=True, location='args', choices=('gi', 'tw', 'ig'),
                           help='Bad choice: {error_msg}')
search_parser.add_argument('query', type=str, required=True, location='args', help='Bad choice: {error_msg}')
