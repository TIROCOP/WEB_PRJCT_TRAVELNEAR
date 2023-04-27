import folium
from branca.element import MacroElement
from flask import Flask, url_for, render_template, json, request
from htmlmerger import HtmlMerger
import codecs
import dash
from jinja2 import Template


class LatLngPopup(MacroElement):
    """
    When one clicks on a Map that contains a LatLngPopup,
    a popup is shown that displays the latitude and longitude of the pointer.

    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                data = e.latlng.lat.toFixed(4) + "," + e.latlng.lng.toFixed(4);
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent( "<br /><a href="+data+"> click </a>")
                        .openOn({{this._parent.get_name()}})
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);

            {% endmacro %}
            """)  # noqa

    def __init__(self):
        super(LatLngPopup, self).__init__()
        self._name = 'LatLngPopup'


sp = [[55.689179, 37.772682],
      [55.690211, 37.784942],
      [55.687925, 37.801329],
      [55.687321, 37.804719],
      [55.681030, 37.817131],
      [55.680892, 37.823656],
      [55.681641, 37.828270],
      [55.670039, 37.827013],
      [55.662859, 37.809713]]

lit = []
#
app = Flask(__name__)


# код кнопок главной страницы

@app.route('/')  # первое что видишь (должно быть (войти, искать путь, создать свой;не работает;))
def main():
    return render_template('main.html', Title='Гость')


@app.route('/status/<title>')
def firstpage(title):  # первая страница страница (создай свой путь ;работает;)
    return render_template('main.html', Title=title)


@app.route('/find')
def find():  # поиск пути по критериям

    return render_template('finder.html')


@app.route('/get-cl', methods=['GET', 'POST'])
def avtorization():  # авторизация ну тут всё понятно не обязательно
    email = request.input_stream['email']
    print(email)


# код карты

@app.route('/open_map')
def open_map():
    map = folium.Map(position='relative', left='35%', width='100%', height='100%', align='right',
                     location=[55.689179, 37.772682], zoom_start=12)
    folium.PolyLine(sp,
                    color='gray',
                    weight=5,
                    opacity=0.8).add_to(map)
    for k in sp:
        folium.Marker(
            k, popup=f"<i>0_0</i>"
        ).add_to(map)
    f = codecs.open("templates/copybase.html", 'r', encoding='UTF-8')
    map.get_root().html.add_child(folium.Element(f.read()))
    map.save('templates/map.html')
    return render_template('map.html')


def update():
    global d
    d = []


d = []


@app.route('/make_map/<kords>')
def make_map(kords):
    if kords == '55.8006,37.6684':
        update()
    map1 = folium.Map(location=[55.7522, 37.6156], left='30%', zoom_start=12)
    pop = LatLngPopup()
    map1.add_child(pop)
    pop_lis = [float(i) for i in kords.split(',')]
    d.append(pop_lis)
    print(d)
    for k in d:
        print(tuple(k))
        folium.Marker(
            tuple(k), popup=f"<i>0_0</i>"
        ).add_to(map1)
    if len(d) > 1:
        folium.PolyLine(d,
                        color='gray',
                        weight=5,
                        opacity=0.8).add_to(map1)
    map1.get_root().html.add_child(folium.Element('''
    <div class="form-floating mb-3">
        <input type="text" class="form-control" id="floatingInput" style="height: 100px " placeholder="Дмитрий Гордон">
        <label for="floatingInput">Название</label>
    </div>
    <div class="form-floating">
        <textarea class="form-control" placeholder="Leave a comment here" id="floatingTextarea2" style="height: 100px width:30%"></textarea>
        <label for="floatingTextarea2">Comments</label>
    </div>
    <button class="button button1" style="!important">SAVE.</button>
    '''))
    map1.save('templates/расходники/make_map.html')

    return render_template('расходники/make_map.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.2')
