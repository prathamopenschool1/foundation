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
    AppId = models.CharField(max_length=200)
    AppName = models.CharField(max_length=200)
    ThumbUrl = models.CharField(max_length=200)
    AppDesc = JSONField(default={}, blank=True)
    AppOrder = models.CharField(max_length=500, default="file name which will be downloaded")
    DateUpdated = models.CharField(max_length=100)

    # print(Key_Id, AppId, ParentId, JsonData, FileDownload, DateUpdated)

    @classmethod
    def create(cls, AppId, AppName, ThumbUrl, AppDesc, AppOrder, DateUpdated):
        app_data = cls(AppId=AppId, AppName=AppName, ThumbUrl=ThumbUrl, AppDesc=AppDesc,
                       AppOrder=AppOrder, DateUpdated=DateUpdated)
        return app_data

    # def __str__(self):
    #     return self.AppId

