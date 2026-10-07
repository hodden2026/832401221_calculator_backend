from flask import (
    Flask,
    jsonify,
    request,
)

from database import (
    add_history,
    clear_history,
    delete_history,
    get_history,
    init_database,
)

from services.calculator_service import (
    ExpressionError,
    calculate_expression,
)


app = Flask(__name__)


init_database()


@app.after_request
def add_cors_headers(response):
    """允许前端访问后端 API。"""

    response.headers[
        "Access-Control-Allow-Origin"
    ] = "*"

    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type"

    response.headers[
        "Access-Control-Allow-Methods"
    ] = (
        "GET, POST, DELETE, OPTIONS"
    )

    return response


@app.route(
    "/",
    methods=["GET"],
)
def home():
    return jsonify({
        "success": True,
        "message":
            "Calculator backend is running",
    }), 200


@app.route(
    "/api/health",
    methods=["GET"],
)
def health():
    return jsonify({
        "success": True,
        "status": "online",
    }), 200


@app.route(
    "/api/calculate",
    methods=["POST"],
)
def calculate():
    data = request.get_json(
        silent=True
    )


    if not data:
        return jsonify({
            "success": False,
            "message":
                "JSON request body is required",
        }), 400


    if "expression" not in data:
        return jsonify({
            "success": False,
            "message":
                "Expression is required",
        }), 400


    expression = (
        data["expression"]
    )


    try:
        result = (
            calculate_expression(
                expression
            )
        )


        history_id = (
            add_history(
                expression,
                result,
            )
        )


        return jsonify({
            "success": True,
            "expression":
                expression,
            "result":
                result,
            "history_id":
                history_id,
        }), 200


    except ExpressionError as error:

        return jsonify({
            "success": False,
            "message":
                str(error),
        }), 400


@app.route(
    "/api/history",
    methods=["GET"],
)
def history_list():

    history = (
        get_history()
    )


    return jsonify({
        "success": True,
        "history":
            history,
    }), 200


@app.route(
    "/api/history/<int:history_id>",
    methods=["DELETE"],
)
def remove_history(
    history_id,
):

    deleted = (
        delete_history(
            history_id
        )
    )


    if not deleted:

        return jsonify({
            "success": False,
            "message":
                "History record not found",
        }), 404


    return jsonify({
        "success": True,
        "message":
            "History record deleted",
    }), 200


@app.route(
    "/api/history",
    methods=["DELETE"],
)
def remove_all_history():

    deleted_count = (
        clear_history()
    )


    return jsonify({
        "success": True,
        "message":
            "All history records deleted",
        "deleted_count":
            deleted_count,
    }), 200


@app.errorhandler(404)
def handle_not_found(error):

    return jsonify({
        "success": False,
        "message":
            "API endpoint not found",
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(
    error,
):

    return jsonify({
        "success": False,
        "message":
            "Method not allowed",
    }), 405


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )