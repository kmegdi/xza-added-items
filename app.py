# </> DISGEND BY XZA TEAM AND MODY 👻
from flask import Flask, request, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

app = Flask(__name__)

freefire_version = "OB50"

# البروتوباف
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6, 30, 0, '', 'data.proto'
)
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ndata.proto\"7\n\x12InnerNestedMessage\x12\x0f\n\x07\x66ield_6\x18\x06 \x01(\x03\x12\x10\n\x08\x66ield_14\x18\x0e \x01(\x03\"\x87\x01\n\nNestedItem\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x0f\n\x07\x66ield_3\x18\x03 \x01(\x05\x12\x0f\n\x07\x66ield_4\x18\x04 \x01(\x05\x12\x0f\n\x07\x66ield_5\x18\x05 \x01(\x05\x12$\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\x13.InnerNestedMessage\"@\n\x0fNestedContainer\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12\x1c\n\x07\x66ield_2\x18\x02 \x03(\x0b\x32\x0b.NestedItem\"A\n\x0bMainMessage\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12!\n\x07\x66ield_2\x18\x02 \x03(\x0b\x32\x10.NestedContainerb\x06proto3'
)
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_pb2', _globals)

MainMessage = _globals['MainMessage']

items_ids = [
    1315000022, 1315000024, 1315000002, 1315000022, 1315000024,
    1315000002, 1315000003, 1315000004, 1315000007, 1315000010,
    1315000019, 1315000021, 1315000020, 1315000016, 1315000012
]

key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
iv  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])

@app.route('/add_item', methods=['POST'])
def add_item():
    data_json = request.get_json()
    jwt_token = data_json.get("jwt_token") if data_json else None

    if not jwt_token:
        return jsonify({"status": "error", "message": "Please provide JWT token"}), 400

    try:
        data = MainMessage()
        data.field_1 = 1
        container1 = data.field_2.add()
        container1.field_1 = 1

        for i, item_id in enumerate(items_ids):
            item = container1.field_2.add()
            item.field_1 = 13
            item.field_3 = 1
            item.field_4 = (i % 6) + 1
            item.field_6.field_6 = item_id

        container2 = data.field_2.add()
        container2.field_1 = 9
        item7 = container2.field_2.add()
        item7.field_4 = 3
        item7.field_6.field_14 = 3048205855

        data_bytes = data.SerializeToString()
        padded_data = pad(data_bytes, AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(padded_data)

        url = "https://clientbp.ggblueshark.com/SetPlayerGalleryShowInfo"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": freefire_version,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; Android 11; SM-A305F Build/RP1A.200720.012)",
            "Host": "clientbp.ggblueshark.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        response = requests.post(url, headers=headers, data=encrypted_data)

        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "message": "Items added successfully",
                "jwt_token": jwt_token,
                "items_added": len(items_ids)
            })
        else:
            return jsonify({
                "status": "error",
                "http_status": response.status_code,
                "response": response.text
            })

    except Exception as e:
        return jsonify({"status": "exception", "error": str(e)}), 500

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    app.run(debug=True, port=5000)