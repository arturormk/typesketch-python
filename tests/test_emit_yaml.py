from typesketch.emit_yaml import emit_yaml

def test_emit_simple():
    shape = {'item': {'id': 'int', 'name': 'string'}}
    yml = emit_yaml(shape)
    assert "item:" in yml
    assert "id: int" in yml
    assert "name: string" in yml
