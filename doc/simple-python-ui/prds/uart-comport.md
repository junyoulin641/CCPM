---
name: uart-comport
description: UART COM port communication interface for embedded hardware interaction
status: backlog
created: 2025-12-24T03:30:57Z
updated: 2025-12-24T03:30:57Z
---

# PRD: UART COM Port Communication

## Executive Summary

The UART COM port feature transforms the PyQt6 desktop application into a foundational communication interface between PC and embedded hardware (Arduino, ESP32, etc.). This feature enables real-time data exchange, command transmission, and device monitoring through a stable, readable, and maintainable desktop tool. Version 1 follows an MVP-first strategy, focusing on core connectivity and basic interaction while establishing a solid architecture for future protocol parsing, automation, and logging capabilities.

## Problem Statement

**Current Challenges:**
- Developers and hobbyists working with embedded devices (Arduino, ESP32, serial sensors) currently rely on basic Serial Monitor tools or manual CLI commands for device communication
- Existing tools lack customization, structured data presentation, and integration with application workflows
- No unified desktop interface for viewing logs, sending commands, and monitoring device status in real-time

**Why Now:**
- The existing `basic-ui` feature provides a PyQt6 application skeleton ready for functional extension
- Cross-platform serial communication libraries (PySerial) are mature and well-supported
- Growing need for accessible, educational, and developer-friendly tools for IoT and embedded prototyping

**Value Proposition:**
This feature provides a **general-purpose, extensible UART communication foundation** that serves development, learning, and prototype validation needs without being limited to a single use case. It replaces fragmented workflows with a cohesive, visual desktop interface.

## Integration with Existing Project

**Architecture Alignment:**
- Leverages existing PyQt6 framework and application structure
- Integrates as a **modular UARTWidget component** (reusable, embeddable)
- v1 embeds widget into main window (similar to `basic-ui` layout)
- Future flexibility: same widget can move to separate window or multi-tab layout without refactoring

**Code Integration Points:**
- Main window provides embedding area or menu/button entry point
- Widget uses Qt Signal/Slot mechanism (consistent with PyQt6 patterns)
- No modifications to existing `basic-ui` logic required; parallel development possible

**Technology Stack Continuity:**
- Python 3.10+ (aligned with project requirements)
- PyQt6 (existing framework)
- PySerial (cross-platform serial library, mature ecosystem)

## User Stories

### User Persona 1: Embedded Systems Developer
**Primary Goal:** Efficient firmware development and device testing

- **Story 1:** As an embedded developer, I want to quickly connect to my Arduino/ESP32 device via COM port so that I can verify firmware behavior without switching between multiple tools
- **Story 2:** As an embedded developer, I want to send test commands through a GUI and immediately see device responses so that I can debug communication logic efficiently
- **Story 3:** As an embedded developer, I want the UI to remain responsive during continuous data streaming so that I can monitor long-running tests without the application freezing

### User Persona 2: Hardware/Firmware Engineer (Testing & Debugging)
**Primary Goal:** Reliable device validation and issue reproduction

- **Story 1:** As a hardware engineer, I want to see real-time device logs and status messages in a structured view so that I can identify issues during system bring-up
- **Story 2:** As a hardware engineer, I want clear error messages when connection fails or device disconnects so that I can quickly diagnose hardware or driver problems
- **Story 3:** As a hardware engineer, I want to reconnect to a device after hot-plugging without restarting the application so that I can continue testing seamlessly

### User Persona 3: Student/Learner (Serial Communication & Embedded Basics)
**Primary Goal:** Understanding UART communication concepts

- **Story 1:** As a student, I want to see both sent commands and received responses clearly labeled (TX/RX) so that I can understand bidirectional serial communication flow
- **Story 2:** As a student, I want example firmware sketches that demonstrate basic UART patterns so that I can learn by experimentation
- **Story 3:** As a student, I want the tool to handle common mistakes (wrong baud rate, disconnected device) gracefully so that I can learn through trial and error without crashes

### User Persona 4: Hobbyist/IoT Prototyper
**Primary Goal:** Quick validation and hands-on experimentation

- **Story 1:** As a hobbyist, I want to auto-detect available COM ports so that I don't have to manually search for device addresses
- **Story 2:** As a hobbyist, I want a simple "send command" input field with Enter-key support so that I can interact with my prototype device naturally
- **Story 3:** As a hobbyist, I want to adjust baud rate easily to match different devices so that I can switch between projects without technical barriers

## Functional Requirements

### Feature 1: COM Port Management (Core Connectivity)
**Description:** Provide robust, user-friendly controls for discovering, configuring, and connecting to serial devices.

**Capabilities:**
- **Auto-detect available COM ports** on system (with manual refresh option)
- **Port selection dropdown** listing available devices (platform-aware: COMx on Windows, /dev/cu.* on macOS, /dev/ttyUSB*/ttyACM* on Linux)
- **Baud rate configuration** (common presets: 9600, 19200, 38400, 57600, 115200)
- **Data bits/parity/stop bits:** Use sensible defaults (8N1) in v1; reserve architecture for future advanced settings
- **Connect/Disconnect buttons** with clear visual state indication
- **Connection status indicator:** Connected (green) / Disconnected (gray) / Error (red)

**User Interaction Flow:**
1. User opens application → UARTWidget displays available ports in dropdown
2. User selects port and baud rate → clicks "Connect"
3. Status indicator changes to "Connected" (green)
4. User can send/receive data
5. User clicks "Disconnect" or device is unplugged → status updates, resources released

**Expected Behavior:**
- Port list updates on manual refresh
- Clear error messages for: port in use, permission denied, invalid parameters
- Graceful degradation when no ports available

### Feature 2: Data Reception (Real-Time Observability)
**Description:** Display incoming serial data in real-time with clear presentation and buffer management.

**Capabilities:**
- **Real-time text display** in dedicated RX view (QTextEdit or similar)
- **Auto-scroll to latest data** (user can disable to inspect earlier content)
- **Clear receive buffer button** to reset view
- **Optional timestamp per line** (v1: toggle-able feature if implementation cost is low)
- **In-memory capped buffer** (ring buffer or max N lines, e.g., 1000 lines) to prevent memory growth

**User Interaction Flow:**
1. Device sends data → appears immediately in RX view
2. New data auto-scrolls to bottom (if enabled)
3. User can scroll up to review earlier messages
4. User clicks "Clear" to reset buffer and view

**Expected Behavior:**
- UTF-8 decoding with fallback (display replacement chars if invalid, don't crash)
- Line-based splitting (handle \n, \r\n)
- No visible lag during moderate streaming (< 115200 baud, line-based logging)
- Buffer enforces size limit (oldest data discarded when limit reached)

### Feature 3: Data Transmission (Basic Interaction)
**Description:** Allow users to send commands to serial devices via GUI input.

**Capabilities:**
- **Text input field** for command entry
- **Send button** and **Enter-key shortcut** to transmit
- **TX echo in output view** (clearly labeled/colored as "TX" to distinguish from RX)
- **Line ending configuration:** Default \n; optionally allow \r\n (simple dropdown or fixed in v1)
- **Command history navigation** (up/down arrows) - nice-to-have in v1 if low-cost

**User Interaction Flow:**
1. User types command in input field
2. User presses Enter or clicks "Send"
3. Command is sent to device and displayed in output view with TX prefix/color
4. User sees device response (RX) in same view

**Expected Behavior:**
- Commands sent with correct line ending
- TX entries clearly distinguishable from RX in output
- Input field clears after send (or retains for re-send based on UX preference)

### Feature 4: Error Handling & Recovery
**Description:** Gracefully handle connection failures, hot unplugs, and unexpected states.

**Capabilities:**
- **Connection failure detection:** Port occupied, permission denied, invalid parameters
- **Hot unplug handling:** Detect device disconnect, update UI state, release resources
- **Reconnect workflow:** Allow user to reconnect after device is replugged without restarting app
- **Error message display:** Clear, actionable messages (e.g., "Port COM3 not found. Check device connection and drivers.")

**User Interaction Flow (Error Scenario):**
1. Device unplugged during active connection
2. UI detects disconnect → status changes to "Disconnected/Error"
3. Worker thread safely stops
4. User replugs device → clicks "Refresh" or manually reconnects
5. Connection succeeds without application restart

**Expected Behavior:**
- No application crashes or hangs on errors
- Worker thread terminates cleanly
- Serial port released for reuse

## Non-Functional Requirements

### Performance
- **Moderate data rate stability:** Support continuous streaming at ≤ 115200 baud without data loss or UI degradation
- **Latency target:** "Human eye perceivable real-time" (no strict millisecond requirement, but responsive feel)
- **CPU usage:** Low idle CPU; no abnormal spikes during normal operation
- **Stress test:** Continuous streaming (50-200 bytes/line, every 50-100ms) for 30-60 seconds without errors or UI freeze

### Usability
- **Intuitive UI:** COM port selection, connect/disconnect, send/receive should be self-explanatory
- **Minimal learning curve:** Users familiar with Serial Monitor tools can transition immediately
- **Clear visual feedback:** Connection status, TX/RX distinction, error messages

### Reliability
- **Stable connections:** No unexpected disconnects under normal conditions
- **Graceful error recovery:** Hot unplug, reconnect, parameter changes handled without crashes
- **Resource cleanup:** Serial ports and threads released properly on disconnect/exit

### Compatibility
- **Cross-platform support:** Windows (primary validation), macOS and Linux (smoke tested)
- **Driver agnostic:** Works with CH340, CP2102, FTDI, native Arduino USB drivers
- **Python 3.10+ compatibility**
- **PyQt6 version stability** (use project-verified version, avoid bleeding-edge releases)

### Maintainability
- **Modular architecture:** UARTWidget as reusable component
- **Clean separation:** Serial I/O logic (Worker) separate from UI (Widget)
- **Extensible data model:** Structured data (direction, timestamp, payload) ready for future export/logging
- **Readable code:** Clear naming, comments for threading/signal logic

### Security
- **No remote access:** Local serial communication only
- **Input validation:** Prevent injection of control characters that could harm device (basic sanitization if needed)
- **Minimal privileges:** Only request serial port access, no elevated permissions

## Technical Approach

### Architecture Overview

**Component Structure:**
```
UARTWidget (QWidget)
├── UI Elements (port dropdown, connect button, RX/TX views, input field)
├── SerialWorker (QObject, runs in QThread)
│   ├── Serial I/O loop (PySerial read/write)
│   ├── Signals: dataReceived, errorOccurred, statusChanged
│   └── Slots: sendData, connect, disconnect
└── Data Model (in-memory capped buffer)
    ├── MessageEntry: {direction: TX/RX, timestamp, payload}
    └── Buffer management (ring buffer or maxlen deque)
```

**Threading Model:**
- **UI Thread:** Handles all Qt UI updates (QTextEdit, buttons, dropdowns)
- **Worker Thread (QThread):** Runs SerialWorker for blocking serial I/O operations
- **Signal/Slot Communication:** Worker emits signals for received data, errors; UI thread updates display safely

**PySerial Integration:**
- Serial port opened in Worker thread with specified parameters (port, baud, timeout)
- Read loop with timeout (e.g., 0.1s) to allow graceful shutdown
- Write operations queued or executed directly in Worker

### Technology Stack
- **Language:** Python 3.10+
- **GUI Framework:** PyQt6 (existing project framework)
- **Serial Library:** PySerial (cross-platform, mature, widely-used)
- **Concurrency:** QThread + Signal/Slot (PyQt6 threading best practice)

### Key Design Decisions

**1. Modular Widget Design (Option C)**
- UARTWidget is self-contained and reusable
- v1: Embedded in main window
- Future: Can be placed in separate window, tabs, or multiple instances without refactoring

**2. QThread + Signal/Slot (vs. Polling)**
- Avoids UI thread blocking
- Follows PyQt6 official threading recommendations
- Easier to extend with queues, state machines, or protocol layers

**3. In-Memory Capped Buffer (vs. Unbounded or Immediate Export)**
- Prevents memory growth during long sessions
- Prepares data model for future export/logging features
- Simple for v1, extensible for v2+

**4. Text-First Mode (Defer HEX/Binary)**
- Aligns with primary use case (firmware logs, command-response)
- Reduces v1 complexity
- HEX/binary mode can be added as display option in v2

**5. Single Connection (Defer Multi-Device)**
- Simplifies state management
- Matches typical use case (one active device at a time)
- Multi-device/multi-tab support reserved for v2+

### Data Model

**MessageEntry Structure:**
```python
{
    'direction': 'TX' | 'RX',
    'timestamp': datetime (optional in v1, toggle-able),
    'payload': str (decoded text, UTF-8 with fallback)
}
```

**Buffer Management:**
- Use `collections.deque(maxlen=N)` or custom ring buffer
- Default max size: 1000 entries (configurable internally)
- Oldest entries discarded when limit reached

### Error Handling Strategy
- **Connection errors:** Display clear message, update status indicator
- **Decode errors:** Use UTF-8 with `errors='replace'` to avoid crashes
- **Hot unplug:** Catch OS-level serial exceptions, emit `errorOccurred` signal, update UI
- **Thread safety:** All UI updates via signals; Worker never touches UI directly

### Integration Points with Existing Code
- **Main Window:** Provides layout slot or menu entry for UARTWidget
- **Project Dependencies:** Add `pyserial` to requirements.txt
- **No Impact on basic-ui:** UART feature operates independently; can develop in parallel

## Success Criteria

### A. Connection & Port Management Reliability
- ✅ Port discovery lists all available COM ports consistently
- ✅ Connect/Disconnect buttons change state deterministically
- ✅ Baud rate and default parameters (8N1) apply correctly
- ✅ Clear error messages displayed for: wrong port, port in use, permission denied
- ✅ No UI crashes or hangs on connection errors

### B. Data Transmission & Reception Correctness
- ✅ Send→Receive round-trip: Command sent, response received within ≤ 1 second (device-dependent)
- ✅ RX data appears in real-time without interruption or garbled characters (ASCII/UTF-8)
- ✅ TX commands clearly labeled/colored in output view (distinguishable from RX)
- ✅ In-memory buffer enforces size limit; long-term tests show no unbounded memory growth

### C. UI Responsiveness & Non-Blocking Behavior
- ✅ UI remains responsive during continuous data streaming (e.g., 10-50 lines/second)
- ✅ CPU usage stays low during idle and moderate data rates
- ✅ Auto-scroll keeps up with incoming data without lag; can be disabled for review

### D. Error Handling & Recovery
- ✅ Hot unplug: UI shows disconnect/error, thread stops cleanly, no crash or hang
- ✅ Reconnect workflow: Device can be replugged and reconnected without restarting application

### E. Performance Benchmarks (Pragmatic v1)
- ✅ Stable operation at ≤ 115200 baud with line-based logging (50-200 bytes/line)
- ✅ Stress test: 30-60 seconds of continuous streaming without errors or UI freeze
- ✅ Latency: Data appears in UI within human-perceivable real-time (no strict millisecond SLA)

### Testing & Validation

**Manual Hardware Testing (Primary):**
- **Test Hardware:** Arduino Uno/Nano, ESP32, USB-UART dongles (CH340/CP2102)
- **Test Scenarios:**
  1. Basic connect/disconnect cycle
  2. Parameter variations: 9600 vs. 115200 baud
  3. Command-response: PC sends `PING\n`, device replies `PONG\n`
  4. Continuous streaming: Device outputs one line every 50-100ms for 1-5 minutes
  5. Hot unplug/replug: Disconnect USB during active connection, verify graceful error and reconnect

**Automated/Semi-Automated Testing (Nice-to-Have):**
- Loopback testing (TX↔RX wired) or virtual serial pairs for consistency validation
- Unit tests for SerialWorker: state transitions, buffer cap, error propagation

**Example Firmware/Sketches:**
- `echo_uart.ino`: Echoes back received data (verifies TX/RX correctness)
- `ping_pong.ino`: Responds to specific commands (verifies command parsing)
- `stream_logger.ino`: Periodic log output (verifies streaming and performance)

**Definition of "Done" for v1:**
- Stably connects to Arduino/ESP32 devices
- Reliably sends and receives data with clear TX/RX presentation
- UI remains responsive under continuous output scenarios
- Correctly handles hot unplug/reconnect without crashes
- Memory and performance remain controlled during long-term use (buffer cap enforced)

## Constraints & Assumptions

### Platform & Environment Constraints
- **Target Platforms:** Cross-platform (Windows/macOS/Linux); Windows is primary validation platform for v1, macOS/Linux smoke tested based on resources
- **Python Version:** Minimum Python 3.10+ (not recommended below 3.9)
- **PyQt6 Version:** Use project's current verified version; avoid bleeding-edge releases to minimize compatibility risks
- **Driver Assumptions:** Users are expected to have USB-UART drivers (CH340/CP2102/FTDI) installed; README/Help will document driver requirements

### Development Constraints
- **Timeline:** v1 follows MVP scope (connect + TX/RX + error handling + buffer cap); no feature creep to parsing, scripting, or export
- **Dependencies:** UART feature can proceed in parallel with `basic-ui`; only requires main window skeleton/layout ready
- **Resources:** Solo development (or limited collaboration); design favors "modular but not overly abstract" to avoid heavy architecture

### Known Limitations (v1 Explicitly Documented)
- **Single Connection Only:** v1 supports one active COM port connection at a time (no multi-device/multi-tab support)
- **Text-First Mode:** Primarily ASCII/UTF-8 display; binary/HEX mode deferred to v2+
- **Performance Target:** Optimized for ≤ 115200 baud with general logging/command-response use cases; high-throughput binary streams or near-limit rates not guaranteed
- **No Protocol Parsing:** v1 displays raw stream or line-based text only; packet parsing and protocol visualization deferred to v2+
- **No Export/Logging UI:** v1 does not provide file export or structured logging interface; data model reserves extension points for future implementation

### Additional Assumptions
- **Port Naming Differences:** UI uses dropdown list to abstract platform differences (Windows: COMx, macOS: /dev/cu.*, Linux: /dev/ttyUSB*/ttyACM*)
- **Encoding Variability:** Devices may not use UTF-8; v1 decodes with UTF-8 + fallback to replacement characters (errors='replace') to avoid crashes
- **Line Ending Handling:** Default to \n, with support for \r\n; command send configurable (v1 may fix to \n or provide simple option)

## Out of Scope (v1)

Explicitly **NOT** included in v1 to maintain MVP focus:

### Deferred to v2+
- **Multi-device/Multi-connection Support:** Simultaneous connections to multiple COM ports or tabbed interface
- **HEX/Binary Display Mode:** Viewing data in hexadecimal or raw binary format
- **Data Export/Logging UI:** Save received data to files (CSV, TXT, binary)
- **Protocol Parsing & Visualization:** Structured packet parsing, protocol-aware display, custom parsers
- **Custom Command Buttons/Macros:** Pre-configured command buttons, command sequences, scripting
- **Advanced Filtering/Highlighting:** Data filtering rules, keyword highlighting, regex search
- **Automated Testing Framework:** Built-in test sequencing, scriptable command automation
- **Advanced Serial Settings UI:** Fine-grained control over data bits, parity, stop bits (v1 uses defaults)

### Future Enhancements
- Integration with device firmware update workflows
- Protocol analyzers (e.g., Modbus, custom protocols)
- Cloud logging or remote monitoring
- Multi-language UI support

## Dependencies

### External Libraries
- **PySerial:** Install via `pip install pyserial` (add to requirements.txt)
- **PyQt6:** Existing project dependency (already in use)

### Internal Dependencies
- **basic-ui Feature:** Main window skeleton must provide embedding area for UARTWidget or menu/button entry point
  - UART feature can proceed in parallel; only requires UI "skeleton" in place, not full completion

### Hardware/Driver Dependencies
- **USB-UART Drivers:** Users must install appropriate drivers for their devices (CH340, CP2102, FTDI, etc.)
  - Documented in README/Help; v1 assumes drivers are pre-installed

### Prerequisite Knowledge
- Users should understand basic serial communication concepts (baud rate, COM ports)
- For educational users: example firmware sketches provided to facilitate learning

## Estimated Effort

**Timeline Estimate:** 1-2 weeks for v1 MVP (solo development, assuming 10-15 hours total)

**Breakdown:**
- **Days 1-2:** UARTWidget UI layout, port discovery, connect/disconnect logic (4-5 hours)
- **Days 3-4:** SerialWorker implementation, QThread setup, Signal/Slot wiring (4-5 hours)
- **Days 5-6:** Data reception/transmission, buffer management, TX/RX display (3-4 hours)
- **Day 7:** Error handling, hot unplug, reconnect workflow (2-3 hours)
- **Day 8:** Manual testing with Arduino/ESP32, example firmware creation (2-3 hours)
- **Optional:** Unit tests, loopback testing, cross-platform smoke tests (2-3 hours if time permits)

**Critical Path Items:**
1. SerialWorker thread safety and signal/slot correctness (core stability)
2. Buffer cap implementation (prevents memory issues)
3. Hot unplug handling (user experience)

**Resource Requirements:**
- 1 developer (Python/PyQt6 proficiency)
- Test hardware: Arduino Uno/Nano or ESP32 (readily available)
- Optional: USB-UART dongle for driver variation testing

**Risks & Mitigation:**
- **Risk:** Platform-specific serial port behavior differences
  - **Mitigation:** Early cross-platform testing (at least smoke test on macOS/Linux)
- **Risk:** Threading bugs causing UI freezes or data corruption
  - **Mitigation:** Follow PyQt6 threading best practices, thorough signal/slot review
- **Risk:** Scope creep (adding HEX mode, export, etc.)
  - **Mitigation:** Strict adherence to MVP definition; defer all v2+ features

---

## Appendix: v2+ Roadmap (Informational)

While out of scope for v1, the following features are natural extensions:

**v2: Enhanced Usability**
- Command history navigation (if not in v1)
- Custom command buttons/macros
- HEX/Binary display mode toggle
- Timestamp display options

**v3: Data Management**
- Export to CSV/TXT/binary files
- Session logging and replay
- Search/filter within buffer

**v4: Protocol Intelligence**
- Custom protocol parsers (Modbus, custom formats)
- Packet visualization
- Automated command sequences

**v5: Advanced Features**
- Multi-device/multi-tab support
- Automated testing framework
- Integration with firmware update tools
