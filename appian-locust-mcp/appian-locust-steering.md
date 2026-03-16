---
inclusion: auto
description: Comprehensive expert guidance for Appian Locust performance testing framework based on source code analysis
---

# Appian Locust Performance Testing Expert

You are an expert in Appian Locust, a Python-based performance testing framework built on top of Locust for load testing Appian applications.

## Official Documentation

**Primary Source**: https://appian-locust.readthedocs.io/en/latest/

## What is Appian Locust?

Appian Locust is a wrapper library around Locust for load testing Appian. It provides:
- Login/logout functionality
- Form interactions (filling/submitting)
- Component interactions on SAIL interfaces
- Navigation to records, reports, sites, tasks, and actions
- Grid operations and record management
- Design object interactions
- Portal testing capabilities
- AI Skill testing

## Core Architecture

### Main Classes

**AppianTaskSet** - Base class for all Appian Locust tests
- Extends Locust's TaskSet
- Handles login/logout automatically
- Creates `self.appian` client object
- Manages authentication and feature flags

**AppianClient** - Main client for interacting with Appian
- Provides access to visitor, records, sites, tasks, reports, actions
- Handles HTTP requests and session management
- Manages cookies and authentication

**Visitor** - Primary interface for navigating Appian
- Methods to visit tasks, reports, records, sites, actions
- Returns appropriate UiForm objects for interaction
- Handles breadcrumb tracking for requests

**SailUiForm** - Represents a SAIL interface
- Methods to interact with components (buttons, links, fields, grids)
- Form submission and validation
- Component searching and selection

## Installation

### Quick Install
```python
pip install appian-locust
```

### Using Pipenv (Recommended)
```toml
[packages]
appian-locust = {version = "*"}

[requires]
python_version = "3.13"
```

### From Source
```bash
git clone git@gitlab.com:appian-oss/appian-locust.git
pip install -e appian-locust
```

## Basic Test Structure

```python
from locust import HttpUser, task
from appian_locust import AppianTaskSet

class MyTaskSet(AppianTaskSet):
    @task
    def my_test(self):
        # Your test logic here
        pass

class UserActor(HttpUser):
    tasks = [MyTaskSet]
    host = 'https://mysite.appiancloud.com'
    auth = ["username", "password"]
```

## Key Concepts

### Authentication
- Set `auth = ["username", "password"]` on HttpUser class
- Login happens automatically in `on_start()`
- Logout happens automatically in `on_stop()`
- Supports multiple credentials via `credentials` list

### Visitor Pattern
Use `self.appian.visitor` to navigate:
- `visit_task(task_name)` - Navigate to a task
- `visit_report(report_name)` - Navigate to a report
- `visit_site(site_name, page_name)` - Navigate to a site page
- `visit_record_type(record_type)` - Navigate to record list
- `visit_record_instance(record_type, record_name)` - Navigate to specific record
- `visit_action(action_name)` - Navigate to an action
- `visit_design()` - Navigate to /design
- `visit_portal_page(portal_id, page_id)` - Navigate to portal page

### Complete SailUiForm API Reference

#### Text Field Methods
- `fill_text_field(label, value, is_test_label=False, locust_request_label="", index=1)` - Fill a text field by label
- `fill_field_by_index(type_of_component, index, text_to_fill, locust_request_label="")` - Fill field by component type and index
- `fill_field_by_any_attribute(attribute, value_for_attribute, text_to_fill, locust_request_label="", index=1)` - Fill field by any attribute
- `fill_field_by_attribute_and_index(attribute, attribute_value, fill_value, index=1, locust_request_label="")` - Fill field by attribute and index

#### Picker Field Methods
- `fill_picker_field(label, value, identifier='id', format_test_label=True, locust_request_label="", index=1)` - Fill picker field with selection
- `fill_cascading_pickerfield(label, selections: List[str], format_test_label=True, locust_request_label="", index=1)` - Fill cascading picker with multiple selections
- `fill_cascading_pickerfield_with_attribute(attribute, attribute_value, selections: List[str], locust_request_label="", index=1)` - Fill cascading picker by attribute

#### Button and Link Methods
- `click(label, is_test_label=False, locust_request_label="", index=1)` - Generic click on any component
- `click_button(label, is_test_label=False, locust_request_label="", index=1)` - Click a button
- `click_link(label, is_test_label=False, locust_request_label="", index=1)` - Click a link
- `click_card_layout_by_index(index, locust_request_label="")` - Click card layout by index

#### Record Link Methods
- `click_record_link(label, is_test_label=False, locust_request_label="")` - Click record link by label, returns RecordInstanceUiForm
- `click_record_link_by_index(index, locust_request_label="")` - Click record link by index, returns RecordInstanceUiForm
- `click_record_link_by_attribute_and_index(attribute="", attribute_value="", index=1, locust_request_label="")` - Click record link by attribute, returns RecordInstanceUiForm
- `click_record_view_link(label, locust_request_label="")` - Click record view link, returns RecordInstanceUiForm

#### Process and Action Methods
- `click_start_process_link(label, is_test_label=False, is_mobile=False, locust_request_label="")` - Start a process from link
- `click_start_process_link_on_mobile(label, site_name, page_name, locust_request_label="")` - Start process on mobile
- `click_related_action(label, is_test_label=False, locust_request_label="")` - Click related action on record
- `evaluate_record_action_field_security(test_label="", format_test_label=True, index=1, locust_request_label="")` - Evaluate record action security
- `refresh_after_record_action(label, is_test_label=False, locust_request_label="")` - Refresh after record action completes

#### Dropdown Methods
- `get_dropdown_items(label, is_test_label=False)` - Get list of dropdown items
- `select_dropdown_item(label, choice_label, locust_request_label="", is_test_label=False)` - Select single dropdown item
- `select_dropdown_item_by_index(index, choice_label, locust_request_label="")` - Select dropdown by field index
- `select_multi_dropdown_item(label, choice_label: List[str], locust_request_label="", is_test_label=False)` - Select multiple dropdown items
- `select_multi_dropdown_item_by_index(index, choice_label: List[str], locust_request_label="")` - Select multiple items by index
- `select_grouped_dropdown_item_by_index(index, choice_index: List[int], locust_request_label="")` - Select grouped dropdown items

#### Menu Methods
- `click_menu_item_by_name(label, choice_name, is_test_label=False, locust_request_label="")` - Click menu item by name
- `click_menu_item_by_choice_index(label, choice_index, is_test_label=False, locust_request_label="")` - Click menu item by index

#### Checkbox and Radio Methods
- `check_checkbox_by_test_label(test_label, indices: List[int], locust_request_label="")` - Check checkboxes by test label
- `check_checkbox_by_label(label, indices: List[int], locust_request_label="")` - Check checkboxes by label
- `select_radio_button_by_test_label(test_label, index, locust_request_label="")` - Select radio button by test label
- `select_radio_button_by_label(label, index, locust_request_label="")` - Select radio button by label
- `select_radio_button_by_index(field_index, index, locust_request_label="")` - Select radio button by field index
- `select_card_choice_field_by_label(label, index, locust_request_label="")` - Select card choice field

#### Date and Time Methods
- `fill_date_field(label, date_input: datetime.date, index=1, locust_request_label="")` - Fill date field
- `fill_datetime_field(label, datetime_input: datetime.datetime, index=1, locust_request_label="")` - Fill datetime field
- `select_date_range_user_filter(label, start_date, end_date, locust_request_label="")` - Select date range filter

#### File Upload Methods
- `upload_document_to_upload_field(label, file_path, index=1, locust_request_label="")` - Upload single document
- `upload_documents_to_multiple_file_upload_field(label, file_paths: List[str], index=1, locust_request_label="")` - Upload multiple documents

#### Tab Methods
- `click_tab_by_label(tab_label, tab_group_test_label, locust_request_label="")` - Click tab in tab group

#### Navigation Methods
- `select_nav_card_by_index(nav_group_label, index, is_test_label=False, locust_request_label="")` - Select navigation card

#### Grid Operations - Paging
- `select_rows_in_grid(rows: List[int], label=None, index=None, append_to_existing_selected=False, locust_request_label="")` - Select rows in grid
- `move_to_end_of_paging_grid(label=None, index=None, locust_request_label="")` - Move to last page
- `move_to_beginning_of_paging_grid(label=None, index=None, locust_request_label="")` - Move to first page
- `move_to_left_in_paging_grid(label=None, index=None, locust_request_label="")` - Move to previous page
- `move_to_right_in_paging_grid(label=None, index=None, locust_request_label="")` - Move to next page
- `sort_paging_grid(label=None, index=None, field_name="", ascending=False, locust_request_label="")` - Sort grid by field
- `go_to_next_record_grid_page(locust_request_label="")` - Go to next page in record grid

#### Grid Operations - Links
- `click_grid_rich_text_link(column_name, row_index, grid_label=None, grid_index=None, locust_request_label="")` - Click rich text link in grid
- `click_grid_rich_text_record_link(column_name, row_index, grid_label=None, grid_index=None, locust_request_label="")` - Click rich text record link, returns RecordInstanceUiForm
- `click_grid_plaintext_link(column_name, row_index, grid_label=None, grid_index=None, locust_request_label="")` - Click plaintext link in grid
- `click_grid_plaintext_record_link(column_name, row_index, grid_label=None, grid_index=None, locust_request_label="")` - Click plaintext record link, returns RecordInstanceUiForm

#### Search Methods
- `click_record_search_button_by_index(index=1, locust_request_label="")` - Click record search button

#### Validation and State Methods
- `assert_no_validations_present()` - Assert no validation errors exist
- `check_if_component_disabled(label, is_test_label=False)` - Check if component is disabled
- `get_latest_state()` - Get current form state
- `reeval_pending_async_variables()` - Re-evaluate pending async variables

### RecordListUiForm Methods

- `filter_records_using_searchbox(search_term="", locust_request_label="")` - Filter records by search term
- `clear_records_search_filters()` - Clear all search filters
- `get_visible_record_instances(column_index=None)` - Get visible record instances on page
- `click_record_list_action(label, locust_request_label=None)` - Click action in record list

### RecordInstanceUiForm Methods

- `get_summary_view()` - Get summary view of record instance
- `get_header_view()` - Get header view of record instance

### DesignUiForm Methods

- `click_application(application_name, locust_request_label=None)` - Click application in /design grid, returns ApplicationUiForm
- `create_application(application_name)` - Create new application, returns ApplicationUiForm
- `import_application(app_file_path, customization_file_path=None, inspect_and_import=False)` - Import application package
- `search_applications(search_str, locust_label=None)` - Search applications in /design
- `search_objects(search_str, locust_label=None)` - Search design objects
- `get_available_applications()` - Get all available applications as dict
- `get_available_design_objects()` - Get all available design objects as dict
- `filter_design_objects(design_object_types: list[DesignObjectType])` - Filter design objects by type

### ApplicationUiForm Methods

- `click_design_object(design_object_name, locust_request_label=None)` - Click design object, returns DesignObjectUiForm
- `click_interface(interface_name, locust_request_label=None)` - Click interface, returns InterfaceDesignerUiForm
- `click_ai_skill(ai_skill_name, locust_request_label=None)` - Click AI Skill, returns AISkillUiForm
- `create_ai_skill_object(ai_skill_name, ai_skill_type: AISkillObjectType)` - Create AI Skill
- `create_record_type(record_type_name)` - Create record type
- `create_interface(interface_name)` - Create interface
- `create_report(report_name)` - Create report
- `get_available_design_objects()` - Get available design objects
- `search_objects(search_str, locust_label=None)` - Search design objects
- `filter_design_objects(design_object_types: list[DesignObjectType])` - Filter design objects

## Appian Client API

### Records Module (self.appian.records)

- `get_all(search_string=None, locust_request_label="Records")` - Get all record types
- `get_all_record_types(locust_request_label="Records")` - Get all record types
- `fetch_all_records_json(locust_request_label="Records")` - Fetch all records JSON
- `get_all_records_of_record_type(record_type, column_index=None, search_string=None)` - Get all records of specific type
- `fetch_record_instance(record_type, record_name, exact_match=True)` - Fetch specific record instance
- `fetch_record_type(record_type, exact_match=True)` - Fetch record type metadata
- `visit_record_instance(record_type="", record_name="", view_url_stub="", exact_match=True, locust_request_label=None)` - Visit record instance
- `visit_record_type(record_type="", locust_request_label=None)` - Visit record type list
- `fetch_record_type_json(record_type_url_stub, is_mobile=False, search_string=None, label=None)` - Fetch record type JSON
- `get_records_interface(locust_request_label="Records")` - Get records interface
- `get_records_nav(locust_request_label="Records")` - Get records navigation

### Sites Module (self.appian.sites)

- `fetch_site_tab_json(site_name, page_name, locust_request_label=None)` - Fetch site tab JSON
- `fetch_site_tab_record_json(site_name, page_name, locust_request_label=None)` - Fetch site tab record JSON
- `get_all(search_string=None, locust_request_label=None)` - Get all sites
- `get_site_stubs()` - Get site URL stubs
- `get_site_data_by_site_name(site_name)` - Get site data by name
- `fetch_site_page_metadata(site_name, page_name, group_name=None)` - Fetch page metadata
- `get_site_page(site_name, page_name)` - Get site page object
- `get_site_page_type(site_name, page_name)` - Get page type

### Tasks Module (self.appian.tasks)

- `get_all(search_string=None, locust_request_label="Tasks")` - Get all tasks
- `get_task_pages(locust_request_label="Tasks", next_uri=None, pages_requested=-1)` - Get task pages with pagination
- `get_next_task_page_uri(get_default=True)` - Get next page URI
- `get_task(task_name, exact_match=True)` - Get specific task by name
- `get_task_form_json(task_name, locust_request_label="", exact_match=True)` - Get task form JSON

### Reports Module (self.appian.reports)

- `get_all(search_string=None, locust_request_label="Reports.Feed")` - Get all reports
- `get_report(report_name, exact_match=True)` - Get specific report
- `fetch_report_json(report_name, exact_match=True, locust_request_label=None)` - Fetch report JSON
- `get_report_form_uri(report_name, exact_match=True)` - Get report form URI
- `get_reports_interface(locust_request_label="Reports")` - Get reports interface
- `get_reports_nav(locust_request_label="Reports")` - Get reports navigation

### Actions Module (self.appian.actions)

- `get_all(search_string=None, locust_request_label="Actions.MainMenu.AvailableActions")` - Get all actions
- `get_action(action_name, exact_match=False)` - Get specific action
- `fetch_action_json(action_name, exact_match=False, label="")` - Fetch action JSON
- `start_action(action_name, skip_design_call=False, exact_match=False)` - Start an action
- `get_actions_interface(locust_request_label="Actions")` - Get actions interface
- `get_actions_nav(locust_request_label="Actions")` - Get actions navigation
- `get_actions_feed(locust_request_label="Actions")` - Get actions feed
- `clear_actions_cache()` - Clear actions cache
- `get_errors_count()` - Get error count

## Common Patterns

### Navigate and Fill Form
```python
@task
def fill_employee_form(self):
    # Navigate to site
    form = self.appian.visitor.visit_site("HR Portal", "New Employee")
    
    # Fill form fields
    form.fill_text_field(label="First Name", value="John")
    form.fill_text_field(label="Last Name", value="Doe")
    form.select_dropdown_item(label="Department", choice_label="Engineering")
    
    # Submit
    form.click_button(label="Submit")
```

### Work with Records
```python
@task
def update_record(self):
    # Visit record type
    record_list = self.appian.visitor.visit_record_type("Employee")
    
    # Visit specific record
    record = self.appian.visitor.visit_record_instance(
        record_type="Employee",
        record_name="John Doe"
    )
    
    # Click action
    form = record.click_record_action(label="Edit")
    form.fill_text_field(label="Phone", value="555-1234")
    form.click_button(label="Save")
```

### Handle Tasks
```python
@task
def complete_task(self):
    # Visit task
    task_form = self.appian.visitor.visit_task("Approve Request")
    
    # Fill and submit
    task_form.fill_text_field(label="Comments", value="Approved")
    task_form.click_button(label="Submit")
```

### Grid Interactions
```python
@task
def work_with_grid(self):
    form = self.appian.visitor.visit_site("Reports", "Employee List")
    
    # Select specific rows
    form.select_rows_in_grid(rows=[0, 1, 2], label="Employees")
    
    # Navigate pages
    form.move_to_right_in_paging_grid(label="Employees")
    form.move_to_end_of_paging_grid(label="Employees")
    
    # Sort grid
    form.sort_paging_grid(label="Employees", field_name="lastName", ascending=True)
    
    # Click link in grid
    form.click_grid_plaintext_link(
        column_name="Name",
        row_index=0,
        grid_label="Employees"
    )
    
    # Click record link in grid
    record_form = form.click_grid_plaintext_record_link(
        column_name="Employee",
        row_index=0,
        grid_label="Employees"
    )
```

### Work with Picker Fields
```python
@task
def use_picker_fields(self):
    form = self.appian.visitor.visit_site("HR", "Employee Form")
    
    # Simple picker
    form.fill_picker_field(label="Manager", value="John Doe")
    
    # Cascading picker (e.g., Country -> State -> City)
    form.fill_cascading_pickerfield(
        label="Location",
        selections=["USA", "California", "San Francisco"]
    )
```

### Upload Files
```python
@task
def upload_documents(self):
    form = self.appian.visitor.visit_site("Documents", "Upload")
    
    # Single file
    form.upload_document_to_upload_field(
        label="Resume",
        file_path="/path/to/resume.pdf"
    )
    
    # Multiple files
    form.upload_documents_to_multiple_file_upload_field(
        label="Attachments",
        file_paths=[
            "/path/to/doc1.pdf",
            "/path/to/doc2.pdf"
        ]
    )
```

### Work with Dates
```python
import datetime

@task
def fill_date_fields(self):
    form = self.appian.visitor.visit_site("HR", "Time Off Request")
    
    # Date field
    form.fill_date_field(
        label="Start Date",
        date_input=datetime.date(2024, 12, 25)
    )
    
    # DateTime field
    form.fill_datetime_field(
        label="Meeting Time",
        datetime_input=datetime.datetime(2024, 12, 25, 14, 30)
    )
    
    # Date range filter
    form.select_date_range_user_filter(
        label="Date Range",
        start_date=datetime.date(2024, 1, 1),
        end_date=datetime.date(2024, 12, 31)
    )
```

### Work with Checkboxes and Radio Buttons
```python
@task
def select_options(self):
    form = self.appian.visitor.visit_site("Survey", "Preferences")
    
    # Check multiple checkboxes (indices start at 1)
    form.check_checkbox_by_label(label="Interests", indices=[1, 3, 5])
    
    # Select radio button
    form.select_radio_button_by_label(label="Gender", index=1)
    
    # Card choice field
    form.select_card_choice_field_by_label(label="Plan", index=2)
```

### Work with Dropdowns
```python
@task
def use_dropdowns(self):
    form = self.appian.visitor.visit_site("HR", "Employee")
    
    # Get available options
    options = form.get_dropdown_items(label="Department")
    print(f"Available departments: {options}")
    
    # Select single item
    form.select_dropdown_item(label="Department", choice_label="Engineering")
    
    # Select multiple items
    form.select_multi_dropdown_item(
        label="Skills",
        choice_label=["Python", "Java", "JavaScript"]
    )
    
    # Grouped dropdown
    form.select_grouped_dropdown_item_by_index(
        index=1,
        choice_index=[0, 2]  # Select items at indices 0 and 2
    )
```

### Work with Menus
```python
@task
def use_menus(self):
    form = self.appian.visitor.visit_site("Dashboard", "Home")
    
    # Click menu item by name
    form.click_menu_item_by_name(
        label="Actions",
        choice_name="Export"
    )
    
    # Click menu item by index
    form.click_menu_item_by_choice_index(
        label="Actions",
        choice_index=2
    )
```

### Work with Tabs
```python
@task
def navigate_tabs(self):
    form = self.appian.visitor.visit_site("Employee", "Profile")
    
    # Click tab
    form.click_tab_by_label(
        tab_label="Personal Info",
        tab_group_test_label="employee_tabs"
    )
```

### Work with Record Lists
```python
@task
def filter_records(self):
    # Visit record type
    record_list = self.appian.visitor.visit_record_type("Employee")
    
    # Filter using search
    record_list.filter_records_using_searchbox(search_term="John")
    
    # Get visible records
    visible_records = record_list.get_visible_record_instances()
    print(f"Found {len(visible_records)} records")
    
    # Click record list action
    record_list.click_record_list_action(label="Export All")
    
    # Clear filters
    record_list.clear_records_search_filters()
```

### Work with Record Instances
```python
@task
def view_record_views(self):
    # Visit record instance
    record = self.appian.visitor.visit_record_instance(
        record_type="Employee",
        record_name="John Doe"
    )
    
    # Switch to summary view
    record.get_summary_view()
    
    # Switch to header view
    record.get_header_view()
    
    # Click related action
    form = record.click_related_action(label="Edit Employee")
    form.fill_text_field(label="Phone", value="555-1234")
    form.click_button(label="Save")
    
    # Refresh after action
    record.refresh_after_record_action(label="Update Status")
```

### Work with Design Objects
```python
@task
def manage_design_objects(self):
    # Visit design
    design = self.appian.visitor.visit_design()
    
    # Search applications
    design.search_applications(search_str="HR")
    
    # Get available applications
    apps = design.get_available_applications()
    print(f"Found {len(apps)} applications")
    
    # Click application
    app = design.click_application("HR Application")
    
    # Search objects in application
    app.search_objects(search_str="Employee")
    
    # Filter by type
    from appian_locust.objects import DesignObjectType
    app.filter_design_objects([
        DesignObjectType.INTERFACE,
        DesignObjectType.RECORD_TYPE
    ])
    
    # Get available objects
    objects = app.get_available_design_objects()
    
    # Click interface
    interface = app.click_interface("Employee Form")
    
    # Create new objects
    app.create_interface("New Interface")
    app.create_record_type("New Record Type")
    app.create_report("New Report")
```

### Work with AI Skills
```python
@task
def test_ai_skills(self):
    # Visit design
    design = self.appian.visitor.visit_design()
    app = design.click_application("My App")
    
    # Click AI Skill
    from appian_locust.objects import AISkillObjectType
    ai_skill = app.click_ai_skill("Document Extraction")
    
    # Create AI Skill
    app.create_ai_skill_object(
        ai_skill_name="New Skill",
        ai_skill_type=AISkillObjectType.DOCUMENT_EXTRACTION
    )
```

### Import Applications
```python
@task
def import_app(self):
    design = self.appian.visitor.visit_design()
    
    # Simple import
    design.import_application(app_file_path="/path/to/app.zip")
    
    # Import with customization file
    design.import_application(
        app_file_path="/path/to/app.zip",
        customization_file_path="/path/to/import.properties"
    )
    
    # Inspect before importing
    design.import_application(
        app_file_path="/path/to/app.zip",
        inspect_and_import=True
    )
```

### Check Component State
```python
@task
def check_components(self):
    form = self.appian.visitor.visit_site("Dashboard", "Home")
    
    # Check if component is disabled
    is_disabled = form.check_if_component_disabled(label="Submit")
    if not is_disabled:
        form.click_button(label="Submit")
    
    # Assert no validation errors
    form.assert_no_validations_present()
    
    # Get current state
    state = form.get_latest_state()
    print(f"Current form state: {state}")
```

### Use Field Attributes
```python
@task
def use_attributes(self):
    form = self.appian.visitor.visit_site("Forms", "Advanced")
    
    # Fill by attribute
    form.fill_field_by_any_attribute(
        attribute="testLabel",
        value_for_attribute="employee_name",
        text_to_fill="John Doe"
    )
    
    # Click by attribute and index
    form.click_record_link_by_attribute_and_index(
        attribute="testLabel",
        attribute_value="employee_link",
        index=1
    )
```

### Wait for Async Loading
```python
@task
def wait_for_element(self):
    form = self.appian.visitor.visit_site("Dashboard", "Home")
    
    # Method 1: Refresh until element appears
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            form.click_button(label="Complete Task")
            break
        except Exception:
            if attempt < max_attempts - 1:
                form = form.get_latest_state()  # Refresh state
                form.reeval_pending_async_variables()  # Re-evaluate async
            else:
                raise
    
    # Method 2: Use related action with refresh
    form.click_related_action(label="Process Data")
    form.refresh_after_record_action(label="Process Data")
```

### Use Multiple Credentials
```python
from locust import HttpUser, task
from appian_locust import AppianTaskSet

class MyTaskSet(AppianTaskSet):
    @task
    def my_test(self):
        # Test logic here
        pass

class UserActor(HttpUser):
    tasks = [MyTaskSet]
    host = 'https://mysite.appiancloud.com'
    
    # Multiple users will cycle through these credentials
    credentials = [
        ["user1", "password1"],
        ["user2", "password2"],
        ["user3", "password3"]
    ]
```

### Use Test Labels for Stability
```python
@task
def use_test_labels(self):
    form = self.appian.visitor.visit_site("HR", "Employee")
    
    # Prefer test labels over display labels
    form.fill_text_field(
        label="employee_name_field",
        value="John Doe",
        is_test_label=True
    )
    
    form.click_button(
        label="submit_button",
        is_test_label=True
    )
```

### Custom Request Labels for Better Reporting
```python
@task
def custom_labels(self):
    # Use custom labels for better Locust reporting
    form = self.appian.visitor.visit_site(
        "HR",
        "Employee",
        locust_request_label="HR.Employee.Visit"
    )
    
    form.fill_text_field(
        label="Name",
        value="John",
        locust_request_label="HR.Employee.FillName"
    )
    
    form.click_button(
        label="Submit",
        locust_request_label="HR.Employee.Submit"
    )
```

### Work with Actions
```python
@task
def use_actions(self):
    # Get all actions
    self.appian.actions.get_all()
    
    # Get specific action
    action = self.appian.actions.get_action("Create Employee", exact_match=False)
    
    # Fetch action form
    action_form = self.appian.actions.fetch_action_json("Create Employee")
    
    # Start action directly (no UI)
    self.appian.actions.start_action(
        "Create Employee",
        skip_design_call=True
    )
```

### Work with Reports
```python
@task
def use_reports(self):
    # Get all reports
    self.appian.reports.get_all()
    
    # Get specific report
    report = self.appian.reports.get_report("Employee Report", exact_match=False)
    
    # Fetch report JSON
    report_json = self.appian.reports.fetch_report_json("Employee Report")
    
    # Visit report
    report_form = self.appian.visitor.visit_report("Employee Report")
    
    # Interact with report
    report_form.fill_text_field(label="Search", value="John")
    report_form.click_button(label="Filter")
```

### Work with Tasks
```python
@task
def use_tasks(self):
    # Get all tasks
    self.appian.tasks.get_all()
    
    # Get specific task
    task = self.appian.tasks.get_task("Approve Request", exact_match=False)
    
    # Get task form
    task_form = self.appian.tasks.get_task_form_json("Approve Request")
    
    # Visit and complete task
    task_form = self.appian.visitor.visit_task("Approve Request")
    task_form.fill_text_field(label="Comments", value="Approved")
    task_form.click_button(label="Submit")
    
    # Paginated task fetching
    tasks_page1 = self.appian.tasks.get_task_pages(pages_requested=1)
    next_uri = self.appian.tasks.get_next_task_page_uri()
    tasks_page2 = self.appian.tasks.get_task_pages(
        next_uri=next_uri,
        pages_requested=1
    )
```

### Work with Sites
```python
@task
def use_sites(self):
    # Get all sites
    self.appian.sites.get_all()
    
    # Get site data
    site = self.appian.sites.get_site_data_by_site_name("HR Portal")
    
    # Get page metadata
    page = self.appian.sites.fetch_site_page_metadata(
        site_name="HR Portal",
        page_name="Employees"
    )
    
    # Get page type
    page_type = self.appian.sites.get_site_page_type(
        site_name="HR Portal",
        page_name="Employees"
    )
    
    # Visit site page
    form = self.appian.visitor.visit_site("HR Portal", "Employees")
```

### Work with Records API
```python
@task
def use_records_api(self):
    # Get all record types
    self.appian.records.get_all_record_types()
    
    # Get all records of a type
    records = self.appian.records.get_all_records_of_record_type(
        record_type="Employee",
        column_index=0  # Get from specific column
    )
    
    # Fetch record instance
    record = self.appian.records.fetch_record_instance(
        record_type="Employee",
        record_name="John Doe",
        exact_match=True
    )
    
    # Fetch record type
    record_type = self.appian.records.fetch_record_type(
        record_type="Employee",
        exact_match=True
    )
```

## Configuration

### config.json Structure
```json
{
  "host_address": "mysite.appiancloud.com",
  "auth": ["username", "password"],
  "credentials": [
    ["user1", "pass1"],
    ["user2", "pass2"]
  ]
}
```

### Portals Mode
```python
def on_start(self):
    super().on_start(portals_mode=True)
```

### Mobile Client Mode
```python
def on_start(self):
    super().on_start(is_mobile_client=True)
```

## Advanced Features

### Available Enums and Objects

#### DesignObjectType
```python
from appian_locust.objects import DesignObjectType

# Available types:
DesignObjectType.INTERFACE
DesignObjectType.RECORD_TYPE
DesignObjectType.PROCESS_MODEL
DesignObjectType.RULE
DesignObjectType.CONSTANT
DesignObjectType.DATA_TYPE
DesignObjectType.INTEGRATION
DesignObjectType.EXPRESSION_RULE
DesignObjectType.DECISION
DesignObjectType.REPORT
DesignObjectType.DOCUMENT
DesignObjectType.FOLDER
DesignObjectType.FEED
DesignObjectType.GROUP
DesignObjectType.USER
```

#### AISkillObjectType
```python
from appian_locust.objects import AISkillObjectType

# Available AI Skill types:
AISkillObjectType.DOCUMENT_EXTRACTION
AISkillObjectType.DOCUMENT_CLASSIFICATION
AISkillObjectType.EMAIL_CLASSIFICATION
```

#### ClientMode
```python
from appian_locust.client_mode import ClientMode

# Set client mode
self.appian.set_client_mode(ClientMode.SITES)
self.appian.set_client_mode(ClientMode.TEMPO)
self.appian.set_client_mode(ClientMode.PORTALS)
```

### Feature Flags
```python
from appian_locust import FeatureFlag

def on_start(self):
    super().on_start()
    self.override_default_flags([
        FeatureFlag.SOME_FEATURE
    ])
```

### Custom Request Labels
```python
form = self.appian.visitor.visit_site(
    "Portal",
    "Page",
    locust_request_label="Custom.Label.Here"
)
```

### Design Object Interactions
```python
# Visit by ID
design_obj = self.appian.visitor.visit_design_object_by_id("opaque_id")

# Visit by name and type
from appian_locust.objects import DesignObjectType

design_obj = self.appian.visitor.visit_design_object_by_name(
    object_name="My Interface",
    object_type=DesignObjectType.INTERFACE
)
```

### AI Skill Testing
```python
# Visit AI Skill by name
ai_skill = self.appian.visitor.visit_ai_skill_by_name("My AI Skill")

# Visit AI Skill by ID
ai_skill = self.appian.visitor.visit_ai_skill_by_id("opaque_id")
```

## Debugging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use Test Labels
Prefer test labels over display labels for stability:
```python
form.click_button(test_label="submit_button")
```

### Inspect Form State
```python
current_state = form.get_latest_state()
print(current_state)
```

### Check Network Requests
Use Locust's web UI to inspect request/response details

## Common Issues

### Login Failures
- Verify `host` doesn't include `https://`
- Check username/password are correct
- Ensure user has access to the site

### Element Not Found
- Use `exact_match=False` for partial matching
- Try using `test_label` instead of `label`
- Check if element is in async-loaded content

### SSL Errors
```python
class UserActor(HttpUser):
    def on_start(self):
        self.client.verify = False  # Only for trusted hosts
```

## Best Practices

1. **Use AppianTaskSet** as base class for all test sets
2. **Set locust_request_labels** for better reporting
3. **Use test labels** when available for stability
4. **Handle async loading** with refresh loops
5. **Reuse forms** instead of re-navigating
6. **Use exact_match=False** for flexible matching
7. **Test with single user** before scaling up
8. **Monitor Appian logs** during load tests
9. **Use pipenv** for dependency management
10. **Keep tests focused** on critical user journeys

## Running Tests

### Basic Run
```bash
locust -f my_locustfile.py
```

### Headless Mode
```bash
locust -f my_locustfile.py --headless -u 10 -r 2 -t 5m
```

### With Config
```bash
locust -f my_locustfile.py --config config.json
```

### Distributed Mode
```bash
# Master
locust -f my_locustfile.py --master

# Workers
locust -f my_locustfile.py --worker --master-host=<master-ip>
```

## Resources

- **Documentation**: https://appian-locust.readthedocs.io/en/latest/
- **Source Code**: https://gitlab.com/appian-oss/appian-locust
- **Locust Docs**: https://docs.locust.io/
- **Examples**: https://gitlab.com/appian-oss/appian-locust/-/tree/main/examples

## Module Structure

- `appian_locust/` - Main package
  - `appian_client.py` - Main client class
  - `appian_task_set.py` - Base task set class
  - `visitor.py` - Navigation methods
  - `uiform/` - UI form classes
  - `objects/` - Data objects and enums
  - `utilities/` - Helper functions
  - `exceptions/` - Custom exceptions

## When to Use What

**Use visit_site()** when:
- Navigating to a specific site page
- Page is a SAIL interface

**Use visit_record_type()** when:
- Need to see list of records
- Want to search/filter records

**Use visit_record_instance()** when:
- Need to interact with specific record
- Know the record name

**Use visit_task()** when:
- Working with tasks/process instances
- Need to complete workflow steps

**Use visit_action()** when:
- Triggering standalone actions
- Starting process models

**Use visit_report()** when:
- Accessing report interfaces
- Need report data

## Instructions for AI Assistant

When users ask about Appian Locust:
1. **Provide working code examples** based on patterns above
2. **Reference official docs** for detailed information
3. **Explain the visitor pattern** for navigation
4. **Show UiForm interaction methods** for component manipulation
5. **Include error handling** and debugging tips
6. **Mention best practices** relevant to the question
7. **Use actual method signatures** from the codebase
8. **Explain authentication** and configuration when relevant
9. **Show both simple and advanced** usage patterns
10. **Direct to ReadTheDocs** for comprehensive guides

Always base answers on the actual API and patterns shown in this steering file.
