# GitHub Issue Mapping

Epic: #8 - https://github.com/junyoulin641/CCPM/issues/8

## Tasks (27 total)

### Phase 1: Setup & Infrastructure
- #9: Create uart_widget.py module structure
- #10: Set up QThread and SerialWorker skeleton
- #11: Add PySerial to requirements and verify installation
- #12: Create example firmware directory structure

### Phase 2: UI Implementation
- #13: Implement connection controls panel
- #14: Implement data display panel (UI)
- #15: Implement command input panel (UI)
- #16: Implement status indicator with color states

### Phase 3: Serial I/O Core
- #17: Implement port discovery integration
- #18: Implement SerialWorker.connectPort() with error handling
- #19: Implement SerialWorker.read_loop() with non-blocking reads
- #20: Implement SerialWorker.sendData() for TX operations
- #21: Implement SerialWorker.disconnectPort() with resource cleanup
- #22: Wire up Signal/Slot connections between worker and UI

### Phase 4: Buffer & Display Features
- #23: Implement capped message buffer (deque)
- #24: Implement auto-scroll functionality
- #25: Implement optional timestamp display

### Phase 5: Error Handling
- #26: Implement connection error handling
- #27: Implement hot unplug detection and recovery
- #28: Implement reconnect workflow
- #29: Add error message display UI

### Phase 6: Testing & Example Firmware
- #30: Create echo_uart.ino example sketch
- #31: Create ping_pong.ino example sketch
- #32: Create stream_logger.ino example sketch
- #33: Manual hardware testing (Arduino/ESP32)
- #34: Stress test - 60-second continuous streaming

### Phase 7: Integration
- #35: Integrate UARTWidget into main window

---

**Synced:** 2025-12-24T08:22:46Z

**Labels Applied:**
- `epic`: Applied to epic issue #8
- `task`: Applied to all task issues #9-#35
- `feature:uart-comport`: Applied to all issues
- `epic:epic-uart-widget`: Applied to all issues

**Relationship Type:** Parent-child (using gh-sub-issue extension)
