Feature: Patient Vital Signs Monitoring Interface

  Scenario: Trigger critical heart rate alert
    Given the bedside patient monitor is initialized and active
    When the heart rate sensor reads a value of 145 beats per minute
    Then a high-priority audible and visual warning alarm must activate

  Scenario: Silence temporary monitor alarm
    Given a high-priority warning alarm is currently active on screen
    When the attending nurse presses the physical audio pause button
    Then the system audio indicators should mute cleanly for 120 seconds

  Scenario: Log incoming blood pressure reading
    Given a patient profile is actively loaded into the terminal unit
    When the telemetry cuff completes a non-invasive cycling measurement
    Then the exact systolic and diastolic parameters must sync to the chart

  Scenario: Detect network infrastructure loss
    Given the terminal is broadcasting data metrics to the central station
    When the local area network interface link suddenly drops offline
    Then a distinct amber technical alert icon must flash continuously

  Scenario: Switch over to backup battery power
    Given the patient vital station is connected to alternating current grid power
    When the primary local facility electrical infrastructure goes down completely
    Then the internal emergency lithium reserve cells must engage without data loss
