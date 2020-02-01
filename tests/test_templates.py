from jinja2 import Environment, DictLoader

from carnival import templates


def test_render(mocker):
    mocker.patch(
        'carnival.templates.j2_env',
        new=Environment(loader=DictLoader({"index.html": "Hello: {{ name }}"})),
    )
    rendered = templates.render("index.html", name="world")
    assert rendered == "Hello: world"
