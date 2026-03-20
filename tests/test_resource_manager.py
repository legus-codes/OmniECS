from dataclasses import dataclass

from omniecs.managers import ResourceManager
from omniecs.types import Resource


class ResourceA(Resource): ...


@dataclass
class ResourceB(Resource):
    value: str


def test_set_resource():
    resource_manager = ResourceManager()
    resource_manager.set(ResourceA())
    resource = resource_manager.get(ResourceA)
    assert isinstance(resource, ResourceA)


def test_overwrite_resource():
    resource_manager = ResourceManager()
    resource_manager.set(ResourceB('old'))
    resource_manager.set(ResourceB('new'))
    resource = resource_manager.get(ResourceB)
    assert resource.value == 'new'


def test_remove_resource():
    resource_manager = ResourceManager()
    resource_manager.set(ResourceA())
    resource_manager.remove(ResourceA)
    resource = resource_manager.get(ResourceA)
    assert resource is None
