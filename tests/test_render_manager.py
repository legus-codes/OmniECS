from dataclasses import dataclass

from omniecs.managers import RenderManager
from omniecs.types import DrawCommand



@dataclass(kw_only=True)
class MockDrawCommand(DrawCommand):
    text: str


def test_create_command():
    render_manager = RenderManager()
    render_manager.push(MockDrawCommand(global_layer=1, text=''))
    assert len(render_manager._queue) == 1

    
def test_get_commands():
    render_manager = RenderManager()
    render_manager.push(MockDrawCommand(global_layer=3, text='third'))
    render_manager.push(MockDrawCommand(global_layer=1, text='first'))
    render_manager.push(MockDrawCommand(global_layer=2, text='second'))
    commands = render_manager.get()
    assert len(commands) == 3
    assert commands[0].text == 'first'
    assert commands[1].text == 'second'
    assert commands[2].text == 'third'
    assert len(render_manager._queue) == 3

    
def test_clear_commands():
    render_manager = RenderManager()
    render_manager.push(MockDrawCommand(global_layer=3, text='third'))
    render_manager.push(MockDrawCommand(global_layer=1, text='first'))
    render_manager.push(MockDrawCommand(global_layer=2, text='second'))
    render_manager.clear()
    assert len(render_manager._queue) == 0
