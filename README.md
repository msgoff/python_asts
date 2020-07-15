# How to use

Build the docker image and run the container using

    docker run -it -v`pwd`:/scratch --rm pyast python3 ast_test.py /scratch/controller.py /scratch/output.csv
    docker run -it -v`pwd`:/scratch --rm pyast python3 dot_file_from_df.py /scratch/output.csv /scratch/file
    
where "controller.py" is the Python file to be analyzed
