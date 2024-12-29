import numpy as np
from tabulate import tabulate
from scipy.optimize import linprog

#FONCTION POUR AFFICHER LE TABLEAU INITIAL DE LA METHODE
def afficher_premier_tableau(c_grand_m, A_grand_m, b):

    num_v = A_grand_m.shape[1]
    headers = ["b"] + [f"x{i+1}" for i in range(num_v)]
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
def traiter_contrainte(A_grand_m, c_grand_m, s_vars, a_vars, num_c, i, cont_type, M):
    if cont_type == '<=':
        col = np.zeros((num_c,))
        col[i] = 1
        s_vars.append(len(c_grand_m))
        return ajouter_variable(A_grand_m, c_grand_m, col, 0)
    elif cont_type == '>=':
        e_col, a_col = np.zeros((num_c,)), np.zeros((num_c,))
        e_col[i], a_col[i] = -1, 1
        A_grand_m, c_grand_m = ajouter_variable(A_grand_m, c_grand_m, e_col, 0)
        a_vars.append(len(c_grand_m))
        return ajouter_variable(A_grand_m, c_grand_m, a_col, M)
    elif cont_type == '=':
        a_col = np.zeros((num_c,))
        a_col[i] = 1
        a_vars.append(len(c_grand_m))
        return ajouter_variable(A_grand_m, c_grand_m, a_col, M)
    return A_grand_m, c_grand_m


#IMPLEMENTE LA METHODE DE GRAND M 
#EN UTILSANT UNE BOUCLE POUR TRAITER CHAQUE CONTRAINTE EN UTILISANT LA FNCT traiter_contrainte
def GrandM(c, A, b, cont_signes, M=10000):
    num_c, num_v = A.shape
    A_grand_m, c_grand_m, s_vars, a_vars  = A.copy(), np.copy(c), [], []

    #BOUCLE POUR TRAITER LES CONTRAINTES
    for i, cont_type in enumerate(cont_signes):
        A_grand_m, c_grand_m = traiter_contrainte(A_grand_m, c_grand_m, s_vars, a_vars, num_c, i, cont_type, M)

    #1ER TABLEAU
    afficher_premier_tableau(c_grand_m, A_grand_m, b)
    optim = linprog(c_grand_m, A_eq=A_grand_m, b_eq=b, method='simplex')
    print(optim)  # AFFICHER LE RESULTAT DE LINPROG
    sol = optim.x[:num_v]
    return sol, optim.fun


if __name__ == "__main__":

    sol_op, z_optimale = GrandM(
        [-2,-3],
        np.array([[1, 2], [1, 2]]),
        np.array([8, 6]),
        ['<=', '>=']
    )

    print("Solution optimale:")
    for i, val in enumerate(sol_op):
        print(f"x{i+1} = {val}")
    print("Valeur optimale de z:", -z_optimale)  #EN MULTIPLIE PAR -1 POUR LA MAXIMISATION


    #test2
    # sol, z_optimale = GrandM(
    #     [2, 4],
    #     np.array([[2, -2], [4, 2]]),
    #     np.array([4, 6]),
    #     ['=', '>=']
    # )

    # print("Solution optimale:")
    # for i, val in enumerate(sol):
    #     print(f"x{i+1} = {val}")
    # print("Valeur optimale de z:", -z_optimale)  #EN MULTIPLIE PAR -1 POUR LA MAXIMISATION

    # test minimsation
    # solution, z_optimale = GrandM(
    #     [4, 3],
    #     np.array([[2, 1], [-3, 2], [1, 1]]),
    #     np.array([10, 6, 6]),
    #     ['>=','<=','>=' ]
    # )

    # print("Solution optimale:")
    # for i, val in enumerate(solution):
    #     print(f"x{i+1} = {val}")
    # print("Valeur optimale de z:", z_optimale)
