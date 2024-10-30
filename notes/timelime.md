# Aggressively Realistic Timeline

## High Level
| Process            | Status            | Target Date       | Completion Date   |
| ------------------ |:-----------------:|------------------:| ----------------- |
| Backup Deliverable - Production | Alpha | 31 JAN 2025 | --- |
| Backup Deliverable - Management | WIP | 31 JAN 2025 | --- |
| Databases Fully Structured | WIP | 31 JAN 2025 | --- |
| PowerApp Initial Build | WIP | 14 FEB 2025 | --- |
| OEE Algorithms Completed | --- | 03 MAR 2025 | --- |
| PowerApp for Management - Alpha | --- | 10 MAR 2025 | --- |
| PowerApp for Management - Beta | --- | 17 MAR 2025 | --- |
| PowerApp for Management - Launch | --- | 31 MAR 2025 | --- |

## Low Level
| Process            | Status            | Target Date       | Challenges        |
| ------------------ |:-----------------:|------------------:| ----------------- |
| PowerApp for Production | Cancelled | --- | Time loss |
| New FE Reject Database | Cancelled | --- | Time loss |
| Initial Database Setup | Cancelled | --- | Time loss |
| Custom CSV Loader Program - Flet | Completed | 25 OCT 2024 | --- |
| Custom CSV Loader Program - CLI | Completed | 25 OCT 2024 | --- |
| Access DB connection to PowerApp Established | On Hold | 15 NOV 2024 | Transfer system works, waiting on confirmation of OEE focus |
| Relocate CSV outputs to cloud location | On Hold | 01 DEC 2024 | Needs Wrona intervention. |
| Constraint data Updated and Complete | On Hold | 17 JAN 2025 | Current data in use, need data for missing lines |
| Backup Deliverable - Production | Alpha | 31 JAN 2025 | Time loss |
| Backup Deliverable - Management | WIP | 31 JAN 2025 | Time loss |
| PowerApp SharePoint List Databases Structured | On Hold | 31 JAN 2025 | Initial structure implemented |
| PowerApp for Management - Initial Build Completed | WIP | 14 FEB 2025 | Templates/formulas from Encap apps non-transferrable |
| Power Bi connection to PowerApp Established | On Hold | 21 FEB 2025 | Progress determined by dashboard configuration |
| SharePoint List DB to PowerApp Data Algorithms Completed | --- | 24 FEB 2025 | New data connections not plug and play from old system |
| OEE Algorithms Completed | WIP | 03 MAR 2025 | OEE algorithm updated, pulls good OEE percentages, needs confirmation |
| PowerApp for Management - Alpha | --- | 10 MAR 2025 | Bug Fixes |
| PowerApp for Management - Beta | --- | 17 MAR 2025 | Bug Fixes |
| PowerApp for Management - Launch | --- | 31 MAR 2025 | Projected Launch Day |


*Subject to changes*

## Current Challenges

- Time loss due to scope change
    - The first three weeks of work on the project were essentially scrapped as new information made all previous work obsolete.

- Time extension due to scope change
    - Previously acquired assets from the Encapsulation Application are non-transferrable. (Old app templates, database structure)
    - Formula and Algorithm scope has changed, more complex, non-transferrable
    - New knowledge of processes, programs and data transfer are required before actionable progress can be made. 
    - The new work constraints have created a large change of scope for the project.

- These new constraints include:
    - No new inputs for Operators
    - Working with legacy data sources, Access, CSV files
    - Legacy data structures cannot be altered, only hooked into
    - Large databases inhibit automatic information transfer and manipulation

Currently, because of the state of the data collection of downtime and line data The Front End DMS Management Suite will not have the same
functionality or useability as the Encapsulation version of the PowerApp.

- Missing Lot Information for downtime collection
    - Downtime tracking will not be as robust as the Enap version.
    - A simple graphing version can still be made for downtime reasons, but only the built in reasons from the CSV and not the updated LSPS tracking
    - OEE2 Calculations will be simplified, robust data filtering cannot be achieved
    - A new system will need to be created to track Planned Runtime
        - Extracting the planned runtime cannot be achieved in the same way its calculated with the Encap version
- Constraint data not complete
    - Data pulled from databases cannot be parsed though OEE algorithm without constraint data.

- Backup Deliverable
    - Current access and csv databases are too unpredictable and unreliable to confirm completion of a DMS system
    - Creating a backup deliverable with Manual Inputs and Sharepoint Databases

- Cannot compile custom apps without sadm account
    - Time loss, took 2 days to get sadm acct for code compilations
    - Worked on App and Database in the mean time.