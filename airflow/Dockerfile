FROM zhongjiajie/docker-airflow

USER root

ARG AIRFLOW_HOME=/usr/local/airflow

COPY app ${AIRFLOW_HOME}/app
COPY app/requirements.txt /requirements.txt
COPY dags ${AIRFLOW_HOME}/dags
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
RUN chown -R airflow: ${AIRFLOW_HOME}

WORKDIR /usr/local/airflow
USER airflow
