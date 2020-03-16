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
    NodeId = models.CharField(max_length=100, default='')
    NodeType = models.CharField(max_length=100, default='')
    NodeTitle = models.CharField(max_length=100, default='')
    JsonData = JSONField(default={}, blank=True)
    ParentId = models.CharField(max_length=100, blank=True, null=True)
    AppId = models.CharField(max_length=100, default='')
    DateUpdated = models.CharField(max_length=100, default='')

    # print(Key_Id, AppId, ParentId, JsonData, FileDownload, DateUpdated)

    @classmethod
    def create(cls, NodeId, NodeType, NodeTitle, JsonData, ParentId, AppId, DateUpdated):
        app_data = cls(NodeId=NodeId, NodeType=NodeType, NodeTitle=NodeTitle, JsonData=JsonData,
                       ParentId=ParentId, AppId=AppId, DateUpdated=DateUpdated)
        return app_data

    # def __str__(self):
    #     return self.AppId


class FilesRelatedToAppsList(models.Model):
    FileId = models.IntegerField()
    NodeId = models.CharField(max_length=100)
    FileType = models.CharField(max_length=100)
    FileUrl = models.URLField(max_length=500)
    DateUpdated = models.CharField(max_length=100)

    @classmethod
    def create(cls, FileId, NodeId, FileType, FileUrl, DateUpdated):
        file_data = cls(FileId=FileId, NodeId=NodeId, FileType=FileType, FileUrl=FileUrl,
                        DateUpdated=DateUpdated)

        return file_data

