---
name: epic-uart-widget
status: backlog
created: 2025-12-24T03:36:02Z
progress: 0%
prd: ./doc/simple-python-ui/prds/uart-comport.md
github: https://github.com/junyoulin641/CCPM/issues/8
---

# Epic: UART Widget - Complete COM Port Communication Interface

## Overview

This epic delivers a complete, production-ready **UARTWidget** component for the PyQt6 desktop application, enabling real-time serial communication with embedded devices (Arduino, ESP32, etc.). The widget is designed as a **modular, reusable component** that can be embedded in the main window (v1) or moved to separate windows/tabs in future versions without refactoring.

**What This Epic Delivers:**
- Cross-platform COM port discovery and connection management
- Real-time bidirectional data exchange (TX/RX) with clear visual distinction
- Non-blocking architecture using QThread + Signal/Slot for UI responsiveness
- Robust error handling (connection failures, hot unplug, reconnect workflow)
- Capped in-memory buffer to prevent memory growth during long sessions
- Example Arduino firmware sketches for testing and validation

**Why This Epic Matters:**
- Replaces fragmented workflow (switching between Serial Monitor, CLI tools) with unified desktop interface
- Provides educational tool for students learning serial communication concepts
- Serves as foundational communication layer for future protocol parsing, automation, and logging features

## Architecture Decisions

### 1. Modular UARTWidget Design (Reusable Component)
**Decision:** Implement UARTWidget as self-contained QWidget with all functionality encapsulated.

**Rationale:**
- v1 embeds widget in main window (minimal integration effort)
- Future flexibility: same widget can be placed in separate windows, multi-tab interfaces, or even multiple instances
- Clean separation from `basic-ui` feature (parallel development possible)
- Easier testing and maintenance (widget can be tested independently)

**Implementation:**
- UARTWidget inherits from QWidget
- Contains all UI elements: port dropdown, connect/disconnect buttons, RX/TX views, command input
- Exposes minimal public API for embedding (no tight coupling to main window)

### 2. QThread + Signal/Slot Architecture (Non-Blocking I/O)
**Decision:** Use QThread for serial I/O operations, communicate with UI via Signal/Slot.

**Rationale:**
- **Avoids UI freezing** during blocking serial reads (critical user experience requirement)
- **PyQt6 best practice** (official recommendation for I/O operations)
- **Thread-safe UI updates** via signals (prevents race conditions)
- **Extensible** for future protocol parsing, queuing, state machines

**Implementation:**
- **UI Thread:** Handles all Qt widgets (QTextEdit, QPushButton, QComboBox)
- **Worker Thread (QThread):** Runs SerialWorker (QObject) for PySerial operations
- **Signals:** `dataReceived(str)`, `errorOccurred(str)`, `statusChanged(str)`
- **Slots:** `sendData(str)`, `connectPort(port, baud)`, `disconnectPort()`

### 3. PySerial for Cross-Platform Serial Communication
**Decision:** Use PySerial library (not Qt SerialPort) for v1.

**Rationale:**
- **Mature ecosystem:** PySerial is widely-used, well-documented, stable
- **Cross-platform:** Handles Windows (COMx), macOS (/dev/cu.*), Linux (/dev/ttyUSB*) transparently
- **Lower integration risk:** Avoids potential PyQt6 SerialPort binding issues
- **Future flexibility:** Can migrate to Qt SerialPort in v2+ if tighter Qt integration needed

**Trade-offs:**
- Qt SerialPort offers better event loop integration, but PySerial is "good enough" for v1 MVP
- PySerial requires manual thread management (already addressed by QThread design)

### 4. Capped In-Memory Buffer (Ring Buffer / Deque)
**Decision:** Use `collections.deque(maxlen=1000)` for message storage.

**Rationale:**
- **Prevents unbounded memory growth** during long-running sessions (critical for stability)
- **Simple to implement** (Python standard library)
- **Automatic eviction** of oldest messages when buffer is full
- **Prepares data model** for future export/logging features (structured entries)

**Data Structure:**
```python
{
    'direction': 'TX' | 'RX',
    'timestamp': datetime (optional, toggle-able in v1),
    'payload': str (UTF-8 decoded text)
}
```

### 5. Text-First Mode (Defer HEX/Binary Display)
**Decision:** v1 displays only ASCII/UTF-8 text; HEX/binary mode deferred to v2+.

**Rationale:**
- **Aligns with primary use case:** Firmware logs, command-response debugging (80% of user scenarios)
- **Reduces v1 complexity:** Avoids UI mode switching, binary parsing logic
- **Graceful degradation:** Use `errors='replace'` for invalid UTF-8 (shows � instead of crashing)

**Future Extension Point:**
- Add display mode dropdown (Text / HEX / Binary) in v2
- Same data model supports all modes (just changes rendering)

### 6. Single Connection (Defer Multi-Device Support)
**Decision:** v1 supports one active COM port connection at a time.

**Rationale:**
- **Matches typical use case:** Developers/hobbyists usually work with one device at a time
- **Simplifies state management:** No connection multiplexing, port conflict handling
- **Reduces testing surface:** Focus on rock-solid single-connection experience

**Future Extension:**
- v2+ can support multi-tab interface (multiple UARTWidget instances)
- No architectural changes needed (widget already modular)

## Technical Approach

### Component Architecture

```
UARTWidget (QWidget)
├── UI Layout (QVBoxLayout / QHBoxLayout)
│   ├── Connection Controls (Top Panel)
│   │   ├── QComboBox: Port selection (auto-populated)
│   │   ├── QComboBox: Baud rate (9600, 19200, 38400, 57600, 115200)
│   │   ├── QPushButton: Connect / Disconnect (state-dependent)
│   │   ├── QPushButton: Refresh ports (manual refresh)
│   │   └── QLabel: Connection status (green/gray/red indicator)
│   │
│   ├── Data Display (Main Panel)
│   │   ├── QTextEdit: RX/TX output view (read-only, auto-scroll)
│   │   ├── QCheckBox: Auto-scroll toggle
│   │   ├── QCheckBox: Show timestamps (optional v1 feature)
│   │   └── QPushButton: Clear buffer
│   │
│   └── Command Input (Bottom Panel)
│       ├── QLineEdit: Command entry field
│       └── QPushButton: Send (or Enter key shortcut)
│
├── SerialWorker (QObject, runs in QThread)
│   ├── PySerial.Serial: Port handle
│   ├── read_loop(): Continuous read with timeout (e.g., 0.1s)
│   ├── write_data(data): Send command to device
│   ├── Signals:
│   │   ├── dataReceived(str): Emitted on RX data
│   │   ├── errorOccurred(str): Emitted on connection/read errors
│   │   └── statusChanged(str): Emitted on connect/disconnect
│   └── Slots:
│       ├── connectPort(port, baud): Open serial port
│       ├── disconnectPort(): Close serial port, stop loop
│       └── sendData(str): Queue/send data to device
│
└── Data Model
    ├── message_buffer: deque(maxlen=1000)
    └── MessageEntry: {'direction', 'timestamp', 'payload'}
```

### Serial I/O Worker Implementation

**SerialWorker (runs in QThread):**
```python
class SerialWorker(QObject):
    # Signals
    dataReceived = pyqtSignal(str)
    errorOccurred = pyqtSignal(str)
    statusChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.running = False

    @pyqtSlot(str, int)
    def connectPort(self, port, baud):
        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baud,
                bytesize=8, parity='N', stopbits=1,
                timeout=0.1  # Non-blocking read with timeout
            )
            self.running = True
            self.statusChanged.emit("Connected")
            self.read_loop()  # Start continuous read
        except Exception as e:
            self.errorOccurred.emit(f"Connection failed: {e}")

    def read_loop(self):
        while self.running:
            try:
                if self.serial_port.in_waiting > 0:
                    data = self.serial_port.readline()
                    text = data.decode('utf-8', errors='replace').strip()
                    if text:
                        self.dataReceived.emit(text)
            except Exception as e:
                self.errorOccurred.emit(f"Read error: {e}")
                self.running = False
                break

    @pyqtSlot()
    def disconnectPort(self):
        self.running = False
        if self.serial_port:
            self.serial_port.close()
        self.statusChanged.emit("Disconnected")

    @pyqtSlot(str)
    def sendData(self, data):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write((data + '\n').encode('utf-8'))
```

**Threading Setup in UARTWidget:**
```python
self.worker_thread = QThread()
self.serial_worker = SerialWorker()
self.serial_worker.moveToThread(self.worker_thread)

# Connect signals
self.serial_worker.dataReceived.connect(self.on_data_received)
self.serial_worker.errorOccurred.connect(self.on_error)
self.serial_worker.statusChanged.connect(self.on_status_changed)

# Connect UI to worker slots
self.connect_button.clicked.connect(
    lambda: self.serial_worker.connectPort(
        self.port_combo.currentText(),
        int(self.baud_combo.currentText())
    )
)

self.worker_thread.start()
```

### Port Discovery (Cross-Platform)

Use `serial.tools.list_ports.comports()` for auto-detection:
```python
import serial.tools.list_ports

def refresh_ports(self):
    self.port_combo.clear()
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # port.device: /dev/ttyUSB0, COM3, /dev/cu.usbserial, etc.
        self.port_combo.addItem(port.device, port)

    if not ports:
        self.port_combo.addItem("No ports detected")
```

### Error Handling Strategy

**Connection Errors:**
- Catch `serial.SerialException` during port open
- Display clear message: "Port COM3 not found. Check device connection and drivers."
- Update status indicator to red "Error" state

**Hot Unplug Detection:**
- SerialException during read/write → emit `errorOccurred` signal
- UI updates status to "Disconnected/Error"
- Worker thread stops cleanly (`running = False`)
- Serial port handle released (allows immediate reconnect)

**Decode Errors:**
- Use `decode('utf-8', errors='replace')` → invalid bytes become �
- No crashes, user sees garbled data (acceptable for v1 text-first mode)

**Thread Safety:**
- **All UI updates via signals** (Qt queued connections ensure thread safety)
- Worker **never** directly accesses UI elements
- Serial port handle owned exclusively by worker thread

### Buffer Management

**In-Memory Capped Buffer:**
```python
from collections import deque

class UARTWidget(QWidget):
    def __init__(self):
        self.message_buffer = deque(maxlen=1000)  # Auto-evicts oldest

    def on_data_received(self, text):
        entry = {
            'direction': 'RX',
            'timestamp': datetime.now() if self.show_timestamps else None,
            'payload': text
        }
        self.message_buffer.append(entry)
        self.display_message(entry)

    def display_message(self, entry):
        prefix = f"[{entry['timestamp']}] " if entry['timestamp'] else ""
        direction = "→" if entry['direction'] == 'TX' else "←"
        self.output_view.append(f"{prefix}{direction} {entry['payload']}")
```

**Auto-Scroll Implementation:**
```python
def display_message(self, entry):
    self.output_view.append(formatted_text)
    if self.auto_scroll_checkbox.isChecked():
        scrollbar = self.output_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
```

### Integration with Main Window

**Minimal Coupling:**
```python
# In main.py or main_window.py
from uart_widget import UARTWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uart_widget = UARTWidget()

        # Option A: Embed in central widget
        self.setCentralWidget(self.uart_widget)

        # Option B: Add to existing layout
        # self.main_layout.addWidget(self.uart_widget)

        # Option C: Menu entry to show/hide
        # uart_action = QAction("UART Monitor", self)
        # uart_action.triggered.connect(self.uart_widget.show)
```

**No Impact on basic-ui:**
- UART widget is completely independent
- Can develop and test in parallel with basic-ui feature
- Zero changes to existing code (only integration point is embedding)

## Implementation Strategy

### Phase 1: Core Infrastructure (Days 1-2, ~4-5 hours)
**Goal:** Basic widget structure, port discovery, connect/disconnect logic

**Tasks:**
1. Create `uart_widget.py` module with UARTWidget class
2. Implement UI layout (port dropdown, baud dropdown, connect button, status label)
3. Implement port discovery using `serial.tools.list_ports`
4. Add refresh button functionality
5. Create basic SerialWorker class (skeleton, no I/O yet)
6. Set up QThread and move worker to thread
7. Implement connect/disconnect signals and status updates

**Validation:**
- Port dropdown populates with available COM ports
- Baud rate dropdown shows standard rates
- Connect button changes state (disabled when connected)
- Status indicator shows correct state (Disconnected → Connected)

### Phase 2: Serial I/O & Threading (Days 3-4, ~4-5 hours)
**Goal:** Non-blocking serial read/write with thread-safe UI updates

**Tasks:**
1. Implement SerialWorker.read_loop() with timeout-based non-blocking reads
2. Implement SerialWorker.sendData() for TX operations
3. Wire up dataReceived signal to UI display
4. Implement TX echo in output view (with direction prefix)
5. Add command input field and Send button
6. Implement Enter key shortcut for sending commands
7. Test thread safety (UI responsiveness during continuous streaming)

**Validation:**
- Send command → device receives it → response appears in RX view
- UI remains responsive during continuous data streaming
- TX and RX messages clearly distinguishable in output

### Phase 3: Buffer Management & Display Features (Days 5-6, ~3-4 hours)
**Goal:** Capped buffer, auto-scroll, clear buffer, optional timestamps

**Tasks:**
1. Implement `deque(maxlen=1000)` message buffer
2. Create MessageEntry data structure
3. Implement auto-scroll toggle checkbox
4. Implement clear buffer button
5. Add optional timestamp display (toggle-able)
6. Test buffer eviction (verify oldest messages discarded)
7. Verify no memory growth during long-term streaming

**Validation:**
- Buffer enforces 1000-message limit
- Auto-scroll keeps view at bottom when enabled
- Clear button resets buffer and display
- Timestamps appear/disappear based on toggle
- Long-term test (5+ minutes streaming) shows stable memory usage

### Phase 4: Error Handling & Recovery (Day 7, ~2-3 hours)
**Goal:** Graceful handling of connection failures, hot unplug, reconnect

**Tasks:**
1. Implement connection error handling (port not found, permission denied, port in use)
2. Implement hot unplug detection in read_loop
3. Add error message display (QMessageBox or inline label)
4. Implement reconnect workflow (clean resource release)
5. Test hot unplug → UI updates → replug → reconnect
6. Ensure worker thread terminates cleanly on errors

**Validation:**
- Connection failure shows clear error message
- Hot unplug detected within 1 second → status updates to "Error"
- Worker thread stops cleanly (no zombie threads)
- Device can be replugged and reconnected without app restart
- No crashes or hangs during error scenarios

### Phase 5: Testing & Example Firmware (Day 8, ~2-3 hours)
**Goal:** Hardware validation, example sketches, cross-platform smoke test

**Tasks:**
1. Create `examples/echo_uart.ino` (echo back received data)
2. Create `examples/ping_pong.ino` (respond to PING with PONG)
3. Create `examples/stream_logger.ino` (periodic log output)
4. Test on Arduino Uno/Nano at 9600 and 115200 baud
5. Test on ESP32 (different USB-UART driver)
6. Stress test: 60-second continuous streaming
7. Cross-platform smoke test (Windows + macOS/Linux if available)

**Validation:**
- All test scenarios from Success Criteria pass
- Example firmware works as documented
- No errors during 60-second stress test
- Cross-platform behavior consistent (port naming differences handled)

### Risk Mitigation

**Risk 1: Threading Bugs (UI Freezes, Data Corruption)**
- **Mitigation:** Follow PyQt6 threading best practices strictly
- **Validation:** Code review of all Signal/Slot connections
- **Testing:** Long-running tests with continuous data flow

**Risk 2: Platform-Specific Serial Port Behavior**
- **Mitigation:** Early testing on Windows (primary) + macOS/Linux
- **Fallback:** Document platform-specific quirks in README

**Risk 3: Scope Creep (Adding HEX Mode, Export, etc.)**
- **Mitigation:** Strict adherence to PRD v1 scope
- **Process:** Defer all v2+ features to backlog (don't implement "while we're at it")

**Risk 4: PySerial Driver Compatibility Issues**
- **Mitigation:** Test with multiple USB-UART chips (CH340, CP2102, FTDI)
- **Documentation:** Clear driver installation instructions in README

## Task Breakdown Preview

When decomposed, this epic will generate tasks in these categories:

### 1. Setup & Infrastructure (3-4 tasks)
- [ ] Create uart_widget.py module structure
- [ ] Set up QThread and SerialWorker skeleton
- [ ] Add PySerial to requirements.txt and verify installation
- [ ] Create example firmware directory structure

### 2. UI Implementation (4-5 tasks)
- [ ] Implement connection controls panel (port/baud dropdowns, buttons)
- [ ] Implement data display panel (QTextEdit, auto-scroll, clear button)
- [ ] Implement command input panel (QLineEdit, Send button)
- [ ] Implement status indicator with color-coded states

### 3. Serial I/O Core (5-6 tasks)
- [ ] Implement port discovery (serial.tools.list_ports integration)
- [ ] Implement SerialWorker.connectPort() with error handling
- [ ] Implement SerialWorker.read_loop() with non-blocking reads
- [ ] Implement SerialWorker.sendData() for TX operations
- [ ] Implement SerialWorker.disconnectPort() with resource cleanup
- [ ] Wire up Signal/Slot connections between worker and UI

### 4. Buffer & Display Features (3-4 tasks)
- [ ] Implement capped message buffer (deque maxlen=1000)
- [ ] Implement MessageEntry data structure
- [ ] Implement auto-scroll functionality
- [ ] Implement optional timestamp display

### 5. Error Handling (3-4 tasks)
- [ ] Implement connection error handling (port not found, permission, etc.)
- [ ] Implement hot unplug detection and recovery
- [ ] Implement reconnect workflow
- [ ] Add error message display UI

### 6. Testing & Validation (5-6 tasks)
- [ ] Create echo_uart.ino example sketch
- [ ] Create ping_pong.ino example sketch
- [ ] Create stream_logger.ino example sketch
- [ ] Manual testing: Arduino/ESP32 at multiple baud rates
- [ ] Stress test: 60-second continuous streaming
- [ ] Cross-platform smoke test (Windows + macOS/Linux)

### 7. Integration & Documentation (2-3 tasks)
- [ ] Integrate UARTWidget into main window
- [ ] Create README section for UART feature (driver requirements, usage)
- [ ] Document example firmware usage and testing procedures

**Estimated Total Tasks:** 25-30 tasks

## Dependencies

### External Dependencies
- **PySerial Library:** Must be installed (`pip install pyserial`)
  - Version: Latest stable (3.5+)
  - Dependency added to requirements.txt during setup phase

### Internal Dependencies
- **basic-ui Feature (Soft Dependency):**
  - UART widget can be developed independently
  - Only needs main window skeleton for embedding (minimal coupling)
  - Can proceed in parallel; no blocking dependency

### Hardware Dependencies (For Testing)
- **Arduino Uno/Nano or ESP32:** For manual validation
- **USB-UART Dongles (Optional):** CH340, CP2102, FTDI for driver variation testing
- **User Responsibility:** USB-UART drivers must be pre-installed (documented in README)

### No Dependencies From Other Epics
- This is the only epic for uart-comport feature (single epic strategy)
- Self-contained implementation (no coordination needed)

## Success Criteria (Technical)

### Functional Requirements
- ✅ **Port Discovery:** Auto-detect and list all available COM ports
- ✅ **Connection Management:** Connect/Disconnect with correct state transitions
- ✅ **Data Reception:** Display incoming data in real-time without lag or garbled text
- ✅ **Data Transmission:** Send commands via GUI, see TX echo in output
- ✅ **Error Handling:** Graceful handling of hot unplug, connection errors, decode errors
- ✅ **Buffer Management:** Capped buffer prevents unbounded memory growth

### Performance Requirements
- ✅ **UI Responsiveness:** No freezing during continuous streaming (10-50 lines/sec)
- ✅ **CPU Efficiency:** Low idle CPU usage, no abnormal spikes
- ✅ **Data Rate Stability:** Support ≤ 115200 baud without data loss
- ✅ **Stress Test:** 60-second continuous streaming without errors

### Code Quality Standards
- ✅ **Thread Safety:** All UI updates via Signal/Slot (no direct worker→UI access)
- ✅ **Error Handling:** Try/except blocks for all serial operations
- ✅ **Code Documentation:** Docstrings for public methods, comments for threading logic
- ✅ **Modularity:** UARTWidget is reusable, self-contained component

### Testing Coverage
- ✅ **Manual Testing:** All scenarios from PRD success criteria validated
- ✅ **Hardware Testing:** Arduino/ESP32 at multiple baud rates (9600, 115200)
- ✅ **Example Firmware:** 3 sketches (echo, ping-pong, stream logger) working
- ✅ **Cross-Platform:** Windows validated, macOS/Linux smoke tested (if resources available)

### Documentation Completeness
- ✅ **Code Comments:** Threading, signal/slot, error handling well-documented
- ✅ **README Section:** Usage instructions, driver requirements, example firmware
- ✅ **Example Sketches:** Documented with upload/testing instructions

## Estimated Effort

**Timeline:** 1-2 weeks (10-15 hours total, solo development)

**Breakdown by Phase:**
- **Phase 1 (Infrastructure):** 4-5 hours
- **Phase 2 (Serial I/O):** 4-5 hours
- **Phase 3 (Buffer/Display):** 3-4 hours
- **Phase 4 (Error Handling):** 2-3 hours
- **Phase 5 (Testing):** 2-3 hours

**Critical Path:**
1. **SerialWorker thread safety** (Phase 2) → Core stability depends on this
2. **Buffer cap implementation** (Phase 3) → Prevents memory issues in production
3. **Hot unplug handling** (Phase 4) → Critical user experience requirement

**Resource Requirements:**
- 1 developer with Python/PyQt6 proficiency
- Arduino Uno/Nano or ESP32 for hardware testing
- Windows development environment (primary), macOS/Linux optional for smoke test

**Confidence Level:** High
- PySerial is mature and well-documented
- QThread + Signal/Slot is established PyQt6 pattern
- No novel algorithms or complex protocols (v1 is text-based)
- Clear scope prevents feature creep

## Tasks Created

### Phase 1: Setup & Infrastructure (Tasks 001-004)
- [ ] 001.md - Create uart_widget.py module structure (parallel)
- [ ] 002.md - Set up QThread and SerialWorker skeleton
- [ ] 003.md - Add PySerial to requirements and verify installation (parallel)
- [ ] 004.md - Create example firmware directory structure (parallel)

### Phase 2: UI Implementation (Tasks 005-008)
- [ ] 005.md - Implement connection controls panel
- [ ] 006.md - Implement data display panel (UI)
- [ ] 007.md - Implement command input panel (UI)
- [ ] 008.md - Implement status indicator with color states

### Phase 3: Serial I/O Core (Tasks 009-014)
- [ ] 009.md - Implement port discovery integration
- [ ] 010.md - Implement SerialWorker.connectPort() with error handling
- [ ] 011.md - Implement SerialWorker.read_loop() with non-blocking reads
- [ ] 012.md - Implement SerialWorker.sendData() for TX operations
- [ ] 013.md - Implement SerialWorker.disconnectPort() with resource cleanup
- [ ] 014.md - Wire up Signal/Slot connections between worker and UI

### Phase 4: Buffer & Display Features (Tasks 015-017)
- [ ] 015.md - Implement capped message buffer (deque) (parallel)
- [ ] 016.md - Implement auto-scroll functionality
- [ ] 017.md - Implement optional timestamp display

### Phase 5: Error Handling (Tasks 018-021)
- [ ] 018.md - Implement connection error handling
- [ ] 019.md - Implement hot unplug detection and recovery
- [ ] 020.md - Implement reconnect workflow
- [ ] 021.md - Add error message display UI

### Phase 6: Testing & Example Firmware (Tasks 022-026)
- [ ] 022.md - Create echo_uart.ino example sketch (parallel)
- [ ] 023.md - Create ping_pong.ino example sketch (parallel)
- [ ] 024.md - Create stream_logger.ino example sketch (parallel)
- [ ] 025.md - Manual hardware testing (Arduino/ESP32)
- [ ] 026.md - Stress test - 60-second continuous streaming

### Phase 7: Integration (Task 027)
- [ ] 027.md - Integrate UARTWidget into main window

**Total tasks:** 27
**Parallel tasks:** 6 (001, 003, 004, 015, 022, 023, 024)
**Sequential tasks:** 21
**Estimated total effort:** 28 hours (approximately 1.5-2 weeks for solo developer)
