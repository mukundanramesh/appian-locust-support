# Appian Locust Library - Consolidated Source Code

This document consolidates the key source files from the Appian Locust library for analysis.

## Project Overview

Appian Locust is a wrapper library around Locust for load testing Appian applications. It provides capabilities for:
- Logging in and logging out
- Form interactions (filling/submitting)
- Finding and interacting with basic components on a SAIL interface
- Navigating to records/reports/sites

## Directory Structure

```
appian-locust-main/
├── appian_locust/           # Main library package
│   ├── __init__.py         # Package initialization
│   ├── appian_client.py    # Main client for Appian interactions
│   ├── appian_task_set.py  # Task set for Locust
│   ├── visitor.py          # Visitor pattern implementation
│   ├── system_operator.py  # System operations
│   ├── feature_flag.py     # Feature flag management
│   ├── objects/            # Object models
│   ├── uiform/             # UI form handling
│   ├── utilities/          # Utility functions
│   ├── info/              # Information classes
│   ├── exceptions/        # Custom exceptions
│   └── docs/              # Documentation
├── tests/                  # Test files
├── examples/              # Example usage files
├── bin/                   # Build/release scripts
├── setup.py              # Package setup
├── README.rst            # Documentation
└── requirements files
```

## Core Source Files

### 1. appian_client.py - Main Client Class

```python
import greenlet
import os
import urllib.parse
from typing import Tuple, Optional

from locust.clients import HttpSession
from requests import Response

from .utilities import logger
from .utilities import loadDriverUtils, DEFAULT_CONFIG_PATH
from ._feature_toggle_helper import get_client_feature_toggles
from ._interactor import _Interactor
from ._actions import _Actions
from ._news import _News
from ._records import _Records
from ._reports import _Reports
from ._sites import _Sites
from ._tasks import _Tasks
from .visitor import Visitor
from .system_operator import SystemOperator
from .info import ActionsInfo, NewsInfo, RecordsInfo, ReportsInfo, SitesInfo, TasksInfo

log = logger.getLogger(__name__)


class AppianClient:
    def __init__(self, session: HttpSession, host: str, base_path_override: Optional[str] = None, portals_mode: bool = False,
                 config_path: str = DEFAULT_CONFIG_PATH, is_mobile_client: bool = False) -> None:
        """
        Appian client class contains all the required functions to interact with Tempo.

        Note: This class will be called inside ``AppianTaskSet`` so it is not necessary to call this explicitly in a test.
        ``self.appian`` can be used directly in a test.

        Args:
            session: Locust session/client object
            host (str): Host URL
            base_path_override (str): override for sites where /suite is not the base path
            config_path (str): path to configuration file
            is_mobile_client(bool): set to True if client should act as mobile

        """
        self.client = session
        self.portals_mode = portals_mode
        self.host = _trim_trailing_slash(host)

        timeout = 300
        if os.path.exists(config_path):
            config_timeout = loadDriverUtils().load_config(config_path).get('request_timeout', None)
            if config_timeout:
                log.info(f"Overriding default timeout to {config_timeout}s")
                timeout = config_timeout

        self._interactor = _Interactor(self.client, self.host, portals_mode=portals_mode, request_timeout=timeout)
        self._news = _News(self._interactor)
        self._actions = _Actions(self._interactor)
        self._tasks = _Tasks(self._interactor)
        self._reports = _Reports(self._interactor)
        self._records = _Records(self._interactor, is_mobile_client=is_mobile_client)
        self._sites = _Sites(self._interactor)

        self._visitor = Visitor(self._interactor,
                                self._tasks,
                                self._reports,
                                self._actions,
                                self._records,
                                self._sites)
        self._system_operator = SystemOperator(self._interactor, self._actions)

        # Adding a few session specific attributes to self.client to that it can be carried and handled by session
        # in case of having multiple sessions in the future.
        setattr(self.client, "feature_flag", "")
        setattr(self.client, "feature_flag_extended", "")

        # Used for sites where /suite is not in the URL, i.e. local builds
        setattr(self.client, "base_path_override", base_path_override)

    @property
    def actions_info(self) -> ActionsInfo:
        """
        Navigate to actions and gather information about available actions
        """
        return ActionsInfo(self._actions)

    @property
    def news_info(self) -> NewsInfo:
        """
        Navigate to news and fetch information on news entries
        """
        return NewsInfo(self._news)

    @property
    def records_info(self) -> RecordsInfo:
        """
        Navigate to records and gather information about available records
        """
        return RecordsInfo(self._records)

    @property
    def reports_info(self) -> ReportsInfo:
        """
        Navigate to reports and gather information about available reports
        """
        return ReportsInfo(self._reports)

    @property
    def sites_info(self) -> SitesInfo:
        """
        Get Site metadata object
        """
        return SitesInfo(self._sites)

    @property
    def tasks_info(self) -> TasksInfo:
        """
        Navigate to tasks and gather information about available tasks
        """
        return TasksInfo(self._tasks)

    @property
    def visitor(self) -> Visitor:
        """
        Visitor that can be used to navigate to different types of pages in an Appian instance
        """
        return self._visitor

    @property
    def system_operator(self) -> SystemOperator:
        """
        Abstraction used for system operation that do not require a UI
        """
        return self._system_operator

    def login(self, auth: Optional[list] = None, check_login: bool = True) -> Tuple[HttpSession, Response]:
        return self._interactor.login(auth, raise_error=check_login)

    def logout(self) -> None:
        """
        Logout from Appian
        """
        logout_uri = (
            self.host
            + "/suite/logout?targetUrl="
            + urllib.parse.quote(self.host + "/suite/tempo/")
        )

        headers = self._interactor.setup_request_headers(logout_uri)
        if hasattr(greenlet.getcurrent(), "minimal_ident"):
            log.info(f"Logging out user {self._interactor.auth[0]} from greenlet id {greenlet.getcurrent().minimal_ident}")
        else:
            log.info(f"Logging out user {self._interactor.auth[0]} from {greenlet.getcurrent()}")
        self._interactor.post_page(logout_uri, headers=headers, label="Logout.LoadUi", raise_error=False, check_login=False)
        self.client.cookies.clear()

    def get_client_feature_toggles(self) -> None:
        self.client.feature_flag, self.client.feature_flag_extended = ("7ffceebc", "1bff7f49dc1fffceebc") if self.portals_mode else (
            get_client_feature_toggles(self._interactor, self.client)
        )


class _NoOpEvents():
    def fire(self, *args: str, **kwargs: int) -> None:
        pass

    def context(self, *args: str, **kwargs: int) -> dict:
        return {}


def _trim_trailing_slash(host: str) -> str:
    return host[:-1] if host and host.endswith('/') else host


def appian_client_without_locust(host: str, record_mode: bool = False,
                                 base_path_override: Optional[str] = None) -> 'AppianClient':
    """
    Returns an AppianClient that can be used without locust to make requests against a host, e.g.

    >>> appian_client_without_locust()
    >>> client.login(auth=('username', 'password'))
    >>> client.get_client_feature_toggles()

    This can be used for debugging/ making CLI style requests, instead of load testing
    You MUST call client.get_client_feature_toggles() to correctly finish initializing the client.

    Returns:
        AppianClient: an Appian client that can be used
    """
    inner_client = HttpSession(_trim_trailing_slash(host), _NoOpEvents(), _NoOpEvents())
    if record_mode:
        setattr(inner_client, 'record_mode', True)
    return AppianClient(inner_client, host=host, base_path_override=base_path_override)
```

### 2. appian_task_set.py - Locust Task Set Integration

```python
import re
import uuid
from typing import List, Generator

from locust import SequentialTaskSet, TaskSet
from requests import JSONDecodeError

from .utilities import logger
from .feature_flag import FeatureFlag
from .utilities import DEFAULT_CONFIG_PATH
from .utilities.url_provider import UrlProvider, URL_PROVIDER_V0, URL_PROVIDER_V1
from .appian_client import AppianClient
from ._feature_toggle_helper import override_default_feature_flags

log = logger.getLogger(__name__)


class AppianTaskSet(TaskSet):
    def __init__(self, parent: TaskSet) -> None:
        """
        Locust performance tests with a TaskSet should set AppianTaskSet as their base class to have access to various functionality.
        This class handles creation of basic objects like ``self.appian`` and actions like ``login`` and ``logout``
        """

        super().__init__(parent)

        self.host = self.parent.host

        # A set of datatypes cached. Used to populate "X-Appian-Cached-Datatypes" header field
        self.cached_datatype: set = set()
        self.url_provider = None

    def on_start(self, portals_mode: bool = False, config_path: str = DEFAULT_CONFIG_PATH, is_mobile_client: bool = False) -> None:
        """
        Overloaded function of Locust's default on_start.

        It will create object self.appian and logs in to Appian

        Args:
            portals_mode (bool): set to True if connecting to portals site
            config_path (str): path to configuration file
            is_mobile_client (bool): set to True if client should act as mobile
        """
        self.portals_mode = portals_mode
        self.workerId = str(uuid.uuid4())
        base_path_override = self.parent.base_path_override \
            if hasattr(self.parent, "base_path_override") else ""
        self._appian = AppianClient(self.client, self.host, base_path_override=base_path_override,
                                    portals_mode=portals_mode, config_path=config_path, is_mobile_client=is_mobile_client)
        if not portals_mode:
            self.auth = self._determine_auth()
            self.appian.login(self.auth)
            resp = self.appian._interactor.get_page(self.host + '/suite/rest/a/sites/latest/locust-templates', check_login=False)
            if not resp.ok:
                resp = self.appian._interactor.get_page(uri=self.host + "/suite/tempo/news")
                test = r'\\\\\\/suite\\\\\\/rest\\\\\\/a\\\\\\/sites\\\\\\/latest\\\\\\/D6JMim\\\\\\/page\\\\\\/(.+)\\\\\\'
                m = re.search(test, resp.text)
                if m is None or m.group(1) == 'news':
                    # old way
                    self.appian._interactor.set_url_provider(URL_PROVIDER_V0)
                elif m.group(1) == 'p.news':
                    # new way
                    self.appian._interactor.set_url_provider(URL_PROVIDER_V1)
                else:
                    log.warning("appian-locust could not determine appian interaction url pattern.  Defaulting to v1.  If errors persist, you may explicitly try v0.")
                    self.appian._interactor.set_url_provider(URL_PROVIDER_V1)
            else:
                try:
                    self.appian._interactor.set_url_provider(UrlProvider(resp.json()))
                except (JSONDecodeError, ValueError):
                    log.warning("appian-locust could not determine appian interaction url pattern.  Defaulting to v1.  If errors persist, you may explicitly try v0.")
                    log.warning(f"content of the url pattern response: {resp.text}")
                    self.appian._interactor.set_url_provider(URL_PROVIDER_V1)

        self.appian.get_client_feature_toggles()

    def _determine_auth(self) -> List[str]:
        """
        Determines what Appian username/password will be used on simulated logins. Auth will be determined
        using the following rules:

        If only "auth" key exists in config file, use the corresponding username and password for every login

        If only "credentials" key exists, pop one pair of credentials per Locust user until there's only one pair left.
        Then use the last pair of credentials for all remaining logins

        If both of the above keys exist, first use up all pairs in the "credentials" key, then use the pair in "auth"
        repeatedly for all remaining logings.

        In distributed mode, if only "credentials" key exists, each load driver will use last pair of credentials in the subset
        assigned to it.

        For example, if there are 3 pairs of credentials and 5 users per driver:
            Load driver 1 user 1 will take credential pair 1
            Load driver 2 users 1-5 will take credential pair 2
            Load driver 1 user 2-5 (and all after) will take credential pair 3

        Args:
            None

        Returns:
            auth: 2-entry list formatted as follows: ["username", "password"]

        """
        auth = self.parent.auth
        if hasattr(self.parent, 'credentials') and \
                isinstance(self.parent.credentials, list) and \
                self.parent.credentials:
            if len(self.parent.credentials) > 1 or (len(self.parent.credentials) == 1 and auth):
                auth = self.parent.credentials.pop(0)
            else:
                auth = self.parent.credentials[0]
        return auth

    def on_stop(self) -> None:
        """
        Overloaded function of Locust's default on_stop.

        It logs out the client from Appian.
        """
        if not self.portals_mode:
            self.appian.logout()

    @property
    def appian(self) -> AppianClient:
        """
        A wrapper around the generated AppianClient
        """
        return self._appian

    def override_default_flags(self, flags_to_override: List[FeatureFlag]) -> None:
        """
        `override_default_flags` gets the flag mask to set all of the flags to true given
        a list of flag enums and overrides the current feature flag extended value to set
        these flags to true.
        """
        def flags_to_override_generator() -> Generator[FeatureFlag, None, None]:
            yield from flags_to_override
        override_default_feature_flags(self.appian._interactor, flags_to_override_generator)


class AppianTaskSequence(SequentialTaskSet, AppianTaskSet):
    """
    Appian Locust SequentialTaskSet. Provides functionality of Locust's SequentialTaskSet and Handles creation of basic
    objects like``self.appian`` and actions like ``login`` and ``logout``
    """

    def __init__(self, parent: SequentialTaskSet) -> None:
        super(AppianTaskSequence, self).__init__(parent)
```
### 3. visitor.py - Navigation and Page Interaction (First 100 lines)

```python
from typing import Optional
from urllib.parse import urlparse

from ._actions import _Actions
from ._data_fabric import _DataFabric
from ._control_panel_workspace import _ControlPanelWorkspace
from .uiform import (
    ApplicationUiForm,
    DesignUiForm,
    DesignObjectUiForm,
    RecordInstanceUiForm,
    RecordListUiForm,
    SailUiForm,
    AISkillUiForm
)
from ._design import _Design, AI_SKILL_DESCRIPTOR, validate_design_object_access_method
from ._interactor import _Interactor
from ._portals import _Portals
from ._rdo_interactor import _RDOInteractor
from ._records import _Records
from ._reports import _Reports
from ._sites import _Sites
from ._admin import _Admin
from ._tasks import _Tasks
from .uiform.InterfaceDesignerUiForm import InterfaceDesignerUiForm
from .utilities.helper import format_label
from .objects import DesignObjectType, PageType

_RDO_TYPE_TO_VISITOR_METHOD = {
    "aiSkill": "visit_ai_skill_by_id"
}


class Visitor:
    """
    Provides methods to get an interactable ``SailUiForm`` from an Appian instance. Each method will return the respected ``SailUiForm`` type for which it will allow
    interactions with the visited page.
    """

    def __init__(self, interactor: _Interactor, tasks: _Tasks, reports: _Reports, actions: _Actions, records: _Records,
                 sites: _Sites):
        self.__interactor = interactor
        self.__tasks = tasks
        self.__reports = reports
        self.__records = records
        self.__sites = sites
        self.__actions = actions
        self.__data_fabric = _DataFabric(self.__interactor)
        self.__design = _Design(self.__interactor)
        self.__admin = _Admin(self.__interactor)
        self.__portals = _Portals(self.__interactor)
        self.__cp_workspace = _ControlPanelWorkspace(self.__interactor)

    def visit_task(self, task_name: str, exact_match: bool = True, locust_request_label: Optional[str] = None) -> SailUiForm:
        """
        Gets the SailUiForm given a task name

        Args:
            task_name (str): Name of the task to search for
            exact_match (bool, optional): Whether or not a full match is returned. Defaults to True.
            locust_request_label (str, optional): label to be used within locust

        Returns:
            SailUiForm: SAIL form for the task
        """
        initial_task_resp: dict = self.__tasks.get_task(task_name, exact_match)
        children = initial_task_resp.get("content", {}).get("children", [])
        task_title = children[0]

        if not locust_request_label:
            breadcrumb = f"Tasks.{task_title}"
        else:
            breadcrumb = locust_request_label
        return SailUiForm(self.__interactor, self.__tasks.get_task_form_json(task_name=task_title, locust_request_label=breadcrumb, exact_match=False), breadcrumb=breadcrumb)

    def visit_report(self, report_name: str, exact_match: bool = True, locust_request_label: Optional[str] = None) -> 'SailUiForm':
        """
        Navigate to a report and return a SailUiForm for that report's UI

        Args:
            report_name (str): Name of the report to be called.
            exact_match (bool, optional): Should report name match exactly or to be partial match. Default : True
            locust_request_label (str, optional): Label locust should associate this request with

        Returns (SailUiForm): Response of report's Get UI call in SailUiForm

        """
        breadcrumb = f'Reports.SailUi.{format_label(report_name, "::", 0)}'
        locust_request_label = locust_request_label or f"Visit.Report.{report_name}"
        return SailUiForm(self.__interactor, self.__reports.fetch_report_json(report_name, exact_match, locust_request_label=locust_request_label), breadcrumb=breadcrumb)

    def visit_design(self, locust_request_label: Optional[str] = None) -> DesignUiForm:
        """
        Navigate to /design
        Args:
            locust_request_label (str, optional): label to be used within locust

        Returns (DesignUiForm): UiForm representing /design

        """
        # ... (method continues)
```
## Example Usage Files

### 4. example_locustfile.py - Basic Example

```python
from locust import HttpUser, task
from appian_locust import AppianTaskSet


class GetReportsTaskSet(AppianTaskSet):

    @task
    def get_all_reports(self):
        self.appian.reports_info.get_all_available_reports()


class UserActor(HttpUser):
    tasks = [GetReportsTaskSet]
    host = 'https://mysitename.net'
    auth = ["myusername", "mypassword"]
```

### 5. example_create_employee_record.py - Record Creation Example

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task


class RecordsTaskSet(AppianTaskSet):

    @task
    def create_new_employee(self):
        # Navigate to Employee Record List
        record_list_uiform = self.appian.visitor.visit_record_type(record_type="Employees")

        # Click on "New Employee" Record List Action
        record_list_uiform.click_record_list_action(label="New Employee")

        # Fill in new Employee information
        record_list_uiform.fill_text_field(label="First Name", value="Sample")
        record_list_uiform.fill_text_field(label="Last Name", value="User")
        record_list_uiform.fill_text_field(label="Department", value="Engineering")
        record_list_uiform.fill_text_field(label="Title", value="Senior Software Engineer")
        record_list_uiform.fill_text_field(label="Phone Number", value="(703) 442-8844")

        # Create Employee!
        record_list_uiform.click_button(label="Create")


class UserActor(HttpUser):
    tasks = [RecordsTaskSet]
    host = 'https://mysitename.net'
    auth = ["myusername", "mypassword"]
```
## Configuration and Utilities

### 6. example_config.json - Configuration Example

```json
{
    "host_address": "site-name.appiancloud.com",
    "auth": ["username", "password"],
    "endpoint_type":"view,list"
}
```

### 7. utilities/helper.py - Helper Functions (First 50 lines)

```python
import functools
import random
import re
import warnings
from typing import Any, Callable, Dict, Generator, List, Union, Optional
from ..exceptions import ComponentNotFoundException

import gevent  # type: ignore
from locust.env import Environment

from . import logger

ENV = Environment()
log = logger.getLogger(__name__)


def format_label(label: str, delimiter: Optional[str] = None, index: int = 0) -> str:
    """
    Simply formats the string by replacing a space with underscores

    Args:
        label: string to be formatted
        delimiter: If provided, string will be split by it
        index: used with delimiter parameter, which item will be used in the "split"ed list.

    Returns:
        formatted string

    """
    if delimiter:
        if not str(index).isnumeric():
            index = 0
        label = label.split(delimiter)[int(index)]

    return label.replace(" ", "_")


def _extract(obj: Any, key: str, vals: List[Any]) -> Generator:
    """Recursively search for values of key in JSON tree."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                yield from _extract(v, key, vals)
            elif k == key and v in vals:
                yield obj

    elif isinstance(obj, list):
        for item in obj:
            yield from _extract(item, key, vals)
```
## Package Structure and Key Components

### 8. objects/__init__.py - Object Model Exports

```python
from .application import Application
from .ai_skill_type import AISkillObjectType
from .design_object import DesignObject, DesignObjectType
from .page import *
from .site import Site
```

### 9. exceptions/exceptions.py - Custom Exception Classes

```python
from datetime import date


class BadCredentialsException(Exception):
    def __init__(self) -> None:
        super(Exception, self).__init__("Could not log in, check the credentials")


class MissingCsrfTokenException(Exception):
    def __init__(self, found_cookies: dict) -> None:
        super(Exception, self).__init__(
            f"Login unsuccessful, no multipart cookie found, only found {found_cookies}, make sure credentials are correct")


class MissingConfigurationException(Exception):
    def __init__(self, missing_keys: list) -> None:
        super(Exception, self).__init__(
            f'Missing keys in configuration file, please verify that all of the following exist and are correct: {missing_keys}')


class IncorrectDesignAccessException(Exception):
    def __init__(self, object_type: str, correct_access_method: str) -> None:
        super().__init__(
            f"Selected Design Object was of type {object_type}, use {correct_access_method} method instead")


class MissingUrlProviderException(Exception):
    def __init__(self) -> None:
        super().__init__("Url Provider not initialized in Interactor")


class InvalidDateRangeException(Exception):
    def __init__(self, start_date: date, end_date: date) -> None:
        super().__init__(
            f"Start Date of {start_date.isoformat()} occurs after End Date of {end_date.isoformat()}")
        
class DisabledComponentException(Exception):
    def __init__(self, label: str) -> None:
        super().__init__(f"Cannot interact with disabled component with label '{label}'")

class IgnoredValidationException(Exception):
    def __init__(self, breadcrumb: str) -> None:
        super().__init__(f"At least one validation was found in the form {breadcrumb}")

class ComponentNotFoundException(Exception):
    pass


class InvalidComponentException(Exception):
    pass


class ChoiceNotFoundException(Exception):
    pass


class SiteNotFoundException(Exception):
    pass


class PageNotFoundException(Exception):
    pass


class InvalidSiteException(Exception):
    pass
```
## Complete File Listing

### Python Source Files (104 total files)

**Core Library Files:**
- `appian_locust/__init__.py` - Package initialization
- `appian_locust/appian_client.py` - Main client class
- `appian_locust/appian_task_set.py` - Locust task set integration
- `appian_locust/visitor.py` - Navigation and page interaction
- `appian_locust/system_operator.py` - System operations
- `appian_locust/feature_flag.py` - Feature flag management

**Internal Modules:**
- `appian_locust/_interactor.py` - Core HTTP interaction layer
- `appian_locust/_actions.py` - Actions functionality
- `appian_locust/_news.py` - News feed interactions
- `appian_locust/_records.py` - Record operations
- `appian_locust/_reports.py` - Report interactions
- `appian_locust/_sites.py` - Site navigation
- `appian_locust/_tasks.py` - Task management
- `appian_locust/_design.py` - Design object interactions
- `appian_locust/_grid_interactor.py` - Grid component interactions

**UI Form Handlers:**
- `appian_locust/uiform/uiform.py` - Base UI form class (107KB - largest file)
- `appian_locust/uiform/record_uiform.py` - Record form interactions
- `appian_locust/uiform/record_list_uiform.py` - Record list interactions
- `appian_locust/uiform/application_uiform.py` - Application form handling
- `appian_locust/uiform/design_uiform.py` - Design interface forms
- `appian_locust/uiform/InterfaceDesignerUiForm.py` - Interface designer

**Object Models:**
- `appian_locust/objects/` - Data models for Appian objects
- `appian_locust/exceptions/` - Custom exception classes
- `appian_locust/info/` - Information gathering classes
- `appian_locust/utilities/` - Helper functions and utilities

**Examples and Tests:**
- `examples/` - Usage examples (10 files)
- `tests/` - Unit tests (39 files)
- `setup.py` - Package configuration

## Key Features Summary

1. **Locust Integration**: Seamless integration with Locust load testing framework
2. **Authentication**: Automatic login/logout handling with credential management
3. **UI Interaction**: Comprehensive SAIL interface interaction capabilities
4. **Navigation**: Visitor pattern for navigating different Appian page types
5. **Form Handling**: Specialized form classes for different UI contexts
6. **Grid Operations**: Advanced grid interaction and data manipulation
7. **Record Management**: Full CRUD operations on Appian records
8. **Report Access**: Report navigation and interaction
9. **Site Navigation**: Multi-site and portal support
10. **Error Handling**: Comprehensive exception handling for common scenarios

## Dependencies

- `locust>=2.40.2` - Load testing framework
- `uritemplate>=4.1.1` - URI template processing
- `sseclient-py>=1.8.0` - Server-sent events client

This consolidated document provides a comprehensive overview of the Appian Locust library structure and key components for LLM analysis.
