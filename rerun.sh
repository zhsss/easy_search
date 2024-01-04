docker stop cucRatingFrontend
docker rm cucRatingFrontend
docker run -d -p 8080:80 --name cucRatingFrontend cuc-rating-frontend