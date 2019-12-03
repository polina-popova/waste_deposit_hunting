# waste_deposit_hunting

The waste_deposit_hunting project has the purpose to handle mobile users's reports about 
waste deposits in Arkhangelsk's area.

---

## Prepare env
```bash
sudo apt-get install binutils libproj-dev gdal-bin
docker run --name=postgis -d -e POSTGRES_USER=your_username -e POSTGRES_PASS=your_password -e POSTGRES_DBNAME=waste_deposit_hunting -p 5432:5432 kartoza/postgis:9.6-2.4
```

## Post report

```bash
curl -X POST -H "Content-Type:multipart/form-data" -F "location=POINT (10.1 10.2)" -F "photo=@test_photo.jpg" http://0.0.0.0:8000/api/v1/reports/
```