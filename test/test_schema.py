import logging

import th1.client.schema.auth as auth
import th1.client.schema.thermostat as ts
import th1.client.schema.smartphone as ss


def test_auth():
    response = {
        "access_token": "dummy_access",
        "expires_in": 3600,
        "token_type": "bearer",
        "scope": "user.basic api.full oa.site oa.subscription oa.user oa.device oa.devicedefinition level.0",
        "refresh_token": "dummy_refresh",
        "legal_fault": False,
    }

    auth.Response.model_validate(response)


def test_thermostat():
    response = {
        "results": [
            {
                "id": "123567890123",
                "name": "Thermostat Connecté",
                "location": {
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "administrativeAreaId": "75",
                    "countryName": "France",
                    "countryCode": "FR",
                },
                "firmware": {
                    "id": 57,
                    "version": "3980v2.8",
                    "weightingVersion": 2008,
                    "filename": "3980v2.8_PROD.duf",
                    "creationDate": "2021-07-02T08:29:19Z",
                    "deletionDate": None,
                    "deletionDescription": None,
                    "deletionUser": None,
                    "isDefault": True,
                    "isDeleted": False,
                    "fsPresence": True,
                },
                "description": None,
                "timeZone": "Europe/Paris",
                "type": {"typeId": 1, "typeLabel": "THERMOSTAT_WIRED"},
                "partner": {"partner_id": 1, "partner_label": "somfy_fr"},
                "gateway": {
                    "gateway_id": 12345,
                    "mac_address": "AABB112233FF",
                    "firmware": {
                        "id": 39,
                        "version": "4101v1.27/4193v0.8",
                        "weightingVersion": 1027000008,
                        "filename": "4101v1.27_4193v0.8_PROD.duf",
                        "creationDate": "2020-07-07T14:44:17Z",
                        "deletionDate": None,
                        "deletionDescription": None,
                        "deletionUser": None,
                        "isDefault": True,
                        "isDeleted": False,
                        "fsPresence": True,
                    },
                    "associated_product_serial": "123567890123",
                    "handle_automatic_update": True,
                },
                "subtype": {"subtypeId": 2, "subtypeLabel": "SOMFY - MULTI_ENERGY"},
                "regulation_type": "Hysteresis",
                "hysteresis_threshold": 0.1,
                "firmware_version": "3980v2.8",
                "sunrise_offset": 0,
                "sunset_offset": 0,
                "temperature_type": "Real",
                "suddendrop_activation": True,
                "activation_status": "Activated",
                "io_slim_presence": None,
                "relays": None,
                "first_connection": None,
                "timestamp_first_connection": None,
                "last_connection": "2023-12-01T15:20:45+0000",
                "timestamp_last_connection": 1701444045,
                "mac_address": "AABB112233FF",
                "user_access_level": 0,
                "handle_automatic_update": True,
                "battery": 37.0,
                "functioning_mode": None,
                "cooling_humidity_threshold": None,
                "cooling_alarm_triggered": None,
                "reversibility": {
                    "available": False,
                    "functioning_mode": "he",
                    "cooling_humidity_threshold": 80.0,
                    "cooling_alarm_triggered": False,
                },
                "summer_protection": True,
            }
        ]
    }
    ts.Response.model_validate(response)


def test_smartphone():
    response = [
        {
            "name": "iPhone",
            "vendor_id": "dummy_vendor_id",
            "phone_type": 1,
            "push_token": "dummy_token",
        },
        {
            "name": "Pixel 4",
            "vendor_id": "dummy_vendor_id",
            "phone_type": 0,
            "push_token": "dummy_token",
        },
    ]
    [ss.Smartphone.model_validate(s) for s in response]


def test_thermostat_info():
    response = {
        "date": 1701444645,
        "autilCoefficient": 0.94,
        "temperature_consigne": 16,
        "schedules_dhw": [
            {
                "sunday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "saturday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "tuesday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "program_name": None,
                "active": True,
                "wednesday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "thursday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "friday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "programming_number": 1,
                "monday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
            },
            {
                "sunday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "saturday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "tuesday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "program_name": None,
                "active": False,
                "wednesday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "thursday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "friday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
                "programming_number": 2,
                "monday": [
                    {"time": "00:00", "type": "at_home"},
                    {"time": "06:00", "type": "away"},
                ],
            },
        ],
        "mode_dhw": "away",
        "regulation_dhw": "Timetable",
        "latest_derogation_dhw": None,
        "geofencing_deltas": {
            "temperature_delta_zone_1": 0,
            "temperature_delta_zone_2": 1,
            "temperature_delta_zone_3": 1,
            "temperature_delta_zone_4": 1,
        },
        "latest_derogation": {
            "finish_at": 1701364500,
            "heating_mode": "at_home",
            "temperature": 18.5,
            "derogation_type": "next_mode",
            "started_at": 1701354383,
        },
        "battery": 37,
        "result": "0",
        "mode": "away",
        "regulation": "Timetable",
        "butilCoefficient": 1.01,
        "schedules": [
            {
                "sunday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:00", "type": "sleep"},
                ],
                "saturday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
                "tuesday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "06:45", "type": "at_home"},
                    {"time": "08:00", "type": "away"},
                    {"time": "18:15", "type": "at_home"},
                    {"time": "22:00", "type": "sleep"},
                ],
                "program_name": None,
                "active": True,
                "wednesday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "06:45", "type": "at_home"},
                    {"time": "22:00", "type": "sleep"},
                ],
                "thursday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "06:45", "type": "at_home"},
                    {"time": "08:00", "type": "away"},
                    {"time": "18:15", "type": "at_home"},
                    {"time": "22:00", "type": "sleep"},
                ],
                "friday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "06:45", "type": "at_home"},
                    {"time": "08:00", "type": "away"},
                    {"time": "18:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
                "programming_number": 1,
                "monday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "06:45", "type": "at_home"},
                    {"time": "08:00", "type": "away"},
                    {"time": "18:15", "type": "at_home"},
                    {"time": "22:00", "type": "sleep"},
                ],
            },
            {
                "sunday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
                "saturday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
                "tuesday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
                "program_name": None,
                "active": False,
                "wednesday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
                "thursday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
                "friday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
                "programming_number": 2,
                "monday": [
                    {"time": "00:00", "type": "sleep"},
                    {"time": "07:15", "type": "at_home"},
                    {"time": "22:30", "type": "sleep"},
                ],
            },
        ],
        "temperature": 15.9,
        "mode_settings": {
            "sleep": 17,
            "at_home": 18.5,
            "sudden_drop": 16,
            "away": 16,
            "freeze": 8,
            "nb_hours_away_to_freeze_derogation": 48,
            "manual": None,
            "geofencing": 18.5,
        },
        "geofencing_distance": {
            "geofencing_distance_zone_1": 0,
            "geofencing_distance_zone_2": 2,
            "geofencing_distance_zone_3": 10,
            "geofencing_distance_zone_4": 40,
        },
        "messages": [],
        "humidity": 54.9,
        "externalCoefficient": -0.09,
        "internalCoefficient": 0.97,
    }

    data = ts.Info.model_validate(response)
    logging.info(data)
