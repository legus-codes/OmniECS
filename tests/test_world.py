from omniecs.managers import ComponentManager, EntityManager, EventManager, RenderManager, ResourceManager, SystemManager
from omniecs.system import System
from omniecs.types import Component, DrawCommand, Event, Resource
from omniecs.world import WorldFactory


class MockComponentA(Component): ...
class MockComponentB(Component): ...
class MockComponentC(Component): ...

class MockSystem(System):
    executed: bool = False
    def execute(self, delta_time: float) -> None:
        self.executed = True

class MockResource(Resource): ...

class MockEvent(Event): ...

class MockDrawCommand(DrawCommand): ...

def test_world_has_all_managers():
    world = WorldFactory.create_world()
    assert isinstance(world._entities, EntityManager)
    assert isinstance(world._components, ComponentManager)
    assert isinstance(world._systems, SystemManager)
    assert len(list(world._systems.all_systems)) == 3
    assert isinstance(world._resources, ResourceManager)
    assert isinstance(world._events, EventManager)
    assert isinstance(world._render, RenderManager)

def test_spawn_entity():
    world = WorldFactory.create_world()
    componentA = MockComponentA()
    componentB = MockComponentB()
    entity_id = world.spawn(componentA, componentB)

    entities = list(world.query(MockComponentA, MockComponentB))
    assert len(entities) == 1
    entity, (compA, compB) = entities[0]
    assert entity == entity_id
    assert compA == componentA
    assert compB == componentB

def test_destroy_entity():
    world = WorldFactory.create_world()
    componentA = MockComponentA()
    componentB = MockComponentB()
    entity_id = world.spawn(componentA, componentB)
    world.destroy(entity_id)

    assert world.query_entities(any_of=(MockComponentA, MockComponentB)) == set()

def test_add_component():
    world = WorldFactory.create_world()
    componentC = MockComponentC()
    entity_id = world.spawn(MockComponentA(), MockComponentB())
    world.add_component(entity_id, componentC)

    entities = list(world.query(MockComponentC))
    assert len(entities) == 1
    entity, (compC,) = entities[0]
    assert entity == entity_id
    assert compC == componentC

def test_remove_component():
    world = WorldFactory.create_world()
    entity_id = world.spawn(MockComponentA(), MockComponentB())
    world.remove_component(entity_id, MockComponentA)

    assert world.query_entities(all_of=(MockComponentA,)) == set()

def test_register_temporary_component():
    world = WorldFactory.create_world()
    world.register_temporary_component(MockComponentA)
    world.spawn(MockComponentA())
    world.spawn(MockComponentA())
    world.spawn(MockComponentA())
    world.execute(0)

    assert world.query_entities(all_of=(MockComponentA,)) == set()

def test_execute_system():
    world = WorldFactory.create_world()
    system = MockSystem()
    world.register_system(system)
    assert not system.executed

    world.execute(0)
    assert system.executed

def test_execute_unregistered_system():
    world = WorldFactory.create_world()
    system = MockSystem()
    world.register_system(system)
    assert not system.executed

    world.unregister_system(MockSystem)
    world.execute(0)
    assert not system.executed

def test_set_resource():
    world = WorldFactory.create_world()
    resource = MockResource()
    world.set_resource(resource)

    assert world.get_resource(MockResource) == resource

def test_overwrite_resource():
    world = WorldFactory.create_world()
    resource = MockResource()
    world.set_resource(MockResource())
    world.set_resource(resource)

    assert world.get_resource(MockResource) == resource

def test_push_events():
    world = WorldFactory.create_world()
    event = MockEvent()
    world.push_event(event)
    world.push_event(event)
    world.push_event(event)

    assert world.get_events() == [event, event, event]
    assert world.get_events() == [event, event, event]

def test_add_draw_commands():
    world = WorldFactory.create_world()
    draw_command = MockDrawCommand(global_layer=1)
    world.add_draw_command(draw_command)
    world.add_draw_command(draw_command)
    world.add_draw_command(draw_command)

    assert world.get_draw_commands() == [draw_command, draw_command, draw_command]
    assert world.get_draw_commands() == [draw_command, draw_command, draw_command]

