import stix2
from stix2.base import STIXJSONEncoder
from stix.models import IdentityType
from dashboard.models import SnortDetails
import json


class StixBase:
    def __init__(self, key):
        self.identity = IdentityType.objects.all().first()
        self.key = key
        self.data = None

    def get_identity_data(self):
        identity = stix2.Identity(
            name=self.identity.name,
            description=self.identity.description,
            identity_class=self.identity.identity_class,
            contact_information=self.identity.contact_information,
            labels=self.identity.label,
            sectors=self.identity.sectors
        )
        return identity

    def get_course_of_action(self):
        course_of_action = stix2.CourseOfAction(
            name=self.data.sig.course_of_action.name,
            description=self.data.sig.course_of_action.description,
            external_references=[{"source_name": self.identity.name, "url": self.data.sig.course_of_action.action}]
        )
        return course_of_action

    def get_attack_pattern_data(self):
        attack_pattern = stix2.AttackPattern(
            name=self.data.sig.attack_pattern_type.name,
            description=self.data.sig.attack_pattern_type.description,
            external_references=None
        )
        return attack_pattern

    def get_threat_actor(self):
        description = "Country Attacking Honeypot"
        label = [
            {
                "ip": self.data.src,
                "port": self.data.srcport,
                "longitude": self.data.src_longitude,
                "latitude": self.data.src_latitude
            }
        ]
        threat_actor = stix2.ThreatActor(
            name=self.data.src_country,
            description=description,
            labels=label
        )
        return threat_actor

    def get_observed_data(self, identity_id):
        first_observed = last_observed = self.data.timestamp
        number_observed = 1
        objects = {
            "0": {
                "type": "ipv4-addr",
                "value": self.data.src
            },
            "1": {
                "type": "ipv4-addr",
                "value": self.data.dst
            },
            "2": {
                "type": "network-traffic",
                "src_ref": "0",
                "src_port": self.data.srcport if self.data.srcport else 0,
                "dst_ref": "1",
                "dst_port": self.data.dstport if self.data.dstport else 0,
                "protocols": [
                    self.data.proto
                ],
                "start": self.data.timestamp
            }
        }
        observed_data_file = stix2.ObservedData(
            first_observed=first_observed,
            last_observed=last_observed,
            number_observed=number_observed,
            created_by_ref=identity_id,
            objects=objects,
        )
        return observed_data_file

    @staticmethod
    def create_relationship(id1, id2, relation_type):
        relationship = stix2.Relationship(id1, relation_type, id2)
        return relationship

    def attack_pattern(self):
        self.data = SnortDetails.objects.get_attack_details(self.key)
        object_list = []
        if self.data:
            identity_data = self.get_identity_data()
            attack_pattern_data = self.get_attack_pattern_data()
            if self.data.src_country:
                threat_actor = self.get_threat_actor()
                object_list.append(threat_actor)
                object_list.append(self.create_relationship(threat_actor, attack_pattern_data, "uses"))
                object_list.append(self.create_relationship(threat_actor, identity_data, "attributed-to"))
            else:
                object_list.append(self.create_relationship(attack_pattern_data, identity_data, "attributed-to"))

            object_list.append(attack_pattern_data)
            object_list.append(identity_data)
            object_list.append(self.get_observed_data(identity_data))

            if self.data.sig.course_of_action:
                course_of_action_data = self.get_course_of_action()
                object_list.append(course_of_action_data)
                object_list.append(self.create_relationship(course_of_action_data, attack_pattern_data, "mitigates"))

            bundle = stix2.Bundle(objects=object_list)
        else:
            bundle = {}
        return json.dumps(bundle, cls=STIXJSONEncoder)
