# Appian-Locust Complete Documentation

**Source:** https://appian-locust.readthedocs.io/en/stable/

**Copyright:** 2026, Appian Corporation

---

## Table of Contents

1. [Overview](#overview)
2. [What is Appian Locust?](#what-is-appian-locust)
3. [Quick Installation Guide](#quick-installation-guide)
4. [How to Write a Locust Test](#how-to-write-a-locust-test)
5. [Appian Locust Companion](#appian-locust-companion)
6. [How to Run Tests](#how-to-run-tests)
7. [Debugging](#debugging)
8. [User Agents](#user-agents)
9. [Library Limitations](#library-limitations)
10. [Advanced Appian Locust Usage](#advanced-appian-locust-usage)
11. [Advanced Test Examples](#advanced-test-examples)
12. [Latest Release](#latest-release)
13. [API Reference](#api-reference)
14. [Contributing](#contributing)

---

## Overview

**Appian-Locust** is a tool for load and performance testing Appian applications. It wraps the Locust load driving framework to enable driving load against Appian instances.

### Key Features
- Logging in and logging out
- Form interactions (filling/submitting)
- Finding and interacting with basic components on a SAIL interface
- Navigating to records/reports/sites

### Repository
- View/contribute on GitLab: https://gitlab.com/appian-oss/appian-locust

---

## What is Appian Locust?

Appian Locust is a wrapper library around Locust for load testing Appian. This library is intended to be used as an alternative to tools such as JMeter and LoadRunner.

### What is Locust?

Locust is an open source Python library for load testing (similar to JMeter, but in Python). It is HTTP-driven by default but can work with other types of interactions.

**Benefits of Locust:**
- Lower overhead than Selenium or browser automation frameworks
- Python is a common language across software and quality engineers
- Easy to compose user operations using TaskSets and TaskSequences
- Appian-Locust extends these with `AppianTaskSet` and `AppianTaskSequence`

### SAIL Navigation

Appian interfaces are built with SAIL (Self-Assembling Interface Layer). It's a RESTful contract controlling state between browser/mobile clients and the server.

**How it works:**
- SAIL interactions require updating server-side context
- Updates are expressed as JSON requests ("SaveRequests")
- Each SaveRequest returns an updated component or new form
- Appian Locust abstracts these requests into easy-to-use methods

---

## Quick Installation Guide

### Prerequisites
- Python 3.13+
- Recommended: `pipenv` and `pyenv` for environment management

### Manual Setup

**Using pip:**
```bash
pip install appian-locust
```

**Using pipenv (recommended):**

Create a `Pipfile`:
```toml
[packages]
appian-locust = {version = "*"}

[requires]
python_version = "3.13"
```

### Build from Source

1. Clone the repository:
```bash
git clone -o prod git@gitlab.com:appian-oss/appian-locust.git
```

2a. Install globally:
```bash
pip install -e appian-locust
```

2b. Or within a virtual environment:
```bash
pipenv install -e appian-locust
```

### Automatic Setup

Use the provided setup script to automate installation:

1. Clone the repository:
```bash
git clone -o prod git@gitlab.com:appian-oss/appian-locust.git
```

2. Make the script executable:
```bash
cd appian-locust/
chmod +x setup.sh
```

3. Run the setup:
```bash
./setup.sh
```

4. Activate the virtual environment:
```bash
pipenv shell
```

### Test Environment Setup

Download the sample test and run it:
```bash
locust -f example_locustfile.py
```

If successful, you'll see a link to the Locust web interface.

### Troubleshooting

**Installation Issues:**
- **Permissions issue when cloning:** Add SSH key to GitLab profile or download ZIP bundle
- **"locust is not available":** Verify installation and check PATH includes Python/Pyenv directory
- **Python version errors:** Requires Python 3.13+, use `pyenv` to manage versions

**Connection & Authentication Issues:**
- **Connection failed:** Verify `host_address` in config.json (without https://)
- **Login unsuccessful:** Verify username/password and user permissions
- **SSL/Certificate errors:** May need to disable SSL verification for self-signed certificates

**Runtime Issues:**
- **Tests run but no interactions complete:** Verify Appian site accessibility and user permissions

For detailed debugging, see the Debugging Guide.

---

## How to Write a Locust Test

The majority of work involves creating Locust Tasks. Each Task represents a workflow for a virtual user to execute.

### Core Concepts
1. **Visitor class:** Handles navigation to Appian interfaces
2. **SailUiForm class:** Handles UI interactions

### Sample Workflow

**Goal:** Create a new Employee record

**Steps:**
1. Navigate to Employee Record List
2. Click "New Employee" button
3. Fill in First Name, Last Name, Department, Title, Phone Number
4. Click "Create" button

### Appian Navigation - Visitor

The `Visitor` class handles all navigation in Appian Locust. It can navigate to Sites, Records, Reports, Portals, and other interfaces, returning a `SailUiForm` for interaction.

**Example:**
```python
@task
def create_new_employee(self):
    # Navigate to Employee Record List
    record_list_uiform = self.appian.visitor.visit_record_type(record_type="Employees")
```

### UI Interactions - SailUiForm

The `SailUiForm` class enables interaction with UI elements. It supports:
- Filling text fields
- Clicking buttons
- And more

**Specialized subclasses:**
- `RecordListUiForm` - For Record Lists (includes `click_record_list_action`)
- Other interface-specific subclasses

**Complete Example:**
```python
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
```

---

## Appian Locust Companion

The Appian Locust Companion (ALC) is a Google Chrome extension that simplifies writing performance tests by recording your interactions.

### Overview

ALC captures your interactions with Appian and converts them into Appian Locust function calls with parameters. It provides a point-and-click way to get started with performance testing.

### Getting Started

1. **Install the Extension** from the Chrome Web Store
2. **Launch the Extension:** Navigate to your Appian interface, launch ALC, grant permissions, refresh the browser tab, and click "Record Interactions"
3. **Generate Performance Test:** As you interact with Appian, the extension outputs Appian Locust function calls

### Best Practices

**Component Configuration:**
- Add labels or test labels to Appian components for better recognition
- Missing labels may result in incomplete function parameters

**Permissions:**
- Extension requests permission to read data (it only reads, never modifies)

### Extension Limitations

- Only supports interactions already supported by Appian Locust library
- Tab-specific behavior - not recommended to switch tabs during recording
- Some functions may appear without parameters if components lack labels

### Support

Reach out via the Support Hub option in the Chrome Web Store for feedback or assistance.

---

## How to Run Tests

### Command Line Flow

Run Locust in headless mode:

```bash
locust -f examples/example_locustfile.py -u 1 -r 10 -t 3600 --headless
```

#### Required Arguments

- `-r` (rate): Hatch rate
- `-u` (users): Number of users
- `-t`: Test duration in seconds
- `--headless`: Run without web UI

**Additional useful arguments:**
- `--csv-full-history`: Prints percentile changes every 30 seconds

**Recommended:** Capture log output
```bash
locust -f example_locustfile.py -u 1 -r 10 -t 3600 --headless | tee run.log
```

### Web Flow

Launch Locust with web interface:

```bash
locust -f example_locustfile.py
```

Navigate to http://localhost:8089/ to see the web interface where you can:
- Configure test parameters
- Start swarming
- View graphs for latencies, errors, and other data

**Note:** Web mode is not recommended for automation as it requires manual interaction.

---

## Debugging

### Initial Troubleshooting Steps

- Start simple: Test with a single user before scaling up
- Use print statements strategically
- Verify test environment is accessible
- Check Locust's web UI for detailed request statistics
- Monitor system resources (CPU, memory)

### Request and Response Recording

Enable detailed recording of HTTP requests and responses:

```python
class YourTaskSet(AppianTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.client.record_mode = True

    @task
    def your_test(self):
        # Your test code here
        pass
```

When enabled, all requests/responses are saved in a `recorded_responses` folder. On Appian Cloud, a trace ID is printed for sharing with Appian Support.

### Common Debugging Scenarios

**Monitoring execution:**
- Look for slow requests
- High failure rates for specific operations
- Review Locust logs for exceptions
- Request trends over time

**Debugging UI State:**
```python
import json

@task
def debug_page_state(self):
    uiform = self.appian.visitor.visit_record_type("YourRecord")
    print(f"Current page components: {uiform._state}")

    # Write to file for easier inspection
    with open('page_state.json', 'w') as f:
        f.write(json.dumps(uiform._state, indent=2))
```

**Increase logging verbosity:**
```bash
locust -f your_test.py --loglevel DEBUG
```

### Browser Comparison

Compare Appian Locust requests with actual browser behavior:
1. Open browser developer tools (F12) → Network tab
2. Perform the same actions manually
3. Compare requests that Appian Locust sends vs. browser
4. Look for differences in requests and payloads
5. Ensure responses are relevant for components being tested

### Single-User Debug Mode

Run tests in single-user mode to use IDE breakpoints:

```python
from locust import run_single_user
from your_test_file import YourUserActor

# Run a single user for debugging
run_single_user(YourUserActor)
```

This allows you to:
- Set breakpoints in your IDE
- Step through test execution
- Inspect variables and state
- Debug complex workflows interactively

### Getting Help

If issues persist:
- Check GitLab Issues for similar problems
- Review full documentation
- Create a new issue if needed
- Consider suggesting documentation improvements

---

## User Agents

Appian Locust uses the following user agent strings:

**Desktop:**
```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
```

**Mobile:**
```
AppianAndroid/24.4 (Google AOSP on IA Emulator, 9; Build 0-SNAPSHOT; AppianPhone)
```

### Override User Agents

```python
def __init__(self, environment) -> None:
    super().__init__(environment)
    self.client.user_agent_desktop = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    self.client.user_agent_mobile = "Mozilla/5.0 (Android 15; Mobile; rv:68.0) Gecko/68.0 Firefox/134.0"
```

---

## Library Limitations

**Disclaimer:** This library is continuously evolving. The main focus is supporting essential use-cases. Contributions are welcome for extending functionality, bug fixes, and usability improvements.

### Currently Unsupported Appian Interactions

- Multiple links with the same name on the same page (use labels to differentiate)
- SafeLinks (can link to locations external to Appian)
- Legacy forms

---

## Advanced Appian Locust Usage

### Loading Test Settings from Config

Load configuration from a `config.json` file:

```python
from appian_locust.utilities import loadDriverUtils

utls = loadDriverUtils()
utls.load_config()

config = utls.c
auth = config['auth']
host = "https://" + config['host_address']
```

**Minimal config.json:**
```json
{
    "host_address": "site-name.appiancloud.com",
    "auth": [
        "user.name",
        "password"
    ]
}
```

### Multiple User Types with Different Credentials

Create different user types with different behaviors, credentials, and weights:

```python
class RegularUserTaskSet(AppianTaskSet):
    @task
    def browse_records(self):
        self.appian.visitor.visit_record_type(record_type="Employees")

class ManagerUserTaskSet(AppianTaskSet):
    @task
    def manager_operations(self):
        self.appian.visitor.visit_record_type(record_type="Departments")

class RegularUserActor(HttpUser):
    """Regular users - weight 3"""
    tasks = [RegularUserTaskSet]
    host = f'https://{utls.c["host_address"]}'
    auth = utls.c["auth"][0]
    wait_time = between(0.5, 1.0)
    weight = 3

class ManagerUserActor(HttpUser):
    """Manager users - weight 1"""
    tasks = [ManagerUserTaskSet]
    host = f'https://{utls.c["host_address"]}'
    auth = utls.c["auth"][1]
    wait_time = between(1.0, 2.0)
    weight = 1
```

**Multiple credentials in config.json:**
```json
{
    "host_address": "site-name.appiancloud.com",
    "auth": [
        ["regular.user", "password123"],
        ["manager.user", "managerpass456"]
    ]
}
```

**Important:** User count is spread evenly across HttpUsers. With weights 3:1, you need at least 4 users to start both user types.

### Procedurally Generated Credentials

For large-scale testing with hundreds or thousands of users:

**Add to config.json:**
```json
{
    "host_address": "site-name.appiancloud.com",
    "procedural_credentials_prefix": "testuser",
    "procedural_credentials_password": "testpassword123",
    "procedural_credentials_count": 100
}
```

**Use in test script:**
```python
from appian_locust.utilities.credentials import procedurally_generate_credentials

class UserActor(HttpUser):
    tasks = [YourTaskSet]
    host = f'https://{utls.c["host_address"]}'
    
    # Generate credentials procedurally
    procedurally_generate_credentials(utls.c)
    credentials = utls.c["credentials"]
```

This creates testuser1, testuser2, ..., testuser100 with the specified password.

### Request Duration Assertions

Add timing assertions for specific operations:

**Warning:** Analyzing aggregate test results after completion is strongly recommended over individual request assertions.

```python
import time
from locust import events

class time_assertion(object):
    def __init__(self, max_time, label="Operation"):
        self.max_time = max_time
        self.label = label

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.end_time = time.perf_counter()
        execution_time = self.end_time - self.start_time

        if execution_time > self.max_time:
            events.request.fire(
                request_type="Assertion",
                name=f"Performance threshold exceeded: {self.label}",
                response_time=execution_time * 1000,
                response_length=0,
                response=None,
                context=None,
                exception=f"{self.label} - execution time exceeded the limit of {self.max_time}s"
            )
            print(f"⚠️  {self.label} - execution time {execution_time:.4f}s exceeded the limit of {self.max_time}s")
```

**Usage:**
```python
@task
def monitored_workflow(self):
    with time_assertion(1.0, "Record Navigation"):
        uiform = self.appian.visitor.visit_record_type(record_type="Orders")

    with time_assertion(0.5, "Button Interaction"):
        uiform.click_button("Create New", locust_request_label="[Records.Create] New Order")
```

---

## Advanced Test Examples

The documentation includes several advanced examples:

1. **Locust Test Example: Records** - Working with record types and instances
2. **Locust Test Example: Grids** - Interacting with grid components
3. **Locust Test Example: Multiple Users** - Managing multiple user types
4. **Advanced Task Execution:**
   - Executing a specific number of tasks
   - Waiting until all users are spawned

Refer to the examples directory in the GitLab repository for complete code samples.

---

## Latest Release

### Version 2.0.0

Appian Locust v2.0 introduces a significant API rework for a clearer and more streamlined development experience.

#### New Paradigm

- **Visitor:** New hub for all SailUiForm navigations
- **SystemOperator:** For non-UI form interactions at system level (e.g., `get_webapi()`)
- **Info module:** Extended from `AppianClient`, provides metadata for News, Tasks, Records, Reports, Actions, and Sites

#### Breaking Changes

- **Python 3.10+ required**
- Fetching SailUIForms from News, Tasks, Records, Reports, Actions, and Sites marked as private - use `Visitor` instead
- SailUIForm types moved to `uiform` module
- Design objects and types moved to `objects` module
- Helper methods moved to `utilities` module
- `loadDriverUtils()` usage changed:
  ```python
  from appian_locust.utilities import loadDriverUtils
  utls = loadDriverUtils()
  ```

For comprehensive migration details, see the Appian Locust 2.0 Migration Guide.

---

## API Reference

### Core Classes

#### AppianClient
Main client for interacting with Appian instances.

**Properties:**
- `actions_info` - Navigate to actions and gather information
- `news_info` - Navigate to news and fetch information
- `records_info` - Navigate to records and gather information
- `reports_info` - Navigate to reports and gather information
- `sites_info` - Get Site metadata
- `system_operator` - System operations without UI
- `tasks_info` - Navigate to tasks and gather information
- `visitor` - Navigate to different page types

**Methods:**
- `get_client_feature_toggles()` - Get feature toggles
- `login(auth, check_login)` - Login to Appian
- `logout()` - Logout from Appian

#### AppianTaskSet
Base class for Appian Locust TaskSets.

**Properties:**
- `appian` - Wrapper around AppianClient
- `tasks` - Collection of callables/TaskSet classes

**Methods:**
- `on_start(portals_mode, config_path, is_mobile_client)` - Creates appian object and logs in
- `on_stop()` - Logs out from Appian
- `override_default_flags(flags_to_override)` - Override feature flags

#### AppianTaskSequence
Appian Locust SequentialTaskSet - provides functionality of Locust's SequentialTaskSet with Appian-specific features.

#### Visitor
Provides methods to get interactable `SailUiForm` from an Appian instance.

**Key Methods:**
- `visit_action(action_name, exact_match, locust_request_label)` - Visit an action
- `visit_record_type(record_type, locust_request_label)` - Visit a record type list
- `visit_record_instance(record_type, record_name, view_url_stub, exact_match, summary_view, locust_request_label)` - Visit a specific record
- `visit_report(report_name, exact_match, locust_request_label)` - Visit a report
- `visit_site(site_name, page_name, locust_request_label)` - Visit a site page
- `visit_task(task_name, exact_match, locust_request_label)` - Visit a task
- `visit_portal_page(portal_unique_identifier, portal_page_unique_identifier, locust_request_label)` - Visit a portal page
- `visit_design(locust_request_label)` - Navigate to /design
- `visit_admin(locust_request_label)` - Navigate to /admin

#### SystemOperator
Class for performing activities that don't require UI interaction.

**Methods:**
- `fetch_autosuggestions(payload, locust_request_label)` - Retrieve suggestions from autosuggest
- `fetch_content(opaque_id, locust_request_label)` - Fetch content element (e.g., image)
- `get_webapi(uri, headers, locust_request_label, query_parameters)` - Make GET request to web API
- `post_webapi(uri, headers, locust_request_label, payload)` - Make POST request to web API
- `start_action(action_name, skip_design_call, exact_match)` - Start an action without UI

### Enumerations

#### ClientMode
- ADMIN
- DESIGN
- DOCS_REPL
- EMBEDDED
- INTERFACE_DESIGN
- PORTALS
- PROCESS_HQ
- SAIL_LIBRARY
- SITES
- TEMPO

#### FeatureFlag
Extensive list of feature flags for controlling Appian functionality (60+ flags including ALL_FEATURES, NO_FEATURES, REACT_CLIENT, RECORD_NEWS, etc.)

### Helper Functions

- `appian_client_without_locust(host, record_mode, base_path_override)` - Returns AppianClient for use without Locust (debugging/CLI)

---

## Contributing

**Note:** By contributing to this Open Source project, you provide Appian Corporation a non-exclusive, perpetual, royalty-free license to use your contribution for any purpose.

### How to Contribute

1. Fork the appian-locust repository
2. Make desired changes
3. Commit changes and push to your fork
4. Make a merge request to upstream - project maintainers will review

### New Development

Core principle: User navigation and resulting interaction.

**Guidelines:**
- Adding interaction capabilities to existing page type? Add method to existing `SailUiForm` type
- New page type? Create new `SailUiForm` extension and ensure `Visitor` can visit it
- Non-interaction functionality? Include in `SiteHelper` class

Submit an issue if your development falls outside these criteria.

### Testing Your Changes

In your test-implementation repo, modify `Pipfile`:

```toml
appian-locust = {path="../appian-locust", editable=true}
```

Run:
```bash
pipenv install --skip-lock
```

### IDE Setup

**PyCharm:**
1. Open Settings → Project → Python Interpreter
2. Click dropdown → Show All
3. Click tree icon → plus icon
4. Navigate to local appian-locust repository

**VSCode:**
1. Open control palette (Cmd + Shift + P)
2. Select Preferences: Open Workspace Settings (JSON)
3. Add:
```json
{
    "python.analysis.extraPaths": ["<absolute-path-to>/appian-locust"]
}
```

### Internal Classes

The library provides internal classes for granular control during development/testing. These include:

- `_Actions` - Action-related operations
- `_Admin` - Admin interface operations
- `_Base` - Base class for common operations
- `_Design` - Design environment operations
- `_Interactor` - Core interaction functionality
- `_Records` - Record-related operations
- `_Reports` - Report-related operations
- `_Sites` - Site-related operations
- `_Tasks` - Task-related operations
- `GridInteractor` - Grid manipulation utilities
- `UiReconciler` - SAIL UI reconciliation

Refer to the API documentation for detailed information on internal classes.

---

## Additional Resources

- **GitLab Repository:** https://gitlab.com/appian-oss/appian-locust
- **Locust Documentation:** https://docs.locust.io/en/stable/
- **Appian SAIL Documentation:** https://docs.appian.com/suite/help/latest/SAIL_Design.html
- **Chrome Web Store (ALC Extension):** Search for "Appian Locust Companion"

---

## License & Copyright

© Copyright 2026, Appian Corporation

Built with Sphinx using a theme provided by Read the Docs.

---

*Content was rephrased for compliance with licensing restrictions*

*This documentation was compiled from the official Appian-Locust documentation available at https://appian-locust.readthedocs.io/en/stable/*
