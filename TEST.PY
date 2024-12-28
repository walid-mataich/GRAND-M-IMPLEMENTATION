import numpy as np
from tabulate import tabulate
from scipy.optimize import linprog
#FONCTION POUR AFFICHER LE TABLEAU INITIAL DE LA METHODE
def afficher_premier_tableau(c_grand_m, A_grand_m, b):
    num_vars = A_grand_m.shape[1]
    headers = ["b"] + [f"x{i+1}" for i in range(num_vars)]
    tableau = np.hstack([b.reshape(-1, 1), A_grand_m])  
    tableau = tableau.tolist()
    tableau.append(["z"] + list(c_grand_m))  
    print("\n----- Premier Tableau -----")
    print(tabulate(tableau, headers=headers, tablefmt="fancy_grid"))
    print("-------------------------------\n")
#FONCTION POUR METTRE A JOUR LE TABLEAU
def ajouter_variable(A_grand_m, c_grand_m, col, cout):
    A_grand_m = np.hstack([A_grand_m, col.reshape(-1, 1)])
    c_grand_m = np.hstack([c_grand_m, cout])
    return A_grand_m, c_grand_m
#UTILISE LA FNCT ajouter_variable() POUR MODIFIER LE TABLEAU SELON LE CONTRAINTE
def traiter_contrainte(A_grand_m, c_grand_m, s_vars, a_vars, num_cons, i, s_ct, M):
    if s_ct == '<=':
        col = np.zeros((num_cons,))
        col[i] = 1
        s_vars.append(len(c_grand_m))
        return ajouter_variable(A_grand_m, c_grand_m, col, 0)
    elif s_ct == '>=':
        e_col, a_col = np.zeros((num_cons,)), np.zeros((num_cons,))
        e_col[i], a_col[i] = -1, 1
        A_grand_m, c_grand_m = ajouter_variable(A_grand_m, c_grand_m, e_col, 0)
        a_vars.append(len(c_grand_m))
        return ajouter_variable(A_grand_m, c_grand_m, a_col, M)
    elif s_ct == '=':
        a_col = np.zeros((num_cons,))
        a_col[i] = 1
        a_vars.append(len(c_grand_m))
        return ajouter_variable(A_grand_m, c_grand_m, a_col, M)
    return A_grand_m, c_grand_m
#IMPLEMENTE LA METHODE DE GRAND M
#EN UTILSANT UNE BOUCLE POUR TRAITER CHAQUE CONTRAINTE EN UTILISANT LA FNCT traiter_contrainte
def GrandM(c, A, b, c_signe, M=1000):
    num_cons, num_vars = A.shape
    A_grand_m, c_grand_m = A.copy(), np.copy(c)
    s_vars, a_vars = [], []
    for i, s_ct in enumerate(c_signe):
        A_grand_m, c_grand_m = traiter_contrainte(A_grand_m, c_grand_m, s_vars, a_vars, num_cons, i, s_ct, M)
    afficher_premier_tableau(c_grand_m, A_grand_m, b)
    result = linprog(c_grand_m, A_eq=A_grand_m, b_eq=b, method='simplex')
    print(result)  # AFFICHER LE RESULTAT DE LINPROG
    final_solution = result.x[:num_vars]
    return final_solution, result.fun
if __name__ == "__main__":
    solution, optimal_value = GrandM(
        [-2,-3],
        np.array([[1, 2], [1, 2]]),
        np.array([8, 6]),
        ['<=', '>=']
    )
    print("Solution optimale:")
    for i, val in enumerate(solution):
        print(f"x{i+1} = {val}")
    print("Valeur optimale de z:", -optimal_value)  #EN MULTIPLIE PAR -1 POUR LA MAXIMISATION