#!/usr/bin/python3
""" Provides frontend-independent access to the functions of the interface """

from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Optional, Union
from .tracer import Tracer
from .virtual_fs import VirtualFs
from .backup_downloader import TodoistBackupDownloader
from .backup_attachments_downloader import TodoistBackupAttachmentsDownloader

class TodoistAuth(NamedTuple):
    """ Represents the properties of a Todoist attachment """
    token: str
    email: Optional[str]
    password: Optional[str]

class ControllerDependencyInjector(metaclass=ABCMeta):
    """ Rudimentary dependency injection container for the controller """

    @abstractmethod
    def __init__(self, auth: TodoistAuth, verbose: bool):
        """ Initializes the dependencies according to the user configuration """

    @property
    @abstractmethod
    def tracer(self) -> Tracer:
        """ Gets an instance of the debug tracer """

    @property
    @abstractmethod
    def backup_downloader(self) -> TodoistBackupDownloader:
        """ Gets an instance of the Todoist backup downloader """

    @property
    @abstractmethod
    def backup_attachments_downloader(self) -> TodoistBackupAttachmentsDownloader:
        """ Gets an instance of the Todoist backup attachment downloader """

class Controller:
    """ Provides frontend-independent access to the functions of the interface """

    __dependencies: ControllerDependencyInjector
    def __init__(self, dependencies: ControllerDependencyInjector):
        self.__dependencies = dependencies

    def download(self, vfs: VirtualFs, with_attachments: Union[bool, str]) -> None:
        # On Python 3.8+ "Literal['ignore-forbidden']" instead of ^^^str^^^ above
        """ Generates a Todoist backup ZIP from the current Todoist items """
        self.__dependencies.backup_downloader.download(vfs)
        if with_attachments:
            self.__dependencies.backup_attachments_downloader.download_attachments(vfs,
                with_attachments == 'ignore-forbidden')
