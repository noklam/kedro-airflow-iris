FROM quay.io/astronomer/astro-runtime:4.1.0

RUN pip install --user src/dist/new_kedro_project-0.1-py3-none-any.whl --ignore-requires-python
# ENV OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
# ENV AIRFLOW__CORE__KILLED_TASK_CLEANUP_TIME=604800