import abc
from bokeh.palettes import Category20_9 as cols
import matplotlib.pyplot as plt
import future.utils
import past

__author__ = 'Giulio Rossetti'
__license__ = "GPL"
__email__ = "giulio.rossetti@gmail.com"


class ComparisonPlot(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, models, trends, classes=("Infected")):
        self.models = models
        self.trends = trends
        if len(models) != len(trends):
            raise Exception

        statuses = [model.available_statuses for model in models]
        self.mnames = ["%s_%s" % (models[i].name, i) for i in past.builtins.xrange(0, len(models))]
        self.srev = {}
        i = 0

        available_classes = {}
        for model in models:
            srev = {v: k for k, v in future.utils.iteritems(statuses[i])}
            for cl in srev.values():
                available_classes[cl] = None

            self.srev["%s_%s" % (model.name, i)] = srev
            i += 1

        cls = set(classes) & set(available_classes.keys())
        if len(cls) > 0:
            self.classes = cls
        else:
            raise Exception

        self.ylabel = ""
        self.title = ""

    @abc.abstractmethod
    def iteration_series(self, percentile):
        """
        Prepare the data to be visualized

        :param percentile: The percentile for the trend variance area
        :return: a dictionary where iteration ids are keys and the associated values are the computed measures
        """
        pass

    def plot(self, filename, percentile=90):

        pres = self.iteration_series(percentile)

        mx = 0
        i, h = 0, 0
        for k, l in pres.iteritems():
            j = 0
            for st in l:
                mx = len(l[st][0])
                plt.plot(range(0, mx), l[st][1], lw=2, label="%s - %s" % (self.mnames[i].split("_")[0], st),
                         alpha=0.9, color=cols[h+j])
                plt.fill_between(range(0,  mx), l[st][0], l[st][2], alpha=0.2, color=cols[h+j])
                j += 1
            i += 1
            h += 2

        plt.grid(axis="y")
        plt.xlabel("Iterations", fontsize=24)
        plt.ylabel(self.ylabel, fontsize=24)
        plt.legend(loc="best", fontsize=20)
        plt.xlim((0, mx))

        plt.tight_layout()
        plt.savefig(filename)
