echo 'deploy script testing'
docker push registry.heroku.com/still-spire-18415/web
heroku container:release web --app still-spire-18415 --verbose