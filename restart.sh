docker stop cuc_rating
docker rm cuc_rating
docker run -d -p 8000:8000 --name cuc_rating --link rating_redis:db --env db=db -e TZ=Asia/Shanghai cuc_rating
