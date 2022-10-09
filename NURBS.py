
from matplotlib import pyplot as plt
import numpy
import mpl_toolkits.mplot3d.axes3d as p3

# initialPoints2D = numpy.array([(28, 6), (6, 5), (40, 0), (6, 2), (5, 10), (-8, 50), (4, 25)], float)
initialPoints3D = numpy.array([(28, 44, 6), (20, 6, 5), (40, -10, 0),
                               (68, 0, 2), (6, 5, 10), (-8, 50, 50), (4, -50, 25)], float)  # PONTOS INICIAIS
# NUMERO DE SEGMENTOS
divisions = 100
# GRAU DO POLINOMIO
degree = 6


def nurbs(p0=numpy.array([(0, 3), (2, 0), (1, 7), (6, 11), (7, 1)], float), deg=2, div=1000, *matrix_w):
    dim = len(p0[0])
    count = 0
    n = p0.shape[0]
    if n >= deg:
        Exception("Invalid number of points for this degree.")
    m = deg + n + 1
    matrix_u = numpy.zeros(m)
    if matrix_w is None:
        matrix_w = numpy.ones(n)        # PESO
    else:
        matrix_w = matrix_w[0]

    for i in range(m):
        if i < deg + 1:
            matrix_u[i] = 0
        elif i >= m - (deg + 1):
            matrix_u[i] = 1
        else:
            count += 1
            matrix_u[i] = count * (1 / (1 + m - 2 * (deg + 1)))
    u = 0.0
    c = 0
    matrix_p = numpy.zeros((div + 1, dim))
    while u <= 1:
        sum_px = 0
        sum_py = 0
        sum_pz = 0
        sum_total = 0
        for i in range(n):
            cox_value = cox_de_boor(i, deg + 1, u, matrix_u)
            sum_px += cox_value * matrix_w[i] * p0[i, 0]
            sum_py += cox_value * matrix_w[i] * p0[i, 1]
            sum_pz += cox_value * matrix_w[i] * p0[i, dim - 1]
            sum_total += cox_value * matrix_w[i]
        if sum_total != 0:
            matrix_p[c, dim - 1] = sum_pz / sum_total
            matrix_p[c, 0] = sum_px / sum_total
            matrix_p[c, 1] = sum_py / sum_total
        else:
            matrix_p[c, dim - 1] = 0
            matrix_p[c, 0] = 0
            matrix_p[c, 1] = 0
        c += 1
        u += 1 / div
    matrix_p[div, dim - 1] = p0[n - 1, dim - 1]
    matrix_p[div, 0] = p0[n - 1, 0]
    matrix_p[div, 1] = p0[n - 1, 1]

    return matrix_p


def cox_de_boor(index, degree, x, matrix):
    v1 = 0
    v2 = 0
    if degree == 1:
        if (x >= matrix[index]) and (x < matrix[index + 1]):
            return 1
        else:
            return 0
    # DIVISÃO POR ZERO
    if (matrix[index + degree - 1] - matrix[index]) != 0:  # 1e-8:
        v1 = (x - matrix[index]) * cox_de_boor(index, degree - 1, x, matrix) / (
            matrix[index + degree - 1] - matrix[index])
    else:
        v1 = 0
    # DIVISÃO POR ZERO
    if (matrix[index + degree] - matrix[index + 1]) != 0:  # > 1e-8:
        v2 = (matrix[index + degree] - x) * cox_de_boor(index + 1, degree - 1, x, matrix) / (
            matrix[index + degree] - matrix[index + 1])
    else:
        v2 = 0
    return v1 + v2


def plot_nurbs(control_points, data):
    fig = plt.figure()
    subplot = fig.add_subplot(111)
    dimension = len(control_points[0])
    size = len(control_points)
    if dimension == 2:
        plt.plot(data[:, 0], data[:, 1])
        plt.plot(control_points[:, 0], control_points[:, 1], 'ro',)
        c = 0
        for i, j in zip(control_points[:, 0], control_points[:, 1]):
            c += 1
            plt.annotate('%s' % c, xy=(i, j), xytext=(
                5, 0), textcoords='offset points')
        return fig, 0
    elif dimension == 3:
        ax = p3.Axes3D(fig)
#        ax.scatter(control_points[:, 0], control_points[:, 1], control_points[:, 2])
        for i in range(len(control_points)):  # plot each point + it's index as text above
            ax.scatter(control_points[i, 0],
                       control_points[i, 1], control_points[i, 2])
            ax.text(control_points[i, 0], control_points[i, 1], control_points[i, 2]+1, '%s' % (str(i+1)),
                    size=15, zorder=3, color='k')
        ax.plot(data[:, 0], data[:, 1], data[:, 2])
        return fig, ax
    else:
        Exception("Os pontos devem ser 2D ou 3D.")
    # plt.show()


# plot_nurbs(initialPoints3D,nurbs(initialPoints3D,2,100)) # TESTING
