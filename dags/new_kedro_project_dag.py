from collections import defaultdict

from pathlib import Path

from airflow import DAG
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.version import version
from datetime import datetime, timedelta

from kedro.framework.session import KedroSession
from kedro.framework.project import configure_project


class KedroOperator(BaseOperator):

    @apply_defaults
    def __init__(
        self,
        package_name: str,
        pipeline_name: str,
        node_name: str,
        project_path: str,
        env: str,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.package_name = package_name
        self.pipeline_name = pipeline_name
        self.node_name = node_name
        self.project_path = project_path
        self.env = env
        import logging
        logging.info("Init Kedro Operator")

    def execute(self, context):
        import logging
        logging.info("******Configure******")
        configure_project(self.package_name)
        logging.info("******Start Kedro Session******")
        try:
            logging.info(self.package_name)
            logging.info(self.project_path)
            logging.info(self.env)
            KedroSession.create(env=self.env) 
        except Exception as e:
            logging.info(f"failed {e}")
            raise e
        logging.info("Done")
        # with KedroSession.create(self.package_name,
        #                          self.project_path,
        #                          env=self.env) as session:
        #     logging.info("******Start Running Kedro******")
        #     session.run(self.pipeline_name, node_names=[self.node_name])

# Kedro settings required to run your pipeline
env = "airflow"
pipeline_name = "__default__"
project_path = Path.cwd()
package_name = "new_kedro_project"

# Default settings applied to all tasks
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG(
    "new-kedro-project",
    start_date=datetime(2019, 1, 1),
    max_active_runs=1,
    schedule_interval=timedelta(minutes=30),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    default_args=default_args,
    catchup=False # enable if you don't want historical dag runs to run
) as dag:
    import logging
    logging.info("Start - 1")
    tasks = {}
    logging.info("Start - 2")
    tasks["split"] = KedroOperator(
        task_id="split",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="split",
        project_path=project_path,
        env=env,
    )
    # logging.info("Start - 3")
    # tasks["train"] = KedroOperator(
    #     task_id="train",
    #     package_name=package_name,
    #     pipeline_name=pipeline_name,
    #     node_name="train",
    #     project_path=project_path,
    #     env=env,
    # )
    # logging.info("Start - 4")
    # tasks["predict"] = KedroOperator(
    #     task_id="predict",
    #     package_name=package_name,
    #     pipeline_name=pipeline_name,
    #     node_name="predict",
    #     project_path=project_path,
    #     env=env,
    # )
    # logging.info("Start - 5")
    # tasks["report"] = KedroOperator(
    #     task_id="report",
    #     package_name=package_name,
    #     pipeline_name=pipeline_name,
    #     node_name="report",
    #     project_path=project_path,
    #     env=env,
    # )



    # tasks["split"] >> tasks["predict"]

    # tasks["split"] >> tasks["report"]

    # tasks["split"] >> tasks["train"]

    # tasks["train"] >> tasks["predict"]

    # tasks["predict"] >> tasks["report"]
if __name__ == "__main__":
    # from airflow.utils.state import State

    # dag.clear(dag_run_state=State.NONE)
    # dag.run()
    import airflow.model

    from airflow.model.dagbag import DagBag
    dag_file_path = "/home/test-user/dags/dag-file.py"
    dagbag = DagBag(dag_folder=dag_file_path)
    dagbag.dags['test-dag-id'].task_dict['task-id'].execute({})