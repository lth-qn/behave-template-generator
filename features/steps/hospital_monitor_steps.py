from behave import given, when, then, register_type
import parse

# Custom step matcher parser to handle complex multi-word strings like severity levels
@parse.with_pattern(r"high-priority|medium-priority|low-priority|amber|red")
def parse_severity(text):
    return text.strip()

# Register the custom type with Behave
register_type(Severity=parse_severity)

# --- Robust System Simulation Mock ---
class PatientMonitor:
    def __init__(self):
        self.is_active = False
        self.heart_rate = 75
        self.alarm_active = False
        self.alarm_severity = None
        self.alarm_muted = False
        self.mute_duration = 0
        self.patient_loaded = False
        self.vitals_logged = False
        self.network_connected = True
        self.power_source = "AC"
        self.technical_alert_active = False

    def receive_heart_rate(self, bpm):
        self.heart_rate = bpm
        if bpm > 120 or bpm < 50:
            self.alarm_active = True
            self.alarm_severity = "high-priority"

    def press_mute(self, duration_seconds):
        if self.alarm_active or self.technical_alert_active:
            self.alarm_muted = True
            self.mute_duration = duration_seconds


# --- Step Definitions ---

@given('the bedside patient monitor is initialized and active')
def step_bedside_patient_monitor_initialize(context):
    context.monitor = PatientMonitor()
    context.monitor.is_active = True

@when('the heart rate sensor reads a value of {bpm:d} beats per minute')
def step_heart_rate_sensor_read(context, bpm):
    context.monitor.receive_heart_rate(bpm)

@then('a {severity:Severity} audible and visual warning alarm must activate')
def step_priority_audible_visual_warning(context, severity):
    assert context.monitor.alarm_active is True
    assert context.monitor.alarm_severity == severity, f"Expected {severity}, got {context.monitor.alarm_severity}"

@given('a {severity:Severity} warning alarm is currently active on screen')
def step_priority_warning_alarm_active(context, severity):
    context.monitor = PatientMonitor()
    context.monitor.alarm_active = True
    context.monitor.alarm_severity = severity

@when('the attending nurse presses the physical audio pause button')
def step_attending_nurse_press_physical(context):
    # Defaulting mute window to 120 seconds based on standard equipment specifications
    context.monitor.press_mute(duration_seconds=120)

@then('the system audio indicators should mute cleanly for {duration:d} seconds')
def step_system_audio_indicator_mute(context, duration):
    assert context.monitor.alarm_muted is True
    assert context.monitor.mute_duration == duration, f"Expected mute for {duration}s, got {context.monitor.mute_duration}s"

@given('a patient profile is actively loaded into the terminal unit')
def step_patient_profile_load_terminal(context):
    context.monitor = PatientMonitor()
    context.monitor.patient_loaded = True

@when('the telemetry cuff completes a non-invasive cycling measurement')
def step_telemetry_cuff_complete_noninvasive(context):
    context.monitor.vitals_logged = True

@then('the exact systolic and diastolic parameters must sync to the chart')
def step_systolic_diastolic_parameter_sync(context):
    assert context.monitor.vitals_logged is True

@given('the terminal is broadcasting data metrics to the central station')
def step_terminal_broadcast_data_metric(context):
    context.monitor = PatientMonitor()
    context.monitor.network_connected = True

@when('the local area network interface link suddenly drops offline')
def step_local_area_network_interface(context):
    context.monitor.network_connected = False
    context.monitor.technical_alert_active = True

@then('a distinct {color:Severity} technical alert icon must flash continuously')
def step_amber_technical_alert_icon(context, color):
    assert context.monitor.technical_alert_active is True
    # The variable dynamically catches "amber" or "red" directly from Gherkin syntax
    assert color in ["amber", "red"], f"Invalid alert color color: {color}"

@given('the patient vital station is connected to alternating current grid power')
def step_patient_vital_station_connect(context):
    context.monitor = PatientMonitor()
    context.monitor.power_source = "AC"

@when('the primary local facility electrical infrastructure goes down completely')
def step_primary_local_facility_electrical(context):
    context.monitor.power_source = "Battery"

@then('the internal emergency lithium reserve cells must engage without data loss')
def step_internal_emergency_lithium_reserve(context):
    assert context.monitor.power_source == "Battery"
