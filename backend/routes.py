from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500



######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500
######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    found = False
    for picture in data:
        if picture['id'] == id:
            found = True
            return jsonify(picture), 200

    return {"message": "Picture not found."}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    request_body = request.get_json()

    found = False
    for picture in data:
        if picture['id'] == request_body['id']:
            found = True
            break

    if found == True:
        return {"Message": f"picture with id {request_body['id']} already present"}, 302
    else:
        data.append(request_body)
        return jsonify(request_body), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    request_body = request.get_json()

    found = False
    found_index = 0
    for index, picture in enumerate(data):
        if picture['id'] == request_body['id']:
            found = True
            found_index = index
            break

    if found:
        data[found_index] = request_body
        return jsonify(request_body), 204

    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    found = False
    found_index = 0
    for index, picture in enumerate(data):
        if picture['id'] == id:
            found = True
            found_index = index
            break
    
    if found:
        data.pop(found_index)
        return {"message": "Picture deleted successfully."}, 204

    return {"message": "Picture not found."}, 404
