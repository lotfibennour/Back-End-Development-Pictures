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
    """return data"""
    if data:
        return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((p for p in data if p["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    existing_picture = next((p for p in data if p['id'] == new_picture['id']), None)
    
    if existing_picture:
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302
    
    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((p for p in data if p["id"] == id), None)
    if not picture:
        return jsonify({"error": "Picture not found"}), 404
    
    updated_picture = request.json
    
    # Update the picture's attributes
    for key, value in updated_picture.items():
        if key in picture:
            picture[key] = value
    
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    original_length = len(data)
    picture_to_delete = next((p for p in data if p["id"] == id), None)
    
    if picture_to_delete:
        data.remove(picture_to_delete)
        return '', 204
    else:
        return jsonify({"error": "Picture not found"}), 404