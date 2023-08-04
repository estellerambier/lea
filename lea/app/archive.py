from __future__ import annotations

import datetime as dt
import json
import os

import lea


def archive(views_dir: str, schema: str, view_name: str):
    from google.oauth2 import service_account
    from lea.clients.bigquery import BigQuery

    client = BigQuery(
        credentials=service_account.Credentials.from_service_account_info(
            json.loads(os.environ["LEA_BQ_SERVICE_ACCOUNT"])
        ),
        project_id="carbonfact-gsheet",
        location="EU",
        dataset_name="archive",
        username=None,
    )

    view = {(view.schema, view.name): view for view in lea.views.load_views(views_dir)}[
        schema, view_name
    ]

    today = dt.date.today()
    archive_view = lea.views.GenericSQLView(
        schema="",
        name=f"kaya__{view.schema}__{view.name}__{today.strftime('%Y_%m_%d')}",
        query=f"SELECT * FROM kaya.{view.schema}__{view.name}",  # HACK
    )
    client.create(archive_view)
