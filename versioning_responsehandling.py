import logging
from flask import Flask, jsonify, render_template, request

ERROR_NOT_FOUND = {"code": 404, "description": "Not found", "message": "Define page."}

# placeholder for resource existence check
resource_exists = False

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(ERROR_NOT_FOUND['message'])
    return jsonify(ERROR_NOT_FOUND), 404

@app.route('/api/resource1', methods=['GET'])
def get_resource():
    if resource_exists:
        return jsonify({"message": "Resource found"}), 200
    else:
        return jsonify({"error": "Resource not found"}), 404

# Remove the extra app = Flask(__name__) here

# URL VERSION
@app.route('/v1/resource')
def v1():
    data_v1 = {"version": "1", "values": [1, 2, 3, 4, 5]}
    return jsonify(data_v1)

@app.route('/v2/resource')
def v2():
    data_v2 = {"version": "1", "values": [4, 5, 34, 2, 23]}
    return jsonify(data_v2)

# HEADER VERSION
@app.route('/query', methods=['GET'])
def get_resource1232331():
    try:
        version = request.args.get('version')
        
        if version is None:
            # Default to version 1 if the parameter is not provided
            version = '1'

        if version == '1':
            data = {"version": "1", "values": [1, 2, 3, 4]}
        elif version == '2':
            data = {"version": "2", "values": [4, 5, 6, 7, 8]}
        else:
            return "Invalid or missing API version in the query parameter", 400

        return jsonify(data)
    except Exception as e:
        print(f"Error: {e}")
        raise




#cache control header
    

@app.route('/api/products')
def get_products():
    response=jsonify({"message":"this is a cacheable resourse "})
    response.headers["Cache-Control"]='max-age=3600'#cache for 1 hr
    expiration_time=60*60
    response.set_cookie('my_cookies','cookie_value' ,max_age=expiration_time)
    return response


#   ETAG header

@app.route('/api/products/list' ,methods=['GET'])
def list():
    resource_data={"message":"this is resourse wqqith Etag support"}
    etag=hash(str(resource_data)) # it use a hash as a Etag
    if request.headers.get('if-None-Match')==str(etag):
        return "",304 #not modified
    else:
        response=jsonify(resource_data)
        response.headers['Etag']=str(etag)
        return response

#conditional response header
    

@app.route('/api/resource/cart', methods=['GET'])
def get_resource1232():
    last_modified = 'Tue, 01 Jan 2022 00:00:00 GMT'  # Replace with the actual last modified date
    if request.headers.get('If-Modified-Since') == last_modified:
        return "", 304  # Not Modified
    else:
        response = jsonify({"message": "This is a conditionally cacheable resource"})
        response.headers['Last-Modified'] = last_modified
        return response

#REST API Response Data Handling Patterns

"""1.STANDARD JSON RESPONSE
 
THE MOST COMMON PATTERN WHERE DATA IS RETURNED AS A JSON OBJECT.
PROVIDES SIMPLICITY, EASE OF PARSING, AND WIDESPREAD SUPPORT.
IDEAL FOR STRAIGHTFORWARD DATA STRUCTURES WITHOUT ADDITIONAL METADATA.
CLIENTS CAN EASILY EXTRACT INFORMATION USING KEY-VALUE PAIRS."""


@app.route('/api/user/id', methods=['GET'])
def get_user_id():
    data = {"message": "Resource data --user : harnoor password :ajit"}
    return jsonify(data), 200

"""2. ENVELOPED RESPONSE
WRAPS THE ACTUAL RESPONSE DATA IN AN ENVELOPE, PROVIDING ADDITIONAL METADATA.
INCLUDES DETAILS LIKE STATUS, ERROR MESSAGES, OR PAGINATION INFORMATION.
ENHANCES COMMUNICATION BY CONVEYING THE CONTEXT OF THE RESPONSE.
ENABLES BETTER ERROR HANDLING AND UNDERSTANDING OF API BEHAVIORS.
"""
@app.route('/api/resource/users/about', methods=['GET'])
def get_resource123():
    data = {"message": "Techlanders is best "}
    response = {"status": "success", "data": data}
    return jsonify(response), 200

"""3.CUSTOM CONTENT NEGOTIATION

ALLOWS CLIENTS TO SPECIFY THE DESIRED RESPONSE FORMAT (JSON, XML, ETC.).
ENHANCES FLEXIBILITY BASED ON CLIENT REQUIREMENTS.
EMPOWERS CLIENTS TO REQUEST DATA IN A FORMAT THEY ARE COMFORTABLE CONSUMING.
REQUIRES SERVER-SIDE LOGIC TO HANDLE AND RESPOND TO DIFFERENT CONTENT TYPES.
"""


@app.route('/api/resource/cart/id', methods=['GET'])
def get_resource12312():
    data = {"message": " "}
    desired_format = request.headers.get('Accept')
    if 'application.xml' in desired_format:
        # Code to handle XML response
        pass
    else:
        return jsonify(data), 200

"""4. HATEOAS (HYPERMEDIA AS THE ENGINE OF APPLICATION STATE)


ENHANCES RESPONSES WITH HYPERMEDIA LINKS FOR NAVIGATING THE API.
CLIENTS CAN DYNAMICALLY DISCOVER AND INTERACT WITH RELATED RESOURCES.
ENCOURAGES A SELF-DESCRIPTIVE API, REDUCING DEPENDENCY ON HARD-CODED URLS.
FACILITATES BETTER CLIENT-SERVER INTERACTION AND SCALABILITY.
"""


@app.route('/api/resource/about', methods=['GET'])
def get_resource_anand():
    data = {"message": "Resource data"}
    links = {"self": "/api/resource", "related": "/api/other_resource"}
    response = {"data": data, "links": links}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
