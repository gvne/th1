import datetime
import enum
import pydantic


class Coordinates(pydantic.BaseModel):
    latitude: float
    longitude: float
    administrativeAreaId: str
    countryName: str
    countryCode: str


class Firmware(pydantic.BaseModel):
    id: int
    version: str
    weightingVersion: int
    filename: str
    creationDate: datetime.datetime
    deletionDate: datetime.datetime | None
    deletionDescription: str | None
    deletionUser: str | None
    isDefault: bool
    isDeleted: bool
    fsPresence: bool


class Thermostat(pydantic.BaseModel):
    class Type(pydantic.BaseModel):
        typeId: int
        typeLabel: str

    class SubType(pydantic.BaseModel):
        subtypeId: int
        subtypeLabel: str

    class Partner(pydantic.BaseModel):
        partner_id: int
        partner_label: str

    class Gateway(pydantic.BaseModel):
        gateway_id: int
        mac_address: str
        firmware: Firmware
        associated_product_serial: str
        handle_automatic_update: bool

    class Reversibility(pydantic.BaseModel):
        available: bool
        functioning_mode: str
        cooling_humidity_threshold: float
        cooling_alarm_triggered: bool

    id: str
    name: str
    location: Coordinates
    firmware: Firmware
    description: str | None
    timeZone: str
    type: Type
    partner: Partner
    gateway: Gateway
    subtype: SubType
    regulation_type: str
    hysteresis_threshold: float
    firmware_version: str
    sunrise_offset: int
    sunset_offset: int
    temperature_type: str
    suddendrop_activation: bool
    activation_status: str
    io_slim_presence: str | None
    relays: str | None
    first_connection: datetime.datetime | None
    timestamp_first_connection: float | None
    last_connection: datetime.datetime
    timestamp_last_connection: float | None
    mac_address: str
    user_access_level: int
    handle_automatic_update: bool
    battery: float
    functioning_mode: str | None
    cooling_humidity_threshold: float | None
    cooling_alarm_triggered: bool | None
    reversibility: Reversibility
    summer_protection: bool


class Response(pydantic.BaseModel):
    results: list[Thermostat]


class Mode(enum.Enum):
    sleep = "sleep"
    at_home = "at_home"
    sudden_drop = "sudden_drop"
    away = "away"
    freeze = "freeze"
    geofencing = "geofencing"


class ModeSettings(pydantic.BaseModel):
    sleep: float
    at_home: float
    sudden_drop: float
    away: float
    freeze: float
    geofencing: float
    manual: float | None
    nb_hours_away_to_freeze_derogation: float


class Schedule(pydantic.BaseModel):
    class Step(pydantic.BaseModel):
        time: datetime.time
        type: Mode

    monday: list[Step]
    tuesday: list[Step]
    wednesday: list[Step]
    thursday: list[Step]
    friday: list[Step]
    saturday: list[Step]
    sunday: list[Step]
    program_name: str | None
    active: bool


class GeofencingDeltas(pydantic.BaseModel):
    temperature_delta_zone_1: int
    temperature_delta_zone_2: int
    temperature_delta_zone_3: int
    temperature_delta_zone_4: int


class GeofencingDistance(pydantic.BaseModel):
    geofencing_distance_zone_1: int
    geofencing_distance_zone_2: int
    geofencing_distance_zone_3: int
    geofencing_distance_zone_4: int


class Derogation(pydantic.BaseModel):
    finish_at: datetime.datetime
    heating_mode: str
    temperature: float
    derogation_type: str
    started_at: datetime.datetime


class Info(pydantic.BaseModel):
    date: datetime.datetime
    autilCoefficient: float
    temperature_consigne: float
    schedules_dhw: list[Schedule]
    mode_dhw: str
    regulation_dhw: str
    latest_derogation_dhw: datetime.datetime | None
    geofencing_deltas: GeofencingDeltas
    latest_derogation: Derogation | None
    battery: float
    result: str
    mode: str
    regulation: str
    butilCoefficient: float
    schedules: list[Schedule]
    temperature: float
    mode_settings: ModeSettings
    geofencing_distance: GeofencingDistance
    messages: list[str]
    humidity: float
    externalCoefficient: float
    internalCoefficient: float
