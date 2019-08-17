from typing import Dict, Any, Optional

import dateutil.parser
import pytz
import jsonschema

from . import Loader, LoaderError
from core.models import Revision, ScopusSnapshot, GoogleScholarSnapshot, SemanticScholarSnapshot, WosSnapshot, Person


_JSON_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'properties': {
        'created_at': {
            'type': 'string',
            'format': 'date-time'
        },
        'scopus': {
            'type': 'object',
            'minProperties': 1,
            'propertyNames': {
                'pattern': r'^[a-zA-Z_\-0-9]+$'
            },
            'patternProperties': {
                '': {
                    'type': 'object',
                    'properties': {
                        'h_index': {
                            'type': 'integer',
                            'minimum': 0
                        },
                        'citations': {
                            'type': 'integer',
                            'minimum': 0
                        },
                        'documents': {
                            'type': 'integer',
                            'minimum': 0
                        }
                    },
                    'required': ['h_index', 'citations', 'documents']
                }
            }
        },
        'google_scholar': {
            'type': 'object',
            'minProperties': 1,
            'propertyNames': {
                'pattern': r'^[a-zA-Z_\-0-9]+$'
            },
            'patternProperties': {
                '': {
                    'type': 'object',
                    'properties': {
                        'h_index': {
                            'type': 'integer',
                            'minimum': 0
                        },
                        'citations': {
                            'type': 'integer',
                            'minimum': 0
                        }
                    },
                    'required': ['h_index', 'citations']
                }
            }
        },
        'semantic_scholar': {
            'type': 'object',
            'minProperties': 1,
            'propertyNames': {
                'pattern': r'^[a-zA-Z_\-0-9]+$'
            },
            'patternProperties': {
                '': {
                    'type': 'object',
                    'properties': {
                        'citation_velocity': {
                            'type': 'integer',
                            'minimum': 0
                        },
                        'influential_citation_count': {
                            'type': 'integer',
                            'minimum': 0
                        },
                    },
                    'required': ['citation_velocity', 'influential_citation_count']
                }
            }
        },
        'wos': {
            'type': 'object',
            'minProperties': 1,
            'propertyNames': {
                'pattern': r'^[a-zA-Z_\-0-9]+$'
            },
            'patternProperties': {
                '': {
                    'type': 'object',
                    'properties': {
                        'publications': {
                            'type': 'integer',
                            'minimum': 0
                        },
                    },
                    'required': ['publications']
                }
            }
        }
    }
}


class RevisionLoader(Loader):

    def __init__(self, data: Dict[str, Any], *, revision_source: Optional[str] = None, chuck_size:  int = 100):
        self.data = data
        self.revision_source = revision_source
        self.chunk_size = chuck_size

    @property
    def revision_source(self) -> str:
        return self._revision_source

    @revision_source.setter
    def revision_source(self, source: str):
        if source and source not in (Revision.SOURCE_IMPORT,):
            raise ValueError(f'{repr(source)} revision source is not allowed')
        self._revision_source = source or ''

    @property
    def data(self) -> Dict[str, Any]:
        return self._data

    @data.setter
    def data(self, data: Dict[str, Any]):
        try:
            jsonschema.validate(data, _JSON_SCHEMA)
            self._data = data

        except jsonschema.ValidationError as e:
            raise LoaderError from e

    def load(self):
        revision = Revision.objects.create(source=self.revision_source)

        if 'created_at' in self.data:
            created_at = dateutil.parser.parse(self.data['created_at']).astimezone(pytz.utc)
            revision.created_at = created_at
            revision.save()

        conf = (
            ('scopus', 'scopus_key', ScopusSnapshot),
            ('google_scholar', 'google_scholar_key', GoogleScholarSnapshot),
            ('semantic_scholar', 'semantic_scholar_key', SemanticScholarSnapshot),
            ('wos', 'wos_key', WosSnapshot),
        )

        for prop, lookup, model in conf:

            chunk = []

            for key, snapshot in self.data.get(prop, {}).items():
                key = key.strip()

                if not key:
                    continue

                person = Person.objects.filter(**{lookup: key}).first()

                if person is None:
                    continue

                chunk.append(model(person=person, revision=revision, **snapshot))

                if len(chunk) == self.chunk_size:
                    model.objects.bulk_create(chunk)
                    chunk.clear()

            if len(chunk) != 0:
                model.objects.bulk_create(chunk)

        return revision
