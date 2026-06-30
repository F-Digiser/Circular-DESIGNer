# Third-Party Software Notices

## Release scope

This notice applies to Circular DESIGNer, release 1.0, built with Python 3.12.3 on 30th June 2026.

The authoritative dependency inventory for this release is:

* `requirements-lock.txt`

## Direct dependencies

| Distribution |   Version          | Role in this release                                     | Licence                                    | Source / notice location |
| ------------ | -----------------: | -------------------------------------------------------- | ------------------------------------------ | ------------------------ |
| CadQuery     | 2.6.0              | Parametric CAD modelling                                 | Apache-2.0                                 | `licenses/Apache-2.0.txt`        |
| cadquery-ocp | OCP 7.8.1.1.post1  | OpenCascade Python bindings used by CadQuery             | Apache-2.0                                 | `licenses/Apache-2.0.txt`        |
| Open CASCADE Technology (OCCT) | Bundled through `cadquery-ocp`; version corresponding to the recorded wheel/build metadata  | Native 3D CAD kernel used through cadquery-ocp/OCP and CadQuery             | LGPL-2.1-only WITH OCCT-exception-1.0                                 | `licenses/OCCT_license`        |
| Matplotlib   | 3.10.1             | Plotting and visualisation                               | LicenseRef-Matplotlib                      | `licenses/Matplotlib-LICENSE-reference.txt`        |
| PyQt5        | 5.15.11            | Desktop graphical user interface                         | GPL-3.0-only                               | `licenses/GPL-3.0-only.txt`        |
| Qt runtime libraries bundled or required by PyQt5           | 5.15.2             | GUI framework/runtime                                    | GPL-3.0-only                               | `licenses/GPL-3.0-only.txt`        |
| Requests     | 2.32.5             | HTTP client functions                                    | Apache-2.0                                 | `licenses/Requests-Apache-2.0.txt`        |
| FastAPI      | 0.120.4            | Optional HTTP API                                        | MIT                                        | `licenses/FastAPI-MIT.txt`        |
| Pydantic     | 2.12.5             | API data models and validation                           | MIT                                        | `licenses/Pydantic-MIT.txt`        |
| Uvicorn      | 0.34.3             | Optional API server                                      | BSD-3-Clause                               | `licenses/Uvicorn-BSD-3-Clause.txt`        |
| tractusx-sdk | 0.7.1              | Optional intended Catena-X connectivity layer            | Apache-2.0                                 | `licenses/Apache-2.0.txt`        |
| PyInstaller  | 6.19.0             | Optional application packaging and splash-screen support | GPL-2.0-or-later WITH Bootloader-exception | `licenses/PyInstaller_license`        |

## Transitive and native dependencies

The complete inventory of direct and transitive dependencies, including native components bundled through CadQuery, OpenCascade/OCP, PyQt5, Matplotlib and PyInstaller, is recorded in `requirements-lock.txt`.

Where licence terms require preservation of licence text, copyright notices, attribution notices or a `NOTICE` file, the applicable original material is included in the `licenses/` directory or distributed with the corresponding component.

## Python runtime

This packaged application was built with CPython 3.12.3, 64-bit.

The Python runtime and standard library are licensed under the Python
Software Foundation License Version 2. The corresponding licence text is
included in `licenses/Python-3.12.3-LICENSE.txt`.

## Python standard library

The application also uses Python standard-library modules. These are supplied with the Python runtime and are not listed module-by-module in this notice. The Python runtime version used for this release is recorded above.
