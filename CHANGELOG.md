<!-- markdownlint-disable MD024 -->
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

## [0.2.1] - 2025-01-06

### Changed

- Bumped minimum required Python version from 3.9 to 3.10

### Fixed

- Fixed a useability issue where one would assume that it was possible to bitwise-or `USBDirecton`, `USBRequestType`, and `USBRequestRecipient` together to form a `bmRequestType`, this was not properly implemented, but is now correct.

## [0.2.0] - 2023-03-14

### Added

- Initial [`UAS-3`](https://standards.incits.org/higherlogic/ws/public/projects/2737/details) descriptor addition.

### Changed

- Updated Copyright Years

### Fixed

- Fixed the `DeviceQualifierDescriptorEmitter` overriding the `DeviceQualifierDescriptor` on assignment.
- Fixed the subclassing from `int` in the `ConnectorColour`.
- Miscellaneous spelling.
- Fixed the `USBPacketID.byte()` call to cast properly.
- Fixed the two failing tests caused by some internal refactoring.
- Minor typing fixups

## [0.1] - 2022-11-13

Initial Release

[Unreleased]: https://github.com/shrine-maiden-heavy-industries/usb-construct/compare/v0.2.1...main
[0.2.1]: https://github.com/shrine-maiden-heavy-industries/usb-construct/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/shrine-maiden-heavy-industries/usb-construct/compare/v0.1...v0.2.0
[0.1]: https://github.com/shrine-maiden-heavy-industries/usb-construct/compare/v0.1...main
