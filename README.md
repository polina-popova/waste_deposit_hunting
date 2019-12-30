# waste_deposit_hunting

The waste_deposit_hunting project has the purpose to handle mobile users's reports about 
waste deposits in Arkhangelsk's area.

---

## API Docs

### Interface to post the report 

| URI         | Method | Authorization |
|-------------|--------|---------------|
|`/reports/`  | `POST` | not required  |


Param: data, where `comment` and `feedback_info` are not required and `lat` and `long` must be in WGS84 
format and belong to the Arkhangelsk's area.
```
lat=12.12334
long=12.12334
photo=test_photo.jpg
comment=some_text_string
feedback_info=some_text_string
```

Success Response:

* Code: 201
* Content: 

```json
{
  "datetime_received": "2019-12-06T19:26:47.796141+03:00",
  "photo": "http://0.0.0.0:8000/api/v1/reports/photos/2019/12/06/test_photo.jpg",
  "lat": 12.12334,
  "long": 12.12334,
  "comment": "some_text_string",
  "feedback_info": "some_text_string",
  "waste_deposit": 1
}
```

Error Responses:

* Code: 400

* Content:
```json
{
  "code": "no_photo",
  "msg" : "Фотография является обязательной."
}
```
* Possible codes: "no_photo" for missing photo argument, "no_long" for longitude, "no_lat" for latitude.
* How to solve: provide missing required argument.

---
* Code: 400

* Content:
```json
{
  "code": "invalid_lat",
  "msg" : "Невалидная широта."
}
```
* Possible codes: "invalid_long" for invalid longitude, "invalid_lat" for latitude.
* How to solve: provide valid argument.
---

* Code: 400

* Content: 
```json
{
  "code": "invalid_geo_state",
  "msg" : "На данным момент приложение работает только на територии Архангельской области. Пожалуйста, измените выбор местоположения."
}
```

* How to solve: provide latitude and longitude belonged to the Arkhangelsk's area.


Sample Call:

```bash
curl -X POST -H "Content-Type:multipart/form-data" -F "long=12.12334" -F "lat=12.12334" -F "photo=@test_photo.jpg" http://0.0.0.0:8000/api/v1/reports/
```

### Interface to list all reports

| URI         | Method | Authorization |
|-------------|--------|---------------|
|`/reports/`  | `GET`  | not required  |

Success Response:

* Code: 200
* Content: 

```json
{
    "count": 2,
    "next": "http://0.0.0.0:8000/api/v1/reports/?page=2",
    "previous": null,
    "results": [
        {
            "datetime_received": "2019-12-30T13:18:39.566743+03:00",
            "photo": "http://0.0.0.0:8000/api/v1/reports/photos/2019/12/06/test_photo.jpg",
            "lat": 64.61833411,
            "long": 40.9587337
        }
    ]
}
```
Page limit is 10 reports per page.

Sample Call to get 11th-20th reports:

```bash
curl http://0.0.0.0:8000/api/v1/reports/?page=2
```
