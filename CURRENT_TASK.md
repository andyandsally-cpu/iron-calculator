Status
READY
Goal
Fix import so the patient name from the imported file is retained, with a suffix of _import_ddmmyy (using the import date), instead of replacing it with "import xxxxxx".
Files likely involved

index.html — grep for the import handler and wherever the imported patient name is set

Implementation notes

Find where the import sets the patient name (likely something like "import " + ...)
Replace with: extracted name from the imported data + _import_ + today's date formatted as ddmmyy
Date should be the date of import, not a date from the file
If the imported data has no patient name, fall back to import_ddmmyy

Out of scope

Export format changes
Any other import/export behaviour

Acceptance checks

Import a file with a known patient name — result is PatientName_import_ddmmyy
Import a file with no patient name — result is import_ddmmyy
No paywall/DEV_MODE regression