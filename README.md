# How to use

Build the docker image and run the container using

    docker run -it -v`pwd`:/scratch --rm pyast python3 ast_test.py /scratch/controller.py /scratch/output.csv
    
where "controller.py" is the Python file to be analyzed
