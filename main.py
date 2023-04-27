import folium

from flask import Flask, url_for, render_template, json, request
from htmlmerger import HtmlMerger
import codecs
import dash

#
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
    map = folium.Map(position='relative', left='0%', width='100%', height='100%', align='right',
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


@app.route('/make_map')
def make_map():
    map1 = folium.Map(location=[55.7522, 37.6156], zoom_start=12)
    pop = folium.ClickForMarker()
    idx = json.loads(dash.callback_context.triggered[0]['prop_id'].split(".")[0])["id"]
    location = locations[idx]
    map1.add_child(pop)
    map1.save('templates/расходники/make_map.html')

    return render_template('расходники/make_map.html')


'''from flask import Flask, render_template, request

#
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


@app.route('/get-cl', methods=['GET', 'POST'])
def foo():
    email = request.input_stream['email']
    print(email)


@app.route('/')
def main():
    return render_template('base.html', Title='Гость')


@app.route('/make')
def make():
    return render_template('base1.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.2')'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.2')
