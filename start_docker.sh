cd ds/search_d3js_graph/
service docker start
docker build -t flask_test .; docker run -it --rm  --publish 5000:5000 flask_test

