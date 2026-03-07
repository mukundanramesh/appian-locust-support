# Appian Locust Library - Comprehensive Guide

> **Official Documentation**: [https://appian-locust.readthedocs.io/en/latest/](https://appian-locust.readthedocs.io/en/latest/)

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Core Concepts](#core-concepts)
4. [AppianClient API](#appianclient-api)
5. [Visitor Methods](#visitor-methods)
6. [SailUiForm Interaction Methods](#sailuiform-interaction-methods)
7. [Info Classes](#info-classes)
8. [SystemOperator](#systemoperator)
9. [Grid Operations](#grid-operations)
10. [Record Operations](#record-operations)
11. [Advanced Features](#advanced-features)
12. [Complete Examples](#complete-examples)

---

## Overview

**Appian Locust** is a Python wrapper library around [Locust](https://locust.io) designed specifically for load testing Appian applications. It provides a high-level API for interacting with Appian SAIL interfaces, records, reports, sites, and more.

### Key Capabilities

- **Authentication**: Automatic login/logout with credential management
- **Navigation**: Visit any Appian page type (sites, records, reports, tasks, actions, portals)
- **UI Interactions**: Fill forms, click buttons, select dropdowns, interact with grids
- **Record Management**: Full CRUD operations on Appian records
- **Report Access**: Navigate and interact with reports
- **Design Objects**: Interact with design objects, interfaces, and AI Skills
- **System Operations**: Trigger actions without UI, call web APIs
- **Load Testing**: Full integration with Locust for performance testing

### Dependencies

```python
locust>=2.40.2
uritemplate>=4.1.1
sseclient-py>=1.8.0
```

---

## Installation

### Quick Installation

```bash
pip install appian-locust
```

### Using Pipenv (Recommended)

```toml
[packages]
appian-locust = {version = "*"}

[requires]
python_version = "3.13"
```

Then run:
```bash
pipenv install
pipenv shell
```


### Build from Source

```bash
git clone -o prod git@gitlab.com:appian-oss/appian-locust.git
pip install -e appian-locust
```

### Automatic Setup Script

```bash
cd appian-locust/
chmod +x setup.sh
./setup.sh
pipenv shell
```

---

## Core Concepts

### 1. AppianTaskSet

Base class for all Locust tests. Handles initialization, login, and logout.

```python
from locust import HttpUser, task
from appian_locust import AppianTaskSet

class MyTaskSet(AppianTaskSet):
    @task
    def my_workflow(self):
        # Your test logic here
        pass

class UserActor(HttpUser):
    tasks = [MyTaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### 2. Visitor Pattern

The `Visitor` class provides navigation to different Appian page types. Every visit method returns a `SailUiForm` (or subclass) for interaction.

```python
# Access visitor through self.appian.visitor
form = self.appian.visitor.visit_record_type("Employees")
```

### 3. SailUiForm

Represents an interactive SAIL interface. Provides methods to fill fields, click buttons, select dropdowns, etc.

```python
form.fill_text_field(label="First Name", value="John")
form.click_button(label="Submit")
```

### 4. Info Classes

Provide read-only access to metadata about actions, records, reports, sites, tasks, and news.

```python
all_reports = self.appian.reports_info.get_all_available_reports()
```

---

## AppianClient API

The `AppianClient` is the main entry point for all Appian interactions. Access it via `self.appian` in your task sets.

### Properties

#### `appian.visitor` → Visitor
Navigate to different page types in Appian.

```python
form = self.appian.visitor.visit_site("My Site", "Home Page")
```

#### `appian.actions_info` → ActionsInfo
Get information about available actions.

```python
actions = self.appian.actions_info.get_all_available_actions()
```

#### `appian.news_info` → NewsInfo
Fetch news entries.

```python
news = self.appian.news_info.get_all_news()
```

#### `appian.records_info` → RecordsInfo
Get information about available records.

```python
records = self.appian.records_info.get_all_available_records()
```

#### `appian.reports_info` → ReportsInfo
Get information about available reports.

```python
reports = self.appian.reports_info.get_all_available_reports()
```

#### `appian.sites_info` → SitesInfo
Get site metadata.

```python
sites = self.appian.sites_info.get_all_sites()
```

#### `appian.tasks_info` → TasksInfo
Get information about available tasks.

```python
tasks = self.appian.tasks_info.get_all_available_tasks()
```

#### `appian.system_operator` → SystemOperator
Perform system operations without UI interaction.

```python
response = self.appian.system_operator.start_action("My Action", skip_design_call=True)
```

### Methods

#### `login(auth=None, check_login=True)`
Log in to Appian. Usually called automatically by `AppianTaskSet.on_start()`.

```python
self.appian.login(auth=["username", "password"])
```

#### `logout()`
Log out from Appian. Usually called automatically by `AppianTaskSet.on_stop()`.

```python
self.appian.logout()
```

#### `get_client_feature_toggles()`
Initialize client feature flags. Must be called after login.

```python
self.appian.get_client_feature_toggles()
```

---

## Visitor Methods

The `Visitor` class provides methods to navigate to different Appian page types. All methods return a `SailUiForm` or specialized subclass.

### Site Navigation

#### `visit_site(site_name, page_name, locust_request_label=None)` → SailUiForm
Navigate to a specific site page.

```python
form = self.appian.visitor.visit_site(
    site_name="Employee Portal",
    page_name="Dashboard"
)
```

#### `visit_site_recordlist(site_name, page_name, locust_request_label=None)` → RecordListUiForm
Navigate to a record list page on a site.

```python
record_list = self.appian.visitor.visit_site_recordlist(
    site_name="Employee Portal",
    page_name="All Employees"
)
```

#### `visit_site_recordlist_and_get_random_record_form(site_name, page_name, locust_request_label=None)` → RecordInstanceUiForm
Navigate to a site record list and click a random record.

```python
record_form = self.appian.visitor.visit_site_recordlist_and_get_random_record_form(
    site_name="Employee Portal",
    page_name="All Employees"
)
```

### Record Navigation

#### `visit_record_type(record_type, locust_request_label=None)` → RecordListUiForm
Navigate to a record type list.

```python
record_list = self.appian.visitor.visit_record_type(record_type="Employees")
```

#### `visit_record_instance(record_type, record_name, view_url_stub='', exact_match=False, summary_view=True, locust_request_label=None)` → RecordInstanceUiForm
Navigate to a specific record instance.

```python
record = self.appian.visitor.visit_record_instance(
    record_type="Employees",
    record_name="John Doe",
    summary_view=True
)
```

### Report Navigation

#### `visit_report(report_name, exact_match=True, locust_request_label=None)` → SailUiForm
Navigate to a report.

```python
report = self.appian.visitor.visit_report(
    report_name="Employee Report",
    exact_match=True
)
```

### Task Navigation

#### `visit_task(task_name, exact_match=True, locust_request_label=None)` → SailUiForm
Navigate to a task.

```python
task_form = self.appian.visitor.visit_task(
    task_name="Approve Request",
    exact_match=True
)
```

### Action Navigation

#### `visit_action(action_name, exact_match=False, locust_request_label=None)` → SailUiForm
Navigate to an action and return its form.

```python
# With full name including opaque ID
action_form = self.appian.visitor.visit_action(
    action_name="Create Employee::_a-0000e8a4-8d8e-8000-0f8f-011c48011c48_19427",
    exact_match=True
)

# With partial name match
action_form = self.appian.visitor.visit_action(
    action_name="Create Employee",
    exact_match=False
)
```

### Design Navigation

#### `visit_design(locust_request_label=None)` → DesignUiForm
Navigate to /design.

```python
design = self.appian.visitor.visit_design()
```

#### `visit_design_object_by_id(opaque_id, locust_request_label=None)` → DesignObjectUiForm
Visit a design object by its opaque ID.

```python
design_obj = self.appian.visitor.visit_design_object_by_id(
    opaque_id="_a-0000e8a4-8d8e-8000-0f8f-011c48011c48_19427"
)
```

#### `visit_design_object_by_name(object_name, object_type, locust_request_label=None)` → DesignObjectUiForm
Visit a design object by name and type.

```python
from appian_locust.objects import DesignObjectType

design_obj = self.appian.visitor.visit_design_object_by_name(
    object_name="Employee Interface",
    object_type=DesignObjectType.INTERFACE
)
```

#### `visit_interface_object_by_id(opaque_id, locust_request_label=None)` → InterfaceDesignerUiForm
Visit an interface in Interface Designer.

```python
interface = self.appian.visitor.visit_interface_object_by_id(
    opaque_id="_a-0000e8a4-8d8e-8000-0f8f-011c48011c48_19427"
)
```

#### `visit_application_by_id(application_id, locust_request_label=None)` → ApplicationUiForm
Visit an application by its opaque ID.

```python
app = self.appian.visitor.visit_application_by_id(
    application_id="_a-0000e8a4-8d8e-8000-0f8f-011c48011c48_19427"
)
```

#### `visit_application_by_name(application_name, application_prefix=None, locust_request_label=None)` → ApplicationUiForm
Visit an application by name.

```python
app = self.appian.visitor.visit_application_by_name(
    application_name="Employee Management"
)
```

### AI Skill Navigation

#### `visit_ai_skill_by_id(opaque_id, locust_request_label=None)` → AISkillUiForm
Visit an AI Skill by its opaque ID.

```python
ai_skill = self.appian.visitor.visit_ai_skill_by_id(
    opaque_id="_a-0000e8a4-8d8e-8000-0f8f-011c48011c48_19427"
)
```

#### `visit_ai_skill_by_name(ai_skill_name, locust_request_label=None)` → AISkillUiForm
Visit an AI Skill by name.

```python
ai_skill = self.appian.visitor.visit_ai_skill_by_name(
    ai_skill_name="Document Classifier"
)
```

### Portal Navigation

#### `visit_portal_page(portal_unique_identifier, portal_page_unique_identifier, locust_request_label=None)` → SailUiForm
Navigate to a portal page.

```python
# Visit https://mysite.com/performance-testing/page/page1
portal_page = self.appian.visitor.visit_portal_page(
    portal_unique_identifier="performance-testing",
    portal_page_unique_identifier="page1"
)
```

### Admin & Data Fabric Navigation

#### `visit_admin(locust_request_label=None)` → SailUiForm
Navigate to /admin.

```python
admin = self.appian.visitor.visit_admin()
```

#### `visit_data_fabric(locust_request_label=None, additional_url_path='', breadcrumb='')` → SailUiForm
Navigate to Data Fabric (Process HQ).

```python
data_fabric = self.appian.visitor.visit_data_fabric(
    additional_url_path="dashboards/new"
)
```

#### `visit_control_panel_workspace(locust_request_label=None)` → SailUiForm
Navigate to Control Panel Workspace.

```python
control_panel = self.appian.visitor.visit_control_panel_workspace()
```

---

## SailUiForm Interaction Methods

The `SailUiForm` class provides methods to interact with SAIL interfaces. All methods return `self` for method chaining unless otherwise noted.

### Text Input Methods

#### `fill_text_field(label, value, is_test_label=False, locust_request_label="", index=1)` → SailUiForm
Fill a text field by its label.

```python
form.fill_text_field(label="First Name", value="John")
form.fill_text_field(label="Last Name", value="Doe")

# Use test label instead of display label
form.fill_text_field(label="EMPLOYEE_NAME", value="John", is_test_label=True)

# Fill the second field with the same label
form.fill_text_field(label="Phone", value="555-1234", index=2)
```

#### `fill_paragraph_field(label, value, is_test_label=False, locust_request_label="", index=1)` → SailUiForm
Alias for `fill_text_field()`. Fills a paragraph field.

```python
form.fill_paragraph_field(label="Comments", value="This is a long comment...")
```

#### `fill_field_by_index(type_of_component, index, text_to_fill, locust_request_label="")` → SailUiForm
Fill a field by its index and component type.

```python
form.fill_field_by_index(
    type_of_component="TextField",
    index=1,
    text_to_fill="John"
)
```

#### `fill_field_by_any_attribute(attribute, value_for_attribute, text_to_fill, locust_request_label="", index=1)` → SailUiForm
Fill a field by any attribute.

```python
form.fill_field_by_any_attribute(
    attribute="testLabel",
    value_for_attribute="EMPLOYEE_NAME",
    text_to_fill="John"
)
```

### Picker Field Methods

#### `fill_picker_field(label, value, identifier='id', format_test_label=True, fill_request_label="", pick_request_label="")` → SailUiForm
Fill a picker field (autocomplete/typeahead).

```python
# Search and select by ID
form.fill_picker_field(
    label="Manager",
    value="123",
    identifier="id"
)

# Search and select by name
form.fill_picker_field(
    label="Department",
    value="Engineering",
    identifier="name"
)
```

#### `fill_cascading_pickerfield(label, selections, format_test_label=True, locust_request_label="")` → SailUiForm
Fill a cascading picker field with multiple selections.

```python
form.fill_cascading_pickerfield(
    label="Location",
    selections=["United States", "California", "San Francisco"]
)
```

#### `fill_cascading_pickerfield_with_attribute(attribute, attribute_value, selections, locust_request_label="")` → SailUiForm
Fill a cascading picker field using a custom attribute.

```python
form.fill_cascading_pickerfield_with_attribute(
    attribute="testLabel",
    attribute_value="LOCATION_PICKER",
    selections=["United States", "California", "San Francisco"]
)
```

### Button & Link Methods

#### `click_button(label, is_test_label=False, locust_request_label="", index=1)` → SailUiForm
Click a button by its label.

```python
form.click_button(label="Submit")
form.click_button(label="Cancel", index=2)
form.click_button(label="SUBMIT_BTN", is_test_label=True)
```

#### `click_link(label, is_test_label=False, locust_request_label="", index=1)` → SailUiForm
Click a link by its label.

```python
form.click_link(label="View Details")
form.click_link(label="DETAILS_LINK", is_test_label=True)
```

#### `click(label, is_test_label=False, locust_request_label="", index=1)` → SailUiForm
Generic click method for any clickable component.

```python
form.click(label="Next")
```

#### `click_card_layout_by_index(index, locust_request_label="")` → SailUiForm
Click a card layout by its index.

```python
form.click_card_layout_by_index(index=1)
```

### Record Link Methods

#### `click_record_link(label, is_test_label=False, locust_request_label="")` → RecordInstanceUiForm
Click a record link by label. Returns a `RecordInstanceUiForm`.

```python
record_form = form.click_record_link(label="John Doe")
```

#### `click_record_link_by_index(index, locust_request_label="")` → RecordInstanceUiForm
Click a record link by its index.

```python
record_form = form.click_record_link_by_index(index=1)
```

#### `click_record_view_link(label, locust_request_label="")` → RecordInstanceUiForm
Click a record view link.

```python
record_form = form.click_record_view_link(label="Employee Details")
```

### Process Link Methods

#### `click_start_process_link(label, is_test_label=False, is_mobile=False, locust_request_label="")` → SailUiForm
Click a start process link.

```python
form.click_start_process_link(label="Start Onboarding")
```

#### `click_start_process_link_on_mobile(label, site_name, page_name, locust_request_label="")` → SailUiForm
Click a start process link on mobile.

```python
form.click_start_process_link_on_mobile(
    label="Start Onboarding",
    site_name="Employee Portal",
    page_name="Home"
)
```

### Related Action Methods

#### `click_related_action(label, is_test_label=False, locust_request_label="")` → SailUiForm
Click a related action button or link.

```python
form.click_related_action(label="Edit Employee")
```

#### `click_record_action(label, is_test_label=False, locust_request_label="")` → SailUiForm
Alias for `click_related_action()`.

```python
form.click_record_action(label="Delete Record")
```

#### `evaluate_record_action_field_security(test_label="", format_test_label=True, index=1, locust_request_label="")` → SailUiForm
Trigger security evaluation to reveal record action items.

```python
form.evaluate_record_action_field_security(test_label="RECORD_ACTIONS")
```

### Dropdown Methods

#### `select_dropdown_item(label, choice_label, locust_request_label="", is_test_label=False)` → SailUiForm
Select an item from a dropdown.

```python
form.select_dropdown_item(
    label="Department",
    choice_label="Engineering"
)
```

#### `select_dropdown_item_by_index(index, choice_label, locust_request_label="")` → SailUiForm
Select a dropdown item by dropdown index.

```python
form.select_dropdown_item_by_index(
    index=1,
    choice_label="Engineering"
)
```

#### `get_dropdown_items(label, is_test_label=False)` → List[str]
Get all available items in a dropdown.

```python
items = form.get_dropdown_items(label="Department")
# Returns: ["Engineering", "Sales", "Marketing"]
```

#### `select_multi_dropdown_item(label, choice_label, locust_request_label="", is_test_label=False)` → SailUiForm
Select multiple items from a multi-select dropdown.

```python
form.select_multi_dropdown_item(
    label="Skills",
    choice_label=["Python", "Java", "JavaScript"]
)
```

#### `select_multi_dropdown_item_by_index(index, choice_label, locust_request_label="")` → SailUiForm
Select multiple items from a multi-select dropdown by index.

```python
form.select_multi_dropdown_item_by_index(
    index=1,
    choice_label=["Python", "Java"]
)
```

#### `select_grouped_dropdown_item_by_index(index, choice_index, locust_request_label="")` → SailUiForm
Select items from a grouped dropdown by indices.

```python
form.select_grouped_dropdown_item_by_index(
    index=1,
    choice_index=[0, 2]  # Select first and third items
)
```

### Menu Methods

#### `click_menu_item_by_name(label, choice_name, is_test_label=False, locust_request_label="")` → SailUiForm
Click a menu item by its choice name.

```python
form.click_menu_item_by_name(
    label="Actions",
    choice_name="Edit"
)
```

#### `click_menu_item_by_choice_index(label, choice_index, is_test_label=False, locust_request_label="")` → SailUiForm
Click a menu item by its choice index.

```python
form.click_menu_item_by_choice_index(
    label="Actions",
    choice_index=1
)
```

### Checkbox Methods

#### `check_checkbox_by_label(label, indices, locust_request_label="")` → SailUiForm
Check checkboxes by label.

```python
# Check first and third checkboxes
form.check_checkbox_by_label(
    label="Terms and Conditions",
    indices=[1, 3]
)
```

#### `check_checkbox_by_test_label(test_label, indices, locust_request_label="")` → SailUiForm
Check checkboxes by test label.

```python
form.check_checkbox_by_test_label(
    test_label="TERMS_CHECKBOX",
    indices=[1]
)
```

### Tab Methods

#### `click_tab_by_label(tab_label, tab_group_test_label, locust_request_label="")` → SailUiForm
Select a tab by its label.

```python
form.click_tab_by_label(
    tab_label="Personal Info",
    tab_group_test_label="EMPLOYEE_TABS"
)
```


### Date & Filter Methods

#### `select_date_range_user_filter(filter_label, start_date, end_date, locust_request_label="")` → SailUiForm
Select a date range in a user filter.

```python
from datetime import date

form.select_date_range_user_filter(
    filter_label="Date Range",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31)
)
```

### File Upload Methods

#### `upload_document_to_file_upload_field(label, file_path, is_test_label=False, locust_request_label="")` → SailUiForm
Upload a single document to a file upload field.

```python
form.upload_document_to_file_upload_field(
    label="Resume",
    file_path="/path/to/resume.pdf"
)
```

#### `upload_documents_to_multiple_file_upload_field(file_paths, label="", is_test_label=False, locust_request_label="")` → SailUiForm
Upload multiple documents to a file upload field.

```python
form.upload_documents_to_multiple_file_upload_field(
    file_paths=[
        "/path/to/doc1.pdf",
        "/path/to/doc2.pdf",
        "/path/to/doc3.pdf"
    ],
    label="Supporting Documents"
)
```

### Utility Methods

#### `get_latest_state()` → Dict[str, Any]
Get a deep copy of the current UI state.

```python
state = form.get_latest_state()
print(state)
```

#### `refresh_after_record_action()` → SailUiForm
Refresh the form after a record action.

```python
form.click_record_action(label="Update Status")
form.refresh_after_record_action()
```

---

## Grid Operations

Grid operations are available on `SailUiForm` and its subclasses for interacting with Appian grids.

### Paging Grid Methods

#### `sort_paging_grid(label, field_name, ascending=True, locust_request_label="")` → SailUiForm
Sort a paging grid by a field.

```python
form.sort_paging_grid(
    label="Employee Directory",
    field_name="Last Name",
    ascending=True
)
```

#### `select_rows_in_grid(rows, label, append_to_existing_selected=False, locust_request_label="")` → SailUiForm
Select specific rows in a grid.

```python
# Select first 3 rows
form.select_rows_in_grid(
    rows=[0, 1, 2],
    label="Employee Directory"
)

# Append to existing selection
form.select_rows_in_grid(
    rows=[3, 4],
    label="Employee Directory",
    append_to_existing_selected=True
)
```

#### `move_to_right_in_paging_grid(label, locust_request_label="")` → SailUiForm
Move to the next page in a paging grid.

```python
form.move_to_right_in_paging_grid(label="Employee Directory")
```

#### `move_to_left_in_paging_grid(label, locust_request_label="")` → SailUiForm
Move to the previous page in a paging grid.

```python
form.move_to_left_in_paging_grid(label="Employee Directory")
```

#### `move_to_first_page_in_paging_grid(label, locust_request_label="")` → SailUiForm
Move to the first page in a paging grid.

```python
form.move_to_first_page_in_paging_grid(label="Employee Directory")
```

#### `move_to_last_page_in_paging_grid(label, locust_request_label="")` → SailUiForm
Move to the last page in a paging grid.

```python
form.move_to_last_page_in_paging_grid(label="Employee Directory")
```

#### `click_grid_row_link(label, row_index, column_index, locust_request_label="")` → SailUiForm
Click a link in a specific grid cell.

```python
form.click_grid_row_link(
    label="Employee Directory",
    row_index=0,
    column_index=1
)
```

### Grid Field Methods

#### `fill_grid_text_field(label, row_index, column_index, value, locust_request_label="")` → SailUiForm
Fill a text field in a grid cell.

```python
form.fill_grid_text_field(
    label="Employee Directory",
    row_index=0,
    column_index=2,
    value="New Value"
)
```

#### `select_grid_dropdown(label, row_index, column_index, choice_label, locust_request_label="")` → SailUiForm
Select a dropdown value in a grid cell.

```python
form.select_grid_dropdown(
    label="Employee Directory",
    row_index=0,
    column_index=3,
    choice_label="Active"
)
```

#### `check_grid_checkbox(label, row_index, column_index, indices, locust_request_label="")` → SailUiForm
Check checkboxes in a grid cell.

```python
form.check_grid_checkbox(
    label="Employee Directory",
    row_index=0,
    column_index=4,
    indices=[1]
)
```

### Complete Grid Example

```python
@task
def interact_with_grid(self):
    # Navigate to report with grid
    report = self.appian.visitor.visit_report("Employee Report with Grid")
    
    # Sort by department
    report.sort_paging_grid(
        label="Employee Directory",
        field_name="Department",
        ascending=True
    )
    
    # Select first 5 rows
    report.select_rows_in_grid(
        rows=[0, 1, 2, 3, 4],
        label="Employee Directory"
    )
    
    # Move to next page
    report.move_to_right_in_paging_grid(label="Employee Directory")
    
    # Select first row on second page (append to selection)
    report.select_rows_in_grid(
        rows=[0],
        label="Employee Directory",
        append_to_existing_selected=True
    )
    
    # Click on a record link in the grid
    report.click_record_link(label="Paul Martin")
```

---

## Record Operations

### RecordListUiForm Methods

The `RecordListUiForm` is returned when visiting a record type list.

#### `click_record_list_action(label, locust_request_label=None)` → RecordListUiForm
Click a record list action button.

```python
record_list = self.appian.visitor.visit_record_type("Employees")
record_list.click_record_list_action(label="New Employee")
```

#### `get_visible_record_instances(column_index=None)` → Dict[str, Any]
Get information about visible records on the page.

```python
record_list = self.appian.visitor.visit_record_type("Employees")
records = record_list.get_visible_record_instances()
```

#### `filter_records_using_searchbox(search_term, locust_request_label=None)` → RecordListUiForm
Filter records using the search box.

```python
record_list = self.appian.visitor.visit_record_type("Employees")
record_list.filter_records_using_searchbox("Janet Coleman")
```

#### `click_record_in_list(record_name, locust_request_label=None)` → RecordInstanceUiForm
Click on a specific record in the list.

```python
record_list = self.appian.visitor.visit_record_type("Employees")
record_form = record_list.click_record_in_list("John Doe")
```

### RecordInstanceUiForm Methods

The `RecordInstanceUiForm` is returned when visiting a specific record instance.

#### `get_summary_view()` → RecordInstanceUiForm
Get the summary view of the record.

```python
record = self.appian.visitor.visit_record_instance(
    record_type="Employees",
    record_name="John Doe"
)
record.get_summary_view()
```

#### `get_header_view()` → RecordInstanceUiForm
Get the header view of the record.

```python
record.get_header_view()
```

### Complete Record Example

```python
@task
def create_employee_record(self):
    # Navigate to Employee Record List
    record_list = self.appian.visitor.visit_record_type(record_type="Employees")
    
    # Click "New Employee" action
    record_list.click_record_list_action(label="New Employee")
    
    # Fill in employee information
    record_list.fill_text_field(label="First Name", value="John")
    record_list.fill_text_field(label="Last Name", value="Doe")
    record_list.fill_text_field(label="Department", value="Engineering")
    record_list.fill_text_field(label="Title", value="Senior Engineer")
    record_list.fill_text_field(label="Phone Number", value="(555) 123-4567")
    record_list.fill_text_field(label="Email", value="john.doe@example.com")
    
    # Submit the form
    record_list.click_button(label="Create")
```

---

## Info Classes

Info classes provide read-only access to metadata about Appian objects. They don't modify state.

### ActionsInfo

#### `get_all_available_actions(search_string=None)` → Dict[str, Any]
Get all available actions.

```python
actions = self.appian.actions_info.get_all_available_actions()
# Returns: {"Action Name": {...action metadata...}}

# Search for specific actions
actions = self.appian.actions_info.get_all_available_actions(
    search_string="Employee"
)
```

#### `get_action(action_name, exact_match=False)` → Dict[str, Any]
Get a specific action by name.

```python
action = self.appian.actions_info.get_action(
    action_name="Create Employee",
    exact_match=False
)
```

### RecordsInfo

#### `get_all_available_records(search_string=None)` → Dict[str, Any]
Get all available record types.

```python
records = self.appian.records_info.get_all_available_records()
# Returns: {"Record Type Name": {...record metadata...}}
```

#### `get_record_type(record_type, exact_match=True)` → Dict[str, Any]
Get a specific record type.

```python
record = self.appian.records_info.get_record_type(
    record_type="Employees",
    exact_match=True
)
```

### ReportsInfo

#### `get_all_available_reports(search_string=None)` → Dict[str, Any]
Get all available reports.

```python
reports = self.appian.reports_info.get_all_available_reports()
# Returns: {"Report Name": {...report metadata...}}
```

#### `get_report(report_name, exact_match=True)` → Dict[str, Any]
Get a specific report.

```python
report = self.appian.reports_info.get_report(
    report_name="Employee Report",
    exact_match=True
)
```

### SitesInfo

#### `get_all_sites(search_string=None)` → Dict[str, Site]
Get all available sites.

```python
sites = self.appian.sites_info.get_all_sites()
# Returns: {"Site Name": Site(...)}
```

#### `get_site_data_by_site_name(site_name)` → Site
Get site data by site name.

```python
site = self.appian.sites_info.get_site_data_by_site_name("Employee Portal")
```

#### `get_site_page(site_name, page_name)` → Page
Get a specific page from a site.

```python
page = self.appian.sites_info.get_site_page(
    site_name="Employee Portal",
    page_name="Dashboard"
)
```

#### `get_site_page_type(site_name, page_name)` → PageType
Get the type of a site page.

```python
from appian_locust.objects import PageType

page_type = self.appian.sites_info.get_site_page_type(
    site_name="Employee Portal",
    page_name="Dashboard"
)
# Returns: PageType.INTERFACE, PageType.RECORD_LIST, etc.
```

### TasksInfo

#### `get_all_available_tasks(search_string=None)` → Dict[str, Any]
Get all available tasks.

```python
tasks = self.appian.tasks_info.get_all_available_tasks()
# Returns: {"Task Name": {...task metadata...}}
```

#### `get_task(task_name, exact_match=True)` → Dict[str, Any]
Get a specific task.

```python
task = self.appian.tasks_info.get_task(
    task_name="Approve Request",
    exact_match=True
)
```

### NewsInfo

#### `get_all_news()` → Dict[str, Any]
Get all news entries.

```python
news = self.appian.news_info.get_all_news()
```

---

## SystemOperator

The `SystemOperator` class provides methods for system-level operations that don't require UI interaction.

### Action Methods

#### `start_action(action_name, skip_design_call=False, exact_match=False)` → Response
Start an action without UI interaction.

```python
# Start action with UI
response = self.appian.system_operator.start_action(
    action_name="Process Data",
    skip_design_call=False
)

# Start action without UI (direct execution)
response = self.appian.system_operator.start_action(
    action_name="Background Job",
    skip_design_call=True
)
```

### Web API Methods

#### `get_webapi(uri, headers=None, locust_request_label=None, query_parameters={})` → Response
Make a GET request to a web API endpoint.

```python
# Simple GET request
response = self.appian.system_operator.get_webapi(
    uri="/suite/webapi/employee-api/employees"
)

# With custom headers
response = self.appian.system_operator.get_webapi(
    uri="/suite/webapi/employee-api/employees",
    headers={"X-Custom-Header": "value"}
)

# With query parameters
response = self.appian.system_operator.get_webapi(
    uri="/suite/webapi/employee-api/employees",
    query_parameters={"department": "Engineering", "status": "Active"}
)
```

#### `post_webapi(uri, headers=None, locust_request_label=None, payload=None)` → Response
Make a POST request to a web API endpoint.

```python
# POST with JSON payload
response = self.appian.system_operator.post_webapi(
    uri="/suite/webapi/employee-api/employees",
    payload={"firstName": "John", "lastName": "Doe"}
)

# POST with custom headers
response = self.appian.system_operator.post_webapi(
    uri="/suite/webapi/employee-api/employees",
    headers={"Content-Type": "application/json"},
    payload={"firstName": "John", "lastName": "Doe"}
)
```

### Content Methods

#### `fetch_content(opaque_id, locust_request_label=None)` → Response
Fetch content such as an image or document.

```python
response = self.appian.system_operator.fetch_content(
    opaque_id="_a-0000e8a4-8d8e-8000-0f8f-011c48011c48_19427"
)
```

### Autosuggestion Methods

#### `fetch_autosuggestions(payload, locust_request_label=None)` → Response
Retrieve suggestions from autosuggest endpoint.

```python
response = self.appian.system_operator.fetch_autosuggestions(
    payload={
        "expression": "search expression",
        "context": {}
    }
)
```

---

## Advanced Features

### Design Object Operations

#### ApplicationUiForm Methods

```python
# Visit an application
app = self.appian.visitor.visit_application_by_name("Employee Management")

# Get available design objects
design_objects = app.get_available_design_objects()

# Click on a design object
design_obj = app.click_design_object("Employee Interface")

# Click on an interface (opens Interface Designer)
interface = app.click_interface("Employee Form")

# Click on an AI Skill
ai_skill = app.click_ai_skill("Document Classifier")

# Filter design objects by type
app.filter_design_objects_by_type(DesignObjectType.INTERFACE)

# Create a new AI Skill
from appian_locust.objects import AISkillObjectType

app.create_ai_skill_object(
    ai_skill_name="My AI Skill",
    ai_skill_type=AISkillObjectType.DOCUMENT_CLASSIFICATION
)
```

#### DesignUiForm Methods

```python
# Visit design page
design = self.appian.visitor.visit_design()

# Get all applications
applications = design.get_available_applications()

# Click on an application
app = design.click_application("Employee Management")

# Create a new application
app = design.create_application("New App")

# Get design objects (when viewing an application)
design_objects = design.get_available_design_objects()
```

#### InterfaceDesignerUiForm Methods

```python
# Visit an interface in Interface Designer
interface = self.appian.visitor.visit_interface_object_by_id(
    opaque_id="_a-0000e8a4-8d8e-8000-0f8f-011c48011c48_19427"
)

# Select a component in the live view
interface.select_component(
    component_label="Employee Name",
    index=1
)

# Fill a text field in design view
interface.fill_designview_text_field(
    label="Label",
    value="Employee Name"
)

# Select a choice in design view
interface.select_designview_choice_component(
    label="Alignment",
    choice_label="Center"
)

# Click a navigation link in design view
interface.click_design_view_navigation_link(
    label="Styling",
    is_test_label=False
)
```

### AI Skill Operations

```python
@task
def create_ai_skill(self):
    # Navigate to design and create app
    design = self.appian.visitor.visit_design()
    app = design.create_application("AI Skill App")
    
    # Navigate to build view
    app = app.select_nav_card_by_index("leftNavbar", 1, True)
    
    # Create AI Skill
    from appian_locust.objects import AISkillObjectType
    
    app.create_ai_skill_object(
        ai_skill_name="Document Classifier",
        ai_skill_type=AISkillObjectType.DOCUMENT_CLASSIFICATION
    )
    
    # Visit the AI Skill
    ai_skill = self.appian.visitor.visit_ai_skill_by_name("Document Classifier")
    
    # Create first model
    ai_skill.click_button("Create First Model")
    
    # Add document type
    ai_skill.click_button("New Document Type")
    ai_skill.fill_text_field("Document Type Name", "Invoices")
    
    # Upload training documents
    invoice_files = [
        "/path/to/invoice1.pdf",
        "/path/to/invoice2.pdf",
        "/path/to/invoice3.pdf"
    ]
    ai_skill.upload_documents_to_multiple_file_upload_field(invoice_files)
    
    # Create document type
    ai_skill.click_button("Create")
    
    # Save changes
    ai_skill.save_ai_skill_changes()
    
    # Train model
    ai_skill.click_button("Train Model")
```

### Feature Flag Override

Override default feature flags for testing specific features.

```python
from appian_locust.feature_flag import FeatureFlag

class MyTaskSet(AppianTaskSet):
    def on_start(self):
        super().on_start()
        
        # Override specific feature flags
        self.override_default_flags([
            FeatureFlag.EVOLVED_GRIDFIELD,
            FeatureFlag.RECORD_CHROME,
            FeatureFlag.NEW_COLUMN_WIDTHS
        ])
```

### Multiple User Credentials

Use different credentials for different virtual users.

```python
class UserActor(HttpUser):
    tasks = [MyTaskSet]
    host = 'https://mysite.appiancloud.com'
    
    # Single auth for all users
    auth = ["username", "password"]
    
    # Multiple credentials (one per user)
    credentials = [
        ["user1", "pass1"],
        ["user2", "pass2"],
        ["user3", "pass3"]
    ]
```

### Configuration File

Create a `config.json` file for centralized configuration:

```json
{
    "host_address": "mysite.appiancloud.com",
    "auth": ["username", "password"],
    "endpoint_type": "view,list",
    "request_timeout": 300
}
```

Load configuration in your test:

```python
from appian_locust.utilities.loadDriverUtils import loadDriverUtils

utls = loadDriverUtils()
utls.load_config()
CONFIG = utls.c

class UserActor(HttpUser):
    host = "https://" + CONFIG['host_address']
    auth = CONFIG["auth"]
```

---

## Complete Examples

### Example 1: Basic Report Access

```python
from locust import HttpUser, task
from appian_locust import AppianTaskSet

class GetReportsTaskSet(AppianTaskSet):
    @task
    def get_all_reports(self):
        # Get metadata about all reports
        reports = self.appian.reports_info.get_all_available_reports()
        print(f"Found {len(reports)} reports")

class UserActor(HttpUser):
    tasks = [GetReportsTaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### Example 2: Create Employee Record

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task

class RecordsTaskSet(AppianTaskSet):
    @task
    def create_new_employee(self):
        # Navigate to Employee Record List
        record_list = self.appian.visitor.visit_record_type(record_type="Employees")
        
        # Click on "New Employee" Record List Action
        record_list.click_record_list_action(label="New Employee")
        
        # Fill in new Employee information
        record_list.fill_text_field(label="First Name", value="Sample")
        record_list.fill_text_field(label="Last Name", value="User")
        record_list.fill_text_field(label="Department", value="Engineering")
        record_list.fill_text_field(label="Title", value="Senior Software Engineer")
        record_list.fill_text_field(label="Phone Number", value="(703) 442-8844")
        
        # Create Employee
        record_list.click_button(label="Create")

class UserActor(HttpUser):
    tasks = [RecordsTaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### Example 3: Grid Interactions

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task, between

class GridTaskSet(AppianTaskSet):
    @task
    def interact_with_grid_in_interface(self):
        # Navigate to the interface backed report that contains a grid
        report_uiform = self.appian.visitor.visit_report(
            report_name="Employee Report with Grid"
        )
        
        # Sort the grid rows by the "Department" field name
        report_uiform.sort_paging_grid(
            label="Employee Directory",
            field_name="Department",
            ascending=True
        )
        
        # Select the first five rows on the first page of the grid
        report_uiform.select_rows_in_grid(
            rows=[0, 1, 2, 3, 4],
            label="Employee Directory"
        )
        
        # Move to the second page of the grid
        report_uiform.move_to_right_in_paging_grid(label="Employee Directory")
        
        # Select the first row on the second page (append to selection)
        report_uiform.select_rows_in_grid(
            rows=[0],
            label="Employee Directory",
            append_to_existing_selected=True
        )
        
        # Click on a record link in the grid
        report_uiform.click_record_link(label="Paul Martin")

class GridUserActor(HttpUser):
    tasks = [GridTaskSet]
    wait_time = between(0.5, 1.0)
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### Example 4: Site Navigation and Form Submission

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task

class SiteTaskSet(AppianTaskSet):
    @task
    def submit_request_form(self):
        # Navigate to site page
        form = self.appian.visitor.visit_site(
            site_name="Employee Portal",
            page_name="Submit Request"
        )
        
        # Fill out the request form
        form.fill_text_field(label="Request Title", value="New Equipment")
        form.fill_paragraph_field(
            label="Description",
            value="Need a new laptop for development work"
        )
        form.select_dropdown_item(
            label="Category",
            choice_label="Hardware"
        )
        form.select_dropdown_item(
            label="Priority",
            choice_label="High"
        )
        
        # Upload supporting documents
        form.upload_document_to_file_upload_field(
            label="Attachments",
            file_path="/path/to/justification.pdf"
        )
        
        # Submit the form
        form.click_button(label="Submit Request")

class UserActor(HttpUser):
    tasks = [SiteTaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### Example 5: Task Approval Workflow

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task

class TaskApprovalSet(AppianTaskSet):
    @task
    def approve_pending_task(self):
        # Get all available tasks
        tasks = self.appian.tasks_info.get_all_available_tasks()
        
        if not tasks:
            return
        
        # Visit the first task
        task_name = list(tasks.keys())[0]
        task_form = self.appian.visitor.visit_task(
            task_name=task_name,
            exact_match=True
        )
        
        # Review task details
        task_form.click_tab_by_label(
            tab_label="Details",
            tab_group_test_label="TASK_TABS"
        )
        
        # Add approval comments
        task_form.fill_paragraph_field(
            label="Comments",
            value="Approved - looks good"
        )
        
        # Select approval decision
        task_form.select_dropdown_item(
            label="Decision",
            choice_label="Approve"
        )
        
        # Submit the task
        task_form.click_button(label="Submit")

class UserActor(HttpUser):
    tasks = [TaskApprovalSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### Example 6: Record Search and Update

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task

class RecordUpdateTaskSet(AppianTaskSet):
    @task
    def search_and_update_employee(self):
        # Navigate to Employee Record List
        record_list = self.appian.visitor.visit_record_type(record_type="Employees")
        
        # Search for specific employee
        record_list.filter_records_using_searchbox("Janet Coleman")
        
        # Click on the employee record
        record_form = record_list.click_record_in_list("Janet Coleman")
        
        # Click edit action
        record_form.click_related_action(label="Edit Employee")
        
        # Update employee information
        record_form.fill_text_field(label="Title", value="Senior Manager")
        record_form.select_dropdown_item(
            label="Department",
            choice_label="Operations"
        )
        
        # Save changes
        record_form.click_button(label="Save")

class UserActor(HttpUser):
    tasks = [RecordUpdateTaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### Example 7: Web API Integration

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task
import json

class WebAPITaskSet(AppianTaskSet):
    @task
    def call_employee_api(self):
        # GET request to fetch employees
        response = self.appian.system_operator.get_webapi(
            uri="/suite/webapi/employee-api/employees",
            query_parameters={"department": "Engineering"}
        )
        
        if response.ok:
            employees = response.json()
            print(f"Found {len(employees)} employees")
        
        # POST request to create new employee
        new_employee = {
            "firstName": "John",
            "lastName": "Doe",
            "department": "Engineering",
            "title": "Software Engineer"
        }
        
        response = self.appian.system_operator.post_webapi(
            uri="/suite/webapi/employee-api/employees",
            headers={"Content-Type": "application/json"},
            payload=new_employee
        )
        
        if response.ok:
            print("Employee created successfully")

class UserActor(HttpUser):
    tasks = [WebAPITaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### Example 8: Multi-User with Configuration

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task, between
from appian_locust.utilities.loadDriverUtils import loadDriverUtils

# Load configuration
utls = loadDriverUtils()
utls.load_config()
CONFIG = utls.c

class MultiUserTaskSet(AppianTaskSet):
    def on_start(self):
        super().on_start()
        print(f"User logged in: {self.auth[0]}")
    
    @task(10)
    def visit_random_record(self):
        if "view" in CONFIG.get("endpoint_type", ""):
            self.appian.visitor.visit_record_instance()
    
    @task(10)
    def visit_employee_list(self):
        if "list" in CONFIG.get("endpoint_type", ""):
            record_list = self.appian.visitor.visit_record_type("Employees")
            record_list.filter_records_using_searchbox("John")

class UserActor(HttpUser):
    tasks = [MultiUserTaskSet]
    wait_time = between(0.5, 2.0)
    host = "https://" + CONFIG['host_address']
    
    # Multiple credentials for different users
    credentials = [
        ["user1@example.com", "password1"],
        ["user2@example.com", "password2"],
        ["user3@example.com", "password3"]
    ]
    
    # Fallback auth when credentials are exhausted
    auth = ["default_user@example.com", "default_password"]
```

### Example 9: Complex Form with Pickers and Cascading Dropdowns

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task

class ComplexFormTaskSet(AppianTaskSet):
    @task
    def fill_complex_form(self):
        # Navigate to form
        form = self.appian.visitor.visit_site(
            site_name="HR Portal",
            page_name="New Hire Form"
        )
        
        # Basic text fields
        form.fill_text_field(label="First Name", value="Jane")
        form.fill_text_field(label="Last Name", value="Smith")
        form.fill_text_field(label="Email", value="jane.smith@example.com")
        
        # Picker field (autocomplete)
        form.fill_picker_field(
            label="Manager",
            value="John Doe",
            identifier="name"
        )
        
        # Cascading picker (location hierarchy)
        form.fill_cascading_pickerfield(
            label="Office Location",
            selections=["United States", "California", "San Francisco"]
        )
        
        # Multi-select dropdown
        form.select_multi_dropdown_item(
            label="Skills",
            choice_label=["Python", "Java", "SQL", "AWS"]
        )
        
        # Checkboxes
        form.check_checkbox_by_label(
            label="I agree to the terms",
            indices=[1]
        )
        
        # Date range filter
        from datetime import date
        form.select_date_range_user_filter(
            filter_label="Start Date Range",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31)
        )
        
        # File upload
        form.upload_documents_to_multiple_file_upload_field(
            file_paths=[
                "/path/to/resume.pdf",
                "/path/to/cover_letter.pdf"
            ],
            label="Documents"
        )
        
        # Submit
        form.click_button(label="Submit")

class UserActor(HttpUser):
    tasks = [ComplexFormTaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

### Example 10: Action Without UI (Background Process)

```python
from appian_locust import AppianTaskSet
from locust import HttpUser, task

class BackgroundActionTaskSet(AppianTaskSet):
    @task
    def trigger_background_job(self):
        # Start an action without UI interaction
        response = self.appian.system_operator.start_action(
            action_name="Daily Data Sync",
            skip_design_call=True,  # Skip UI, execute directly
            exact_match=True
        )
        
        if response.ok:
            print("Background job triggered successfully")
        else:
            print(f"Failed to trigger job: {response.status_code}")

class UserActor(HttpUser):
    tasks = [BackgroundActionTaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

---

## Running Locust Tests

### Basic Run

```bash
locust -f my_locustfile.py
```

Then open [http://localhost:8089](http://localhost:8089) in your browser.

### Headless Mode

```bash
locust -f my_locustfile.py --headless -u 10 -r 2 -t 60s
```

- `-u 10`: 10 concurrent users
- `-r 2`: Spawn 2 users per second
- `-t 60s`: Run for 60 seconds

### Distributed Mode

Master:
```bash
locust -f my_locustfile.py --master
```

Workers:
```bash
locust -f my_locustfile.py --worker --master-host=<master-ip>
```

### With Configuration

```bash
locust -f my_locustfile.py --host=https://mysite.appiancloud.com
```

---

## Debugging

### Enable Debug Logging

```python
from appian_locust.utilities import logger
import logging

log = logger.getLogger(__name__)
log.setLevel(logging.DEBUG)
```

### Use Without Locust (CLI Mode)

```python
from appian_locust.appian_client import appian_client_without_locust

# Create client
client = appian_client_without_locust(host='https://mysite.appiancloud.com')

# Login
client.login(auth=('username', 'password'))
client.get_client_feature_toggles()

# Interact with Appian
form = client.visitor.visit_record_type("Employees")
print(form.get_latest_state())

# Logout
client.logout()
```

### Record Mode

Enable record mode to capture requests:

```python
from appian_locust.appian_client import appian_client_without_locust

client = appian_client_without_locust(
    host='https://mysite.appiancloud.com',
    record_mode=True
)
```

---

## Best Practices

### 1. Use Exact Match When Possible

```python
# Faster and more reliable
form = self.appian.visitor.visit_report("Employee Report", exact_match=True)
```

### 2. Use Test Labels for Stability

```python
# More stable across UI changes
form.fill_text_field(label="EMPLOYEE_FIRST_NAME", value="John", is_test_label=True)
```

### 3. Add Custom Locust Labels

```python
form.click_button(
    label="Submit",
    locust_request_label="Submit_Employee_Form"
)
```

### 4. Handle Errors Gracefully

```python
try:
    form = self.appian.visitor.visit_record_type("Employees")
    form.click_record_list_action(label="New Employee")
except Exception as e:
    print(f"Error: {e}")
```

### 5. Use Wait Times

```python
from locust import between

class UserActor(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
```

### 6. Organize Tasks by Weight

```python
class MyTaskSet(AppianTaskSet):
    @task(10)  # 10x more likely
    def common_task(self):
        pass
    
    @task(1)   # 1x likely
    def rare_task(self):
        pass
```

### 7. Use Configuration Files

Keep credentials and settings in `config.json`:

```json
{
    "host_address": "mysite.appiancloud.com",
    "auth": ["username", "password"],
    "request_timeout": 300
}
```

---

## Troubleshooting

### Common Issues

**Issue**: "Login unsuccessful, no multipart cookie found"
- **Solution**: Verify credentials are correct

**Issue**: "ComponentNotFoundException"
- **Solution**: Check label spelling, use `is_test_label=True`, or verify component exists

**Issue**: "Connection refused"
- **Solution**: Verify host URL is correct (without https://)

**Issue**: "Timeout errors"
- **Solution**: Increase timeout in config.json: `"request_timeout": 600`

### Getting Help

- **Documentation**: [https://appian-locust.readthedocs.io](https://appian-locust.readthedocs.io)
- **GitLab**: [https://gitlab.com/appian-oss/appian-locust](https://gitlab.com/appian-oss/appian-locust)
- **Issues**: Report bugs on GitLab Issues

---

## Summary

Appian Locust provides a comprehensive Python API for load testing Appian applications:

- **Navigation**: Use `visitor` to navigate to any Appian page type
- **Interaction**: Use `SailUiForm` methods to interact with UI elements
- **Metadata**: Use `*_info` properties to gather information
- **System Ops**: Use `system_operator` for API calls and background actions
- **Load Testing**: Full Locust integration for performance testing

The library abstracts away the complexity of Appian's SAIL protocol, allowing you to write readable, maintainable load tests.

---

**Content was rephrased for compliance with licensing restrictions**

*Sources: [Appian Locust Documentation](https://appian-locust.readthedocs.io/en/latest/)*
