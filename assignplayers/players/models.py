from django.db import models
from jsonfield import JSONField


class PlayersDatastore(models.Model):
    data = JSONField(default={}, blank=True)
    filter_name = models.CharField(max_length=100, default='enter filter name')
    table_name = models.CharField(max_length=100, default='enter table name')
    key_id = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @classmethod
    def create(cls, data, filter_name, table_name):
        crl_data = cls(data=data, filter_name=filter_name, table_name=table_name)
        return crl_data
    # def __str__(self):
    #     return self.data[0]


class AppsList(models.Model):
    Key_Id = models.CharField(max_length=200)
    AppId = models.CharField(max_length=200)
    ParentId = models.CharField(max_length=200)
    JsonData = JSONField(default={}, blank=True)
    FileDownload = models.CharField(max_length=500, default="file name which will be downloaded")
    DateUpdated = models.CharField(max_length=100)

    # print(Key_Id, AppId, ParentId, JsonData, FileDownload, DateUpdated)

    @classmethod
    def create(cls, Key_Id, AppId, ParentId, JsonData, FileDownload, DateUpdated):
        app_data = cls(Key_Id=Key_Id, AppId=AppId, ParentId=ParentId, JsonData=JsonData,
                       FileDownload=FileDownload, DateUpdated=DateUpdated)
        return app_data

    # def __str__(self):
    #     return self.AppId

