container_id="$(sudo docker ps|grep flask_test|cut -d ' ' -f1)"
sudo docker cp flask_tree.csv "$container_id":/home/appuser/app/static/ 
