import folium

from flask import Flask, url_for, render_template
from htmlmerger import HtmlMerger

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


@app.route('/')
def main():
    map = folium.Map(location=[55.689179, 37.772682], zoom_start=12)
    folium.PolyLine(sp,
                    color='gray',
                    weight=5,
                    opacity=0.8).add_to(map)
    for k in sp:
        folium.Marker(
            k, popup=f"<i>0_0</i>"
        ).add_to(map)
    #
    map.save('templates/stat.html')

    return render_template('base.html')


@app.route('/make')
def make():
    map1 = folium.Map(location=[55.689179, 37.772682], zoom_start=12)
    pop = folium.LatLngPopup()

    map1.add_child(pop)
    map1.save('templates/every_htm.html')
    merger = HtmlMerger(input_directory="templtes/stat")
    merger.files.append('stat.html')
    merger.files.append('base.html')
    merger.merge(clean=False)

    return render_template('every_htm.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.2')
