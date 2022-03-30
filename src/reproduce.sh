
mkdir astro_cloud_kedro
cd astro_cloud_kedro
astrocloud dev init
python -m venv venv && source venv/bin/activate
pip install kedro --ignore-requires-python
pip install kedro-airflow --ignore-requires-python
kedro new --starter=spaceflights
cp -r new-kedro-project/* . && rm -rf new-kedro-project
pip install -r src/requirements.txt --ignore-requires-python
kedro package

# Edit the DockerFile
FROM [quay.io/astronomer/astro-runtime:4.1.0](http://quay.io/astronomer/astro-runtime:4.1.0)

RUN pip install --user src/dist/new_kedro_project-0.1-py3-none-any.whl --ignore-requires-python
kedro airflow create --target-dir=dags/ --env=base
astrocloud dev start