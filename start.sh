if [ ! -d "$PWD/data" ]; then
  mkdir $PWD/data
fi

docker run --name rating_redis -d -p 6379:6379 -v $PWD/data:/data -v $PWD/redis.conf:/etc/redis/redis.conf  redis:6.0 /etc/redis/redis.conf
docker run -d -p 8000:8000 --name cuc_rating --link rating_redis:db --env db=db -e TZ=Asia/Shanghai cuc_rating
