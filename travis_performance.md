# Totals

Total time:
- 4:13
- 7:04
- 6.36
- 5:48
- 3:58
- 4:15


# Stages

test:
- 1:47
- 2:43
- 2:36
- 2:36
- 2:16

publish:
- 1:22
- 2:08
- 2:06
- 2:09
- 0:47

deploy:
- 1:04
- 2:13
- 1:54
- 1:03
- 0:55


# Commands


## test

### docker build --target test --tag todo-app-test .
- 76.75
- 131.52
- 126.01
- 128.13

### e2e tests
- 6.99
- 7.00
- 6.77
- 6.88


## publish

### docker build --target prod --build-arg BUILDKIT_INLINE_CACHE=1 --tag samseedsoftwire/todo-app-prod:$TRAVIS_COMMIT .
- 45.74
- 95.29
- 93.94
- 93.33

### docker push samseedsoftwire/todo-app-prod:$TRAVIS_COMMIT
- 11.59
- 9.65
- 9.06
- 14.03

## deploy

### docker pull samseedsoftwire/todo-app-prod:latest
- 21.13
- 71.23
- 71.30
- 20.40

### docker build --target prod --cache-from samseedsoftwire/todo-app-prod:latest .
- 2.95
- 3.04
- 3.13
- 3.19

### rvm $(travis_internal_ruby) --fuzzy do ruby -S gem install dpl
- 13.88
- 12.51
- 13.17
- 13.52

### curl 'https://still-spire-18415.herokuapp.com/'
- 0.74
- 20.41
- 0.44
- 0.44