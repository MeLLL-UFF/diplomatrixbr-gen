import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import json

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def namesToCode(name):
    dic = {
    "gpt4o_temp03": "gpt4o_03",
    "gpt4o_temp05": "gpt4o_05",
    "gpt4o_temp07": "gpt4o_07",
    "command_r_plus_08_2024_temp03": "command-r-plus+03",
    "command_r_plus_08_2024_temp03": "command-r-plus+03",
    "command_r_plus_08_2024_temp05": "command-r-plus+05",
    "gemma_27b_temp03": "gemma27b_03",
    "gemma_27b_temp05": "gemma27b_05",
    "gemma_27b_temp07": "gemma27b_07",
    "gemma_2_9b_it_temp03": "gemma9b_03",
    "gemma_2_9b_it_temp05": "gemma9b_05",
    "gemma_2_9b_it_temp07": "gemma9b_07",
    "llama_405b_temp03": "llama405b_03",
    "llama_405b_temp05": "llama405b_05",
    "llama_405b_temp07": "llama405b_07",
    "llama_3.1_8b_instruct_temp03": "llama8b_03",
    "llama_3.1_8b_instruct_temp05": "llama8b_05",
    "llama_3.1_8b_instruct_temp07": "llama8b_07",
    "mixtral_22b_temp03": "mixtral22b_03",
    "mixtral_22b_temp05": "mixtral22b_05",
    "mixtral_22b_temp07": "mixtral22b_07",
    "mistral_7b_instruct_v0.3_temp03": "mixtral7b_03",
    "mistral_7b_instruct_v0.3_temp05": "mixtral7b_05",
    "mistral_7b_instruct_v0.3_temp07": "mixtral7b_07",
    "phi_3_small_8k_instruct_temp03": "phi3_03",
    "phi_3_small_8k_instruct_temp05": "phi3_05",
    "phi_3_small_8k_instruct_temp07": "phi3_07",
    "phi_4_temp03": "phi4_03",
    "phi_4_temp05": "phi4_05",
    "phi_4_temp07": "phi4_07",
    "qwen_72b_temp03": "qwen72b_03",
    "qwen_72b_temp05": "qwen72b_05",
    "qwen_72b_temp07": "qwen72b_07",
    "qwen2.5_7b_instruct_temp03": "qwen7b_03",
    "qwen2.5_7b_instruct_temp05": "qwen7b_05",
    "qwen2.5_7b_instruct_temp07": "qwen7b_07",
    "sabia3_temp03": "sabia_03",
    "sabia3_temp05": "sabia_05",
    "sabia3_temp07": "sabia_07"
    }

    return dic.get(name)

def dataTuples(path):
    df = pd.read_csv(path, sep=';')

    #Coletando nome dos candidatos
    cand = set(df["id"])
    candidatos = sorted(list(cand))

    #Acertando o nome dos modelos
    data = []
    ind = df[df["id"] == candidatos[0]]
    ind = list(ind["generator_model"])

    for i in range(len(ind)):
        ind[i] = namesToCode(ind[i])
    data.append(ind)

    for c in candidatos:
        resp = df[df["id"] == c]

        temp = []
        for col in (list(resp.columns))[3:]:
            tempCorrigida = list(resp[col])
            for i in range(len(tempCorrigida)):
                tempCorrigida[i] = tempCorrigida[i].replace(",", ".")
                tempCorrigida[i] = np.emath.logn(1000, float(tempCorrigida[i])) if float(tempCorrigida[i]) > 1 else float(tempCorrigida[i])
            tempCorrigida = list(map(float, tempCorrigida))
            temp.append(tempCorrigida)
        data.append((c, temp))

    return data

def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` Axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding Axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

if __name__ == '__main__':
    basepath = os.getcwd()
    essaysYears = os.listdir(basepath)
    #Retirando a pasta "Scrips"
    essaysYears.pop(essaysYears.index("Scripts"))

    for year in essaysYears:
        pathcsv = os.path.join(basepath, year, "MetricasRedacoesDiplomatas.csv")

        pathjson = ""
        for file in os.listdir(os.path.join(basepath, year)):
            pathjson = os.path.join(basepath, year, file) if file.endswith(".json") else pathjson

        with open(pathjson, 'r', encoding="utf8") as j:
            jsoncandidatos = json.load(j)

        candidatos = []
        for c in jsoncandidatos["Candidatos"]:
            nome, nota = c["Nome"], c["Nota"]
            candidatos.append((nome, nota))

        if not(os.path.exists(os.path.join(basepath, year, "Graficos"))):
            os.makedirs(os.path.join(basepath, year, "Graficos"))

        data = dataTuples(pathcsv)
        
        spoke_labels = data.pop(0)
        N = len(spoke_labels)

        for i in range(len(data)):
            theta = radar_factory(N, frame='circle')
            fig, axs = plt.subplots(figsize=(12, 9), sharex=True, sharey=False, nrows=1, ncols=1, squeeze=False, subplot_kw=dict(projection='radar'))

            fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

            colors = ["#012DEB", "#61FF00", "#86A800", "#DDFF55", "#FF0D00", "#FF2AAF", "#8D00FF", "#8F0044", "#7090E0", "#70E0C4", "#284E44", "#E07296"]
            # Plot the four cases from the example data on separate Axes

            for ax, (title, case_data) in zip(axs.flat, data):
                ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
                title = title.split("_")[-1]

                #Adicionando a nota antes do nome do candidato
                for c in candidatos:
                    title = str(c[1]).replace(".", ",") + " " + title if c[0] == title else title

                ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                            horizontalalignment='center', verticalalignment='center')

                for d, color in zip(case_data, colors):
                    ax.plot(theta, d, color=color)
                    ax.set_varlabels(spoke_labels)

            # add legend relative to top-left plot
            labels = ("BLEU_score", "BERTScore_Precision", "BERTScore_Recall", "BERTScore_F1", "rouge1", "rouge2", "rougeL", "rougeLsum", "log1000CTC_groundness", "log1000CTC_groundness_ref", "CTC_factual", "CTC_factual_ref")
            legend = axs[0, 0].legend(labels, loc=(0.9, 0.9),
                                    labelspacing=0.1, fontsize='medium')

            fig.text(0.5, 0.965, 'Gráficos Métricas',
                    horizontalalignment='center', color='black', weight='bold',
                    size='large')

            candidato = data[0][0]
            
            candidato = candidato.split("_")[-1]

            plt.savefig(f"{basepath}\{year}\Graficos\{title}.png")
            #plt.show()
            plt.close()
            data.pop(0)