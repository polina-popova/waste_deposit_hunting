# waste_deposit_hunting

The waste_deposit_hunting project has the purpose to handle mobile users's reports about 
waste deposits in Arkhangelsk's area.

---

## API Docs

### Interface to post the report 

| URI         | Method | Authorization |
|-------------|--------|---------------|
|`/reports/`  | `POST` | not required  |


Param: data, where `comment` and `feedback_info` are not required.
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

* Content: {"photo":["Не был загружен файл."]} or {"lat":["Это поле обязательно."]}
* How to solve: provide missing required argument.


Sample Call:

```bash
curl -X POST -H "Content-Type:multipart/form-data" -F "long=12.12334" -F "lat=12.12334" -F "photo=@test_photo.jpg" http://0.0.0.0:8000/api/v1/reports/
```
