from flask import Flask, jsonify
from flask_restful import Resource, Api, abort, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

resource_store = [{
  'id': 1,
  'description': 'some widget'
}]

class WidgetList(Resource):
  def get(self):
    """List of widgets .
    ---
    definitions:
      WidgetList:
        type: array
        items:
          $ref: '#/definitions/Widget'
      Widget:
        type: object
        properties:
          id: 
            type: integer
            format: int32
            example: 1
          description: 
            type: string
            example: 'some widget'
    responses:
      200:
        description: A list of widgets
        schema:
          $ref: '#/definitions/WidgetList'
    """
    return resource_store, 200
  def post(self):
    """Add a widget.
    ---
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        schema:
          $ref: '#/definitions/Widget'
    responses:
      201:
        description: creation ok
    """
    resource_store.append(request.json)
    return 'created', 201

class Widget(Resource):
  def get(self, resource_id):
    """Get a widget.
    ---
    parameters:
      - name: resource_id
        in: path
        type: integer
        required: true
        format: int32
        example: 1
        description: Id of a widget
    responses:
      200:
        description: A single widget
        schema:
          $ref: '#/definitions/Widget'
      404:
        description: Not found
    """
    resources = [x for x in resource_store if x['id'] == resource_id]
    if len(resources) == 0:
      abort(404, message=f'widget with id {resource_id} does not exist')
    else:
      return resources[0], 200
  def put(self, resource_id):
    """Modify a single widget.
    ---
    parameters:
      - name: resource_id
        in: path
        type: integer
        required: true
        format: int32
        example: 1
        description: Id of a widget
      - name: body
        in: body
        schema:
          $ref: '#/definitions/Widget'
    responses:
      202:
        description: update ok
        schema:
          $ref: '#/definitions/Widget'
      404:
        description: Not found
    """
    resource_indexes = [(i, item) for (i,item) in enumerate(resource_store) if item['id'] == resource_id]
    if len(resource_indexes) == 0:
      abort(404, message=f'widget with id {resource_id} does not exist')
    else:
      index = resource_indexes[0][0]
      resource_store[index]['description'] = request.json['description']
      return 'accepted', 202
  def delete(self, resource_id):
    """Delete a widget.
    ---
    parameters:
      - name: resource_id
        in: path
        type: integer
        required: true
        format: int32
        example: 1
        description: Id of a widget
    responses:
      204:
        description: No content
      404:
        description: Not found
    """
    global resource_store
    resource_store = [x for x in resource_store if x['id'] != resource_id]
    return 'accepted', 202

api.add_resource(WidgetList, '/widgets')
api.add_resource(Widget, '/widgets/<int:resource_id>')

if __name__ == '__main__':
  app.run(debug=True)