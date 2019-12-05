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
lon=12.12334
photo=test_photo.jpg
comment=some_text_string
feedback_info=some_text_string
```

Success Response:

* Code: 201

Sample Call:

```bash
curl -X POST -H "Content-Type:multipart/form-data" -F "lon=12.12334" -F "lat=12.12334" -F "photo=@test_photo.jpg" http://0.0.0.0:8000/api/v1/reports/
```
