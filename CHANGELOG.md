# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Unreleased template stuff

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
-->

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed


## [0.2.0]

### Added

 - Initial [`UAS-3`](https://standards.incits.org/apps/group_public/project/details.php?project_id=2737) descriptor addition.
### Changed

 - Updated Copyright Years

### Fixed

 - Fixed the `DeviceQualifierDescriptorEmitter` overriding the `DeviceQualifierDescriptor` on assignment.
 - Fixed the subclassing from `int` in the `ConnectorColour`.
 - Miscellaneous spelling.
 - Fixed the `USBPacketID.byte()` call to cast properly.
 - Fixed the two failing tests caused by some internal refactoring.
 - Minor typing fixups
## [0.1]

Initial Release

[Unreleased]: https://github.com/shrine-maiden-heavy-industries/usb-construct/compare/v0.2.0...main
[0.2.0]: https://github.com/shrine-maiden-heavy-industries/usb-construct/compare/v0.1...v0.2.0
[0.1]: https://github.com/shrine-maiden-heavy-industries/usb-construct/compare/v0.1...main
